"""Unit tests for .github/scripts/issue_to_yaml.py — issue body parser."""

import sys
import os
from pathlib import Path
from unittest.mock import patch
from datetime import date

import pytest

# Make the script importable
sys.path.insert(0, str(Path(__file__).parent / ".github" / "scripts"))

from issue_to_yaml import parse_issue_body, SECTION_MAP, main


# ---------------------------------------------------------------------------
# parse_issue_body
# ---------------------------------------------------------------------------

class TestParseIssueBody:
    def test_basic_fields(self):
        body = (
            "### Resource title\n\nMy Dashboard\n\n"
            "### URL\n\nhttps://example.com\n\n"
            "### Description\n\nA useful dashboard.\n"
        )
        fields = parse_issue_body(body)
        assert fields["Resource title"] == "My Dashboard"
        assert fields["URL"] == "https://example.com"
        assert fields["Description"] == "A useful dashboard."

    def test_no_response_becomes_empty(self):
        body = "### Authors\n\n_No response_\n"
        fields = parse_issue_body(body)
        assert fields["Authors"] == ""

    def test_empty_value(self):
        body = "### Authors\n\n\n"
        fields = parse_issue_body(body)
        assert fields["Authors"] == ""

    def test_multiline_value(self):
        body = "### Description\n\nLine one.\nLine two.\n"
        fields = parse_issue_body(body)
        assert "Line one." in fields["Description"]
        assert "Line two." in fields["Description"]

    def test_field_with_no_body(self):
        body = "### Empty field"
        fields = parse_issue_body(body)
        assert fields["Empty field"] == ""

    def test_multiple_fields(self):
        body = (
            "### Resource title\n\nTitle\n\n"
            "### URL\n\nhttps://x.com\n\n"
            "### Resource type\n\nDashboard\n\n"
            "### Suggested section\n\nDashboards\n\n"
            "### Authors\n\nJane\n\n"
            "### Organisation\n\nWHO\n\n"
            "### Description\n\nDesc here.\n"
        )
        fields = parse_issue_body(body)
        assert len(fields) == 7
        assert fields["Resource title"] == "Title"
        assert fields["Organisation"] == "WHO"


# ---------------------------------------------------------------------------
# SECTION_MAP
# ---------------------------------------------------------------------------

class TestSectionMap:
    def test_all_expected_sections_present(self):
        expected = [
            "Dashboards", "Epi Parameters", "Outbreak Size Estimates",
            "Risk of Spread", "Mobility Data", "Humanitarian Data",
            "Therapeutics & Vaccines",
        ]
        for label in expected:
            assert label in SECTION_MAP, f"Missing section: {label}"

    def test_unknown_section_falls_back_to_other(self):
        assert SECTION_MAP.get("Nonexistent", "other") == "other"


# ---------------------------------------------------------------------------
# main — integration
# ---------------------------------------------------------------------------

class TestMain:
    def _make_issue_body(self, **overrides):
        defaults = {
            "Resource title": "Test Resource",
            "URL": "https://test.example.com",
            "Resource type": "Dashboard",
            "Suggested section": "Dashboards",
            "Authors": "Test Author",
            "Organisation": "Test Org",
            "Description": "A test description.",
        }
        defaults.update(overrides)
        parts = []
        for label, value in defaults.items():
            parts.append(f"### {label}\n\n{value}\n")
        return "\n".join(parts)

    def test_appends_yaml_to_file(self, tmp_path):
        data_file = tmp_path / "data" / "resources.yml"
        data_file.parent.mkdir()
        data_file.write_text("# existing\n")

        body = self._make_issue_body()

        with patch.dict(os.environ, {"ISSUE_BODY": body}), \
             patch("issue_to_yaml.Path", return_value=data_file), \
             patch("issue_to_yaml.date") as mock_date:
            mock_date.today.return_value = date(2026, 6, 5)
            mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
            main()

        content = data_file.read_text()
        assert '- title: "Test Resource"' in content
        assert '  url: "https://test.example.com"' in content
        assert "  type: dashboard" in content
        assert "  section: dashboards" in content
        assert '  authors: "Test Author"' in content
        assert '  organisation: "Test Org"' in content
        assert "  date_added: 2026-06-05" in content
        assert "  description: >-" in content
        assert "    A test description." in content

    def test_unknown_section_maps_to_other(self, tmp_path):
        data_file = tmp_path / "data" / "resources.yml"
        data_file.parent.mkdir()
        data_file.write_text("")

        body = self._make_issue_body(**{"Suggested section": "Unknown Section"})

        with patch.dict(os.environ, {"ISSUE_BODY": body}), \
             patch("issue_to_yaml.Path", return_value=data_file), \
             patch("issue_to_yaml.date") as mock_date:
            mock_date.today.return_value = date(2026, 1, 1)
            mock_date.side_effect = lambda *a, **kw: date(*a, **kw)
            main()

        content = data_file.read_text()
        assert "  section: other" in content

    def test_missing_env_var_raises(self):
        with patch.dict(os.environ, {}, clear=True), \
             pytest.raises(KeyError):
            main()
