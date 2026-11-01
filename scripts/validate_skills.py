#!/usr/bin/env python3
"""
validate_skills.py — Gatekeeper CI check for bioconductor/ai-agent-skills.

Derived from: skills/validate-skill/SKILL.md (the gold standard for validation rules).

Checks performed:
  1. Required frontmatter fields present and non-empty (name, description, and
     metadata.version, metadata.category, metadata.author)
  2. Only top-level frontmatter fields accepted by Claude skill upload; no
     prohibited fields (platforms, triggers)
  2a. name/description meet Claude upload limits (kebab-case name <= 64 chars,
      description <= 1024 chars with no angle brackets)
  3. Directory name matches the `name` field
  4. Skill name is globally unique (no collisions with other skills)
  5. SKILLS.md is in sync (new/changed descriptions must appear in the index)
  6. Relative links in the skill body resolve to existing files on disk
  7. Version was bumped if the file was modified (not newly created)
  8. .claude-plugin/marketplace.json lists every skill in exactly one plugin

Usage:
  python scripts/validate_skills.py
  BASE_REF=devel python scripts/validate_skills.py

Exit codes:
  0 — all checks passed
  1 — one or more checks failed
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SKILLS_MD = REPO_ROOT / "SKILLS.md"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"

REQUIRED_FIELDS = {"name", "description"}
REQUIRED_METADATA = {"version", "category", "author"}
# Top-level keys accepted by claude.ai / Skills API upload; everything else
# belongs under `metadata:` (see AGENTS.md § Minimal Required Fields).
ALLOWED_FIELDS = {"name", "description", "metadata", "license", "allowed-tools", "compatibility"}
PROHIBITED_FIELDS = {"platforms", "triggers"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024

# ──────────────────────────────────────────────────────────────────────────────
# Git helpers
# ──────────────────────────────────────────────────────────────────────────────

def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=REPO_ROOT)
    if result.returncode != 0:
        cmd = " ".join(["git", *args])
        print(f"ERROR: {cmd} failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def get_modified_skill_files():
    """Return SKILL.md paths modified in the current PR (vs BASE_REF)."""
    base_ref = os.environ.get("BASE_REF", "devel")
    changed = git("diff", "--name-only", f"origin/{base_ref}...HEAD")
    skill_files = []
    for line in changed.splitlines():
        p = REPO_ROOT / line
        if p.name == "SKILL.md" and p.exists():
            skill_files.append(p)
    return skill_files


def get_base_content(skill_path):
    """Return file content from the base branch, or None if newly added."""
    base_ref = os.environ.get("BASE_REF", "devel")
    rel = skill_path.relative_to(REPO_ROOT)
    result = subprocess.run(
        ["git", "show", f"origin/{base_ref}:{rel}"],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    if result.returncode != 0:
        return None  # file is new
    return result.stdout


# ──────────────────────────────────────────────────────────────────────────────
# Parsing helpers
# ──────────────────────────────────────────────────────────────────────────────

def parse_frontmatter(content):
    """Extract YAML frontmatter from a markdown file. Returns (dict, body_str)."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    raw_yaml = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    try:
        data = yaml.safe_load(raw_yaml) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse error: {e}")
    return data, body


def extract_relative_links(body):
    """Return all relative link targets from markdown body."""
    # matches [text](path) where path does not start with http/https/#
    pattern = re.compile(r'\[.*?\]\(([^)]+)\)')
    links = []
    for match in pattern.finditer(body):
        target = match.group(1)
        if not target.startswith(("http://", "https://", "#", "mailto:")):
            links.append(target)
    return links


def get_all_skill_names():
    """Return mapping of {name: Path} for all skills in the repo."""
    names = {}
    for skill_dir in SKILLS_DIR.iterdir():
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            fm, _ = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
            if "name" in fm:
                names[fm["name"]] = skill_dir
        except Exception:
            pass
    return names


# ──────────────────────────────────────────────────────────────────────────────
# Individual checks
# ──────────────────────────────────────────────────────────────────────────────

def get_metadata(fm):
    """Return the `metadata` mapping, or {} if absent or malformed."""
    meta = fm.get("metadata")
    return meta if isinstance(meta, dict) else {}


