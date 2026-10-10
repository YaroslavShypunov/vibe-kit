"""Read selected observable fields from local Copilot history without writing files."""

import argparse
import collections
import json
from pathlib import Path
import sys
import uuid


EVENT_FIELDS = {
    "session.start": (
        "sessionId", "startTime", "selectedModel", "copilotVersion", "contextTier",
    ),
    "user.message": ("content",),
    "assistant.message": ("content", "model"),
    "tool.execution_start": ("toolCallId", "toolName", "toolTitle", "arguments"),
    "tool.execution_complete": ("toolCallId", "success", "result"),
    "skill.invoked": ("name", "path", "source", "trigger"),
    "subagent.started": (
        "agentName", "agentDisplayName", "agentDescription", "agentType",
        "executionMode", "model", "toolCallId",
    ),
    "subagent.configured": ("model", "reasoningEffort", "multiTurn"),
    "subagent.selected": ("agentName", "agentDisplayName"),
    "subagent.completed": (
        "agentName", "agentDisplayName", "durationMs", "model", "toolCallId",
        "totalTokens", "totalToolCalls",
    ),
    "session.model_change": ("newModel", "reasoningEffort", "source"),
    "session.usage_checkpoint": ("totalNanoAiu", "totalPremiumRequests"),
    "session.error": ("errorType", "message"),
    "session.abort": ("reason",),
}

PROTECTED_FIELDS = frozenset({
    "reasoningText", "reasoningBlocks", "reasoningOpaque", "responsesReasoning",
    "encryptedContent", "systemPrompt", "developerPrompt", "thinking",
    "reasoning", "redactedThinking",
})

PROTECTED_CONTENT_TYPES = frozenset({
    "thinking", "redacted_thinking", "reasoning", "reasoning_text", "analysis",
})


def positive_integer(value):
    integer_value = int(value)
    if integer_value < 1:
        raise argparse.ArgumentTypeError("Value must be a positive integer.")
    return integer_value


def nonnegative_integer(value):
    integer_value = int(value)
    if integer_value < 0:
        raise argparse.ArgumentTypeError("Value must not be negative.")
    return integer_value


def resolve_history_path(session_id):
    canonical_session_id = str(uuid.UUID(session_id))
    history_root = (Path.home() / ".copilot" / "session-state").resolve()
    history_path = (
        history_root / canonical_session_id / "events.jsonl"
    ).resolve()
    if not history_path.is_relative_to(history_root):
        raise ValueError("History path must stay inside the local session directory.")
    return history_path


def iterate_history_events(history_path):
    with history_path.open(encoding="utf-8") as history_file:
        for line_number, event_line in enumerate(history_file, start=1):
            if not event_line.strip():
                continue
            try:
                session_event = json.loads(event_line)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Malformed history record at line {line_number}: {error.msg}"
                ) from error
            if not isinstance(session_event, dict):
                raise ValueError(f"History record at line {line_number} is not an object.")
            if not isinstance(session_event.get("type"), str):
                raise ValueError(f"History record at line {line_number} has no valid type.")
            if not isinstance(session_event.get("data", {}), dict):
                raise ValueError(f"History data at line {line_number} is not an object.")
            for metadata_field in ("id", "timestamp", "agentId"):
                metadata_value = session_event.get(metadata_field)
                if metadata_value is not None and not isinstance(metadata_value, str):
                    raise ValueError(
                        f"History {metadata_field} at line {line_number} is not a string."
                    )
            yield line_number, session_event


def remove_protected_fields(value):
    if isinstance(value, dict):
        content_type = value.get("type")
        if (
            (isinstance(content_type, str) and content_type in PROTECTED_CONTENT_TYPES)
            or value.get("role") in ("system", "developer")
        ):
            return {"omitted_protected_content": True}
        return {
            field_name: remove_protected_fields(field_value)
            for field_name, field_value in value.items()
            if field_name not in PROTECTED_FIELDS
        }
    if isinstance(value, list):
        return [remove_protected_fields(list_item) for list_item in value]
    return value


def project_history_event(line_number, session_event):
    event_type = session_event["type"]
    if event_type not in EVENT_FIELDS:
        raise ValueError(f"Event type {event_type!r} is not exposed by this reader.")
    event_data = session_event.get("data", {})
    projected_event = {
        "source_line": line_number,
        "event_id": session_event.get("id"),
        "timestamp": session_event.get("timestamp"),
        "type": event_type,
        "agent_id": session_event.get("agentId"),
        "data": {
            field_name: remove_protected_fields(event_data[field_name])
            for field_name in EVENT_FIELDS[event_type]
            if field_name in event_data
        },
    }
    return projected_event


