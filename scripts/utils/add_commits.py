#!/usr/bin/env python3
"""
Add Commits to Notion Database
Intelligently maps commit data to database columns based on column names.
Supports multiple languages (English, Japanese, etc.)
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Try to import requests, provide helpful error if not available
try:
    import requests
except ImportError:
    print("Error: 'requests' library not installed.")
    print("Install with: pip install requests")
    sys.exit(1)


class ColumnNameAnalyzer:
    """
    Analyzes column names to determine what commit data they should contain.
    Supports multiple languages and common naming patterns.
    """

    # Keyword patterns for each data type (supports multiple languages)
    PATTERNS = {
        "commit_hash": {
            "keywords": [
                # English
                "hash", "sha", "commit id", "commit_id", "commitid", "id",
                "revision", "rev", "oid",
                # Japanese
                "ハッシュ", "コミットid", "コミットID", "リビジョン", "識別子",
                # Common abbreviations
                "sha1", "sha256", "commit"
            ],
            "priority": 10,
            "type_hint": "rich_text"
        },
        "message": {
            "keywords": [
                # English
                "message", "msg", "description", "desc", "summary", "comment",
                "content", "body", "text", "note", "details",
                # Japanese
                "メッセージ", "説明", "内容", "コメント", "概要", "詳細", "本文",
                # Common patterns
                "commit message", "commit_message", "log"
            ],
            "priority": 9,
            "type_hint": "rich_text"
        },
        "author_name": {
            "keywords": [
                # English
                "author", "committer", "name", "user", "contributor", "developer",
                "created by", "created_by", "createdby", "by", "owner",
                # Japanese
                "作者", "作成者", "著者", "コミッター", "ユーザー", "開発者", "担当者",
                # Common patterns
                "author name", "author_name", "committed by"
            ],
            "priority": 8,
            "type_hint": "rich_text"
        },
        "author_email": {
            "keywords": [
                # English
                "email", "mail", "e-mail", "contact",
                # Japanese
                "メール", "メールアドレス", "連絡先",
                # Common patterns
                "author email", "author_email", "committer email"
            ],
            "priority": 7,
            "type_hint": "email"
        },
        "date": {
            "keywords": [
                # English
                "date", "time", "datetime", "timestamp", "created", "committed",
                "when", "at",
                # Japanese
                "日付", "日時", "作成日", "コミット日", "時刻", "いつ",
                # Common patterns
                "commit date", "commit_date", "created_at", "committed_at"
            ],
            "priority": 6,
            "type_hint": "date"
        },
        "github_url": {
            "keywords": [
                # English
                "url", "link", "github", "repository", "repo", "source",
                "reference", "ref", "web", "browse",
                # Japanese
                "リンク", "URL", "参照", "ソース", "ウェブ",
                # Common patterns
                "github url", "github_url", "commit url", "commit_url"
            ],
            "priority": 5,
            "type_hint": "url"
        },
        "type": {
            "keywords": [
                # English
                "type", "kind", "category", "classification", "tag", "label",
                "status", "state",
                # Japanese
                "タイプ", "種類", "カテゴリ", "分類", "種別", "ラベル", "状態",
                # Common patterns
                "commit type", "commit_type", "entry type"
            ],
            "priority": 4,
            "type_hint": "select"
        },
        "files_changed": {
            "keywords": [
                # English
                "files", "file count", "file_count", "filecount", "changes",
                "modified", "changed", "affected", "diff", "stats",
                # Japanese
                "ファイル", "ファイル数", "変更数", "変更", "差分",
                # Common patterns
                "files changed", "files_changed", "num files", "file changes"
            ],
            "priority": 3,
            "type_hint": "number"
        },
        "memo": {
            "keywords": [
                # English
                "memo", "notes", "remark", "annotation", "extra", "additional",
                "custom", "personal", "my",
                # Japanese
                "メモ", "備考", "ノート", "注釈", "追記", "補足",
                # Common patterns
                "my notes", "my_notes", "personal notes"
            ],
            "priority": 2,
            "type_hint": "rich_text"
        },
        "pr_number": {
            "keywords": [
                # English
                "pr", "pull request", "pull_request", "pullrequest", "mr",
                "merge request", "merge_request",
                # Japanese
                "プルリクエスト", "マージリクエスト",
                # Common patterns
                "pr number", "pr_number", "pr no", "pr_no"
            ],
            "priority": 1,
            "type_hint": "rich_text"
        }
    }

    def __init__(self):
        """Initialize the analyzer."""
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for faster matching."""
        self._compiled = {}
        for data_type, config in self.PATTERNS.items():
            # Create a combined pattern from all keywords
            escaped_keywords = [re.escape(kw) for kw in config["keywords"]]
            pattern = re.compile(
                r"(?:^|[\s_\-])(" + "|".join(escaped_keywords) + r")(?:[\s_\-]|$)",
                re.IGNORECASE
            )
            self._compiled[data_type] = {
                "pattern": pattern,
                "priority": config["priority"],
                "type_hint": config["type_hint"],
                "keywords": config["keywords"]
            }

    def analyze_column(self, column_name: str, column_type: str) -> Tuple[Optional[str], float]:
        """
        Analyze a column name and determine what data it should contain.

        Args:
            column_name: The name of the column
            column_type: The Notion property type (rich_text, url, date, etc.)

        Returns:
            Tuple of (data_type, confidence_score)
            data_type is None if no match found
        """
        name_lower = column_name.lower()
        best_match = None
        best_score = 0.0

        for data_type, config in self._compiled.items():
            # Check if column type is compatible
            if not self._is_type_compatible(column_type, config["type_hint"]):
                continue

            # Calculate match score
            score = self._calculate_match_score(name_lower, column_name, config)

            if score > best_score:
                best_score = score
                best_match = data_type

        return best_match, best_score

    def _is_type_compatible(self, actual_type: str, expected_type: str) -> bool:
        """Check if the actual Notion type is compatible with expected type."""
        # Type compatibility mapping
        compatible_types = {
            "rich_text": ["rich_text", "title"],
            "url": ["url"],
            "date": ["date", "created_time", "last_edited_time"],
            "select": ["select", "status"],
            "number": ["number"],
            "email": ["email", "rich_text"],  # email can fallback to rich_text
        }

        expected_list = compatible_types.get(expected_type, [expected_type])
        return actual_type in expected_list

    def _calculate_match_score(self, name_lower: str, name_original: str, config: dict) -> float:
        """Calculate match score for a column name against patterns."""
        score = 0.0

        # Exact match gets highest score
        for keyword in config["keywords"]:
            if name_lower == keyword.lower():
                return 1.0 * config["priority"]

            # Partial match
            if keyword.lower() in name_lower:
                # Score based on how much of the name the keyword covers
                coverage = len(keyword) / len(name_lower)
                score = max(score, 0.7 * coverage * config["priority"])

        # Regex pattern match
        if config["pattern"].search(name_original):
            score = max(score, 0.5 * config["priority"])

        return score