def check_required_fields(fm, skill_path, errors):
    missing = REQUIRED_FIELDS - set(fm.keys())
    for field in sorted(missing):
        errors.append(f"[{skill_path.parent.name}] MISSING required frontmatter field: `{field}`")
    for field in sorted(REQUIRED_FIELDS & set(fm.keys())):
        if not fm[field]:
            errors.append(f"[{skill_path.parent.name}] EMPTY required frontmatter field: `{field}`")

    if "metadata" in fm and not isinstance(fm["metadata"], dict):
        errors.append(f"[{skill_path.parent.name}] `metadata` must be a mapping of string keys to string values")
        return
    meta = get_metadata(fm)
    for field in sorted(REQUIRED_METADATA - set(meta.keys())):
        errors.append(f"[{skill_path.parent.name}] MISSING required frontmatter field: `metadata.{field}`")
    for key, value in meta.items():
        if not isinstance(value, str):
            errors.append(
                f"[{skill_path.parent.name}] `metadata.{key}` must be a string "
                f"(got {type(value).__name__}; quote it, or write lists as comma-separated text)"
            )
        elif key in REQUIRED_METADATA and not value.strip():
            errors.append(f"[{skill_path.parent.name}] EMPTY required frontmatter field: `metadata.{key}`")


def check_prohibited_fields(fm, skill_path, errors):
    present = PROHIBITED_FIELDS & set(fm.keys())
    for field in sorted(present):
        errors.append(
            f"[{skill_path.parent.name}] PROHIBITED frontmatter field present: `{field}` "
            f"(skills must be agent-agnostic — see AGENTS.md)"
        )
    for field in sorted(set(fm.keys()) - ALLOWED_FIELDS - PROHIBITED_FIELDS):
        errors.append(
            f"[{skill_path.parent.name}] UNEXPECTED top-level frontmatter field: `{field}`. "
            f"Move it under `metadata:` (Claude skill upload rejects other top-level keys — see AGENTS.md)"
        )


def check_upload_limits(fm, skill_path, errors):
    """Check name/description against the limits enforced by Claude skill upload."""
    name = fm.get("name", "")
    if isinstance(name, str) and name:
        if not NAME_PATTERN.match(name):
            errors.append(
                f"[{skill_path.parent.name}] `name: {name}` must be kebab-case "
                f"(lowercase letters, digits, single hyphens)"
            )
        if len(name) > MAX_NAME_LENGTH:
            errors.append(
                f"[{skill_path.parent.name}] `name` is {len(name)} characters; maximum is {MAX_NAME_LENGTH}"
            )
    description = fm.get("description", "")
    if not isinstance(description, str):
        errors.append(f"[{skill_path.parent.name}] `description` must be a string")
        return
    if "<" in description or ">" in description:
        errors.append(f"[{skill_path.parent.name}] `description` cannot contain angle brackets (< or >)")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"[{skill_path.parent.name}] `description` is {len(description)} characters; "
            f"maximum is {MAX_DESCRIPTION_LENGTH}"
        )


def check_name_matches_directory(fm, skill_path, errors):
    expected = skill_path.parent.name
    actual = fm.get("name", "")
    if actual != expected:
        errors.append(
            f"[{skill_path.parent.name}] `name: {actual}` does not match directory name `{expected}`. "
            f"They must be identical."
        )


def check_name_uniqueness(fm, skill_path, all_names, errors):
    name = fm.get("name", "")
    if not name:
        return
    collision_path = all_names.get(name)
    if collision_path and collision_path != skill_path.parent:
        errors.append(
            f"[{skill_path.parent.name}] Skill name `{name}` collides with existing skill "
            f"at `{collision_path.relative_to(REPO_ROOT)}`"
        )


def check_skills_md_sync(fm, skill_path, base_content, errors):
    """Check that new skills or changed descriptions appear in SKILLS.md."""
    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name or not description:
        return  # structural errors already caught above

    skills_md_content = SKILLS_MD.read_text(encoding="utf-8") if SKILLS_MD.exists() else ""

    # Determine if this is a new skill or if description changed
    is_new = base_content is None
    if not is_new:
        try:
            base_fm, _ = parse_frontmatter(base_content)
            description_changed = base_fm.get("description", "") != description
        except Exception:
            description_changed = False
    else:
        description_changed = False

    if is_new or description_changed:
        # Both the skill name and current description should appear in SKILLS.md
        if name not in skills_md_content or description not in skills_md_content:
            change_type = "new skill added" if is_new else "description changed"
            errors.append(
                f"[{name}] SKILLS.md is out of sync ({change_type}). "
                f"Add or update the entry for `{name}` in SKILLS.md so it includes the current description. "
                f"(See SKILL_STANDARD.md § When Updating Skills)"
            )


def check_relative_links(body, skill_path, errors):
    links = extract_relative_links(body)
    skill_dir = skill_path.parent
    for link in links:
        # Strip any anchor fragment
        path_part = link.split("#")[0]
        if not path_part:
            continue  # pure anchor link

        if Path(path_part).is_absolute():
            errors.append(f"[{skill_path.parent.name}] Absolute link paths are not allowed: `{link}`")
            continue

        target = (skill_dir / path_part).resolve()
        repo_root = REPO_ROOT.resolve()
        if target != repo_root and repo_root not in target.parents:
            errors.append(
                f"[{skill_path.parent.name}] Relative link resolves outside repository: `{link}` "
                f"(resolved to `{target}`)"
            )
            continue

        if not target.exists():
            errors.append(
                f"[{skill_path.parent.name}] Broken relative link: `{link}` "
                f"(resolved to `{target}`, which does not exist)"
            )


