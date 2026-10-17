"""Repository selection and safety tests for laptop-synchronize."""

import importlib.machinery
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader("laptop_sync", str(ROOT / "laptop-synchronize"))
spec = importlib.util.spec_from_loader(loader.name, loader)
sync = importlib.util.module_from_spec(spec)
loader.exec_module(sync)


class ToolchainSelectionTests(unittest.TestCase):
    def test_manifest_covers_approved_toolchain(self):
        cfg = json.loads((ROOT / "laptop-synchronize.json").read_text())
        paths = {item["path"] for item in cfg["toolchain_repos"]}
        self.assertEqual(paths, {
            "src/code-puppy-ide", "src/idea-markdown-editor",
            "src/vscode-markdown-editor", "src/wibey-jetbrains-plugin",
            "src/wibey-vscode-extension",
        })

    @patch.object(sync, "sync_repository", return_value=True)
    def test_missing_optional_repo_is_skipped(self, synchronize):
        cfg = {"toolchain_repos": [{"path": "/tmp/nonexistent-rollo-toolchain", "optional": True}]}
        self.assertTrue(sync.sync_toolchain(cfg))
        self.assertEqual(synchronize.call_count, 1)

    @patch.object(sync, "sync_repository", side_effect=[True, False])
    def test_missing_required_repo_is_not_silently_skipped(self, synchronize):
        cfg = {"toolchain_repos": [{"path": "/tmp/nonexistent-rollo-toolchain"}]}
        self.assertFalse(sync.sync_toolchain(cfg))
        self.assertEqual(synchronize.call_count, 2)

    @patch.object(sync, "sync_repository", return_value=True)
    def test_remote_override_and_internal_scope_are_forwarded(self, synchronize):
        cfg = {"toolchain_repos": [{
            "path": "src/tools", "label": "duplicate tools",
        }, {
            "path": "src/wibey-jetbrains-plugin", "remote": "fork",
            "branch": "brian/local-combined", "public": False,
        }]}
        self.assertTrue(sync.sync_toolchain(cfg))
        self.assertEqual(synchronize.call_count, 2)
        self.assertEqual(synchronize.call_args.kwargs, {
            "remote": "fork", "branch": "brian/local-combined", "public": False,
        })


if __name__ == "__main__":
    unittest.main()
