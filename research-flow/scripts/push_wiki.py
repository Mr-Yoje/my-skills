#!/usr/bin/env python3
"""
research-flow helper: push study notes repo changes to remote with proper auth.
Repo: https://github.com/Mr-Yoje/study-notes
Usage: python3 scripts/push_wiki.py
"""
import json, os, subprocess, sys

NOTES_DIR = os.path.expanduser("~/study-notes")
SECRETS_FILE = os.path.expanduser("/home/admin/.openclaw/workspaces/brucex/secrets.json")


def main():
    os.chdir(NOTES_DIR)

    # Read token
    try:
        with open(SECRETS_FILE) as f:
            secrets = json.load(f)
        token = secrets["github"]["token"]
        username = secrets["github"]["username"]
        repo = secrets["github"].get("repo", "study-notes")
    except (FileNotFoundError, KeyError) as e:
        print(f"❌ Cannot read token: {e}")
        sys.exit(1)

    # Check git status
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not result.stdout.strip():
        print("No changes to push.")
        return

    # Get current branch
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True).stdout.strip() or "master"

    # Set remote with token
    repo_url = f"https://{username}:{token}@github.com/{username}/{repo}.git"
    subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)

    print(f"📤 Pushing to {username}/{repo} ({branch})...")
    result = subprocess.run(["git", "push", "origin", branch], capture_output=True, text=True)
    if result.returncode != 0:
        if "rejected" in result.stderr:
            print("⚠️  Push rejected, pulling first...")
            subprocess.run(["git", "pull", "origin", branch, "--no-rebase", "--allow-unrelated-histories"],
                           capture_output=True, text=True)
            result = subprocess.run(["git", "push", "origin", branch], capture_output=True, text=True)

    if "Everything up-to-date" in result.stdout or result.returncode == 0:
        print("✅ Notes pushed to remote successfully!")
    else:
        print(f"❌ Push failed:\n{result.stderr}")

    # Remove token from remote URL (security)
    subprocess.run(["git", "remote", "set-url", "origin",
                    f"https://github.com/{username}/{repo}.git"], check=True)


if __name__ == "__main__":
    main()