def check_structural_headers(body, skill_path, errors):
    """Check that the skill body contains required markdown headings."""
    required_headers = [
        ("Usage", r"^##\s+Usage\b"),
        ("Prerequisites", r"^##\s+Prerequisites\b"),
        ("Process", r"^##\s+Process\b"),
        ("Examples", r"^##\s+Examples\b"),
    ]
    for header_name, pattern in required_headers:
        if not re.search(pattern, body, re.MULTILINE):
            errors.append(
                f"[{skill_path.parent.name}] MISSING structural header: `## {header_name}`. "
                f"See SKILL_STANDARD.md for required sections."
            )


def check_version_bumped(fm, skill_path, base_content, errors):
    """If the file was modified (not new), version must have changed."""
    if base_content is None:
        return  # new file, no bump required
    try:
        base_fm, _ = parse_frontmatter(base_content)
    except Exception:
        return
    # Fall back to a top-level `version` for base files predating the move to `metadata:`
    old_version = get_metadata(base_fm).get("version") or base_fm.get("version", "")
    new_version = get_metadata(fm).get("version", "")
    if old_version and str(old_version) == str(new_version):
        errors.append(
            f"[{skill_path.parent.name}] `metadata.version` was not bumped (still `{old_version}`). "
            f"Update the version following semver. "
            f"(See SKILL_STANDARD.md § Version Management)"
        )


def check_marketplace_sync(errors):
    """Every skill directory must appear in exactly one plugin of marketplace.json."""
    if not MARKETPLACE_JSON.exists():
        return
    try:
        marketplace = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"[marketplace] Cannot parse {MARKETPLACE_JSON.relative_to(REPO_ROOT)}: {e}")
        return

    listed = {}
    for plugin in marketplace.get("plugins", []):
        for entry in plugin.get("skills", []):
            skill_dir = (REPO_ROOT / plugin.get("source", "./") / entry).resolve()
            if not (skill_dir / "SKILL.md").exists():
                errors.append(f"[marketplace] Plugin `{plugin.get('name')}` lists `{entry}`, which has no SKILL.md")
            listed.setdefault(skill_dir, []).append(plugin.get("name"))

    for skill_dir in sorted(d.resolve() for d in SKILLS_DIR.iterdir() if (d / "SKILL.md").exists()):
        plugins = listed.get(skill_dir, [])
        if len(plugins) != 1:
            where = f"plugins {', '.join(f'`{n}`' for n in plugins)}" if plugins else "no plugin"
            errors.append(
                f"[{skill_dir.name}] Listed in {where} in "
                f"{MARKETPLACE_JSON.relative_to(REPO_ROOT)}; add it to exactly one plugin's `skills`"
            )


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    modified = get_modified_skill_files()
    all_errors = []
    check_marketplace_sync(all_errors)

    if not modified and not all_errors:
        print("No SKILL.md files were modified. Nothing to validate.")
        sys.exit(0)

    print(f"Validating {len(modified)} modified SKILL.md file(s)...\n")

    all_names = get_all_skill_names()

    for skill_path in modified:
        print(f"  Checking: {skill_path.relative_to(REPO_ROOT)}")
        content = skill_path.read_text(encoding="utf-8")
        base_content = get_base_content(skill_path)

        try:
            fm, body = parse_frontmatter(content)
        except ValueError as e:
            all_errors.append(f"[{skill_path.parent.name}] Cannot parse frontmatter: {e}")
            continue

        check_required_fields(fm, skill_path, all_errors)
        check_prohibited_fields(fm, skill_path, all_errors)
        check_upload_limits(fm, skill_path, all_errors)
        check_name_matches_directory(fm, skill_path, all_errors)
        check_name_uniqueness(fm, skill_path, all_names, all_errors)
        check_skills_md_sync(fm, skill_path, base_content, all_errors)
        check_relative_links(body, skill_path, all_errors)
        check_structural_headers(body, skill_path, all_errors)
        check_version_bumped(fm, skill_path, base_content, all_errors)

    print()
    if all_errors:
        print(f"❌ VALIDATION FAILED — {len(all_errors)} error(s) found:\n")
        for err in all_errors:
            print(f"  • {err}")
        print()
        print("Fix all errors above before merging. See SKILL_STANDARD.md for guidance.")
        sys.exit(1)
    else:
        print("✅ All structural checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
