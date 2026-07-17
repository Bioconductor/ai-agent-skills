#!/usr/bin/env python3
"""
llm_validate_skills.py — LLM qualitative review of bioconductor/ai-agent-skills.

This script uses the Gemini API to perform a subjective review of modified SKILL.md
files in a pull request. It checks for compliance with standard repository guidelines
(e.g., agent neutrality, workflow structure) that cannot be caught by deterministic
static checks.

Usage (in GitHub Actions):
  python scripts/llm_validate_skills.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Try importing the pinned dependencies
try:
    from google import genai
    from google.genai import types
    from github import Github
except ImportError:
    print("ERROR: Required dependencies missing. Ensure google-genai and PyGithub are installed.")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
COMMENT_MARKER = "<!-- llm-skill-validation-report -->"

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
    if not base_ref:
        print("Warning: BASE_REF not set. Defaulting to 'devel'.")
        base_ref = "devel"
        
    try:
        changed = git("diff", "--name-only", f"origin/{base_ref}...HEAD")
    except SystemExit:
        # Fallback if the standard diff fails (e.g. running locally without origin/devel setup)
        changed = git("diff", "--name-only", f"{base_ref}...HEAD")

    skill_files = []
    for line in changed.splitlines():
        p = REPO_ROOT / line
        if p.name == "SKILL.md" and p.exists():
            skill_files.append(p)
    return skill_files

# ──────────────────────────────────────────────────────────────────────────────
# GitHub API helpers
# ──────────────────────────────────────────────────────────────────────────────

def post_or_update_pr_comment(gh_token, repo_name, pr_number, body):
    """Post a new comment or update an existing one matching COMMENT_MARKER."""
    g = Github(gh_token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # Prepend the marker to the body
    full_body = f"{COMMENT_MARKER}\n{body}"
    
    # Find existing comment
    for comment in pr.get_issue_comments():
        if comment.body.startswith(COMMENT_MARKER):
            print("Updating existing PR comment.")
            comment.edit(full_body)
            return
            
    print("Creating new PR comment.")
    pr.create_issue_comment(full_body)

# ──────────────────────────────────────────────────────────────────────────────
# LLM Validation helpers
# ──────────────────────────────────────────────────────────────────────────────

def get_standard_docs():
    """Read the contents of the standards files used for LLM evaluation."""
    docs = {}
    
    files_to_read = [
        "AGENTS.md", 
        "SKILL_STANDARD.md", 
        ".github/copilot-instructions.md"
    ]
    
    for filename in files_to_read:
        path = REPO_ROOT / filename
        if path.exists():
            docs[filename] = path.read_text(encoding="utf-8")
        else:
            print(f"Warning: Expected standard doc {filename} not found.")
            
    return docs

def validate_skill_with_llm(client, skill_path, standard_docs):
    """Run the Gemini LLM against the skill content and standard docs."""
    skill_content = skill_path.read_text(encoding="utf-8")
    skill_name = skill_path.parent.name
    
    prompt = f"""
You are an expert Bioconductor AI Agent Skill Reviewer.
Your task is to review a proposed AI agent skill file and determine if it meets the repository's subjective/qualitative standards.

### Standards Context
Here are the foundational documents defining the rules. The `copilot-instructions.md` file contains the definitive rubric of what to flag.

==== AGENTS.md ====
{standard_docs.get("AGENTS.md", "")}

==== SKILL_STANDARD.md ====
{standard_docs.get("SKILL_STANDARD.md", "")}

==== .github/copilot-instructions.md (THE REVIEW RUBRIC) ====
{standard_docs.get(".github/copilot-instructions.md", "")}

### Target Skill to Review
File path: {skill_path.relative_to(REPO_ROOT)}

==== SKILL CONTENT ====
{skill_content}
==== END SKILL CONTENT ====

### Instructions
1. Review the Target Skill using the explicit CRITICAL, IMPORTANT, and ADVISORY rules defined in `.github/copilot-instructions.md`.
2. Pay special attention to "What NOT to Flag". Do not fail a skill for normal markdown variations or embedded domain-specific code snippets.
3. Determine the overall status:
   - If you find ANY violation of the CRITICAL or IMPORTANT rules (e.g. platform-specific instructions, missing workflow steps, duplicated standard docs), the status must be "FAIL".
   - If there are only ADVISORY issues, or no issues at all, the status is "PASS".
