import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid


reader_path = Path(__file__).resolve().parents[1] / "scripts" / "read_session_history.py"
module_specification = importlib.util.spec_from_file_location("session_history_reader", reader_path)
session_history_reader = importlib.util.module_from_spec(module_specification)
module_specification.loader.exec_module(session_history_reader)


class SessionHistoryReaderTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.history_path = Path(self.temporary_directory.name) / "events.jsonl"

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_events(self, events):
        self.history_path.write_text(
            "".join(json.dumps(event) + "\n" for event in events),
            encoding="utf-8",
        )

    def create_event(self, event_type, event_data, agent_id=None):
        session_event = {
            "id": str(uuid.uuid4()),
            "timestamp": "2026-10-08T12:00:00Z",
            "type": event_type,
            "data": event_data,
        }
        if agent_id is not None:
            session_event["agentId"] = agent_id
        return session_event

    def test_clean_task_preserves_requirement_and_recorded_check_without_inventing_usage(self):
        self.write_events([
            self.create_event("user.message", {"content": "Add the requested behavior."}),
            self.create_event("tool.execution_complete", {
                "toolCallId": "check-1", "success": True, "result": {"content": "1 test passed"},
            }),
            self.create_event("assistant.message", {"content": "Implemented the behavior."}),
        ])
        history_index = session_history_reader.index_history(self.history_path)
        history_page = session_history_reader.read_history_page(self.history_path, 1, 12, 1600)
        self.assertEqual(history_index["record_count"], 3)
        self.assertEqual(history_index["analysis_event_count"], 3)
        self.assertEqual(history_page["next_start_line"], None)
        self.assertIn("1 test passed", history_page["events"][1]["preview"])
        self.assertNotIn("totalTokens", json.dumps(history_index))

    def test_repair_history_keeps_failed_checks_and_nested_agent_attribution(self):
        self.write_events([
            self.create_event("tool.execution_complete", {
                "success": False, "result": {"content": "Expected behavior missing"},
            }),
            self.create_event("assistant.message", {
                "content": "Investigating the failure",
            }, agent_id="worker-1"),
            self.create_event("tool.execution_complete", {
                "success": True, "result": {"content": "Focused regression passed"},
            }, agent_id="worker-1"),
        ])
        history_index = session_history_reader.index_history(self.history_path)
        first_page = session_history_reader.read_history_page(self.history_path, 1, 1, 1600)
        second_page = session_history_reader.read_history_page(
            self.history_path, first_page["next_start_line"], 2, 1600,
        )
        self.assertEqual(history_index["agent_event_counts"], {"main": 1, "worker-1": 2})
        self.assertEqual(first_page["events"][0]["source_line"], 1)
        self.assertEqual(second_page["events"][0]["agent_id"], "worker-1")
        self.assertEqual(second_page["next_start_line"], None)
        self.assertFalse(json.loads(first_page["events"][0]["preview"])["success"])

    def test_incomplete_and_unknown_records_are_visible_in_coverage_metadata(self):
        self.write_events([
            {"type": "user.message", "data": {"content": "Task"}},
            self.create_event("future.event", {"unknown": "value"}),
        ])
        history_index = session_history_reader.index_history(self.history_path)
        self.assertEqual(history_index["missing_event_ids"], 1)
        self.assertEqual(history_index["missing_timestamps"], 1)
        self.assertEqual(history_index["types_not_exposed"], ["future.event"])
        self.assertEqual(history_index["analysis_event_count"], 1)

    def test_protected_fields_and_system_messages_are_not_exposed(self):
        self.write_events([
            self.create_event("system.message", {"content": "PROTECTED_SYSTEM_TEXT"}),
            self.create_event("assistant.message", {
                "content": "Visible answer",
                "reasoningText": "PROTECTED_REASONING",
                "encryptedContent": "PROTECTED_ENCRYPTED",
            }),
            self.create_event("tool.execution_complete", {
                "result": {"content": "Visible result", "reasoningBlocks": ["PROTECTED_NESTED"]},
            }),
            self.create_event("skill.invoked", {"name": "example", "content": "PROTECTED_SKILL"}),
        ])
        history_page = session_history_reader.read_history_page(self.history_path, 1, 12, 1600)
        serialized_page = json.dumps(history_page)
        self.assertEqual(len(history_page["events"]), 3)
        self.assertNotIn("PROTECTED_", serialized_page)
        with self.assertRaisesRegex(ValueError, "not exposed"):
            session_history_reader.read_event_detail(self.history_path, 1, 0, 1600)

    def test_detail_pagination_reconstructs_the_entire_projected_payload(self):
        self.write_events([
            self.create_event("user.message", {"content": "Requirement " * 50}),
        ])
        history_page = session_history_reader.read_history_page(self.history_path, 1, 12, 30)
        self.assertTrue(history_page["events"][0]["needs_detail"])
        detail_offset = 0
        detail_chunks = []
        while detail_offset is not None:
            event_detail = session_history_reader.read_event_detail(
                self.history_path, 1, detail_offset, 30,
            )
            detail_chunks.append(event_detail["detail_chunk"])
            detail_offset = event_detail["next_detail_offset"]
        self.assertEqual(json.loads("".join(detail_chunks)), {"content": "Requirement " * 50})

    def test_structured_reasoning_and_embedded_system_roles_are_omitted(self):
        self.write_events([
            self.create_event("assistant.message", {
                "content": [
                    {"type": "text", "text": "Visible answer"},
                    {"type": "reasoning", "text": "PROTECTED_BLOCK"},
                ],
            }),
            self.create_event("tool.execution_complete", {
                "result": [
                    {"role": "system", "content": "PROTECTED_EMBEDDED"},
                    {"role": "user", "content": "Visible task"},
                ],
            }),
        ])
        history_page = session_history_reader.read_history_page(self.history_path, 1, 12, 1600)
        serialized_page = json.dumps(history_page)
        self.assertIn("Visible answer", serialized_page)
        self.assertIn("Visible task", serialized_page)
        self.assertNotIn("PROTECTED_", serialized_page)
        self.assertIn("omitted_protected_content", serialized_page)

    def test_malformed_history_fails_explicitly(self):
        self.history_path.write_text('{"type":', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Malformed history record at line 1"):
            session_history_reader.index_history(self.history_path)

    def test_empty_history_fails_explicitly(self):
        self.history_path.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no event records"):
            session_history_reader.index_history(self.history_path)

    def test_nonstring_metadata_fails_explicitly(self):
        self.write_events([{
            "id": {"unexpected": "object"},
            "type": "user.message",
            "data": {"content": "Task"},
        }])
        with self.assertRaisesRegex(ValueError, "History id at line 1 is not a string"):
            session_history_reader.index_history(self.history_path)

    def test_domain_data_with_structured_type_field_is_preserved(self):
        domain_result = {"type": {"schema": "example"}, "role": ["reader"]}
        self.write_events([
            self.create_event("tool.execution_complete", {"result": domain_result}),
        ])
        event_detail = session_history_reader.read_event_detail(self.history_path, 1, 0, 1600)
        self.assertEqual(json.loads(event_detail["detail_chunk"]), {"result": domain_result})

    def test_missing_record_and_excessive_detail_offset_fail_explicitly(self):
        self.write_events([self.create_event("user.message", {"content": "Task"})])
        with self.assertRaisesRegex(ValueError, "No history event"):
            session_history_reader.read_event_detail(self.history_path, 2, 0, 30)
        with self.assertRaisesRegex(ValueError, "offset exceeds"):
            session_history_reader.read_event_detail(self.history_path, 1, 1000, 30)

    def test_duplicate_event_ids_are_reported(self):
        session_event = self.create_event("user.message", {"content": "Task"})
        self.write_events([session_event, session_event])
        history_index = session_history_reader.index_history(self.history_path)
        self.assertEqual(history_index["duplicate_event_ids"], [session_event["id"]])

    def test_session_identifier_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            session_history_reader.resolve_history_path("../../other-session")


if __name__ == "__main__":
    unittest.main()
