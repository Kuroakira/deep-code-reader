#!/usr/bin/env python3
"""
Notion Integration Helpers
Utility functions for exporting analysis results to Notion
"""

import json
import os
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime


class NotionExporter:
    """Export code analysis results to Notion"""

    def __init__(self, config_path: str = None):
        """Initialize with configuration."""
        if config_path is None:
            # Default to repo config
            repo_root = Path(__file__).parent.parent.parent
            config_path = repo_root / "config" / "notion_config.json"

        self.config = self._load_config(config_path)
        self.template = self._load_template()

    def _load_config(self, config_path: str) -> Dict:
        """Load Notion configuration."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(
                f"Notion config not found: {config_path}\n"
                "Run install.sh to configure Notion integration"
            )

        with open(config_file) as f:
            config = json.load(f)

        # Validate required fields
        if not config.get("api_key") or config["api_key"] == "YOUR_NOTION_API_KEY":
            raise ValueError(
                "Notion API key not configured. "
                "Edit ~/.claude/deep-code-reader/notion_config.json with your API key"
            )

        return config

    def _load_template(self) -> Dict:
        """Load Notion page template."""
        repo_root = Path(__file__).parent.parent.parent
        template_path = repo_root / "config" / "notion_template.json"

        with open(template_path) as f:
            return json.load(f)

    def build_page_content(self, analysis_data: Dict) -> Dict:
        """
        Build Notion page content from analysis data.

        Args:
            analysis_data: Complete analysis results containing:
                - project_name: str
                - repo_url: str
                - commit_id: str
                - architecture: Dict with summary and mermaid
                - data_flow: Dict with flows and diagrams
                - dependencies: Dict with modules and summary
                - recommendations: str (optional)

        Returns:
            Notion-compatible page structure
        """
        template = self.template["page_template"]

        # Replace placeholders in title
        title = template["title"].format(
            project_name=analysis_data.get("project_name", "Unknown")
        )

        # Build properties
        properties = {
            "Repository": {
                "url": analysis_data.get("repo_url", "")
            },
            "Commit": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": analysis_data.get("commit_id", "HEAD")
                        }
                    }
                ]
            },
            "Analysis Date": {
                "date": {
                    "start": datetime.now().isoformat()
                }
            },
            "Status": {
                "select": {
                    "name": "Completed"
                }
            }
        }

        # Add architecture patterns if detected
        if "architecture" in analysis_data and "patterns" in analysis_data["architecture"]:
            patterns = analysis_data["architecture"]["patterns"]
            properties["Architecture Pattern"] = {
                "multi_select": [{"name": p} for p in patterns]
            }

        # Build content blocks
        blocks = self._build_content_blocks(analysis_data)

        return {
            "title": title,
            "icon": template.get("icon", "🔍"),
            "properties": properties,
            "children": blocks
        }

    def _build_content_blocks(self, data: Dict) -> List[Dict]:
        """Build content blocks from analysis data."""
        blocks = []

        # Architecture section
        if "architecture" in data:
            blocks.extend([
                self._heading_block("🏗️ Architecture Overview", level=1),
                self._paragraph_block(
                    data["architecture"].get("summary", "No summary available")
                ),
                self._heading_block("📊 Architecture Diagram", level=2),
                self._code_block(
                    data["architecture"].get("mermaid", ""),
                    "mermaid"
                )
            ])

        # Data flow section
        if "data_flow" in data:
            blocks.extend([
                self._heading_block("🔄 Data Flow Analysis", level=1),
                self._heading_block("Key Flows", level=2)
            ])

            flows = data["data_flow"].get("flows", [])
            for flow in flows:
                blocks.append(self._bullet_block(flow))

        # Dependencies section
        if "dependencies" in data:
            blocks.extend([
                self._heading_block("📦 Dependencies", level=1),
                self._heading_block("Module Dependencies", level=2),
                self._paragraph_block(
                    data["dependencies"].get("summary", "No summary available")
                )
            ])

        # Raw data toggle
        blocks.append(
            self._toggle_block(
                "📋 Raw Analysis Data",
                [self._code_block(json.dumps(data, indent=2), "json")]
            )
        )

        # Divider
        blocks.append({"type": "divider", "divider": {}})

        # Recommendations callout
        if "recommendations" in data:
            blocks.append(
                self._callout_block(
                    "💡 Contribution Recommendations",
                    data["recommendations"],
                    emoji="💡"
                )
            )

        return blocks

    # Block builders
    def _heading_block(self, text: str, level: int = 1) -> Dict:
        """Create heading block."""
        heading_type = f"heading_{level}"
        return {
            "type": heading_type,
            heading_type: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": text}
                    }
                ]
            }
        }

    def _paragraph_block(self, text: str) -> Dict:
        """Create paragraph block."""
        return {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": text}
                    }
                ]
            }
        }

    def _code_block(self, code: str, language: str = "plain text") -> Dict:
        """Create code block."""
        return {
            "type": "code",
            "code": {
                "language": language,
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": code}
                    }
                ]
            }
        }

    def _bullet_block(self, text: str) -> Dict:
        """Create bulleted list item."""
        return {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": text}
                    }
                ]
            }
        }

    def _toggle_block(self, title: str, children: List[Dict]) -> Dict:
        """Create toggle block with children."""
        return {
            "type": "toggle",
            "toggle": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": title}
                    }
                ],
                "children": children
            }
        }

    def _callout_block(self, title: str, content: str, emoji: str = "💡") -> Dict:
        """Create callout block."""
        return {
            "type": "callout",
            "callout": {
                "icon": {"emoji": emoji},
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": title},
                        "annotations": {"bold": True}
                    }
                ],
                "children": [
                    self._paragraph_block(content)
                ]
            }
        }

    def export_to_notion(self, analysis_data: Dict) -> str:
        """
        Export analysis to Notion (placeholder - requires Notion MCP).

        Returns:
            Notion page URL
        """
        # Build page content
        page_content = self.build_page_content(analysis_data)

        # In actual implementation, this would use Notion MCP tools
        # For now, return a placeholder
        print("📤 Exporting to Notion...")
        print(f"  Project: {analysis_data.get('project_name', 'Unknown')}")
        print(f"  Database: {self.config.get('database_id', 'Not configured')}")

        # This would be the actual Notion API call via MCP
        # page_url = create_notion_page(self.config['database_id'], page_content)

        # Placeholder return
        return f"https://notion.so/{self.config.get('database_id', 'placeholder')}"


def main():
    """CLI for testing Notion export."""
    import argparse

    parser = argparse.ArgumentParser(description="Test Notion export")
    parser.add_argument("analysis_file", help="JSON file with analysis results")
    args = parser.parse_args()

    # Load analysis data
    with open(args.analysis_file) as f:
        analysis_data = json.load(f)

    # Export to Notion
    exporter = NotionExporter()
    page_content = exporter.build_page_content(analysis_data)

    # Print generated content
    print(json.dumps(page_content, indent=2))


if __name__ == "__main__":
    main()
