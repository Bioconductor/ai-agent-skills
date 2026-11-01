#!/usr/bin/env python3
"""
build_claude_plugins.py — Build uploadable Claude plugin archives.

Reads .claude-plugin/marketplace.json and writes one <plugin>.zip per plugin,
each containing .claude-plugin/plugin.json and the plugin's skills/<name>/
folders. Upload the archives in the Claude desktop app under
Customize → Plugins → Add → Upload plugin.

Usage:
  python scripts/build_claude_plugins.py            # writes to dist/
  python scripts/build_claude_plugins.py OUT_DIR
"""

import json
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
EXCLUDED_PARTS = {"__pycache__", ".DS_Store"}


def git_short_sha():
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd=REPO_ROOT
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def build_plugin(plugin, marketplace, out_dir):
    name = plugin["name"]
    manifest = {
        "name": name,
        "description": plugin.get("description", ""),
        "author": {"name": marketplace["owner"]["name"]},
        "homepage": marketplace["owner"].get("url", ""),
        "license": "MIT",
    }
    sha = git_short_sha()
    if sha:
        manifest["version"] = f"0.0.0+{sha}"

    archive = out_dir / f"{name}.zip"
    source_root = (REPO_ROOT / plugin.get("source", "./")).resolve()
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(".claude-plugin/plugin.json", json.dumps(manifest, indent=2) + "\n")
        zf.write(REPO_ROOT / "LICENSE", "LICENSE")
        skill_list = "\n".join(f"- `{Path(entry).name}`" for entry in plugin["skills"])
        zf.writestr("README.md", f"# {name}\n\n{manifest['description']}\n\n"
                                 f"Skills:\n\n{skill_list}\n\n"
                                 f"Built from {manifest['homepage']}; see SKILLS.md there for details.\n")
        for entry in plugin["skills"]:
            skill_dir = (source_root / entry).resolve()
            if not (skill_dir / "SKILL.md").exists():
                sys.exit(f"ERROR: {entry} in plugin `{name}` has no SKILL.md")
            for path in sorted(skill_dir.rglob("*")):
                if path.is_file() and not EXCLUDED_PARTS & set(path.parts):
                    zf.write(path, Path("skills") / skill_dir.name / path.relative_to(skill_dir))
    print(f"  {archive.relative_to(Path.cwd()) if archive.is_relative_to(Path.cwd()) else archive}"
          f"  ({len(plugin['skills'])} skills)")


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    marketplace = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    print(f"Building {len(marketplace['plugins'])} plugin archive(s):")
    for plugin in marketplace["plugins"]:
        build_plugin(plugin, marketplace, out_dir)


if __name__ == "__main__":
    main()
