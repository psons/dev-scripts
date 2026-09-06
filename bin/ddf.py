#!/usr/bin/env python3
"""ddf.py - Development Description Format parser and serializer.

This module provides lossless parsing and serialization for DDF markdown documents.
DDF preserves all document structure (front-matter, headings, sections, text) as
structured data for script automation and API integration.

Usage as module:
    from ddf import parse_from_markdown, serialize_to_json
    doc = parse_from_markdown(text)
    json_output = serialize_to_json(doc)

Usage as command:
    python ddf.py tojson doc.md > doc.json
    python ddf.py tomd doc.json > doc.md
"""

from __future__ import annotations

import sys
import json
import re
import argparse
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ============================================================================
# Data Model
# ============================================================================

@dataclass
class DDFDoc:
    """A complete DDF document with optional front-matter, preamble, and nested sections."""
    attributes: dict[str, Any] | None = None
    preamble: str | None = None
    sections: list[DDFSection] = field(default_factory=list)


@dataclass
class DDFSection:
    """A markdown section with heading, optional attributes, preamble, and nested sections."""
    heading: str
    attributes: dict[str, Any] | None = None
    preamble: str | None = None
    sections: list[DDFSection] | None = field(default_factory=list)


# ============================================================================
# Helper Functions
# ============================================================================

def _get_heading_level(line: str) -> int | None:
    """
    Get heading level from a line, or None if not a valid heading.
    
    Valid headings:
    - Start at column 0
    - Have 1-6 '#' characters
    - Followed by whitespace
    
    Returns heading level (1-6) or None.
    """
    match = re.match(r'^(#{1,6})\s+', line)
    if match:
        return len(match.group(1))
    return None


def _extract_front_matter(lines: list[str], start_idx: int = 0) -> tuple[dict[str, Any] | None, int]:
    """
    Extract YAML front-matter from lines starting at start_idx.
    
    Returns:
        (attributes_dict, next_line_idx) where attributes_dict is None if no valid front-matter
    """
    if start_idx >= len(lines):
        return None, start_idx
    
    # Check for opening delimiter
    if not re.match(r'^---\s*$', lines[start_idx]):
        return None, start_idx
    
    # Find closing delimiter
    close_idx = None
    for i in range(start_idx + 1, len(lines)):
        if re.match(r'^---\s*$', lines[i]):
            close_idx = i
            break
    
    if close_idx is None:
        # No closing delimiter, not valid front-matter
        return None, start_idx
    
    # Extract YAML content
    yaml_lines = lines[start_idx + 1:close_idx]
    yaml_text = '\n'.join(yaml_lines)
    
    if not yaml_text.strip():
        # Empty front-matter block
        return {}, close_idx + 1
    
    try:
        parsed = yaml.safe_load(yaml_text)
        # Must be a dict/mapping
        if not isinstance(parsed, dict):
            return None, start_idx
        return parsed, close_idx + 1
    except yaml.YAMLError:
        # Invalid YAML, treat as regular text
        return None, start_idx


def _parse_section_content(
    lines: list[str],
    start_idx: int,
    parent_level: int
) -> tuple[DDFSection, int]:
    """
    Parse a single section starting at start_idx.
    
    Args:
        lines: All document lines
        start_idx: Index of the heading line
        parent_level: Heading level of this section
        
    Returns:
        (DDFSection, next_line_idx)
    """
    heading_line = lines[start_idx]
    idx = start_idx + 1
    
    # Skip blank lines before potential front-matter
    while idx < len(lines) and lines[idx].strip() == '':
        idx += 1
    
    # Try to extract section front-matter
    attributes, new_idx = _extract_front_matter(lines, idx)
    
    # If front-matter was found, advance idx; otherwise keep blank lines as preamble
    if attributes is not None or new_idx > idx:
        idx = new_idx
        # Skip one blank line after front-matter if present (markdown structure)
        if idx < len(lines) and lines[idx].strip() == '':
            idx += 1
    else:
        # Reset to include those blank lines in preamble
        idx = start_idx + 1
    
    # Collect preamble and nested sections
    preamble_lines = []
    subsections = []
    
    while idx < len(lines):
        line = lines[idx]
        level = _get_heading_level(line)
        
        if level is not None:
            if level <= parent_level:
                # Same or higher level, close this section
                break
            else:
                # Lower level (more #), nested subsection
                subsection, idx = _parse_section_content(lines, idx, level)
                subsections.append(subsection)
        else:
            # Regular text line
            preamble_lines.append(line)
            idx += 1
    
    # Build preamble
    preamble = None
    if preamble_lines:
        preamble_text = '\n'.join(preamble_lines)
        # Strip trailing newline for cleaner data model
        preamble = preamble_text.rstrip('\n')
    
    return DDFSection(
        heading=heading_line,
        attributes=attributes,
        preamble=preamble,
        sections=subsections
    ), idx


