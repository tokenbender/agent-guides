#!/usr/bin/env python3
"""
Extract Claude Code session data from JSONL files.

This script reads Claude Code conversation history from the local storage
and can export it in various formats for documentation or analysis.

Usage:
    python extract-claude-session.py [--latest] [--session-id <id>] [--format <format>]
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class ClaudeSessionExtractor:
    def __init__(self, project_path: str = None):
        """Initialize the session extractor.
        
        Args:
            project_path: Path to project directory. If None, uses current directory.
        """
        if project_path is None:
            project_path = os.getcwd()
        
        self.sessions_dir = self._resolve_sessions_dir(project_path)
    
    @staticmethod
    def _slugify(path: str) -> str:
        """Approximate Claude Code's project directory naming (non-alphanumerics become '-')."""
        return re.sub(r'[^a-zA-Z0-9]', '-', path)
    
    def _resolve_sessions_dir(self, project_path: str) -> Path:
        """Find the sessions directory for a project, tolerating slug format changes.
        
        Claude Code has used different slug rules over time (replacing '/' only,
        then all non-alphanumerics). Try the current format first, then fall back
        to matching directories by normalized comparison.
        """
        projects_root = Path.home() / '.claude' / 'projects'
        candidates = [
            projects_root / self._slugify(project_path),
            projects_root / project_path.replace('/', '-'),  # legacy format
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        # Fallback: compare normalized forms of existing directories
        target = self._slugify(project_path).strip('-').lower()
        if projects_root.exists():
            for entry in projects_root.iterdir():
                if entry.is_dir() and self._slugify(entry.name).strip('-').lower() == target:
                    return entry
        # Nothing matched; return the default so callers get a clean 'not found'
        return candidates[0]
    
    def list_sessions(self) -> List[Tuple[str, datetime, int]]:
        """List all available sessions for the project.
        
        Returns:
            List of tuples: (session_id, last_modified, file_size)
        """
        if not self.sessions_dir.exists():
            return []
        
        sessions = []
        for jsonl_file in self.sessions_dir.glob('*.jsonl'):
            session_id = jsonl_file.stem
            stat = jsonl_file.stat()
            last_modified = datetime.fromtimestamp(stat.st_mtime)
            file_size = stat.st_size
            sessions.append((session_id, last_modified, file_size))
        
        # Sort by last modified, newest first
        sessions.sort(key=lambda x: x[1], reverse=True)
        return sessions
    
    def get_latest_session(self) -> Optional[str]:
        """Get the ID of the most recently modified session."""
        sessions = self.list_sessions()
        return sessions[0][0] if sessions else None
    
    def extract_messages(self, session_id: str) -> List[Dict]:
        """Extract all messages from a session.
        
        Args:
            session_id: The session UUID
            
        Returns:
            List of message dictionaries with timestamp, role, and content
        """
        session_file = self.sessions_dir / f"{session_id}.jsonl"
        if not session_file.exists():
            raise FileNotFoundError(f"Session file not found: {session_file}")
        
        messages = []
        with open(session_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    data = json.loads(line.strip())
                    
                    # Claude Code stores messages differently - check for 'message' key directly
                    if 'message' in data and isinstance(data['message'], dict):
                        msg = data['message']
                        if 'role' in msg and 'content' in msg:
                            # Extract timestamp from the data, not the message
                            timestamp = data.get('timestamp', 'unknown')
                            
                            # Parse content if it's a list (tool usage)
                            content = msg['content']
                            if isinstance(content, list):
                                content = self._parse_content_blocks(content)
                            
                            messages.append({
                                'timestamp': timestamp,
                                'role': msg['role'],
                                'content': content,
                                'type': data.get('type', 'unknown'),
                                'raw': msg  # Keep raw message for detailed analysis
                            })
                except json.JSONDecodeError:
                    print(f"Warning: Failed to parse line {line_num}", file=sys.stderr)
                except Exception as e:
                    print(f"Warning: Error on line {line_num}: {e}", file=sys.stderr)
        
        return messages
    
    def _parse_content_blocks(self, content_blocks: List) -> str:
        """Parse content blocks (text, thinking, tool interactions, attachments)."""
        parsed = []
        for block in content_blocks:
            if isinstance(block, dict):
                block_type = block.get('type')
                if block_type == 'text':
                    parsed.append(block.get('text', ''))
                elif block_type == 'thinking':
                    parsed.append(f"[Thinking]\n{block.get('thinking', '')}")
                elif block_type == 'redacted_thinking':
                    parsed.append('[Thinking — redacted]')
                elif block_type == 'tool_use':
                    tool_name = block.get('name', 'unknown')
                    tool_input = block.get('input', {})
                    parsed.append(f"[Tool: {tool_name}]\n{json.dumps(tool_input, indent=2)}")
                elif block_type == 'tool_result':
                    content = block.get('content', '')
                    if isinstance(content, list):
                        # Nested blocks (e.g. text + images inside a tool result)
                        content = self._parse_content_blocks(content)
                    parsed.append(f"[Tool Result]\n{content}")
                elif block_type == 'image':
                    parsed.append('[Image]')
                elif block_type == 'document':
                    parsed.append(f"[Document: {block.get('title', 'untitled')}]")
                else:
                    parsed.append(f"[{block_type or 'unknown'} block]")
            else:
                parsed.append(str(block))
        return '\n'.join(parsed)
    
    def export_markdown(self, session_id: str, output_file: str = None) -> str:
        """Export session as markdown with full conversation history.
        
        Args:
            session_id: The session UUID
            output_file: Output file path. If None, returns markdown string.
            
        Returns:
            Markdown formatted conversation
        """
        messages = self.extract_messages(session_id)
        
        # Build markdown
        md_lines = [
            f"# Claude Code Session: {session_id}",
            f"\nExtracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\nTotal messages: {len(messages)}",
            "\n---\n"
        ]
        
        for i, msg in enumerate(messages, 1):
            timestamp = msg['timestamp']
            role = msg['role'].title()
            content = msg['content']
            
            md_lines.append(f"## Message {i} - {role}")
            md_lines.append(f"*Timestamp: {timestamp}*\n")
            md_lines.append(content)
            md_lines.append("\n---\n")
        
        markdown = '\n'.join(md_lines)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(markdown)
            print(f"Session exported to: {output_file}")
        
        return markdown
    
    def export_jsonl(self, session_id: str, output_file: str) -> None:
        """Export session as cleaned JSONL file."""
        messages = self.extract_messages(session_id)
        
        with open(output_file, 'w') as f:
            for msg in messages:
                # Remove 'raw' field for cleaner export
                export_msg = {k: v for k, v in msg.items() if k != 'raw'}
                f.write(json.dumps(export_msg) + '\n')
        
        print(f"Session exported to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Extract Claude Code session data')
    parser.add_argument('--project', help='Project directory path (default: current directory)')
    parser.add_argument('--latest', action='store_true', help='Extract the latest session')
    parser.add_argument('--session-id', help='Specific session ID to extract')
    parser.add_argument('--list', action='store_true', help='List all available sessions')
    parser.add_argument('--format', choices=['markdown', 'jsonl'], default='markdown', 
                        help='Export format (default: markdown)')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    # Initialize extractor
    extractor = ClaudeSessionExtractor(args.project)
    
    # List sessions
    if args.list:
        sessions = extractor.list_sessions()
        if not sessions:
            print("No sessions found for this project")
            return
        
        print(f"Found {len(sessions)} sessions:\n")
        for session_id, last_modified, size in sessions[:10]:  # Show max 10
            size_mb = size / (1024 * 1024)
            print(f"  {session_id}")
            print(f"    Last modified: {last_modified}")
            print(f"    Size: {size_mb:.2f} MB\n")
        return
    
    # Determine which session to extract
    if args.latest:
        session_id = extractor.get_latest_session()
        if not session_id:
            print("No sessions found for this project")
            return
        print(f"Using latest session: {session_id}")
    elif args.session_id:
        session_id = args.session_id
    else:
        print("Please specify --latest or --session-id")
        return
    
    # Extract and export
    try:
        if args.format == 'markdown':
            if args.output:
                extractor.export_markdown(session_id, args.output)
            else:
                # Generate default filename
                output_file = f"claude-session-{session_id[:8]}-{datetime.now():%Y%m%d-%H%M%S}.md"
                extractor.export_markdown(session_id, output_file)
        elif args.format == 'jsonl':
            output_file = args.output or f"claude-session-{session_id[:8]}-{datetime.now():%Y%m%d-%H%M%S}.jsonl"
            extractor.export_jsonl(session_id, output_file)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main() or 0)