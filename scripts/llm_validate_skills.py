#!/usr/bin/env python3
"""
llm_validate_skills.py — LLM qualitative review of bioconductor/ai-agent-skills.

This script uses a configured LLM provider (GitHub Models or Gemini) to perform
a subjective review of modified SKILL.md files in a pull request. It checks for
compliance with standard repository guidelines
(e.g., agent neutrality, workflow structure) that cannot be caught by deterministic
static checks.

Usage (in GitHub Actions):
  python scripts/llm_validate_skills.py
"""

import json
import os
import sys
import subprocess
from pathlib import Path


# Try importing the pinned dependencies
try:
    from google import genai
    from google.genai import types
    import openai
    from github import Github, Auth
except ImportError:
    print("ERROR: Required dependencies missing. Ensure google-genai, openai, and PyGithub are installed.")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMENT_MARKER = "<!-- llm-skill-validation-report -->"

# ──────────────────────────────────────────────────────────────────────────────
# Git helpers
# ──────────────────────────────────────────────────────────────────────────────

def get_modified_skill_files(gh_token=None, repo_name=None, pr_number=None):
    """
    Return a list of dicts {'path': Path, 'content': str} for modified SKILL.md files.
    If running in a PR context, fetches safely via GitHub API to support pull_request_target.
    Otherwise, falls back to local git diff.
    """
    skills = []
    
    # 1. PR Context: Securely fetch from API
    if gh_token and repo_name and pr_number:
        print(f"Fetching modified files for PR #{pr_number} via GitHub API...")
        g = Github(auth=Auth.Token(gh_token))
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        for file in pr.get_files():
            if file.filename.startswith("skills/") and file.filename.endswith("/SKILL.md"):
                if file.status != "removed":
                    content = repo.get_contents(file.filename, ref=pr.head.sha).decoded_content.decode("utf-8")
                    skills.append({"path": Path(file.filename), "content": content})
        return skills
        
    # 2. Local fallback
    print("Falling back to local git diff...")
    base_ref = os.environ.get("BASE_REF", "devel")
    
    # Safely probe origin diff without hard-failing
    result = subprocess.run(["git", "diff", "--name-only", f"origin/{base_ref}...HEAD"], capture_output=True, text=True, cwd=REPO_ROOT)
    if result.returncode != 0:
        print(f"Warning: 'git diff origin/{base_ref}...HEAD' failed. Trying local branch diff.", file=sys.stderr)
        result = subprocess.run(["git", "diff", "--name-only", f"{base_ref}...HEAD"], capture_output=True, text=True, cwd=REPO_ROOT)
        if result.returncode != 0:
            print("ERROR: Could not determine modified files via git diff.", file=sys.stderr)
            sys.exit(1)
            
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        p = REPO_ROOT / line
        if p.name == "SKILL.md" and p.exists():
            skills.append({"path": p, "content": p.read_text(encoding="utf-8")})
            
    return skills

# ──────────────────────────────────────────────────────────────────────────────
# GitHub API helpers
# ──────────────────────────────────────────────────────────────────────────────

def post_or_update_pr_comment(gh_token, repo_name, pr_number, body):
    """Post a new comment or update an existing one matching COMMENT_MARKER."""
    g = Github(auth=Auth.Token(gh_token))
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

def validate_skill_with_llm(client, provider, skill_path, skill_content, standard_docs):
    """Run the LLM against the skill content and standard docs."""
    skill_name = skill_path.parent.name
    display_path = skill_path
    if skill_path.is_absolute():
        display_path = skill_path.relative_to(REPO_ROOT)
    
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
File path: {display_path}

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
    
    print(f"  Calling {provider} API for {skill_name}...")
    
    try:
        if provider == "gemini":
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
            result = json.loads(response.text)
        elif provider == "github-models":
            model_name = os.environ.get("GH_MODELS_MODEL", "gpt-4o")
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "validation_report",
                        "schema": {
                            "type": "object",
                            "required": ["status", "report_markdown"],
                            "properties": {
                                "status": { "type": "string", "enum": ["PASS", "FAIL"] },
                                "report_markdown": { "type": "string" }
                            },
                            "additionalProperties": False
                        },
                        "strict": True
                    }
                }
            )
            result = json.loads(response.choices[0].message.content)
        else:
            raise ValueError(f"Unknown provider: {provider}")
            
        return result.get("status", "FAIL"), result.get("report_markdown", "Failed to extract report.")
    except Exception as e:
        print(f"Error calling LLM or parsing JSON: {e}")
        raise ValueError(f"LLM output failed or could not be parsed as JSON: {e}")

# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    llm_provider = os.environ.get("LLM_PROVIDER", "github-models").lower()
    gemini_key = os.environ.get("GEMINI_API_KEY")
    gh_token = os.environ.get("GITHUB_TOKEN")
    pr_number = os.environ.get("GH_PR_NUMBER")
    repo_name = os.environ.get("GH_REPO")
    fallback_gemini_client = None
    
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

    if llm_provider == "gemini":
        if not gemini_key:
            msg = "### 🤖 LLM Qualitative Review Skipped\nThe `GEMINI_API_KEY` secret is not configured in this repository. Please configure it to enable automated qualitative skill review."
            print(msg)
            if can_comment:
                try:
                    post_or_update_pr_comment(gh_token, repo_name, pr_number, msg)
                except Exception as e:
                    print(f"Failed to post PR comment: {e}")
            sys.exit(0) # Graceful degradation
        client = genai.Client(api_key=gemini_key)
    elif llm_provider == "github-models":
        if not gh_token:
             print("ERROR: GITHUB_TOKEN is required for github-models but not set. Cannot run LLM.")
             sys.exit(1)
        client = openai.OpenAI(
            api_key=gh_token,
            base_url="https://models.inference.ai.azure.com"
        )
        if gemini_key:
            fallback_gemini_client = genai.Client(api_key=gemini_key)
    else:
        print(f"ERROR: Unknown LLM_PROVIDER '{llm_provider}'. Must be 'gemini' or 'github-models'.")
        sys.exit(1)

    # 2. Identify Targets
    modified_skills = get_modified_skill_files(gh_token, repo_name, pr_number)
    if not modified_skills:
        print("No SKILL.md files were modified. Nothing to review qualitatively.")
        sys.exit(0)

    print(f"Evaluating {len(modified_skills)} modified SKILL.md file(s)...\n")

    # 3. Read Standard Docs
    standard_docs = get_standard_docs()

    # 4 & 5. Aggregate Results
    skill_reports = ""
    any_failures = False
    any_skipped = False

    for skill in modified_skills:
        skill_path = skill["path"]
        skill_content = skill["content"]
        skill_name = skill_path.parent.name
        print(f"Evaluating {skill_name}...")

        try:
            status, report = validate_skill_with_llm(client, llm_provider, skill_path, skill_content, standard_docs)
        except Exception as e:
            if llm_provider == "github-models" and fallback_gemini_client is not None:
                print(f"Primary github-models call failed for {skill_name}: {e}")
                print(f"Retrying {skill_name} with gemini fallback...")
                try:
                    status, report = validate_skill_with_llm(
                        fallback_gemini_client,
                        "gemini",
                        skill_path,
                        skill_content,
                        standard_docs
                    )
                    report = (
                        "> [!NOTE]\n"
                        "> github-models failed for this skill and evaluation was retried with gemini.\n\n"
                        + report
                    )
                except Exception as fallback_error:
                    e = f"github-models error: {e}; gemini fallback error: {fallback_error}"
                else:
                    if status == "FAIL":
                        any_failures = True
                    emoji = "✅" if status == "PASS" else "❌"
                    skill_reports += f"<details open>\n<summary>{emoji} <b>{skill_name}</b>: {status}</summary>\n\n{report}\n\n</details>\n\n"
                    continue
            # Catch API errors / timeouts — mark skill as skipped and continue
            # so that already-evaluated skills' reports are not discarded.
            print(f"API Error during LLM call for {skill_name}: {e}")
            any_skipped = True
            skill_reports += (
                f"<details>\n"
                f"<summary>⏭️ <b>{skill_name}</b>: SKIPPED</summary>\n\n"
                f"The {llm_provider} API encountered an error during evaluation: `{e}`.\n"
                f"Human review is required for this skill.\n\n"
                f"</details>\n\n"
            )
            continue

        if status == "FAIL":
            any_failures = True

        emoji = "✅" if status == "PASS" else "❌"
        skill_reports += f"<details open>\n<summary>{emoji} <b>{skill_name}</b>: {status}</summary>\n\n{report}\n\n</details>\n\n"

    if any_skipped:
        skill_reports += (
            "\n> [!WARNING]\n"
            f"> One or more skills could not be evaluated due to a {llm_provider} API error. "
            "Human review is required for the skipped skill(s).\n"
        )

    if any_failures:
        badge_url = "https://img.shields.io/badge/Qualitative%20Review-Fail-critical"
    elif any_skipped:
        badge_url = "https://img.shields.io/badge/Qualitative%20Review-No%20Review-inactive"
    else:
        badge_url = "https://img.shields.io/badge/Qualitative%20Review-Pass-success"

    aggregate_report = f"### 🤖 LLM Qualitative Skill Review\n\n![Qualitative Review]({badge_url})\n\n" + skill_reports

    # 6. Deduplicate Comment
    if can_comment:
        try:
            post_or_update_pr_comment(gh_token, repo_name, pr_number, aggregate_report)
        except Exception as e:
            print(f"Failed to post PR comment: {e}")
            print("\n--- LLM Validation Report (Fallback) ---\n")
            print(aggregate_report)
            print("-----------------------------\n")
    else:
        print("\n--- LLM Validation Report ---\n")
        print(aggregate_report)
        print("-----------------------------\n")

    # 7. Enforce Standards
    if any_failures:
        print("❌ One or more skills FAILED the qualitative review. See the PR comment for details.")
        sys.exit(1)
    elif any_skipped:
        print("⚠️ One or more skills were skipped due to API errors. Qualitative review is incomplete.")
        sys.exit(1)
    else:
        print("✅ All skills passed the qualitative review.")
        sys.exit(0)

if __name__ == "__main__":
    main()
