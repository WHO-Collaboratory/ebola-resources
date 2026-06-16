"""Parse a GitHub issue body from the 'Suggest a Resource' form and generate a resource page.

Usage:
    python parse-issue.py --issue-body "$BODY" --output-dir docs/resources

Outputs:
    - A .md file in docs/resources/
    - An updated section file with an {include} directive

Prints the generated file path and (if applicable) the section file path to stdout,
one per line, for use by the calling workflow.
"""

import argparse
import os
import re
import sys
from pathlib import Path


SECTION_MAP = {
    "Resources and tools": "docs/resources/tools.md",
    "Data": "docs/resources/data.md",
    "Emerging evidence": "docs/resources/outbreak-size.md",
    "Analytical questions": None,
    "Community meeting materials": "docs/resources/community-meetings.md",
}


def parse_body(body: str) -> dict:
    """Extract fields from a GitHub issue form body.

    Issue form bodies render as:
        ### Label\n\nValue\n\n### Next Label\n\n...
    """
    fields = {}
    parts = re.split(r"^### ", body, flags=re.MULTILINE)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.split("\n", 1)
        label = lines[0].strip()
        value = lines[1].strip() if len(lines) > 1 else ""
        # Normalise label to match issue template ids
        key = label.lower().replace(" ", "_")
        fields[key] = value
    return fields


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug[:80]


def generate_page(fields: dict) -> str:
    title = fields.get("title_of_the_ebola_resource", "Untitled")
    rtype = fields.get("resource_type", "Resource")
    org = fields.get("organisation", "")
    authors = fields.get("authors", "")
    date = fields.get("date", "")
    desc = fields.get("description", "")
    url = fields.get("url", "")

    header_parts = [rtype]
    if org:
        header_parts.append(f"**{org}**")
    if authors:
        header_parts.append(authors)
    if date:
        header_parts.append(date)
    header_line = " · ".join(header_parts)

    lines = [f"# {title}", "", header_line, "", desc]
    if url:
        lines += ["", f"[Visit resource]({url})"]
    return "\n".join(lines) + "\n"


def update_section_file(section_path: Path, resource_filename: str) -> bool:
    """Append an {include} directive to a section file.

    Returns True if the entry was added, False if the section file wasn't found.
    """
    if not section_path.exists():
        return False

    content = section_path.read_text().rstrip("\n")
    addition = f"\n\n---\n\n```{{include}} {resource_filename}\n```\n"
    section_path.write_text(content + addition)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-body", required=True)
    parser.add_argument("--output-dir", default="docs/resources")
    args = parser.parse_args()

    fields = parse_body(args.issue_body)

    title = fields.get("title_of_the_ebola_resource", "")
    if not title:
        print("ERROR: Could not parse resource title from issue body", file=sys.stderr)
        sys.exit(1)

    slug = slugify(title)
    section = fields.get("suggested_section", "Other / New section")

    # All resources go into docs/resources/ (flat structure)
    if section in SECTION_MAP:
        out_dir = Path(args.output_dir)
    else:
        out_dir = Path("docs/_incoming")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"
    out_path.write_text(generate_page(fields))

    # Update section file if section is known
    section_file_str = SECTION_MAP.get(section)
    if section_file_str:
        section_path = Path(section_file_str)
        updated = update_section_file(section_path, f"{slug}.md")
        if not updated:
            print(
                f"WARNING: Could not find section file '{section_path}'. "
                "Maintainer must add the include manually.",
                file=sys.stderr,
            )
        else:
            # Print both paths: resource file, then section file
            print(str(out_path))
            print(str(section_path))
            return

    # Only resource file created (no section update)
    print(str(out_path))


if __name__ == "__main__":
    main()
