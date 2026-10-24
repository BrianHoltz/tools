#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Brian Holtz
# SPDX-License-Identifier: MIT

import importlib.util
import zipfile
from datetime import datetime, timedelta
from importlib.machinery import SourceFileLoader
from pathlib import Path

PATH = Path(__file__).parent.parent / "prune-artifacts"
SPEC = importlib.util.spec_from_loader("prune_artifacts", SourceFileLoader("prune_artifacts", str(PATH)))
prune = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(prune)


def at(text):
    return datetime.strptime(text, "%Y.%m.%d.%H%M")


class TestParse:
    def test_build_timestamp_conventions(self):
        cases = {
            "langley-1.1.20261024-Sat.1109-plot-frame.zip": ("langley.zip", at("2026.10.24.1109")),
            "code-puppy-jetbrains-0.31.2-20261023.Fri.1943-paste-shortcut.zip":
                ("code-puppy-jetbrains.zip", at("2026.10.23.1943")),
            "markdown-editor-2.0.7-local.16-20261023.Fri.083012-live-theme.zip":
                ("markdown-editor.zip", datetime(2026, 10, 23, 8, 30, 12)),
            "langley-1.0.20261020.zip": ("langley.zip", datetime(2026, 10, 20, 23, 59, 59)),
        }
        for name, expected in cases.items():
            assert prune.parse_artifact(name) == expected, name

    def test_variants_and_packaging_are_separate_products(self):
        names = ["code-puppy-jetbrains-legacy-0.31.2-20261021.Wed.0808-jcef.zip",
                 "markdown-editor-0.1.22-local.7-20261019.Mon.1812-listfix.vsix"]
        assert [prune.parse_artifact(name)[0] for name in names] == [
            "code-puppy-jetbrains-legacy.zip", "markdown-editor.vsix"]

    def test_unrecognized_or_inconsistent_names_are_ineligible(self):
        for name in ["air-plugin.zip", "notes-20261024.Sat.1109.txt",
                     "langley-1.1.20261024-Fri.1109-wrong-day.zip", "photo-2026.zip",
                     "tool-1.0-20261399.Sat.1200-bad-date.zip", "2026-build.zip"]:
            assert prune.parse_artifact(name) is None, name


class TestRetention:
    def test_newest_of_last_three_hours_days_weeks_and_months(self):
        builds = [datetime(2026, 10, 1, 12) + timedelta(days=day) for day in range(55)]
        assert sorted(prune.retained(builds), reverse=True) == [
            at("2026.11.24.1200"), at("2026.11.23.1200"), at("2026.11.22.1200"),
            at("2026.11.15.1200"), at("2026.10.31.1200")]

    def test_busy_day_keeps_newest_of_each_active_hour(self):
        builds = [at("2026.10.24.1155"), at("2026.10.24.1109"), at("2026.10.24.1006"),
                  at("2026.10.24.0815"), at("2026.10.23.2342")]
        assert set(prune.retained(builds)) == {
            at("2026.10.24.1155"), at("2026.10.24.1006"), at("2026.10.24.0815"), at("2026.10.23.2342")}


def make_zip(path, entries):
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in entries.items():
            archive.writestr(name, data)


class TestPlan:
    def test_installed_jetbrains_and_vscode_builds_survive(self, tmp_path):
        downloads = tmp_path / "Downloads"; downloads.mkdir()
        plugins = tmp_path / "plugins" / "langley" / "lib"; plugins.mkdir(parents=True)
        (plugins / "langley.jar").write_bytes(b"installed")
        extensions = tmp_path / "extensions" / "me.editor-1.0.0"; extensions.mkdir(parents=True)
        (extensions / "main.js").write_text("installed")
        (extensions / "package.json").write_text('{"__metadata": {}}')
        make_zip(downloads / "langley-1.0.20260101-Thu.1200-old.zip", {"langley/lib/langley.jar": b"installed"})
        newer = [datetime(2026, 2, day) for day in range(2, 9)] + [datetime(2026, 3, 1), datetime(2026, 4, 1)]
        for day in newer:
            make_zip(downloads / f"langley-1.0.{day:%Y%m%d}-{day:%a}.1200-new.zip",
                     {"langley/lib/langley.jar": b"new"})
        package = '{"publisher": "me", "name": "editor", "version": "1.0.0"}'
        make_zip(downloads / "editor-1.0.0-20250101.Wed.1200-old.vsix",
                 {"extension/main.js": "installed", "extension/package.json": package})
        for day in [datetime(2026, 1, 1), datetime(2026, 2, 1), datetime(2026, 3, 1)]:
            make_zip(downloads / f"editor-1.0.0-{day:%Y%m%d.%a}.1200-new.vsix",
                     {"extension/main.js": "new", "extension/package.json": package})
        plan = prune.plan(downloads, [tmp_path / "plugins"], [tmp_path / "extensions"])
        reasons = {item.path.name: item.reasons for item in plan}
        assert reasons["langley-1.0.20260101-Thu.1200-old.zip"] == ["installed"]
        assert reasons["editor-1.0.0-20250101.Wed.1200-old.vsix"] == ["installed"]
        assert "hour" in reasons["editor-1.0.0-20260301.Sun.1200-new.vsix"]
        assert reasons["langley-1.0.20260202-Mon.1200-new.zip"] == []

    def test_dry_run_moves_nothing_and_apply_trashes_only_unretained(self, tmp_path):
        names = [f"tool-1.0-202610{day:02d}.{datetime(2026, 10, day):%a}.1200-x.zip" for day in range(1, 25)]
        for name in names + ["air-plugin.zip"]:
            make_zip(tmp_path / name, {"x": "y"})
        trashed = []
        prune.main([str(tmp_path)], trash=trashed.append, jetbrains=[], vscode=[])
        assert trashed == []
        prune.main(["--apply", str(tmp_path)], trash=trashed.append, jetbrains=[], vscode=[])
        assert sorted(path.name for path in trashed) == sorted(
            name for name in names if not any(day in name for day in ["1024", "1023", "1022", "1018", "1011"]))
        assert (tmp_path / "air-plugin.zip") not in trashed
