#!/usr/bin/env python3
"""
research-flow-general helper: push study-notes to GitHub with PAT auth.

Works with Cursor / Claude Code / Codex on Windows, macOS, Linux.

Usage:
  python path/to/research-flow-general/scripts/push_wiki.py

Env overrides:
  STUDY_NOTES_DIR       notes repo root (default: ~/study-notes)
  RESEARCH_FLOW_SECRETS path to github.json
  GITHUB_TOKEN          PAT (optional if json exists)
  GITHUB_USERNAME       default Mr-Yoje
  GITHUB_REPO           default study-notes
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HOME = Path(os.environ.get("USERPROFILE") or os.environ.get("HOME") or Path.home())


def notes_dir() -> Path:
    override = os.environ.get("STUDY_NOTES_DIR")
    if override:
        return Path(override).expanduser()
    return HOME / "study-notes"


def secrets_candidates() -> list[Path]:
    env = os.environ.get("RESEARCH_FLOW_SECRETS")
    paths: list[Path] = []
    if env:
        paths.append(Path(env).expanduser())
    paths.extend(
        [
            HOME / ".config" / "research-flow" / "github.json",
            HOME / ".cursor" / "secrets" / "github.json",
            HOME / ".claude" / "secrets" / "github.json",
            HOME / ".codex" / "secrets" / "github.json",
        ]
    )
    return paths


def load_github_auth() -> tuple[str, str, str, Path | None]:
    """Return token, username, repo, secrets_path_used."""
    username = os.environ.get("GITHUB_USERNAME", "Mr-Yoje")
    repo = os.environ.get("GITHUB_REPO", "study-notes")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("RESEARCH_FLOW_GITHUB_TOKEN")

    used: Path | None = None
    for path in secrets_candidates():
        if not path.is_file():
            continue
        try:
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
            gh = data.get("github", data)
            token = token or gh.get("token")
            username = gh.get("username") or username
            repo = gh.get("repo") or repo
            used = path
            if token:
                break
        except (OSError, json.JSONDecodeError, AttributeError):
            continue

    if not token:
        tried = "\n".join(f"  - {p}" for p in secrets_candidates())
        raise FileNotFoundError(
            "No GitHub token found. Set GITHUB_TOKEN or create one of:\n" + tried
        )
    return token, username, repo, used


def run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def main() -> None:
    notes = notes_dir()
    if not notes.is_dir():
        print(f"[error] Notes repo not found: {notes}")
        print('   Clone: git clone https://github.com/Mr-Yoje/study-notes.git "<path>"')
        print("   Or set STUDY_NOTES_DIR.")
        sys.exit(1)

    os.chdir(notes)

    try:
        token, username, repo, used = load_github_auth()
    except FileNotFoundError as e:
        print(f"[error] {e}")
        sys.exit(1)

    if used:
        print(f"[auth] Using secrets: {used}")
    else:
        print("[auth] Using GITHUB_TOKEN from environment")

    status = run(["git", "status", "--porcelain"])
    if status.returncode != 0:
        print(f"[error] Not a git repo or git error:\n{status.stderr}")
        sys.exit(1)
    if not status.stdout.strip():
        print("No changes to push.")
        return

    branch_p = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    branch = (branch_p.stdout or "").strip() or "master"

    clean_url = f"https://github.com/{username}/{repo}.git"
    auth_url = f"https://{username}:{token}@github.com/{username}/{repo}.git"

    try:
        run(["git", "remote", "set-url", "origin", auth_url], check=True)
        print(f"[push] {username}/{repo} ({branch})...")
        result = run(["git", "push", "origin", branch])

        if result.returncode != 0 and "rejected" in (result.stderr or ""):
            print("[warn] Push rejected, pulling first...")
            run(
                [
                    "git",
                    "pull",
                    "origin",
                    branch,
                    "--no-rebase",
                    "--allow-unrelated-histories",
                ]
            )
            result = run(["git", "push", "origin", branch])

        if result.returncode == 0 or "Everything up-to-date" in (result.stdout or ""):
            print("[ok] Notes pushed to remote successfully!")
        else:
            print(f"[error] Push failed:\n{result.stderr or result.stdout}")
            sys.exit(result.returncode or 1)
    finally:
        run(["git", "remote", "set-url", "origin", clean_url], check=False)
        print(f"[secure] Remote reset to {clean_url}")


if __name__ == "__main__":
    main()
