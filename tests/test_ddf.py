"""
Comprehensive tests for ddf.py Phase 1 implementation.

Test coverage includes:
- Basic document parsing
- Heading nesting (relative levels)
- Document and section front-matter
- Round-trip conversions
- Edge cases
- Error handling
- Acceptance test with normal-ddf.md
"""

import json
import pytest
from pathlib import Path
import sys

# Add bin directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'bin'))

from ddf import (
    DDFDoc,
    DDFSection,
    parse_from_markdown,
    parse_from_markdown_file,
    parse_from_json,
    parse_from_json_file,
    serialize_to_markdown,
    serialize_to_markdown_file,
    serialize_to_json,
    serialize_to_json_file,
)


# ============================================================================
# Test 1: Basic Parsing
# ============================================================================

def test_empty_document():
    """Empty document should parse to empty DDFDoc."""
    doc = parse_from_markdown("")
    assert doc.attributes is None
    assert doc.preamble is None
    assert doc.sections == []


def test_document_with_preamble_only():
    """Document with only text (no headings) should have preamble."""
    text = "Just some text.\nNo headings here.\n"
    doc = parse_from_markdown(text)
    assert doc.attributes is None
    assert doc.preamble == "Just some text.\nNo headings here."
    assert doc.sections == []


def test_document_with_front_matter():
    """Document with front-matter should parse attributes."""
    text = """---
title: My Doc
author: Test
---
"""
    doc = parse_from_markdown(text)
    assert doc.attributes == {"title": "My Doc", "author": "Test"}
    assert doc.preamble is None
    assert doc.sections == []


def test_document_with_front_matter_and_preamble():
    """Document with front-matter and preamble should parse both."""
    text = """---
title: My Doc
---
This is preamble text.
"""
    doc = parse_from_markdown(text)
    assert doc.attributes == {"title": "My Doc"}
    assert doc.preamble == "This is preamble text."
    assert doc.sections == []


def test_single_section():
    """Document with single section should parse correctly."""
    text = """# Heading One
Section content.
"""
    doc = parse_from_markdown(text)
    assert doc.attributes is None
    assert doc.preamble is None
    assert len(doc.sections) == 1
    assert doc.sections[0].heading == "# Heading One"
    assert doc.sections[0].preamble == "Section content."


def test_multiple_sections_same_level():
    """Multiple sections at same level should be siblings."""
    text = """# First
Content 1.

# Second
Content 2.
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 2
    assert doc.sections[0].heading == "# First"
    assert doc.sections[0].preamble == "Content 1."
    assert doc.sections[1].heading == "# Second"
    assert doc.sections[1].preamble == "Content 2."


# ============================================================================
# Test 2: Heading Nesting
# ============================================================================

def test_h3_as_first_heading():
    """H3 as first heading should be top-level section."""
    text = """### Third Level
Content.
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 1
    assert doc.sections[0].heading == "### Third Level"


def test_descending_nesting():
    """Lower-level headings should nest under higher-level."""
    text = """## Section
Content.

### Subsection
Nested content.
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 1
    assert doc.sections[0].heading == "## Section"
    assert len(doc.sections[0].sections) == 1
    assert doc.sections[0].sections[0].heading == "### Subsection"


def test_ascending_closes_section():
    """Higher-level heading should close current section."""
    text = """### H3 First
Content.

## H2 Second
Content 2.
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 2
    assert doc.sections[0].heading == "### H3 First"
    assert doc.sections[1].heading == "## H2 Second"


def test_multiple_nesting_levels():
    """Multiple levels of nesting should work."""
    text = """# H1
Content 1.

## H2
Content 2.

### H3
Content 3.

#### H4
Content 4.
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 1
    h1 = doc.sections[0]
    assert h1.heading == "# H1"
    assert len(h1.sections) == 1
    
    h2 = h1.sections[0]
    assert h2.heading == "## H2"
    assert len(h2.sections) == 1
    
    h3 = h2.sections[0]
    assert h3.heading == "### H3"
    assert len(h3.sections) == 1
    
    h4 = h3.sections[0]
    assert h4.heading == "#### H4"


def test_same_level_after_nesting():
    """Same level heading after nesting should create sibling."""
    text = """## First
