---
description: Save the full session history to disk with citations, then prepare for context compaction — OS-style paging for Claude's memory
argument-hint: "[filename_prefix] [output_directory]"
allowed-tools: Bash, Read, Write, WebFetch
disable-model-invocation: true
---

# Page - Session History Dump with Citations and Memory Management

Like OS paging for processes, this command saves the entire conversation state to disk by extracting it from Claude Code's local storage (`~/.claude/projects/`). After running this command, you can use `/compact` to free up Claude's context memory.

> **Built-in alternatives:** `/export` saves the current conversation as plain text, and `/rewind` rolls back to checkpoints. Use `page` when you need the full-citation, two-file (full + compact) archive this command produces.

## Usage

```
/page [filename_prefix] [output_directory]
```

## Arguments

- `filename_prefix` (optional): Custom prefix for output files. Defaults to "session-dump"
- `output_directory` (optional): Directory to save files. Defaults to current working directory

## Description

This command implements a memory management strategy similar to OS paging:

1. **Page Out (Save to Disk)**:
   - Saves complete conversation state with full citations
   - Creates indexed source references for quick retrieval
   - Preserves all context before memory compaction

2. **Generated Files**:
   - **Full History File** (`{prefix}-{timestamp}-full.md`):
     - Compact summary at top for quick reference
     - Complete conversation transcript with timestamps
     - All file operations with paths and content
     - Web resources with URLs and excerpts
     - Command executions with outputs
     - Full citation index for all sources
   
   - **Compact Memory File** (`{prefix}-{timestamp}-compact.md`):
     - Executive summary of session
     - Key decisions and outcomes
     - Important code changes made
     - Quick reference links
     - Optimized for future context loading

3. **Memory Management Workflow**:
   - First: Run `/page` to save everything to disk
   - Then: Run `/compact` to free up Claude's context memory
   - Result: Fresh context while preserving full history
   - Essential for long development sessions
   - Related: `/rewind` for rolling back to an earlier checkpoint instead of compacting

**Note**: This prepares for `/compact` by saving everything first. Run `/compact` after this command completes.

## Implementation

Please execute this comprehensive session documentation process:

### Phase 1: History Extraction from Claude Code Storage
1. Download and use the extract-claude-session.py script from agent-guides:
   - Script URL: `https://raw.githubusercontent.com/tokenbender/agent-guides/main/scripts/extract-claude-session.py`
   - Download it to a temporary location and run it
   - This will automatically find and extract the current session
   
2. The script handles:
   - Finding the current project's Claude storage directory
   - Locating the most recent session file
   - Extracting all messages with proper formatting
   - Preserving tool usage information and timestamps

### Phase 2: Source Attribution  
Parse and cite all sources encountered:
- **Local Files**: `file:///path/to/file.ext#L10-L20` 
- **Web Pages**: `[Source Title](https://url.com)` with content excerpt
- **Command Outputs**: `$ command` with full output and exit codes
- **Tool Results**: Tool name, parameters, and results
- **Generated Content**: Mark AI-generated vs user-provided content

### Phase 3: Full History Generation
Create comprehensive markdown with compact summary at top:
```markdown
# Session History - {timestamp}

## Quick Summary (Compact Memory)

### Executive Summary
{2-3 sentence summary of what was accomplished}

### Key Accomplishments
1. **Task 1**: Brief description and outcome
2. **Task 2**: What was done and result
3. **Task 3**: Achievement and impact

### Important Findings
- ✅ Key finding or verification
- 📄 Created file: path/to/file
- 🔧 Fixed issue: description

### Quick Links
- **Main Files**: Links to key files touched
- **Documentation**: Links to docs created/updated
- **References**: External resources used

---

## Full Session Overview
- Start Time: {start}
- Duration: {duration} 
- Total Messages: {count}
- Files Modified: {file_count}
- Web Pages Accessed: {web_count}
- Commands Executed: {cmd_count}

## Conversation Timeline

### Message 1 - User ({timestamp})
{content}

**Sources Referenced:**
- [file.py](file:///path/file.py#L1-L50) - Function implementation
- [Documentation](https://example.com/docs) - API reference

### Message 2 - Assistant ({timestamp})
{content}

**Tools Used:**
- read_file: `/path/to/file.py` (lines 1-50)
- web_search: "claude code best practices" (8 results)
- Bash: `git status` (exit code: 0)

**Files Created/Modified:**
- [new_feature.py](file:///path/new_feature.py) - Created
- [config.json](file:///path/config.json#L15) - Modified line 15

{continue for all messages...}

## Source Index

### Local Files Accessed
1. [file1.py](file:///path/file1.py) - Read 3 times, modified once
2. [config.json](file:///path/config.json) - Modified

### Web Resources  
1. [Claude Code Best Practices](https://anthropic.com/...) - Retrieved Apr 18
2. [GitHub Repository](https://github.com/...) - Searched for examples

### Command Executions
1. `git status` - Check repository state
2. `npm run build` - Build verification  

## Generated Artifacts
- Commands created: 4
- Files created: 2  
- Files modified: 3
```

### Phase 4: Memory Compaction
Generate executive summary:
```markdown
# Session Compact Memory - {timestamp}

## Executive Summary
{2-3 sentence summary of what was accomplished}

## Key Decisions Made
- Decision 1: Reasoning and outcome
- Decision 2: Context and implementation

## Code Changes Summary  
- Feature A: Added functionality X to file Y
- Bug Fix B: Resolved issue Z in component W

## Important Context for Future Sessions
- Project uses framework X with pattern Y
- Key files: config.json, main.py, utils/helpers.py
- Build command: `npm run build`
- Test command: `npm test`

## Quick Reference Links
- [Full History](./{prefix}-{timestamp}-full.md)
- [Key File 1](file:///path/key-file.py)
- [Important Documentation](https://url.com)

## Session Metrics
- Duration: {duration}
- Files touched: {count}
- Major features added: {count}
- Issues resolved: {count}
```

### Phase 5: File Management and Final Steps
- Generate compact memory file first
- Include compact content at top of full history file
- Save both files in current working directory (unless output_directory specified)
- Use timestamp format: YYYY-MM-DD_HHMMSS
- Confirm successful save with file paths and sizes
- Display the compact summary in the conversation
- **IMPORTANT**: After everything is saved, instruct the user to run `/compact` to free up Claude's memory

## Output Format

The command generates two files:
1. `{prefix}-{timestamp}-full.md` - Complete history (typically large)
2. `{prefix}-{timestamp}-compact.md` - Executive summary (optimized for context)

Both files use consistent markdown formatting with proper citations and are immediately available for reference or inclusion in future sessions.

## Example Usage

```bash
# Basic usage - creates session-dump files in current directory
/page

# Custom prefix
/page feature-implementation

# Custom prefix and directory
/page bug-fix-session ./docs/sessions/

# Results in current directory (or specified directory):
# - feature-implementation-2025-06-20_143022-full.md
# - feature-implementation-2025-06-20_143022-compact.md

# After completion, run /compact to free up memory:
/compact
```

This command is essential for maintaining context across long development sessions and creating comprehensive documentation of AI-assisted development workflows.
