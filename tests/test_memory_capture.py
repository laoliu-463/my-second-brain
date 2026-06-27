import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import memory_capture as mc


class MemoryCaptureTests(unittest.TestCase):
    def test_redact_removes_secrets_and_user_paths(self):
        text = "OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz C:\\Users\\caojianing\\.ssh"
        redacted = mc.redact(text)

        self.assertNotIn("sk-abcdefghijklmnopqrstuvwxyz", redacted)
        self.assertNotIn("caojianing", redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_summary_marks_cognitive_content(self):
        summary, cognitive = mc.build_cloud_summary(
            agent="codex",
            source="test",
            session_id="s1",
            capture_id="c1",
            raw_text="用户讨论政治经济问题，并确认这些认知内容必须写入记忆。",
        )

        self.assertTrue(cognitive)
        self.assertIn("cognitive_required: true", summary)
        self.assertIn("政治经济", summary)

    def test_claude_stop_json_reads_transcript_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = Path(tmpdir) / "transcript.txt"
            transcript.write_text("hello transcript", encoding="utf-8")
            event = json.dumps({"transcript_path": str(transcript), "session_id": "abc"})

            text, metadata = mc.read_claude_stop_json(event)

        self.assertEqual(text, "hello transcript")
        self.assertEqual(metadata["input_format"], "claude-stop-json")

    def test_codex_hook_json_extracts_prompt_text(self):
        event = json.dumps(
            {
                "cwd": str(ROOT),
                "prompt": "用户讨论政治经济问题，要求 Codex hook 自动写入记忆。",
            },
            ensure_ascii=False,
        )

        text, metadata = mc.read_codex_hook_json(event)

        self.assertIn("政治经济", text)
        self.assertEqual(metadata["input_format"], "codex-hook-json")
        self.assertEqual(metadata["extracted_text_sections"], 1)

    def test_codex_hook_json_reads_transcript_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = Path(tmpdir) / "codex-transcript.txt"
            transcript.write_text("codex transcript 认知内容", encoding="utf-8")
            event = json.dumps({"transcriptPath": str(transcript), "cwd": str(ROOT)})

            text, metadata = mc.read_codex_hook_json(event)

        self.assertEqual(text, "codex transcript 认知内容")
        self.assertEqual(metadata["input_format"], "codex-hook-json")

    def test_codex_user_prompt_submit_prefers_prompt_over_transcript(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = Path(tmpdir) / "codex-transcript.txt"
            transcript.write_text("old full transcript", encoding="utf-8")
            event = json.dumps(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "transcript_path": str(transcript),
                    "prompt": "fresh prompt 认知内容",
                    "cwd": str(ROOT),
                },
                ensure_ascii=False,
            )

            text, metadata = mc.read_codex_hook_json(event)

        self.assertEqual(text, "fresh prompt 认知内容")
        self.assertEqual(metadata["extracted_text_sections"], 1)

    def test_capture_writes_local_transcript_without_cloud(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            args = Namespace(
                agent="codex",
                source="test",
                session_id="s1",
                everos_session_id=None,
                user_id=None,
                input_file=None,
                input_format="text",
                text="用户确认认知讨论必须自动写入记忆。",
                encoding="utf-8",
                output_dir=tmpdir,
                max_cloud_chars=4000,
                capture_id="fixed",
                save_raw=True,
                cloud=False,
                flush=True,
                dry_run=False,
                fail_on_cloud_error=False,
            )

            record = mc.capture(args)

            self.assertFalse(record.cloud_written)
            self.assertTrue(Path(record.transcript_path).exists())
            self.assertTrue(Path(record.metadata_path).exists())
            self.assertTrue(record.cognitive_required)


if __name__ == "__main__":
    unittest.main()