Content.

### Nested
Nested content.

## Second
Content 2.
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 2
    assert doc.sections[0].heading == "## First"
    assert doc.sections[1].heading == "## Second"
    assert len(doc.sections[0].sections) == 1


# ============================================================================
# Test 3: Front-Matter Handling
# ============================================================================

def test_front_matter_with_various_types():
    """Front-matter should support various YAML types."""
    text = """---
string: "hello"
number: 42
boolean: true
null_value: null
list: [1, 2, 3]
nested:
  key: value
---
"""
    doc = parse_from_markdown(text)
    assert doc.attributes == {
        "string": "hello",
        "number": 42,
        "boolean": True,
        "null_value": None,
        "list": [1, 2, 3],
        "nested": {"key": "value"}
    }


def test_invalid_yaml_treated_as_text():
    """Invalid YAML should be treated as regular text."""
    text = """---
not: valid: yaml
---

# Heading
"""
    # Invalid YAML should be treated as preamble
    doc = parse_from_markdown(text)
    assert doc.attributes is None
    assert "---" in doc.preamble


def test_missing_closing_delimiter():
    """Front-matter without closing delimiter should be treated as text."""
    text = """---
title: My Doc

# Heading
"""
    doc = parse_from_markdown(text)
    assert doc.attributes is None
    assert "---" in doc.preamble


def test_second_front_matter_as_text():
    """Second front-matter block should be part of preamble."""
    text = """---
attrib1: value1
---
raw text
---
attrib2: value2
---
"""
    doc = parse_from_markdown(text)
    assert doc.attributes == {"attrib1": "value1"}
    assert "attrib2" in doc.preamble


def test_empty_front_matter():
    """Empty front-matter block should parse as empty dict."""
    text = """---
---

# Heading
"""
    doc = parse_from_markdown(text)
    assert doc.attributes == {}


# ============================================================================
# Test 4: Section Front-Matter
# ============================================================================

def test_section_with_front_matter():
    """Section with front-matter should parse attributes."""
    text = """## My Section

---
status: active
priority: high
---

Section content.
"""
    doc = parse_from_markdown(text)
    section = doc.sections[0]
    assert section.attributes == {"status": "active", "priority": "high"}
    assert section.preamble == "Section content."


def test_multiple_sections_with_front_matter():
    """Multiple sections can each have front-matter."""
    text = """## First

---
status: done
---

Content 1.

## Second

---
status: active
---

Content 2.
"""
    doc = parse_from_markdown(text)
    assert doc.sections[0].attributes == {"status": "done"}
    assert doc.sections[1].attributes == {"status": "active"}


def test_nested_section_with_front_matter():
    """Nested sections can have front-matter."""
    text = """## Parent

---
level: 1
---

Parent content.

### Child

---
level: 2
---

Child content.
"""
    doc = parse_from_markdown(text)
    parent = doc.sections[0]
    child = parent.sections[0]
    assert parent.attributes == {"level": 1}
    assert child.attributes == {"level": 2}


# ============================================================================
# Test 5: Round-Trip Conversion
# ============================================================================

def test_markdown_round_trip_basic():
    """Parse markdown then serialize should match."""
    original = """---
title: Test
---

Preamble text.

# Heading

Section content.
"""
    doc = parse_from_markdown(original)
    serialized = serialize_to_markdown(doc)
    doc2 = parse_from_markdown(serialized)
    
    # Compare structure
    assert doc2.attributes == doc.attributes
    assert doc2.preamble == doc.preamble
    assert len(doc2.sections) == len(doc.sections)


