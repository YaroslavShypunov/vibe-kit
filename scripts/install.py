#!/usr/bin/env python3
"""Install the toolkit and merge its portable Copilot settings."""

import argparse
import copy
import datetime
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile


KIT_ROOT = Path(__file__).resolve().parent.parent
MANAGED_BLOCK_NAMES = ("user-owned-workflows", "user-build-models")


def read_settings(settings_path):
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    if not isinstance(settings, dict):
        raise ValueError(f"Settings must be a JSON object: {settings_path}")
    return settings


def merge_settings(existing_settings, portable_settings):
    merged_settings = copy.deepcopy(existing_settings)
    for setting_name, setting_value in portable_settings.items():
        if isinstance(setting_value, dict):
            existing_value = merged_settings.get(setting_name, {})
            if not isinstance(existing_value, dict):
                raise ValueError(f"Existing setting must be an object: {setting_name}")
            merged_settings[setting_name] = merge_settings(existing_value, setting_value)
        else:
            merged_settings[setting_name] = setting_value
    return merged_settings


def merge_instructions(existing_instructions, portable_instructions):
    merged_instructions = existing_instructions
    for block_name in MANAGED_BLOCK_NAMES:
        start_marker = f"<!-- {block_name}:start -->"
        end_marker = f"<!-- {block_name}:end -->"
        if portable_instructions.count(start_marker) != 1 or portable_instructions.count(end_marker) != 1:
            raise ValueError(f"Portable instructions need one complete block: {block_name}")
        source_start = portable_instructions.index(start_marker)
        source_end = portable_instructions.index(end_marker) + len(end_marker)
        if source_end <= source_start:
            raise ValueError(f"Portable instruction markers are out of order: {block_name}")
        portable_block = portable_instructions[source_start:source_end]
        start_count = merged_instructions.count(start_marker)
        end_count = merged_instructions.count(end_marker)
        if start_count == 0 and end_count == 0:
            separator = ""
            if merged_instructions and not merged_instructions.endswith("\n\n"):
                separator = "\n" if merged_instructions.endswith("\n") else "\n\n"
            merged_instructions += separator + portable_block + "\n"
        elif start_count == 1 and end_count == 1:
            existing_start = merged_instructions.index(start_marker)
            existing_end = merged_instructions.index(end_marker) + len(end_marker)
            if existing_end <= existing_start:
                raise ValueError(f"Existing instruction markers are out of order: {block_name}")
            merged_instructions = (
                merged_instructions[:existing_start]
                + portable_block
                + merged_instructions[existing_end:]
            )
        else:
            raise ValueError(f"Existing instructions have duplicate or incomplete markers: {block_name}")
    return merged_instructions


def collect_links(home_folder):
    link_targets = []
    skill_folders = (
        home_folder / ".copilot" / "skills",
        home_folder / ".agents" / "skills",
        home_folder / ".codex" / "skills",
    )
    for skill_source in sorted((KIT_ROOT / "skills").iterdir()):
        if not skill_source.is_dir():
            continue
        if not (skill_source / "SKILL.md").is_file():
            raise ValueError(f"Skill has no SKILL.md: {skill_source}")
        for skill_folder in skill_folders:
            link_targets.append((skill_source, skill_folder / skill_source.name))
    for agent_source in sorted((KIT_ROOT / "agents").glob("*.agent.md")):
        link_targets.append((agent_source, home_folder / ".copilot" / "agents" / agent_source.name))
    for instruction_source in sorted((KIT_ROOT / "instructions").glob("*.instructions.md")):
        link_targets.append(
            (instruction_source, home_folder / ".copilot" / "instructions" / instruction_source.name)
        )
    return link_targets


def has_expected_link(source_path, destination_path):
    return destination_path.is_symlink() and destination_path.resolve() == source_path.resolve()


def backup_existing(destination_path, home_folder, backup_folder, move=False):
    backup_folder.mkdir(mode=0o700, parents=True, exist_ok=True)
    backup_path = backup_folder / destination_path.relative_to(home_folder)
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if move:
        destination_path.rename(backup_path)
    else:
        shutil.copy2(destination_path, backup_path)
    print(f"Backed up {destination_path} -> {backup_path}")


def write_file(destination_path, contents):
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    existing_mode = stat.S_IMODE(destination_path.stat().st_mode) if destination_path.exists() else 0o600
    with tempfile.NamedTemporaryFile(dir=destination_path.parent, delete=False) as temporary_file:
        temporary_path = Path(temporary_file.name)
    try:
        temporary_path.write_bytes(contents)
        temporary_path.chmod(existing_mode)
        os.replace(temporary_path, destination_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    print(f"Updated {destination_path}")


def install(replace_existing):
    home_folder = Path.home()
    copilot_folder = home_folder / ".copilot"
    settings_path = copilot_folder / "settings.json"
    instructions_path = copilot_folder / "copilot-instructions.md"
    for configuration_path in (settings_path, instructions_path):
        if configuration_path.is_symlink():
            raise ValueError(f"Configuration is a symlink; merge it manually: {configuration_path}")
    portable_settings = read_settings(KIT_ROOT / "settings" / "build-settings.json")
    existing_settings = read_settings(settings_path) if settings_path.exists() else {}
    merged_settings = merge_settings(existing_settings, portable_settings)
    existing_instructions = (
        instructions_path.read_bytes().decode("utf-8") if instructions_path.exists() else ""
    )
    portable_instructions = (KIT_ROOT / "settings" / "copilot-instructions.md").read_text(encoding="utf-8")
    merged_instructions = merge_instructions(existing_instructions, portable_instructions)

    pending_writes = []
    if merged_settings != existing_settings or not settings_path.exists():
        pending_writes.append((settings_path, (json.dumps(merged_settings, indent=2) + "\n").encode("utf-8")))
    if merged_instructions != existing_instructions:
        pending_writes.append((instructions_path, merged_instructions.encode("utf-8")))

    link_targets = collect_links(home_folder)
    conflicts = [
        destination_path
        for source_path, destination_path in link_targets
        if os.path.lexists(destination_path) and not has_expected_link(source_path, destination_path)
    ]
    if conflicts and not replace_existing:
        conflict_list = "\n".join(f"  {destination_path}" for destination_path in conflicts)
        raise ValueError(
            f"Existing files or links conflict with the toolkit:\n{conflict_list}\n"
            "Nothing was changed. Run ./install.sh --replace to back them up and install toolkit links."
        )
    for destination_path in [destination for source, destination in link_targets] + [
        destination for destination, contents in pending_writes
    ]:
        for parent_folder in destination_path.parents:
            if parent_folder == home_folder:
                break
            if os.path.lexists(parent_folder) and not parent_folder.is_dir():
                raise ValueError(f"Installation parent is not a directory: {parent_folder}")

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_folder = copilot_folder / "backups" / f"vibe-kit-{timestamp}"
    for source_path, destination_path in link_targets:
        if has_expected_link(source_path, destination_path):
            continue
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        if os.path.lexists(destination_path):
            backup_existing(destination_path, home_folder, backup_folder, move=True)
        destination_path.symlink_to(source_path, target_is_directory=source_path.is_dir())
        print(f"Linked {destination_path} -> {source_path}")
    for destination_path, contents in pending_writes:
        if destination_path.exists():
            backup_existing(destination_path, home_folder, backup_folder)
        write_file(destination_path, contents)
    print("Installed toolkit. Restart Copilot CLI, then check /skills info build and /subagents.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--replace",
        action="store_true",
        help="back up conflicting existing skills, agents, and instructions before replacing them with links",
    )
    arguments = parser.parse_args()
    try:
        install(arguments.replace)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