class NotionCommitAdder:
    """
    Adds commits to a Notion database with intelligent column mapping.
    """

    def __init__(self, api_key: str, database_id: str):
        """
        Initialize the commit adder.

        Args:
            api_key: Notion integration API key
            database_id: Target database ID
        """
        self.api_key = api_key
        self.database_id = database_id.replace("-", "")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.analyzer = ColumnNameAnalyzer()
        self.column_mapping = {}
        self.title_property = None

    def get_database_schema(self) -> Dict[str, Any]:
        """Retrieve the database schema from Notion."""
        url = f"{self.base_url}/databases/{self.database_id}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Failed to get database: {response.status_code} - {response.text}")

        return response.json()

    def analyze_and_map_columns(self) -> Dict[str, str]:
        """
        Analyze database columns and create mapping to commit data.

        Returns:
            Dictionary mapping commit data fields to column names
        """
        schema = self.get_database_schema()
        properties = schema.get("properties", {})

        print(f"\n📊 Analyzing database columns...")
        print(f"   Found {len(properties)} properties\n")

        # Store all columns with their types
        columns = []
        for prop_name, prop_config in properties.items():
            prop_type = prop_config.get("type", "unknown")
            columns.append({
                "name": prop_name,
                "type": prop_type,
                "config": prop_config
            })

            # Track title property (required)
            if prop_type == "title":
                self.title_property = prop_name

        # Analyze each column
        mapping = {}
        used_columns = set()

        print("   Column Analysis:")
        print("   " + "-" * 50)

        # Sort columns by analysis confidence to assign best matches first
        column_scores = []
        for col in columns:
            data_type, score = self.analyzer.analyze_column(col["name"], col["type"])
            column_scores.append((col, data_type, score))

        # Sort by score (descending)
        column_scores.sort(key=lambda x: x[2], reverse=True)

        for col, data_type, score in column_scores:
            if data_type and data_type not in mapping and col["name"] not in used_columns:
                mapping[data_type] = col["name"]
                used_columns.add(col["name"])
                print(f"   ✓ '{col['name']}' ({col['type']}) → {data_type} (score: {score:.2f})")
            elif col["name"] not in used_columns:
                print(f"   - '{col['name']}' ({col['type']}) → (unmapped)")

        print("   " + "-" * 50)

        # Ensure title is mapped
        if self.title_property and "title" not in mapping:
            mapping["title"] = self.title_property

        self.column_mapping = mapping

        print(f"\n   Final mapping:")
        for data_type, col_name in mapping.items():
            print(f"   • {data_type} → '{col_name}'")

        return mapping

    def get_existing_commits(self) -> set:
        """Get set of existing commit hashes in the database."""
        existing = set()
        has_more = True
        start_cursor = None

        hash_column = self.column_mapping.get("commit_hash")

        while has_more:
            url = f"{self.base_url}/databases/{self.database_id}/query"
            payload = {"page_size": 100}
            if start_cursor:
                payload["start_cursor"] = start_cursor

            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code != 200:
                print(f"Warning: Failed to query existing entries: {response.text}")
                break

            data = response.json()

            for page in data.get("results", []):
                props = page.get("properties", {})

                # Try to get commit hash
                if hash_column and hash_column in props:
                    prop_data = props[hash_column]
                    if prop_data.get("type") == "rich_text":
                        texts = prop_data.get("rich_text", [])
                        if texts:
                            commit_hash = texts[0].get("plain_text", "")
                            if commit_hash:
                                existing.add(commit_hash)
                                existing.add(commit_hash[:7])

                # Also extract from title
                if self.title_property and self.title_property in props:
                    title_data = props[self.title_property]
                    if title_data.get("type") == "title":
                        titles = title_data.get("title", [])
                        if titles:
                            title_text = titles[0].get("plain_text", "")
                            if ":" in title_text:
                                short_hash = title_text.split(":")[0].strip()
                                if short_hash and len(short_hash) >= 7:
                                    existing.add(short_hash)

            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")

        return existing

    def build_page_properties(self, commit: Dict, owner: str, repo: str) -> Dict:
        """Build Notion page properties from commit data."""
        properties = {}

        # Title (required)
        title_col = self.column_mapping.get("title", self.title_property)
        if title_col:
            short_sha = commit.get("short_sha", commit["sha"][:7])
            message_first_line = commit["message"].split('\n')[0][:50]
            title_text = f"{short_sha}: {message_first_line}"

            properties[title_col] = {
                "title": [{"text": {"content": title_text}}]
            }

        # Commit hash
        if "commit_hash" in self.column_mapping:
            properties[self.column_mapping["commit_hash"]] = {
                "rich_text": [{"text": {"content": commit["sha"]}}]
            }

        # Message
        if "message" in self.column_mapping:
            properties[self.column_mapping["message"]] = {
                "rich_text": [{"text": {"content": commit["message"][:2000]}}]
            }

        # Author name
        if "author_name" in self.column_mapping:
            properties[self.column_mapping["author_name"]] = {
                "rich_text": [{"text": {"content": commit.get("author_name", "")}}]
            }

        # Author email
        if "author_email" in self.column_mapping:
            col_name = self.column_mapping["author_email"]
            # Check if it's email type or rich_text
            email = commit.get("author_email", "")
            if email:
                # Try email type first, fallback to rich_text
                properties[col_name] = {"email": email}

        # GitHub URL
        if "github_url" in self.column_mapping:
            github_url = f"https://github.com/{owner}/{repo}/commit/{commit['sha']}"
            properties[self.column_mapping["github_url"]] = {
                "url": github_url
            }

        # Type
        if "type" in self.column_mapping:
            properties[self.column_mapping["type"]] = {
                "select": {"name": "Commit"}
            }

        # Date
        if "date" in self.column_mapping:
            date_str = commit.get("date", "")
            if date_str:
                date_only = date_str.split("T")[0] if "T" in date_str else date_str
                properties[self.column_mapping["date"]] = {
                    "date": {"start": date_only}
                }

        # Files changed
        if "files_changed" in self.column_mapping:
            properties[self.column_mapping["files_changed"]] = {
                "number": commit.get("files_changed", 0)
            }

        return properties

    def create_page(self, commit: Dict, owner: str, repo: str) -> Dict:
        """Create a Notion page for a commit."""
        properties = self.build_page_properties(commit, owner, repo)

        # Build content blocks
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": f"Commit: {commit['sha']}\n"
                                       f"Author: {commit.get('author_name', 'Unknown')} <{commit.get('author_email', '')}>\n"
                                       f"Date: {commit.get('date', 'Unknown')}\n"
                                       f"Files Changed: {commit.get('files_changed', 'N/A')}"
                        }
                    }]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Commit Message"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": commit["message"][:2000]}}]
                }
            }
        ]

        payload = {
            "parent": {"database_id": self.database_id},
            "properties": properties,
            "children": children
        }

        url = f"{self.base_url}/pages"
        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Failed to create page: {response.status_code} - {response.text}")

        return response.json()


