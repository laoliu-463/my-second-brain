import argparse
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import everos_local_memory as elm


class EverOSLocalMemoryTests(unittest.TestCase):
    def namespace(self, **kwargs):
        defaults = {
            "app_id": None,
            "project_id": None,
            "session_id": None,
            "user_id": None,
            "agent_id": None,
            "role": "user",
            "sender_id": None,
            "timestamp": 1234567890000,
        }
        defaults.update(kwargs)
        return argparse.Namespace(**defaults)

    def test_add_payload_uses_local_oss_schema(self):
        payload = elm.build_add_payload(self.namespace(), "hello")

        self.assertEqual(payload["app_id"], "second-brain")
        self.assertEqual(payload["project_id"], "my-second-brain")
        self.assertEqual(payload["session_id"], "my-second-brain")
        self.assertEqual(payload["messages"][0]["sender_id"], "my-second-brain-owner")
        self.assertEqual(payload["messages"][0]["role"], "user")
        self.assertEqual(payload["messages"][0]["content"], "hello")

    def test_assistant_sender_defaults_to_agent_id(self):
        payload = elm.build_add_payload(self.namespace(role="assistant"), "done")
        self.assertEqual(payload["messages"][0]["sender_id"], "codex")

    def test_search_payload_uses_exactly_one_owner(self):
        user_payload = elm.build_search_payload(
            argparse.Namespace(
                app_id=None,
                project_id=None,
                user_id=None,
                agent_id=None,
                query="memory",
                method="hybrid",
                top_k=5,
                include_profile=True,
                agent=False,
                radius=None,
                min_score=None,
            )
        )
        agent_payload = elm.build_search_payload(
            argparse.Namespace(
                app_id=None,
                project_id=None,
                user_id=None,
                agent_id="codex",
                query="memory",
                method="hybrid",
                top_k=5,
                include_profile=False,
                agent=True,
                radius=None,
                min_score=None,
            )
        )

        self.assertIn("user_id", user_payload)
        self.assertNotIn("agent_id", user_payload)
        self.assertIn("agent_id", agent_payload)
        self.assertNotIn("user_id", agent_payload)

    def test_openapi_memory_route_detection(self):
        good = {
            "paths": {
                "/api/v1/memory/add": {},
                "/api/v1/memory/flush": {},
                "/api/v1/memory/search": {},
            }
        }
        wrong_service = {"paths": {"/health": {}, "/api/v1/kb/ask": {}}}

        self.assertTrue(elm.openapi_has_memory_api(good))
        self.assertFalse(elm.openapi_has_memory_api(wrong_service))
        self.assertFalse(elm.openapi_has_memory_api(None))


if __name__ == "__main__":
    unittest.main()
