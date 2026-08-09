#!/usr/bin/env python3
"""Validate the plugin manifest and every Codex Skill in this repository."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}


def validate_plugin(errors: list[str]) -> None:
    path = ROOT / ".codex-plugin" / "plugin.json"
    data = load_json(path, errors)
    required = ("name", "version", "description", "author", "skills", "interface")
    for key in required:
        if not data.get(key):
            errors.append(f".codex-plugin/plugin.json: missing {key}")
    if data.get("name") != ROOT.name:
        errors.append("plugin name must match repository directory name")
    if not SEMVER_PATTERN.fullmatch(str(data.get("version", ""))):
        errors.append("plugin version must use semantic versioning")
    skills_path = ROOT / str(data.get("skills", "")).removeprefix("./")
    if not skills_path.is_dir():
        errors.append("plugin skills path does not exist")
    interface = data.get("interface", {})
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not interface.get(key):
            errors.append(f"plugin interface missing {key}")


def read_frontmatter(path: Path, errors: list[str]) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return {}
    try:
        _, raw, _ = text.split("---", 2)
        return yaml.safe_load(raw) or {}
    except (ValueError, yaml.YAMLError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid frontmatter: {exc}")
        return {}


def validate_skill(skill_dir: Path, errors: list[str]) -> None:
    if not NAME_PATTERN.fullmatch(skill_dir.name):
        errors.append(f"invalid skill directory name: {skill_dir.name}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
        return
    metadata = read_frontmatter(skill_md, errors)
    if metadata.get("name") != skill_dir.name:
        errors.append(f"{skill_md.relative_to(ROOT)}: name must match directory")
    if not metadata.get("description"):
        errors.append(f"{skill_md.relative_to(ROOT)}: missing description")
    extra = set(metadata) - {"name", "description"}
    if extra:
        errors.append(f"{skill_md.relative_to(ROOT)}: unsupported frontmatter keys: {sorted(extra)}")

    ui_path = skill_dir / "agents" / "openai.yaml"
    if not ui_path.is_file():
        errors.append(f"{skill_dir.relative_to(ROOT)}: missing agents/openai.yaml")
    else:
        try:
            ui = yaml.safe_load(ui_path.read_text(encoding="utf-8")) or {}
            interface = ui.get("interface", {})
            if not interface.get("display_name") or not interface.get("short_description"):
                errors.append(f"{ui_path.relative_to(ROOT)}: incomplete interface metadata")
            if f"${skill_dir.name}" not in interface.get("default_prompt", ""):
                errors.append(f"{ui_path.relative_to(ROOT)}: default_prompt must mention ${skill_dir.name}")
        except yaml.YAMLError as exc:
            errors.append(f"{ui_path.relative_to(ROOT)}: invalid YAML: {exc}")

    for path in skill_dir.rglob("*.json"):
        load_json(path, errors)
    for path in skill_dir.rglob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc.msg}")


def main() -> int:
    errors: list[str] = []
    validate_plugin(errors)
    skill_dirs = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("repository must contain at least one skill")
    for skill_dir in skill_dirs:
        validate_skill(skill_dir, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"PASS: plugin manifest and {len(skill_dirs)} skill(s) are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
