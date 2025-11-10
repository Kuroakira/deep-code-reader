#!/usr/bin/env python3
"""
Repository Clone Utility
Clones a GitHub repository and checks out a specific commit
"""

import argparse
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil


def clone_repository(repo_url: str, commit_id: str = "HEAD", target_dir: str = None) -> Path:
    """
    Clone a GitHub repository and checkout a specific commit.

    Args:
        repo_url: GitHub repository URL
        commit_id: Commit hash or branch name (default: HEAD)
        target_dir: Target directory (default: temporary directory)

    Returns:
        Path to cloned repository
    """
    # Create target directory
    if target_dir:
        clone_path = Path(target_dir)
        clone_path.mkdir(parents=True, exist_ok=True)
    else:
        clone_path = Path(tempfile.mkdtemp(prefix="oss_analysis_"))

    print(f"📦 Cloning repository: {repo_url}")
    print(f"📁 Target directory: {clone_path}")

    try:
        # Clone repository
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(clone_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Repository cloned successfully")

        # Checkout specific commit if not HEAD
        if commit_id and commit_id.upper() != "HEAD":
            print(f"🔄 Checking out commit: {commit_id}")

            # Fetch the specific commit if needed
            subprocess.run(
                ["git", "fetch", "--depth", "1", "origin", commit_id],
                cwd=clone_path,
                check=True,
                capture_output=True
            )

            # Checkout the commit
            subprocess.run(
                ["git", "checkout", commit_id],
                cwd=clone_path,
                check=True,
                capture_output=True
            )
            print("✅ Commit checked out successfully")

        return clone_path

    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        if clone_path.exists():
            shutil.rmtree(clone_path)
        sys.exit(1)


def get_repo_info(repo_path: Path) -> dict:
    """Get repository information."""
    try:
        # Get current commit hash
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            text=True
        ).strip()

        # Get commit message
        commit_msg = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"],
            cwd=repo_path,
            text=True
        ).strip()

        # Get repository URL
        repo_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=repo_path,
            text=True
        ).strip()

        # Get branch name
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo_path,
                text=True
            ).strip()
        except:
            branch = "detached"

        return {
            "commit_hash": commit_hash,
            "commit_message": commit_msg,
            "repository_url": repo_url,
            "branch": branch,
            "path": str(repo_path)
        }
    except Exception as e:
        print(f"⚠️ Warning: Could not get repository info: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="Clone a GitHub repository for analysis"
    )
    parser.add_argument(
        "repo_url",
        help="GitHub repository URL"
    )
    parser.add_argument(
        "-c", "--commit",
        default="HEAD",
        help="Commit hash or branch name (default: HEAD)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: temporary directory)"
    )
    parser.add_argument(
        "-i", "--info",
        action="store_true",
        help="Print repository information after cloning"
    )

    args = parser.parse_args()

    # Clone repository
    repo_path = clone_repository(args.repo_url, args.commit, args.output)

    # Print info if requested
    if args.info:
        print("\n📋 Repository Information:")
        info = get_repo_info(repo_path)
        for key, value in info.items():
            print(f"  {key}: {value}")

    print(f"\n✅ Repository ready at: {repo_path}")
    return str(repo_path)


if __name__ == "__main__":
    main()
