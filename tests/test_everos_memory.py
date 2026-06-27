import os
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import everos_memory as em


class EverOSMemoryTests(unittest.TestCase):
    def test_read_env_prefers_process_env(self):
        with mock.patch.dict(os.environ, {"EVEROS_TEST_KEY": "process-value"}):
            with mock.patch.object(em, "read_windows_user_env", return_value="user-value"):
                self.assertEqual(em.read_env("EVEROS_TEST_KEY"), "process-value")

    def test_read_windows_user_env_falls_back_to_hkcu_environment(self):
        class FakeKey:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        fake_winreg = types.SimpleNamespace(
            HKEY_CURRENT_USER=object(),
            OpenKey=lambda root, path: FakeKey(),
            QueryValueEx=lambda key, name: ("user-value", 1),
        )

        with mock.patch.object(em.os, "name", "nt"):
            with mock.patch.dict(sys.modules, {"winreg": fake_winreg}):
                self.assertEqual(em.read_windows_user_env("EVEROS_TEST_KEY"), "user-value")


if __name__ == "__main__":
    unittest.main()