def get_commits_from_repo(repo_path: str, start: int, end: int) -> List[Dict]:
    """
    Get commits from local git repository.

    Args:
        repo_path: Path to local git repository
        start: Starting commit number (1-indexed, oldest first)
        end: Ending commit number (inclusive)

    Returns:
        List of commit dictionaries
    """
    # Get total commit count
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Failed to count commits: {result.stderr}")

    total_commits = int(result.stdout.strip())

    # Adjust end if it exceeds total
    if end > total_commits:
        print(f"Warning: Requested end ({end}) exceeds total commits ({total_commits})")
        end = total_commits

    # Calculate skip and take for oldest-first order
    skip_count = max(0, total_commits - end)
    take_count = end - start + 1

    # Get commits
    result = subprocess.run(
        ["git", "log", "--reverse", f"--skip={skip_count}", f"-{take_count}",
         "--format=%H|%h|%s|%an|%ae|%aI|%P"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Failed to get commits: {result.stderr}")

    commits = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) >= 6:
                sha = parts[0]

                # Get file count for this commit
                file_result = subprocess.run(
                    ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", sha],
                    cwd=repo_path,
                    capture_output=True,
                    text=True
                )
                files_changed = 0
                if file_result.returncode == 0:
                    files = [f for f in file_result.stdout.strip().split('\n') if f]
                    files_changed = len(files)

                commits.append({
                    "sha": sha,
                    "short_sha": parts[1],
                    "message": parts[2],
                    "author_name": parts[3],
                    "author_email": parts[4],
                    "date": parts[5],
                    "parents": parts[6] if len(parts) > 6 else "",
                    "files_changed": files_changed
                })

    return commits


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Add commits to Notion database with intelligent column mapping"
    )
    parser.add_argument("start", type=int, help="Starting commit number (1-indexed, oldest first)")
    parser.add_argument("end", type=int, help="Ending commit number (inclusive)")
    parser.add_argument("--repo", required=True, help="Path to local git repository")
    parser.add_argument("--owner", required=True, help="Repository owner (e.g., 'facebook')")
    parser.add_argument("--name", required=True, help="Repository name (e.g., 'react')")
    parser.add_argument("--database", required=True, help="Notion database ID")
    parser.add_argument("--api-key", help="Notion API key (or set NOTION_API_KEY env var)")

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("Error: Notion API key required. Set NOTION_API_KEY or use --api-key")
        sys.exit(1)

    # Validate arguments
    if args.start < 1:
        print("Error: start must be >= 1")
        sys.exit(1)
    if args.end < args.start:
        print("Error: end must be >= start")
        sys.exit(1)

    print(f"""
{'='*60}
Add Commits to Notion
{'='*60}

Repository: {args.owner}/{args.name}
Local Path: {args.repo}
Database: {args.database}
Range: {args.start} to {args.end}
""")

    try:
        # Initialize commit adder
        adder = NotionCommitAdder(api_key, args.database)

        # Analyze columns
        adder.analyze_and_map_columns()

        # Get existing commits
        print("\n🔍 Checking for existing entries...")
        existing = adder.get_existing_commits()
        print(f"   Found {len(existing)} existing commit entries")

        # Get commits from repo
        print(f"\n📥 Fetching commits {args.start} to {args.end}...")
        commits = get_commits_from_repo(args.repo, args.start, args.end)
        print(f"   Fetched {len(commits)} commits")

        # Filter duplicates
        commits_to_add = []
        skipped = 0
        for commit in commits:
            if commit["sha"] in existing or commit["short_sha"] in existing:
                skipped += 1
            else:
                commits_to_add.append(commit)

        print(f"\n📊 Summary:")
        print(f"   Commits to add: {len(commits_to_add)}")
        print(f"   Duplicates skipped: {skipped}")

        if not commits_to_add:
            print("\n✅ No new commits to add!")
            return

        # Add commits
        print(f"\n📤 Adding {len(commits_to_add)} commits to Notion...")
        added = 0
        errors = []

        for i, commit in enumerate(commits_to_add):
            try:
                adder.create_page(commit, args.owner, args.name)
                added += 1

                if (i + 1) % 10 == 0:
                    print(f"   Progress: {i + 1}/{len(commits_to_add)}")

            except Exception as e:
                errors.append({"sha": commit["sha"][:7], "error": str(e)})
                print(f"   Error: {commit['short_sha']} - {e}")

        # Final summary
        print(f"""
{'='*60}
Complete!
{'='*60}

Added: {added}
Errors: {len(errors)}
Skipped: {skipped}

View in Notion: https://notion.so/{args.database.replace('-', '')}
""")

        if errors:
            print("\nErrors:")
            for err in errors[:5]:
                print(f"  - {err['sha']}: {err['error'][:50]}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more errors")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