# ============================================================================
# Parsing Functions
# ============================================================================

def parse_from_markdown(text: str) -> DDFDoc:
    """
    Parse markdown text into a DDFDoc object.
    
    Args:
        text: Markdown text to parse
        
    Returns:
        DDFDoc object representing the parsed document
        
    Raises:
        ValueError: If YAML front-matter is invalid
    """
    lines = text.split('\n')
    
    # Strip trailing whitespace from each line (preserving markdown structure)
    lines = [line.rstrip() for line in lines]
    
    # Try to extract document front-matter
    attributes, idx = _extract_front_matter(lines, 0)
    
    # Skip one blank line after front-matter if present (markdown structure)
    if attributes is not None and idx < len(lines) and lines[idx].strip() == '':
        idx += 1
    
    # Collect preamble lines (before first heading)
    preamble_lines = []
    first_heading_idx = None
    
    for i in range(idx, len(lines)):
        if _get_heading_level(lines[i]) is not None:
            first_heading_idx = i
            break
        preamble_lines.append(lines[i])
    
    # Build preamble
    preamble = None
    if preamble_lines:
        preamble_text = '\n'.join(preamble_lines)
        # Only set preamble if there's actual content
        if preamble_text.strip():
            # Strip trailing newline for cleaner data model
            preamble = preamble_text.rstrip('\n')
    
    # Parse sections
    sections = []
    if first_heading_idx is not None:
        idx = first_heading_idx
        while idx < len(lines):
            level = _get_heading_level(lines[idx])
            if level is not None:
                section, idx = _parse_section_content(lines, idx, level)
                sections.append(section)
            else:
                # This shouldn't happen, but handle gracefully
                idx += 1
    
    return DDFDoc(
        attributes=attributes,
        preamble=preamble,
        sections=sections
    )


def parse_from_markdown_file(
    path: str | Path,
    encoding: str = "utf-8"
) -> DDFDoc:
    """
    Parse a markdown file into a DDFDoc object.
    
    Args:
        path: Path to markdown file
        encoding: File encoding (default: utf-8)
        
    Returns:
        DDFDoc object representing the parsed document
        
    Raises:
        FileNotFoundError: If file doesn't exist
        UnicodeDecodeError: If file can't be decoded
        ValueError: If YAML front-matter is invalid
    """
    path = Path(path)
    text = path.read_text(encoding=encoding)
    return parse_from_markdown(text)


def parse_from_json(text: str) -> DDFDoc:
    """
    Parse JSON text into a DDFDoc object.
    
    Args:
        text: JSON text conforming to DDF schema
        
    Returns:
        DDFDoc object
        
    Raises:
        json.JSONDecodeError: If JSON is invalid
        ValueError: If JSON doesn't match DDF schema
    """
    data = json.loads(text)
    return _dict_to_doc(data)


def parse_from_json_file(
    path: str | Path,
    encoding: str = "utf-8"
) -> DDFDoc:
    """
    Parse a JSON file into a DDFDoc object.
    
    Args:
        path: Path to JSON file
        encoding: File encoding (default: utf-8)
        
    Returns:
        DDFDoc object
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
        ValueError: If JSON doesn't match DDF schema
    """
    path = Path(path)
    text = path.read_text(encoding=encoding)
    return parse_from_json(text)


def _dict_to_doc(data: dict) -> DDFDoc:
    """Convert dict to DDFDoc."""
    return DDFDoc(
        attributes=data.get("attributes"),
        preamble=data.get("preamble"),
        sections=[_dict_to_section(s) for s in data.get("sections", [])]
    )


def _dict_to_section(data: dict) -> DDFSection:
    """Convert dict to DDFSection."""
    if "heading" not in data:
        raise ValueError("Section missing required 'heading' field")

    sections = data.get("sections", [])
    
    return DDFSection(
        heading=data["heading"],
        attributes=data.get("attributes"),
        preamble=data.get("preamble"),
        sections=None if sections is None else [_dict_to_section(s) for s in sections]
    )


# ============================================================================
# Serialization Functions
# ============================================================================

def serialize_to_markdown(doc: DDFDoc) -> str:
    """
    Serialize a DDFDoc object to markdown text.
    
    Args:
        doc: DDFDoc object to serialize
        
    Returns:
        Markdown text representation
    """
    output = []
    
    # Document front-matter
    if doc.attributes is not None:
        output.append("---")
        yaml_text = yaml.safe_dump(
            doc.attributes,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )
        output.append(yaml_text.rstrip())
        output.append("---")
    
    # Document preamble
    if doc.preamble is not None:
        if output:  # Add blank line after front-matter
            output.append("")
        output.append(doc.preamble.rstrip())
    
    # Sections
    for section in doc.sections:
        if output:  # Add blank line before section
            output.append("")
        output.append(_serialize_section(section).rstrip())
    
    result = '\n'.join(output)
    if result and not result.endswith('\n'):
        result += '\n'
    
    return result