def index_history(history_path):
    event_type_counts = collections.Counter()
    agent_event_counts = collections.Counter()
    event_ids = set()
    duplicate_event_ids = set()
    missing_event_ids = 0
    missing_timestamps = 0
    first_timestamp = None
    last_timestamp = None
    for line_number, session_event in iterate_history_events(history_path):
        event_type_counts[session_event["type"]] += 1
        agent_event_counts[session_event.get("agentId") or "main"] += 1
        event_id = session_event.get("id")
        if not event_id:
            missing_event_ids += 1
        elif event_id in event_ids:
            duplicate_event_ids.add(event_id)
        else:
            event_ids.add(event_id)
        timestamp = session_event.get("timestamp")
        if timestamp:
            first_timestamp = first_timestamp or timestamp
            last_timestamp = timestamp
        else:
            missing_timestamps += 1
    if not event_type_counts:
        raise ValueError("History file contains no event records.")
    return {
        "history_path": str(history_path),
        "record_count": sum(event_type_counts.values()),
        "analysis_event_count": sum(
            event_count for event_type, event_count in event_type_counts.items()
            if event_type in EVENT_FIELDS
        ),
        "event_type_counts": dict(event_type_counts),
        "agent_event_counts": dict(agent_event_counts),
        "types_not_exposed": sorted(set(event_type_counts) - set(EVENT_FIELDS)),
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "duplicate_event_ids": sorted(duplicate_event_ids),
        "missing_event_ids": missing_event_ids,
        "missing_timestamps": missing_timestamps,
    }


def read_history_page(history_path, start_line, maximum_events, maximum_characters):
    previews = []
    next_start_line = None
    for line_number, session_event in iterate_history_events(history_path):
        if line_number < start_line or session_event["type"] not in EVENT_FIELDS:
            continue
        if len(previews) == maximum_events:
            next_start_line = line_number
            break
        projected_event = project_history_event(line_number, session_event)
        detail_text = json.dumps(projected_event["data"], ensure_ascii=True)
        previews.append({
            "source_line": line_number,
            "event_id": projected_event["event_id"],
            "timestamp": projected_event["timestamp"],
            "type": projected_event["type"],
            "agent_id": projected_event["agent_id"],
            "preview": detail_text[:maximum_characters],
            "detail_characters": len(detail_text),
            "needs_detail": len(detail_text) > maximum_characters,
        })
    return {"events": previews, "next_start_line": next_start_line}


def read_event_detail(history_path, event_line, detail_offset, maximum_characters):
    for line_number, session_event in iterate_history_events(history_path):
        if line_number != event_line:
            continue
        projected_event = project_history_event(line_number, session_event)
        detail_text = json.dumps(projected_event.pop("data"), ensure_ascii=True)
        if detail_offset > len(detail_text):
            raise ValueError("Detail offset exceeds the projected event length.")
        detail_end = min(detail_offset + maximum_characters, len(detail_text))
        return {
            **projected_event,
            "detail_chunk": detail_text[detail_offset:detail_end],
            "detail_characters": len(detail_text),
            "detail_offset": detail_offset,
            "next_detail_offset": detail_end if detail_end < len(detail_text) else None,
        }
    raise ValueError(f"No history event exists at line {event_line}.")


def main():
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("session_id", help="Confirmed local Copilot session UUID.")
    argument_parser.add_argument("--mode", choices=("index", "page", "event"), default="index")
    argument_parser.add_argument("--start-line", type=positive_integer, default=1)
    argument_parser.add_argument("--maximum-events", type=positive_integer, default=12)
    argument_parser.add_argument("--maximum-characters", type=positive_integer, default=1600)
    argument_parser.add_argument("--event-line", type=positive_integer)
    argument_parser.add_argument("--detail-offset", type=nonnegative_integer, default=0)
    arguments = argument_parser.parse_args()
    if arguments.mode == "event" and arguments.event_line is None:
        argument_parser.error("--event-line is required in event mode.")
    try:
        history_path = resolve_history_path(arguments.session_id)
        if arguments.mode == "index":
            output = index_history(history_path)
        elif arguments.mode == "page":
            output = read_history_page(
                history_path, arguments.start_line, arguments.maximum_events,
                arguments.maximum_characters,
            )
        else:
            output = read_event_detail(
                history_path, arguments.event_line, arguments.detail_offset,
                arguments.maximum_characters,
            )
    except (OSError, ValueError) as error:
        print(f"History reader error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(output, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