def test_json_round_trip():
    """Parse markdown → JSON → parse JSON → markdown should preserve structure."""
    original = """---
title: Test
---

# Section

---
key: value
---

Content.
"""
    doc1 = parse_from_markdown(original)
    json_text = serialize_to_json(doc1)
    doc2 = parse_from_json(json_text)
    markdown2 = serialize_to_markdown(doc2)
    doc3 = parse_from_markdown(markdown2)
    
    # Compare final document structure
    assert doc3.attributes == doc1.attributes
    assert len(doc3.sections) == len(doc1.sections)
    assert doc3.sections[0].attributes == doc1.sections[0].attributes


def test_round_trip_preserves_nesting():
    """Round-trip should preserve section nesting."""
    text = """# Parent

Parent content.

## Child

Child content.
"""
    doc1 = parse_from_markdown(text)
    json_text = serialize_to_json(doc1)
    doc2 = parse_from_json(json_text)
    
    assert len(doc2.sections) == 1
    assert len(doc2.sections[0].sections) == 1
    assert doc2.sections[0].sections[0].heading == "## Child"


# ============================================================================
# Test 6: Edge Cases
# ============================================================================

def test_heading_with_trailing_hashes():
    """Heading with trailing # should be preserved."""
    text = "## Heading ##\n"
    doc = parse_from_markdown(text)
    assert doc.sections[0].heading == "## Heading ##"


def test_seven_hashes_not_heading():
    """Line with >6 # characters should not be a heading."""
    text = """####### Not a heading
# Real heading
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 1
    assert doc.sections[0].heading == "# Real heading"
    assert "####### Not a heading" in doc.preamble


def test_heading_not_at_margin():
    """Heading not at left margin should not be a heading."""
    text = """  ## Not a heading
# Real heading
"""
    doc = parse_from_markdown(text)
    assert len(doc.sections) == 1
    assert doc.sections[0].heading == "# Real heading"


def test_unicode_content():
    """Unicode content should be preserved."""
    text = """---
title: 日本語
---

Unicode: 你好世界 🎉

# Heading with émojis 🚀
"""
    doc = parse_from_markdown(text)
    assert doc.attributes["title"] == "日本語"
    assert "你好世界" in doc.preamble
    assert "émojis 🚀" in doc.sections[0].heading


def test_empty_preamble_is_none():
    """Empty preamble should be None, not empty string."""
    text = "# Heading\n"
    doc = parse_from_markdown(text)
    assert doc.preamble is None


def test_empty_attributes_vs_none():
    """Empty front-matter {} vs no front-matter None."""
    text1 = """---
---
# Heading
"""
    text2 = "# Heading\n"
    
    doc1 = parse_from_markdown(text1)
    doc2 = parse_from_markdown(text2)
    
    assert doc1.attributes == {}
    assert doc2.attributes is None


def test_windows_line_endings():
    """Windows line endings should be handled."""
    text = "---\r\ntitle: Test\r\n---\r\n\r\n# Heading\r\n"
    doc = parse_from_markdown(text)
    assert doc.attributes == {"title": "Test"}
    assert len(doc.sections) == 1


# ============================================================================
# Test 7: Error Handling
# ============================================================================

def test_parse_from_markdown_file_not_found():
    """Parsing non-existent file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_from_markdown_file("/nonexistent/file.md")


def test_parse_invalid_json():
    """Parsing invalid JSON should raise JSONDecodeError."""
    with pytest.raises(json.JSONDecodeError):
        parse_from_json("not valid json")


def test_parse_json_missing_heading():
    """JSON with section missing 'heading' should raise ValueError."""
    json_text = '{"sections": [{"preamble": "content"}]}'
    with pytest.raises(ValueError, match="heading"):
        parse_from_json(json_text)


# ============================================================================
# Test 8: Acceptance Test
# ============================================================================