def _serialize_section(section: DDFSection) -> str:
    """Serialize a DDFSection to markdown text."""
    output = []
    
    # Section heading
    output.append(section.heading.rstrip())
    
    # Section front-matter
    if section.attributes is not None:
        output.append("")
        output.append("---")
        yaml_text = yaml.safe_dump(
            section.attributes,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )
        output.append(yaml_text.rstrip())
        output.append("---")
    
    # Section preamble
    if section.preamble is not None:
        if section.attributes is not None:
            output.append("")
        output.append(section.preamble.rstrip())
    
    # Nested sections
    for subsection in section.sections or []:
        output.append("")
        output.append(_serialize_section(subsection).rstrip())
    
    return '\n'.join(output)


def serialize_to_markdown_file(
    doc: DDFDoc,
    path: str | Path,
    encoding: str = "utf-8"
) -> None:
    """
    Serialize a DDFDoc object to a markdown file.
    
    Args:
        doc: DDFDoc object to serialize
        path: Path to output file
        encoding: File encoding (default: utf-8)
    """
    path = Path(path)
    text = serialize_to_markdown(doc)
    path.write_text(text, encoding=encoding)


def serialize_to_json(doc: DDFDoc, indent: int = 2) -> str:
    """
    Serialize a DDFDoc object to JSON text.
    
    Args:
        doc: DDFDoc object to serialize
        indent: JSON indentation (default: 2)
        
    Returns:
        JSON text representation
    """
    data = _doc_to_dict(doc)
    return json.dumps(data, indent=indent, ensure_ascii=False)


def serialize_to_json_file(
    doc: DDFDoc,
    path: str | Path,
    encoding: str = "utf-8",
    indent: int = 2
) -> None:
    """
    Serialize a DDFDoc object to a JSON file.
    
    Args:
        doc: DDFDoc object to serialize
        path: Path to output file
        encoding: File encoding (default: utf-8)
        indent: JSON indentation (default: 2)
    """
    path = Path(path)
    text = serialize_to_json(doc, indent=indent)
    path.write_text(text, encoding=encoding)


def _doc_to_dict(doc: DDFDoc) -> dict:
    """Convert DDFDoc to dict."""
    result = {}
    if doc.attributes is not None:
        result["attributes"] = doc.attributes
    if doc.preamble is not None:
        result["preamble"] = doc.preamble
    if doc.sections:
        result["sections"] = [_section_to_dict(s) for s in doc.sections]
    return result


def _section_to_dict(section: DDFSection) -> dict:
    """Convert DDFSection to dict."""
    result = {"heading": section.heading}
    if section.attributes is not None:
        result["attributes"] = section.attributes
    if section.preamble is not None:
        result["preamble"] = section.preamble
    if section.sections:
        result["sections"] = [_section_to_dict(s) for s in section.sections]
    return result


# ============================================================================
# Command-Line Interface
# ============================================================================

def _print_help():
    """Print help message."""
    help_text = """usage: ddf.py <subcommand> [options] [file]

Development Description Format (DDF) parser and serializer.

subcommands:
  tomd      Convert JSON to markdown
  tojson    Convert markdown to JSON
  help      Show this help message

For markdown ↔ JSON conversion with lossless round-trip.
Read from FILE or stdin if FILE is omitted.

Examples:
  ddf.py tojson doc.md > doc.json
  ddf.py tomd doc.json > doc.md
  cat doc.md | ddf.py tojson
"""
    print(help_text)


def main(argv: list[str] | None = None) -> int:
    """Command entrypoint."""
    if argv is None:
        argv = sys.argv[1:]
    
    # Handle help
    if not argv or argv[0] in ('help', '--help', '-h'):
        _print_help()
        return 0
    
    subcommand = argv[0]
    
    if subcommand not in ('tomd', 'tojson'):
        print(f"Error: Unknown subcommand '{subcommand}'", file=sys.stderr)
        print("Run 'ddf.py help' for usage information", file=sys.stderr)
        return 1
    
    # Parse remaining args
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('file', nargs='?', help='Input file (default: stdin)')
    
    try:
        args = parser.parse_args(argv[1:])
    except SystemExit:
        return 1
    
    # Read input
    try:
        if args.file:
            input_text = Path(args.file).read_text(encoding='utf-8')
        else:
            input_text = sys.stdin.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    except UnicodeDecodeError as e:
        print(f"Error: Unable to decode file: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        return 1
    
    # Process based on subcommand
    try:
        if subcommand == 'tojson':
            doc = parse_from_markdown(input_text)
            output = serialize_to_json(doc, indent=2)
            print(output)
        elif subcommand == 'tomd':
            doc = parse_from_json(input_text)
            output = serialize_to_markdown(doc)
            print(output, end='')
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        return 1
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML front-matter: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
