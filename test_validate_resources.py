"""PR validation: ensure resources.yml is valid and will render correctly.

Run with:  .venv/bin/pytest test_validate_resources.py -v
"""

from pathlib import Path
from unittest.mock import MagicMock

import yaml
import pytest

from main import define_env, TYPE_BADGES

DATA_FILE = Path("data/resources.yml")
DOCS_DIR = Path("docs")

VALID_TYPES = set(TYPE_BADGES.keys())

VALID_SECTIONS = {
    "dashboards",
    "epi-parameters",
    "outbreak-size-estimates",
    "risk-of-spread",
    "mobility-data",
    "humanitarian-data",
    "therapeutics-vaccines",
}

REQUIRED_FIELDS = {"title", "type", "section"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def resources():
    with open(DATA_FILE) as f:
        data = yaml.safe_load(f)
    assert isinstance(data, list), "resources.yml must be a YAML list"
    return data


@pytest.fixture(scope="module")
def render():
    """Return the render_resources macro wired to the real data file."""
    env = MagicMock()
    registered = {}
    env.macro = lambda fn: registered.update({fn.__name__: fn})
    define_env(env)
    return registered["render_resources"]


# ---------------------------------------------------------------------------
# YAML structure validation
# ---------------------------------------------------------------------------

class TestYamlStructure:
    def test_file_exists(self):
        assert DATA_FILE.exists(), f"{DATA_FILE} not found"

    def test_is_valid_yaml(self):
        with open(DATA_FILE) as f:
            data = yaml.safe_load(f)
        assert data is not None, "resources.yml is empty"
        assert isinstance(data, list), "resources.yml root must be a list"

    def test_not_empty(self, resources):
        assert len(resources) > 0, "resources.yml has no entries"


# ---------------------------------------------------------------------------
# Per-entry schema validation
# ---------------------------------------------------------------------------

class TestEntrySchema:
    def test_every_entry_is_a_dict(self, resources):
        for i, entry in enumerate(resources):
            assert isinstance(entry, dict), f"Entry {i} is not a mapping"

    def test_required_fields_present(self, resources):
        for i, entry in enumerate(resources):
            for field in REQUIRED_FIELDS:
                assert field in entry and entry[field], (
                    f"Entry {i} ({entry.get('title', '?')}) missing required field '{field}'"
                )

    def test_type_is_known(self, resources):
        for i, entry in enumerate(resources):
            assert entry.get("type") in VALID_TYPES, (
                f"Entry {i} ({entry.get('title', '?')}) has unknown type '{entry.get('type')}'. "
                f"Valid types: {VALID_TYPES}"
            )

    def test_section_is_known(self, resources):
        for i, entry in enumerate(resources):
            assert entry.get("section") in VALID_SECTIONS, (
                f"Entry {i} ({entry.get('title', '?')}) has unknown section '{entry.get('section')}'. "
                f"Valid sections: {VALID_SECTIONS}"
            )

    def test_no_duplicate_titles(self, resources):
        titles = [r.get("title") for r in resources]
        seen = set()
        for t in titles:
            assert t not in seen, f"Duplicate title: '{t}'"
            seen.add(t)

    def test_url_format_if_present(self, resources):
        for i, entry in enumerate(resources):
            url = entry.get("url", "")
            if url:
                assert url.startswith("http://") or url.startswith("https://"), (
                    f"Entry {i} ({entry.get('title', '?')}) has invalid URL: '{url}'"
                )


# ---------------------------------------------------------------------------
# Docs pages exist for every section
# ---------------------------------------------------------------------------

class TestDocsCoverage:
    def test_every_section_has_docs_page(self):
        for section in VALID_SECTIONS:
            page = DOCS_DIR / f"{section}.md"
            assert page.exists(), f"Missing docs page for section '{section}': {page}"

    def test_docs_pages_call_render_resources(self):
        for section in VALID_SECTIONS:
            page = DOCS_DIR / f"{section}.md"
            content = page.read_text()
            expected = f'render_resources("{section}")'
            assert expected in content, (
                f"{page} does not call render_resources(\"{section}\")"
            )


# ---------------------------------------------------------------------------
# Rendering produces valid output for every section in the data
# ---------------------------------------------------------------------------

class TestRenderingIntegration:
    def test_every_section_renders_without_error(self, resources, render):
        sections_in_data = {r.get("section") for r in resources}
        for section in sections_in_data:
            result = render(section)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_every_section_produces_headings(self, resources, render):
        sections_in_data = {r.get("section") for r in resources}
        for section in sections_in_data:
            result = render(section)
            assert "###" in result, f"Section '{section}' produced no headings"

    def test_every_entry_title_appears_in_output(self, resources, render):
        for entry in resources:
            section = entry["section"]
            title = entry["title"]
            result = render(section)
            assert title in result, f"Title '{title}' missing from rendered '{section}'"