4. Generate a human-readable validation report formatted as markdown. Provide clear quotes of any offending text and suggest fixes based on the guidelines.
5. You MUST return your response as a valid JSON object matching the required schema.
"""
    
    print(f"  Calling Gemini API for {skill_name}...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "required": ["status", "report_markdown"],
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["PASS", "FAIL"]
                    },
                    "report_markdown": {
                        "type": "string"
                    }
                }
            },
        ),
    )
    
    import json
    try:
        # With response_json_schema and response_mime_type, response.text should be guaranteed valid JSON
        result = json.loads(response.text)
        return result.get("status", "FAIL"), result.get("report_markdown", "Failed to extract report.")
    except Exception as e:
        print(f"Error parsing JSON from LLM: {e}")
        return "FAIL", f"Error parsing response from LLM:\n\n```json\n{response.text}\n```"

# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    gh_token = os.environ.get("GITHUB_TOKEN")
    pr_number = os.environ.get("GH_PR_NUMBER")
    repo_name = os.environ.get("GH_REPO")
    
    # 1. Pre-flight Checks
    can_comment = True
    if not gh_token or not pr_number or not repo_name:
        print("Warning: GITHUB_TOKEN, GH_PR_NUMBER, or GH_REPO not provided in environment. Will not post to PR.")
        can_comment = False
    else:
        try:
            pr_number = int(pr_number)
        except ValueError:
            print("Error: GH_PR_NUMBER must be an integer.")
            can_comment = False

    if not gemini_key:
        msg = "### 🤖 LLM Qualitative Review Skipped\nThe `GEMINI_API_KEY` secret is not configured in this repository. Please configure it to enable automated qualitative skill review."
        print(msg)
        if can_comment:
            post_or_update_pr_comment(gh_token, repo_name, pr_number, msg)
        sys.exit(0) # Graceful degradation
        
    client = genai.Client(api_key=gemini_key)

    # 2. Identify Targets
    modified = get_modified_skill_files()
    if not modified:
        print("No SKILL.md files were modified. Nothing to review qualitatively.")
        sys.exit(0)

    print(f"Evaluating {len(modified)} modified SKILL.md file(s)...\n")

    # 3. Read Standard Docs
    standard_docs = get_standard_docs()

    # 4 & 5. Aggregate Results
    aggregate_report = "### 🤖 LLM Qualitative Skill Review\n\n"
    any_failures = False
    
    for skill_path in modified:
        skill_name = skill_path.parent.name
        print(f"Evaluating {skill_name}...")
        
        try:
            status, report = validate_skill_with_llm(client, skill_path, standard_docs)
        except Exception as e:
            # Catch API errors, timeouts, etc.
            print(f"API Error during LLM call: {e}")
            msg = f"### 🤖 LLM Qualitative Review Skipped\nThe Gemini API encountered an error during evaluation: `{e}`. Human review is required."
            if can_comment:
                post_or_update_pr_comment(gh_token, repo_name, pr_number, msg)
            sys.exit(0) # Graceful degradation
            
        if status == "FAIL":
            any_failures = True
            
        emoji = "✅" if status == "PASS" else "❌"
        aggregate_report += f"<details open>\n<summary>{emoji} <b>{skill_name}</b>: {status}</summary>\n\n{report}\n\n</details>\n\n"

    # 6. Deduplicate Comment
    if can_comment:
        post_or_update_pr_comment(gh_token, repo_name, pr_number, aggregate_report)
    else:
        print("\n--- LLM Validation Report ---\n")
        print(aggregate_report)
        print("-----------------------------\n")

    # 7. Enforce Standards
    if any_failures:
        print("❌ One or more skills FAILED the qualitative review. See the PR comment for details.")
        sys.exit(1)
    else:
        print("✅ All skills passed the qualitative review.")
        sys.exit(0)

if __name__ == "__main__":
    main()