def test_acceptance_normal_ddf():
    """
    Acceptance test: Parse normal-ddf.md and verify it matches normal-ddf.json.
    
    This is the canonical test from the specification.
    """
    # Paths to test files
    spec_dir = Path(__file__).parent.parent / 'docs' / 'dev' / 'spec' / 'usecases' / 'ddf'
    md_file = spec_dir / 'normal-ddf.md'
    json_file = spec_dir / 'normal-ddf.json'
    
    # Skip if test files don't exist
    if not md_file.exists() or not json_file.exists():
        pytest.skip(f"Test files not found: {md_file} or {json_file}")
    
    # Parse markdown
    doc = parse_from_markdown_file(md_file)
    
    # Load expected JSON
    with open(json_file, 'r', encoding='utf-8') as f:
        expected = json.load(f)
    
    # Convert doc to dict and compare
    actual = json.loads(serialize_to_json(doc))
    
    # Compare structure
    assert actual == expected, f"Parsed structure doesn't match expected JSON.\nActual: {json.dumps(actual, indent=2)}\nExpected: {json.dumps(expected, indent=2)}"


# ============================================================================
# Test 9: Serialization Specific Tests
# ============================================================================

def test_serialize_to_json_omits_none():
    """JSON serialization should omit None values."""
    doc = DDFDoc(
        attributes=None,
        preamble="Just text.\n",
        sections=[]
    )
    json_text = serialize_to_json(doc)
    data = json.loads(json_text)
    
    assert "attributes" not in data
    assert "preamble" in data
    assert "sections" not in data  # Empty list also omitted


def test_serialize_section_with_no_subsections():
    """Section with no subsections should omit sections key in JSON."""
    doc = DDFDoc(
        sections=[
            DDFSection(
                heading="# Test",
                preamble="Content.\n",
                sections=[]
            )
        ]
    )
    json_text = serialize_to_json(doc)
    data = json.loads(json_text)
    
    assert "sections" not in data["sections"][0]


def test_section_sections_may_be_none():
    """A section may represent no subsections with None."""
    doc = DDFDoc(sections=[DDFSection(heading="# Test", sections=None)])

    assert serialize_to_markdown(doc) == "# Test\n"
    assert "sections" not in json.loads(serialize_to_json(doc))["sections"][0]

    parsed = parse_from_json('{"sections": [{"heading": "# Test", "sections": null}]}')
    assert parsed.sections[0].sections is None


def test_markdown_serialization_blank_lines():
    """Markdown serialization should have proper blank lines."""
    doc = DDFDoc(
        attributes={"title": "Test"},
        preamble="Preamble.\n",
        sections=[
            DDFSection(heading="# Section", preamble="Content.\n")
        ]
    )
    markdown = serialize_to_markdown(doc)
    
    # Should have blank lines between front-matter, preamble, and sections
    assert "---\n\nPreamble" in markdown
    assert "Preamble.\n\n# Section" in markdown


def test_section_serialization_with_front_matter():
    """Section with front-matter should have proper formatting."""
    section = DDFSection(
        heading="## Test",
        attributes={"key": "value"},
        preamble="Content.\n"
    )
    doc = DDFDoc(sections=[section])
    markdown = serialize_to_markdown(doc)
    
    assert "## Test\n\n---" in markdown
    assert "---\n\nContent" in markdown


# ============================================================================
# Test 10: API Functions
# ============================================================================

def test_parse_and_serialize_file_functions(tmp_path):
    """Test file-based parse and serialize functions."""
    # Create test markdown file
    md_path = tmp_path / "test.md"
    md_content = """---
title: Test
---

# Heading
Content.
"""
    md_path.write_text(md_content, encoding='utf-8')
    
    # Parse from file
    doc = parse_from_markdown_file(md_path)
    assert doc.attributes == {"title": "Test"}
    
    # Serialize to JSON file
    json_path = tmp_path / "test.json"
    serialize_to_json_file(doc, json_path)
    assert json_path.exists()
    
    # Parse from JSON file
    doc2 = parse_from_json_file(json_path)
    assert doc2.attributes == doc.attributes
    
    # Serialize to markdown file
    md_path2 = tmp_path / "test2.md"
    serialize_to_markdown_file(doc2, md_path2)
    assert md_path2.exists()
    
    # Verify round-trip
    doc3 = parse_from_markdown_file(md_path2)
    assert doc3.attributes == doc.attributes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
