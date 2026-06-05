"""Parse a GitHub Issue form body and append a YAML entry to resources.yml."""

import os
import re
import yaml
from datetime import date
from pathlib import Path

SECTION_MAP = {
    "Dashboards": "dashboards",
    "Epi Parameters": "epi-parameters",
    "Outbreak Size Estimates": "outbreak-size-estimates",
    "Risk of Spread": "risk-of-spread",
    "Mobility Data": "mobility-data",
    "Humanitarian Data": "humanitarian-data",
    "Therapeutics & Vaccines": "therapeutics-vaccines",
}


def parse_issue_body(body: str) -> dict:
    """Extract field values from a GitHub Issue form body.

    GitHub renders issue form responses as:
    ### Field Label

    value
    """
    fields = {}
    chunks = re.split(r"^### ", body, flags=re.MULTILINE)
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.split("\n", 1)
        label = lines[0].strip()
        value = lines[1].strip() if len(lines) > 1 else ""
        if value == "_No response_":
            value = ""
        fields[label] = value
    return fields


def main():
    body = os.environ["ISSUE_BODY"]
    fields = parse_issue_body(body)

    title = fields.get("Resource title", "").strip()
    url = fields.get("URL", "").strip()
    resource_type = fields.get("Resource type", "").strip().lower()
    section_label = fields.get("Suggested section", "").strip()
    authors = fields.get("Authors", "").strip()
    organisation = fields.get("Organisation", "").strip()
    description = fields.get("Description", "").strip()

    section = SECTION_MAP.get(section_label, "other")

    entry = {
        "title": title,
        "url": url,
        "type": resource_type,
        "section": section,
        "authors": authors,
        "organisation": organisation,
        "date_added": date.today().isoformat(),
        "description": description,
    }

    data_file = Path("data/resources.yml")
    with open(data_file) as f:
        resources = yaml.safe_load(f) or []

    resources.append(entry)

    with open(data_file, "w") as f:
        yaml.dump(resources, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Added '{title}' to section '{section}'")


if __name__ == "__main__":
    main()
