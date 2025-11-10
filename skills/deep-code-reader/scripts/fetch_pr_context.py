#!/usr/bin/env python3
"""
PR Context Fetcher

Fetches comprehensive context for a GitHub Pull Request including:
- PR metadata and description
- Linked issues
- Review comments and discussions
- Related commits
- Changed files
"""

import os
import json
import argparse
import subprocess
from typing import Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse


class GitHubPRFetcher:
    """Fetch PR context from GitHub API"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            print("Warning: No GitHub token provided. Rate limits will be restrictive.")
            print("Set GITHUB_TOKEN environment variable for higher limits.")
    
    def fetch_pr_context(self, repo_owner: str, repo_name: str, pr_number: int) -> Dict:
        """Fetch complete context for a PR"""
        print(f"Fetching context for {repo_owner}/{repo_name}#{pr_number}...")
        
        context = {
            'pr': self._fetch_pr_details(repo_owner, repo_name, pr_number),
            'commits': self._fetch_pr_commits(repo_owner, repo_name, pr_number),
            'files': self._fetch_pr_files(repo_owner, repo_name, pr_number),
            'comments': self._fetch_pr_comments(repo_owner, repo_name, pr_number),
            'reviews': self._fetch_pr_reviews(repo_owner, repo_name, pr_number),
            'linked_issues': [],
            'timeline': self._fetch_pr_timeline(repo_owner, repo_name, pr_number)
        }
        
        # Extract linked issues from PR body and comments
        context['linked_issues'] = self._extract_linked_issues(context)
        
        return context
    
    def _make_api_request(self, url: str) -> Dict:
        """Make GitHub API request using curl"""
        headers = []
        if self.token:
            headers = ['-H', f'Authorization: token {self.token}']
        
        headers.extend(['-H', 'Accept: application/vnd.github.v3+json'])
        
        cmd = ['curl', '-s'] + headers + [url]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"API request failed: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            return {}
    
    def _fetch_pr_details(self, owner: str, repo: str, pr_num: int) -> Dict:
        """Fetch PR details"""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}"
        pr_data = self._make_api_request(url)
        
        return {
            'number': pr_data.get('number'),
            'title': pr_data.get('title'),
            'body': pr_data.get('body'),
            'state': pr_data.get('state'),
            'user': pr_data.get('user', {}).get('login'),
            'created_at': pr_data.get('created_at'),
            'updated_at': pr_data.get('updated_at'),
            'merged_at': pr_data.get('merged_at'),
            'base_branch': pr_data.get('base', {}).get('ref'),
            'head_branch': pr_data.get('head', {}).get('ref'),
            'labels': [label['name'] for label in pr_data.get('labels', [])],
            'milestone': pr_data.get('milestone', {}).get('title') if pr_data.get('milestone') else None,
            'url': pr_data.get('html_url')
        }
    
    def _fetch_pr_commits(self, owner: str, repo: str, pr_num: int) -> List[Dict]:
        """Fetch commits in the PR"""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}/commits"
        commits_data = self._make_api_request(url)
        
        if not isinstance(commits_data, list):
            return []
        
        commits = []
        for commit in commits_data:
            commits.append({
                'sha': commit.get('sha'),
                'message': commit.get('commit', {}).get('message'),
                'author': commit.get('commit', {}).get('author', {}).get('name'),
                'date': commit.get('commit', {}).get('author', {}).get('date'),
                'url': commit.get('html_url')
            })
        
        return commits
    
    def _fetch_pr_files(self, owner: str, repo: str, pr_num: int) -> List[Dict]:
        """Fetch files changed in the PR"""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}/files"
        files_data = self._make_api_request(url)
        
        if not isinstance(files_data, list):
            return []
        
        files = []
        for file in files_data:
            files.append({
                'filename': file.get('filename'),
                'status': file.get('status'),  # added, modified, removed
                'additions': file.get('additions'),
                'deletions': file.get('deletions'),
                'changes': file.get('changes'),
                'patch': file.get('patch', '')[:500]  # Limit patch size
            })
        
        return files
    
    def _fetch_pr_comments(self, owner: str, repo: str, pr_num: int) -> List[Dict]:
        """Fetch review comments (inline code comments)"""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}/comments"
        comments_data = self._make_api_request(url)
        
        if not isinstance(comments_data, list):
            return []
        
        comments = []
        for comment in comments_data:
            comments.append({
                'id': comment.get('id'),
                'user': comment.get('user', {}).get('login'),
                'body': comment.get('body'),
                'path': comment.get('path'),
                'line': comment.get('line'),
                'created_at': comment.get('created_at'),
                'url': comment.get('html_url')
            })
        
        return comments
    
    def _fetch_pr_reviews(self, owner: str, repo: str, pr_num: int) -> List[Dict]:
        """Fetch PR reviews"""
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}/reviews"
        reviews_data = self._make_api_request(url)
        
        if not isinstance(reviews_data, list):
            return []
        
        reviews = []
        for review in reviews_data:
            reviews.append({
                'id': review.get('id'),
                'user': review.get('user', {}).get('login'),
                'state': review.get('state'),  # APPROVED, CHANGES_REQUESTED, COMMENTED
                'body': review.get('body'),
                'submitted_at': review.get('submitted_at'),
                'url': review.get('html_url')
            })
        
        return reviews
    
    def _fetch_pr_timeline(self, owner: str, repo: str, pr_num: int) -> List[Dict]:
        """Fetch PR timeline events"""
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_num}/timeline"
        # Note: timeline API requires special accept header
        headers = ['-H', 'Accept: application/vnd.github.mockingbird-preview+json']
        
        if self.token:
            headers.extend(['-H', f'Authorization: token {self.token}'])
        
        cmd = ['curl', '-s'] + headers + [url]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            timeline_data = json.loads(result.stdout)
        except:
            return []
        
        if not isinstance(timeline_data, list):
            return []
        
        timeline = []
        for event in timeline_data:
            event_type = event.get('event')
            timeline.append({
                'event': event_type,
                'created_at': event.get('created_at'),
                'actor': event.get('actor', {}).get('login') if event.get('actor') else None,
                'label': event.get('label', {}).get('name') if event.get('label') else None,
                'milestone': event.get('milestone', {}).get('title') if event.get('milestone') else None
            })
        
        return timeline
    
    def _extract_linked_issues(self, context: Dict) -> List[Dict]:
        """Extract issue references from PR body and comments"""
        import re
        
        linked_issues = []
        issue_pattern = r'#(\d+)'
        
        # Check PR body
        pr_body = context['pr'].get('body', '')
        if pr_body:
            for match in re.finditer(issue_pattern, pr_body):
                linked_issues.append({
                    'number': int(match.group(1)),
                    'source': 'pr_body'
                })
        
        # Check review comments
        for comment in context.get('comments', []):
            body = comment.get('body', '')
            for match in re.finditer(issue_pattern, body):
                linked_issues.append({
                    'number': int(match.group(1)),
                    'source': 'comment',
                    'comment_id': comment.get('id')
                })
        
        # Deduplicate
        seen = set()
        unique_issues = []
        for issue in linked_issues:
            issue_num = issue['number']
            if issue_num not in seen:
                seen.add(issue_num)
                unique_issues.append(issue)
        
        return unique_issues


class LocalGitAnalyzer:
    """Analyze local git repository for additional context"""
    
    def __init__(self, repo_path: str = '.'):
        self.repo_path = repo_path
    
    def get_commit_context(self, commit_sha: str, context_size: int = 3) -> Dict:
        """Get commits before and after a specific commit"""
        try:
            # Get commits around the target commit
            cmd = [
                'git', '-C', self.repo_path, 'log', 
                '--oneline', f'-{context_size * 2 + 1}',
                '--format=%H|%an|%ad|%s', '--date=iso',
                commit_sha
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    sha, author, date, message = line.split('|', 3)
                    commits.append({
                        'sha': sha,
                        'author': author,
                        'date': date,
                        'message': message,
                        'is_target': sha.startswith(commit_sha)
                    })
            
            return {'commits': commits}
        except subprocess.CalledProcessError:
            return {'commits': []}
    
    def get_file_history(self, filepath: str, limit: int = 10) -> List[Dict]:
        """Get commit history for a specific file"""
        try:
            cmd = [
                'git', '-C', self.repo_path, 'log',
                f'-{limit}', '--format=%H|%an|%ad|%s',
                '--date=iso', '--', filepath
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    sha, author, date, message = line.split('|', 3)
                    commits.append({
                        'sha': sha,
                        'author': author,
                        'date': date,
                        'message': message
                    })
            
            return commits
        except subprocess.CalledProcessError:
            return []


def format_context_markdown(context: Dict) -> str:
    """Format PR context as readable markdown"""
    md = []
    
    # PR Header
    pr = context['pr']
    md.append(f"# PR #{pr['number']}: {pr['title']}")
    md.append(f"\n**Author:** {pr['user']}")
    md.append(f"**State:** {pr['state']}")
    md.append(f"**Branch:** {pr['head_branch']} → {pr['base_branch']}")
    md.append(f"**Created:** {pr['created_at']}")
    if pr['merged_at']:
        md.append(f"**Merged:** {pr['merged_at']}")
    md.append(f"**URL:** {pr['url']}\n")
    
    # Labels
    if pr['labels']:
        md.append(f"**Labels:** {', '.join(pr['labels'])}\n")
    
    # Description
    if pr['body']:
        md.append("## Description\n")
        md.append(pr['body'])
        md.append("\n")
    
    # Linked Issues
    if context['linked_issues']:
        md.append("## Linked Issues\n")
        for issue in context['linked_issues']:
            md.append(f"- #{issue['number']} (from {issue['source']})")
        md.append("\n")
    
    # Commits
    if context['commits']:
        md.append(f"## Commits ({len(context['commits'])})\n")
        for commit in context['commits']:
            md.append(f"- `{commit['sha'][:7]}` {commit['message']}")
        md.append("\n")
    
    # Changed Files
    if context['files']:
        md.append(f"## Changed Files ({len(context['files'])})\n")
        for file in context['files']:
            status_emoji = {'added': '✨', 'modified': '📝', 'removed': '🗑️'}.get(file['status'], '📄')
            md.append(f"- {status_emoji} `{file['filename']}` (+{file['additions']} -{file['deletions']})")
        md.append("\n")
    
    # Reviews
    if context['reviews']:
        md.append(f"## Reviews ({len(context['reviews'])})\n")
        for review in context['reviews']:
            state_emoji = {'APPROVED': '✅', 'CHANGES_REQUESTED': '❌', 'COMMENTED': '💬'}.get(review['state'], '📝')
            md.append(f"- {state_emoji} **{review['user']}** ({review['state']})")
            if review['body']:
                md.append(f"  > {review['body'][:100]}...")
        md.append("\n")
    
    # Comments
    if context['comments']:
        md.append(f"## Review Comments ({len(context['comments'])})\n")
        for comment in context['comments'][:10]:  # Limit to 10
            md.append(f"- **{comment['user']}** on `{comment['path']}:{comment['line']}`")
            md.append(f"  > {comment['body'][:100]}...")
        md.append("\n")
    
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description='Fetch GitHub PR context')
    parser.add_argument('pr_url', help='GitHub PR URL (e.g., https://github.com/owner/repo/pull/123)')
    parser.add_argument('--output', default='pr_context', help='Output file prefix')
    parser.add_argument('--format', choices=['json', 'markdown', 'both'], default='both',
                        help='Output format')
    parser.add_argument('--token', help='GitHub personal access token (or set GITHUB_TOKEN env var)')
    
    args = parser.parse_args()
    
    # Parse PR URL
    try:
        path_parts = urlparse(args.pr_url).path.strip('/').split('/')
        owner, repo = path_parts[0], path_parts[1]
        pr_number = int(path_parts[3])
    except (IndexError, ValueError):
        print(f"Error: Invalid PR URL format. Expected: https://github.com/owner/repo/pull/123")
        return 1
    
    # Fetch PR context
    fetcher = GitHubPRFetcher(token=args.token)
    context = fetcher.fetch_pr_context(owner, repo, pr_number)
    
    # Output results
    if args.format in ['json', 'both']:
        json_file = f"{args.output}.json"
        with open(json_file, 'w') as f:
            json.dump(context, f, indent=2)
        print(f"\n✅ Context saved to: {json_file}")
    
    if args.format in ['markdown', 'both']:
        md_content = format_context_markdown(context)
        md_file = f"{args.output}.md"
        with open(md_file, 'w') as f:
            f.write(md_content)
        print(f"✅ Markdown summary saved to: {md_file}")
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"  PR: #{context['pr']['number']} - {context['pr']['title']}")
    print(f"  Commits: {len(context['commits'])}")
    print(f"  Changed files: {len(context['files'])}")
    print(f"  Reviews: {len(context['reviews'])}")
    print(f"  Comments: {len(context['comments'])}")
    print(f"  Linked issues: {len(context['linked_issues'])}")


if __name__ == '__main__':
    main()
