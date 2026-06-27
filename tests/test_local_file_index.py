import sqlite3
import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import local_file_index as lfi


class LocalFileIndexTests(unittest.TestCase):
    def test_sensitive_files_are_skipped(self):
        self.assertTrue(lfi.is_sensitive_file(Path(".env")))
        self.assertTrue(lfi.is_sensitive_file(Path("id_rsa")))
        self.assertTrue(lfi.is_sensitive_file(Path("secret.pem")))
        self.assertFalse(lfi.is_sensitive_file(Path("notes.md")))

    def test_indexes_and_searches_markdown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            note = root / "note.md"
            note.write_text("alpha beta EverOS local index", encoding="utf-8")
            (root / ".env").write_text("SECRET=1", encoding="utf-8")

            db = root / "index.sqlite3"
            conn = lfi.connect(db)
            try:
                files = list(
                    lfi.iter_files(
                        [root],
                        allowed_extensions={".md", ".txt"},
                        extra_skip_dirs=set(),
                        max_bytes=1024 * 1024,
                    )
                )
                self.assertEqual(files, [note])
                extracted = lfi.extract_text(note, 1000)
                lfi.upsert_file(conn, note, extracted)
                conn.commit()

                row = conn.execute(
                    "SELECT path FROM file_fts WHERE file_fts MATCH ?",
                    (lfi.escape_fts_query("EverOS"),),
                ).fetchone()
                self.assertEqual(Path(row[0]), note.resolve())
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
