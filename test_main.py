"""Unit tests for main.py — MkDocs macros hook."""

from unittest.mock import MagicMock, patch, mock_open

import pytest

from main import define_env, TYPE_BADGES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_env_and_get_macro(resources_yaml: str):
    """Call define_env with faked YAML data and return the render_resources macro."""
    env = MagicMock()
    registered = {}

    def capture_macro(fn):
        registered[fn.__name__] = fn

    env.macro = capture_macro

    with patch("builtins.open", mock_open(read_data=resources_yaml)):
        define_env(env)

    return registered["render_resources"]


# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------

class TestYamlLoading:
    def test_empty_yaml_file(self):
        render = _build_env_and_get_macro("")
        assert render("anything") == "*No resources listed yet.*"

    def test_null_yaml_file(self):
        render = _build_env_and_get_macro("# just a comment\n")
        assert render("anything") == "*No resources listed yet.*"

    def test_loads_real_data_file(self):
        """Smoke test against the actual resources.yml."""
        env = MagicMock()
        registered = {}
        env.macro = lambda fn: registered.update({fn.__name__: fn})
        define_env(env)
        render = registered["render_resources"]
        result = render("dashboards")
        assert "*No resources listed yet.*" not in result
        assert "###" in result


# ---------------------------------------------------------------------------
# Section filtering
# ---------------------------------------------------------------------------

SAMPLE_YAML = """
- title: "Alpha"
  section: dashboards
  type: dashboard
  description: "Dashboard A"
  organisation: "Org A"
  authors: "Author A"
  url: "https://example.com/a"

- title: "Beta"
  section: epi-parameters
  type: tool
  description: "Tool B"
  organisation: "Org B"
  authors: ""
  url: "https://example.com/b"

- title: "Gamma"
  section: dashboards
  type: report
  description: "Report C"
  organisation: ""
  authors: ""
  url: ""
"""


class TestSectionFiltering:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.render = _build_env_and_get_macro(SAMPLE_YAML)

    def test_returns_only_matching_section(self):
        result = self.render("dashboards")
        assert "Alpha" in result
        assert "Gamma" in result
        assert "Beta" not in result

    def test_different_section(self):
        result = self.render("epi-parameters")
        assert "Beta" in result
        assert "Alpha" not in result

    def test_missing_section_returns_fallback(self):
        assert self.render("nonexistent") == "*No resources listed yet.*"


# ---------------------------------------------------------------------------
# Rendering — badges
# ---------------------------------------------------------------------------

class TestBadgeRendering:
    def test_known_type_gets_icon_badge(self):
        yml = """
- title: "D"
  section: s
  type: dashboard
"""
        result = _build_env_and_get_macro(yml)("s")
        assert ":material-monitor-dashboard: Dashboard" in result

    def test_all_known_types(self):
        for type_key, badge_text in TYPE_BADGES.items():
            yml = f"""
- title: "X"
  section: s
  type: {type_key}
"""
            result = _build_env_and_get_macro(yml)("s")
            assert badge_text in result, f"Badge missing for type '{type_key}'"

    def test_unknown_type_uses_raw_value(self):
        yml = """
- title: "U"
  section: s
  type: custom-thing
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "custom-thing" in result

    def test_missing_type_does_not_crash(self):
        yml = """
- title: "NoType"
  section: s
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "NoType" in result


# ---------------------------------------------------------------------------
# Rendering — metadata line
# ---------------------------------------------------------------------------

class TestMetadataLine:
    def test_organisation_bold(self):
        yml = """
- title: "T"
  section: s
  type: tool
  organisation: "WHO"
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "**WHO**" in result

    def test_authors_present(self):
        yml = """
- title: "T"
  section: s
  type: tool
  authors: "Jane Doe"
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "Jane Doe" in result

    def test_empty_organisation_omitted(self):
        yml = """
- title: "T"
  section: s
  type: tool
  organisation: ""
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "****" not in result


# ---------------------------------------------------------------------------
# Rendering — optional fields (url, notes)
# ---------------------------------------------------------------------------

class TestOptionalFields:
    def test_url_renders_link(self):
        yml = """
- title: "L"
  section: s
  type: tool
  url: "https://example.com"
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "[https://example.com](https://example.com)" in result

    def test_empty_url_no_link(self):
        yml = """
- title: "L"
  section: s
  type: tool
  url: ""
"""
        result = _build_env_and_get_macro(yml)("s")
        assert ":octicons-arrow-right-16:" not in result

    def test_missing_url_no_link(self):
        yml = """
- title: "L"
  section: s
  type: tool
"""
        result = _build_env_and_get_macro(yml)("s")
        assert ":octicons-arrow-right-16:" not in result

    def test_notes_rendered_italic(self):
        yml = """
- title: "N"
  section: s
  type: tool
  notes: "Contact someone for access."
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "*Contact someone for access.*" in result

    def test_no_notes_no_italic_line(self):
        yml = """
- title: "N"
  section: s
  type: tool
"""
        result = _build_env_and_get_macro(yml)("s")
        lines = [l for l in result.strip().split("\n") if l.strip()]
        assert not lines[-1].startswith("*") or lines[-1].startswith("*No")


# ---------------------------------------------------------------------------
# Rendering — separator between entries
# ---------------------------------------------------------------------------

class TestMultipleEntries:
    def test_entries_separated_by_hr(self):
        yml = """
- title: "A"
  section: s
  type: tool
- title: "B"
  section: s
  type: dashboard
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "\n\n---\n\n" in result
        assert "### A" in result
        assert "### B" in result

    def test_single_entry_no_separator(self):
        yml = """
- title: "Solo"
  section: s
  type: tool
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "---" not in result


# ---------------------------------------------------------------------------
# Rendering — description
# ---------------------------------------------------------------------------

class TestDescription:
    def test_description_present(self):
        yml = """
- title: "D"
  section: s
  type: tool
  description: "Some important info."
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "Some important info." in result

    def test_missing_description_does_not_crash(self):
        yml = """
- title: "D"
  section: s
  type: tool
"""
        result = _build_env_and_get_macro(yml)("s")
        assert "### D" in result
