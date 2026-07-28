#!/usr/bin/env python3
"""
validate_skills.py — Gatekeeper CI check for bioconductor/ai-agent-skills.

Derived from: skills/validate-skill/SKILL.md (the gold standard for validation rules).

Checks performed:
  1. Required frontmatter fields present (name, description, version, category)
  2. No prohibited frontmatter fields (platforms, triggers)
  3. Directory name matches the `name` field
  4. Skill name is globally unique (no collisions with other skills)
  5. SKILLS.md is in sync (new/changed descriptions must appear in the index)
  6. Relative links in the skill body resolve to existing files on disk
  7. Version was bumped if the file was modified (not newly created)

Usage:
  python scripts/validate_skills.py
  BASE_REF=devel python scripts/validate_skills.py

Exit codes:
  0 — all checks passed
  1 — one or more checks failed
"""

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

REQUIRED_FIELDS = {"name", "description", "version", "category", "author"}
PROHIBITED_FIELDS = {"platforms", "triggers"}

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

def check_required_fields(fm, skill_path, errors):
    missing = REQUIRED_FIELDS - set(fm.keys())
    for field in sorted(missing):
        errors.append(f"[{skill_path.parent.name}] MISSING required frontmatter field: `{field}`")


def check_prohibited_fields(fm, skill_path, errors):
    present = PROHIBITED_FIELDS & set(fm.keys())
    for field in sorted(present):
        errors.append(
            f"[{skill_path.parent.name}] PROHIBITED frontmatter field present: `{field}` "
            f"(skills must be agent-agnostic — see AGENTS.md)"
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
    old_version = base_fm.get("version", "")
    new_version = fm.get("version", "")
    if old_version and old_version == new_version:
        errors.append(
            f"[{skill_path.parent.name}] `version` was not bumped (still `{old_version}`). "
            f"Update the version following semver. "
            f"(See SKILL_STANDARD.md § Version Management)"
        )


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    modified = get_modified_skill_files()

    if not modified:
        print("No SKILL.md files were modified. Nothing to validate.")
        sys.exit(0)

    print(f"Validating {len(modified)} modified SKILL.md file(s)...\n")

    all_names = get_all_skill_names()
    all_errors = []

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
