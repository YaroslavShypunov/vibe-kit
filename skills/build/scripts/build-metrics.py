#!/usr/bin/env python3
"""Read-only cost, time, and loop metrics for /build sessions.

Usage:
  build-metrics.py [--brief] <session-id-or-folder> [...]
  build-metrics.py [--brief] --last N

Reads ~/.copilot/session-state/<id>/events.jsonl and, when present,
~/.copilot/session-store.db (opened read-only). Writes nothing.
"""

import argparse
import collections
import datetime
import json
import os
import sqlite3
import sys

COPILOT_HOME = os.path.expanduser("~/.copilot")
SESSION_STATE = os.path.join(COPILOT_HOME, "session-state")
SESSION_STORE = os.path.join(COPILOT_HOME, "session-store.db")


def parse_time(text):
    return datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))


def minutes(seconds):
    return f"{seconds / 60:.0f}m"


def events_path(session):
    if os.path.isdir(session):
        return os.path.join(session, "events.jsonl")
    return os.path.join(SESSION_STATE, session, "events.jsonl")


def is_build_session(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if '"skill.invoked"' in line and '"name": "build"' in line:
                    return True
                if '"skill.invoked"' in line and '"name":"build"' in line:
                    return True
    except OSError:
        return False
    return False


def last_build_sessions(count):
    candidates = []
    for name in os.listdir(SESSION_STATE):
        path = os.path.join(SESSION_STATE, name, "events.jsonl")
        if os.path.isfile(path):
            candidates.append((os.path.getmtime(path), name, path))
    candidates.sort(reverse=True)
    found = []
    for _, name, path in candidates:
        if is_build_session(path):
            found.append(name)
            if len(found) == count:
                break
    return found


def read_credits(session_id):
    result = {"main": 0.0, "subagents": 0.0, "by_model": collections.Counter(), "calls": 0, "cache_write": 0}
    if not os.path.isfile(SESSION_STORE):
        return None
    try:
        connection = sqlite3.connect(f"file:{SESSION_STORE}?mode=ro", uri=True)
        rows = connection.execute(
            "SELECT agent_id IS NULL, model, COUNT(*), SUM(total_nano_aiu), SUM(cache_write_tokens) "
            "FROM assistant_usage_events WHERE session_id = ? GROUP BY 1, 2",
            (session_id,),
        ).fetchall()
        connection.close()
    except sqlite3.Error:
        return None
    for is_main, model, calls, nano, cache_write in rows:
        credits = (nano or 0) / 1e9
        result["main" if is_main else "subagents"] += credits
        result["by_model"][model] += credits
        result["calls"] += calls
        result["cache_write"] += cache_write or 0
    return result


def analyze(session):
    path = events_path(session)
    session_id = os.path.basename(os.path.dirname(os.path.abspath(path)))
    metrics = {
        "session": session_id,
        "builds": 0,
        "first": None,
        "last": None,
        "user_wait_seconds": 0.0,
        "compactions": 0,
        "aborts": 0,
        "main_tools": collections.Counter(),
        "agents": collections.Counter(),
        "agent_modes": collections.Counter(),
        "agent_seconds": collections.Counter(),
        "agent_tokens": collections.Counter(),
        "failed_tools": collections.Counter(),
        "failed_messages": collections.Counter(),
    }
    tool_names = {}
    ask_started = {}
    turn_ended_at = None
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_type = event.get("type")
            data = event.get("data") or {}
            stamp = event.get("timestamp")
            moment = parse_time(stamp) if stamp else None
            if moment:
                metrics["first"] = metrics["first"] or moment
                metrics["last"] = moment
            is_main = "agentId" not in event
            if event_type == "skill.invoked" and data.get("name") == "build":
                metrics["builds"] += 1
            elif event_type == "session.compaction_start":
                metrics["compactions"] += 1
            elif event_type == "abort":
                metrics["aborts"] += 1
            elif event_type == "assistant.turn_end" and is_main:
                turn_ended_at = moment
            elif event_type == "user.message" and is_main:
                if turn_ended_at and moment:
                    metrics["user_wait_seconds"] += (moment - turn_ended_at).total_seconds()
                turn_ended_at = None
            elif event_type == "assistant.turn_start" and is_main:
                turn_ended_at = None
            elif event_type == "tool.execution_start":
                name = data.get("toolName", "?")
                tool_names[data.get("toolCallId")] = name
                if is_main:
                    metrics["main_tools"][name] += 1
                    if name == "ask_user" and moment:
                        ask_started[data.get("toolCallId")] = moment
            elif event_type == "tool.execution_complete":
                call_id = data.get("toolCallId")
                name = tool_names.get(call_id, "?")
                if call_id in ask_started and moment:
                    metrics["user_wait_seconds"] += (moment - ask_started.pop(call_id)).total_seconds()
                if data.get("success") is False:
                    metrics["failed_tools"][name] += 1
                    message = ((data.get("error") or {}).get("message") or "").strip().splitlines()
                    if message:
                        metrics["failed_messages"][message[0][:70]] += 1
            elif event_type == "subagent.started":
                agent = data.get("agentName", "?")
                metrics["agents"][agent] += 1
                metrics["agent_modes"][data.get("executionMode", "?")] += 1
            elif event_type in ("subagent.completed", "subagent.failed"):
                agent = data.get("agentName", "?")
                metrics["agent_seconds"][agent] += (data.get("durationMs") or 0) / 1000
                metrics["agent_tokens"][agent] += data.get("totalTokens") or 0
    wall = (metrics["last"] - metrics["first"]).total_seconds() if metrics["first"] else 0.0
    metrics["wall_seconds"] = wall
    metrics["active_seconds"] = max(wall - metrics["user_wait_seconds"], 0.0)
    metrics["credits"] = read_credits(session_id)
    return metrics


def credits_text(credits):
    if credits is None:
        return "credits n/a"
    total = credits["main"] + credits["subagents"]
    return f"{total:.0f} credits (main {credits['main']:.0f}, agents {credits['subagents']:.0f})"


def brief(metrics):
    tools = metrics["main_tools"]
    return (
        f"{metrics['session'][:8]}: active {minutes(metrics['active_seconds'])}, "
        f"user wait {minutes(metrics['user_wait_seconds'])}, {credits_text(metrics['credits'])}, "
        f"agents {sum(metrics['agents'].values())}, write_agent {tools['write_agent']}, "
        f"ask_user {tools['ask_user']}, failed tools {sum(metrics['failed_tools'].values())}, "
        f"compactions {metrics['compactions']}"
    )


def report(metrics):
    lines = [f"== {metrics['session']}", "  " + brief(metrics)]
    lines.append(f"  wall {minutes(metrics['wall_seconds'])}, /build invocations {metrics['builds']}, aborts {metrics['aborts']}")
    credits = metrics["credits"]
    if credits:
        by_model = ", ".join(f"{model} {value:.0f}" for model, value in credits["by_model"].most_common())
        lines.append(f"  credits by model: {by_model}; model calls {credits['calls']}, cache writes {credits['cache_write']:,} tokens")
    if metrics["agents"]:
        modes = ", ".join(f"{mode} {count}" for mode, count in metrics["agent_modes"].most_common())
        lines.append(f"  agent runs ({modes}):")
        for agent, count in metrics["agents"].most_common():
            lines.append(
                f"    {agent:<22} runs {count:>2}  time {minutes(metrics['agent_seconds'][agent]):>5}  "
                f"tokens {metrics['agent_tokens'][agent]:>10,}"
            )
    tools = metrics["main_tools"]
    lines.append(
        f"  main tools: task {tools['task']}, write_agent {tools['write_agent']}, read_agent {tools['read_agent']}, "
        f"ask_user {tools['ask_user']}, view {tools['view']}, bash {tools['bash']}"
    )
    if metrics["failed_tools"]:
        failed = ", ".join(f"{name} {count}" for name, count in metrics["failed_tools"].most_common(6))
        lines.append(f"  failed tools: {failed}")
        for message, count in metrics["failed_messages"].most_common(4):
            lines.append(f"    {count:>3} x {message}")
    return "\n".join(lines)


def averages(all_metrics):
    count = len(all_metrics)
    active = sum(item["active_seconds"] for item in all_metrics) / count
    wait = sum(item["user_wait_seconds"] for item in all_metrics) / count
    known = [item["credits"] for item in all_metrics if item["credits"]]
    credits = sum(item["main"] + item["subagents"] for item in known) / len(known) if known else 0.0
    agents = sum(sum(item["agents"].values()) for item in all_metrics) / count
    asks = sum(item["main_tools"]["ask_user"] for item in all_metrics) / count
    failed = sum(sum(item["failed_tools"].values()) for item in all_metrics) / count
    return (
        f"== average of {count}: active {minutes(active)}, user wait {minutes(wait)}, {credits:.0f} credits, "
        f"agents {agents:.1f}, ask_user {asks:.1f}, failed tools {failed:.1f}"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sessions", nargs="*", help="session ids or session folders")
    parser.add_argument("--last", type=int, help="analyze the last N sessions that invoked /build")
    parser.add_argument("--brief", action="store_true", help="print one line per session")
    arguments = parser.parse_args()
    sessions = list(arguments.sessions)
    if arguments.last:
        sessions.extend(last_build_sessions(arguments.last))
    if not sessions:
        parser.error("give session ids or --last N")
    results = []
    for session in sessions:
        path = events_path(session)
        if not os.path.isfile(path):
            print(f"skip {session}: no events.jsonl", file=sys.stderr)
            continue
        results.append(analyze(session))
    for metrics in results:
        print(brief(metrics) if arguments.brief else report(metrics))
    if len(results) > 1:
        print(averages(results))
    return 0 if results else 1


if __name__ == "__main__":
    sys.exit(main())
