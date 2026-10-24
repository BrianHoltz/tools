import importlib.util
from importlib.machinery import SourceFileLoader
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

SOURCE = Path(__file__).resolve().parents[1] / "langley-install"
SPEC = importlib.util.spec_from_loader("langley_install", SourceFileLoader("langley_install", str(SOURCE)))
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


def make_package(path, plugin_id="com.walmart.langley", extra=None):
    jar_bytes = io.BytesIO()
    with ZipFile(jar_bytes, "w") as jar:
        jar.writestr("META-INF/plugin.xml", f"<idea-plugin><id>{plugin_id}</id><version>1.1.20261024</version></idea-plugin>")
    with ZipFile(path, "w") as archive:
        archive.writestr("langley/lib/langley.jar", jar_bytes.getvalue())
        for name, data in (extra or {}).items():
            archive.writestr(name, data)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "plugin.zip"
        make_package(self.package)

    def test_package_and_exact_tree(self):
        files, version = installer.package_files(self.package)
        self.assertEqual(version, "1.1.20261024")
        folder = self.root / "installed"
        for path, data in files.items():
            (folder / path).parent.mkdir(parents=True, exist_ok=True)
            (folder / path).write_bytes(data)
        installer.verify_tree(folder, files)
        (folder / "extra").write_text("old")
        with self.assertRaises(ValueError):
            installer.verify_tree(folder, files)

    def test_reject_wrong_plugin(self):
        make_package(self.package, "different.plugin")
        with self.assertRaises(ValueError):
            installer.package_files(self.package)

    def test_reject_traversal_absolute_and_foreign_root(self):
        for name in ("langley/../escape", "/langley/escape", "other/lib/file"):
            with self.subTest(name=name):
                make_package(self.package, extra={name: "unsafe"})
                with self.assertRaises(ValueError):
                    installer.package_files(self.package)

    def test_install_preserves_previous_plugin(self):
        destination = self.root / "destination"
        destination.mkdir()
        (destination / "old").write_text("previous")
        stage = self.root / "staged"
        stage.mkdir()
        (stage / "new").write_bytes(b"new")
        backup = self.root / "backup"
        installer.install_staged(stage, destination, backup, {Path("new"): b"new"})
        self.assertEqual((backup / "old").read_text(), "previous")
        self.assertEqual((destination / "new").read_bytes(), b"new")

    def test_failed_verification_restores_previous_plugin(self):
        destination = self.root / "destination"
        destination.mkdir()
        (destination / "old").write_text("previous")
        stage = self.root / "staged"
        stage.mkdir()
        (stage / "new").write_bytes(b"wrong")
        with self.assertRaises(ValueError):
            installer.install_staged(stage, destination, self.root / "backup", {Path("new"): b"expected"})
        self.assertEqual((destination / "old").read_text(), "previous")
        self.assertEqual((stage / "new").read_bytes(), b"wrong")

    def test_does_not_replace_existing_backup(self):
        backup = self.root / "backup"
        backup.mkdir()
        with self.assertRaises(FileExistsError):
            installer.install_staged(self.root / "stage", self.root / "dest", backup, {})

    def test_pid_matching_is_exact(self):
        with patch.object(installer.subprocess, "check_output", return_value="12 /Applications/IDE.app/Contents/MacOS/idea\n13 /Applications/IDE.app/Contents/MacOS/idea-other\n"):
            self.assertEqual(installer.idea_pids(Path("/Applications/IDE.app")), [12])

    def test_wait_timeout(self):
        with self.assertRaises(TimeoutError):
            installer.wait_until(lambda: False, 0, "stopped")

    def test_dry_run_has_no_process_side_effects(self):
        with patch("sys.argv", [str(SOURCE), str(self.package)]), patch.object(installer.subprocess, "run") as run:
            self.assertEqual(installer.main(), 0)
            run.assert_not_called()

    def execute_args(self):
        from argparse import Namespace
        app = self.root / "IDE.app"
        (app / "Contents/MacOS").mkdir(parents=True)
        (app / "Contents/MacOS/idea").touch()
        plugins = self.root / "plugins"
        (plugins / "langley").mkdir(parents=True)
        (plugins / "langley/old").write_text("previous")
        run_dir = self.root / "run"
        run_dir.mkdir()
        return Namespace(app=app, plugins=plugins, timeout=0), run_dir

    def test_execute_quit_install_relaunch(self):
        args, run_dir = self.execute_args()
        with patch.object(installer, "idea_pids", side_effect=[[12], [], [13]]), patch.object(installer.subprocess, "run") as run:
            installer.execute(args, {Path("new"): b"new"}, run_dir)
        self.assertEqual(run.call_args_list[0].args[0][0], "osascript")
        self.assertEqual(run.call_args_list[1].args[0][:2], ["open", "-a"])
        self.assertEqual((run_dir / "previous-langley/old").read_text(), "previous")
        self.assertEqual((args.plugins / "langley/new").read_bytes(), b"new")

    def test_quit_timeout_leaves_installed_plugin_untouched(self):
        args, run_dir = self.execute_args()
        with patch.object(installer, "idea_pids", return_value=[12]), patch.object(installer.subprocess, "run") as run:
            with self.assertRaises(TimeoutError):
                installer.execute(args, {Path("new"): b"new"}, run_dir)
        self.assertEqual((args.plugins / "langley/old").read_text(), "previous")
        self.assertFalse((run_dir / "previous-langley").exists())
        self.assertEqual(run.call_count, 1)

    def test_quit_error_still_installs_when_idea_exited(self):
        errors = [
            installer.subprocess.CalledProcessError(1, "osascript", stderr="User canceled. (-128)"),
            installer.subprocess.TimeoutExpired("osascript", 1),
        ]
        for index, error in enumerate(errors):
            with self.subTest(error=type(error).__name__), tempfile.TemporaryDirectory() as temp:
                original_root = self.root
                self.root = Path(temp)
                args, run_dir = self.execute_args()
                self.root = original_root
                with patch.object(installer, "idea_pids", side_effect=[[12], [], [13]]), patch.object(installer.subprocess, "run", side_effect=[error, None]) as run:
                    installer.execute(args, {Path("new"): b"new"}, run_dir)
                self.assertEqual(run.call_count, 2)
                self.assertEqual((args.plugins / "langley/new").read_bytes(), b"new")

    def test_canceled_quit_never_installs_while_idea_remains_running(self):
        args, run_dir = self.execute_args()
        error = installer.subprocess.CalledProcessError(1, "osascript", stderr="User canceled. (-128)")
        with patch.object(installer, "idea_pids", return_value=[12]), patch.object(installer.subprocess, "run", side_effect=error) as run:
            with self.assertRaises(TimeoutError):
                installer.execute(args, {Path("new"): b"new"}, run_dir)
        self.assertEqual((args.plugins / "langley/old").read_text(), "previous")
        self.assertEqual(run.call_count, 1)

    def test_failed_install_relaunches_restored_plugin(self):
        args, run_dir = self.execute_args()
        with patch.object(installer, "idea_pids", side_effect=[[12], [], [13]]), patch.object(installer.subprocess, "run") as run, patch.object(installer, "install_staged", side_effect=ValueError("verification failed")):
            with self.assertRaisesRegex(ValueError, "verification failed"):
                installer.execute(args, {Path("new"): b"new"}, run_dir)
        self.assertEqual(run.call_args_list[-1].args[0][:2], ["open", "-a"])
        self.assertEqual((args.plugins / "langley/old").read_text(), "previous")

    def test_apply_requires_agent_preflight(self):
        with patch("sys.argv", [str(SOURCE), str(self.package), "--apply"]):
            with self.assertRaises(SystemExit):
                installer.main()


if __name__ == "__main__":
    unittest.main()
