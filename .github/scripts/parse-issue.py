"""Parse a GitHub issue body from the 'Suggest a Resource' form and generate a resource page.

Usage:
    python parse-issue.py --issue-body "$BODY" --output-dir docs/resources --myst-yml myst.yml

Outputs:
    - A .md file in the appropriate section directory
    - An updated myst.yml with the new entry appended to the correct section

Prints the generated file path to stdout for use by the calling workflow.
"""

import argparse
import re
import sys
from pathlib import Path


SECTION_MAP = {
    "Resources and tools": "tools",
    "Data": "data",
    "Emerging evidence": "emerging-evidence",
    "Analytical questions": "analytical-questions",
    "Community meeting materials": "community-meetings",
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
    title = fields.get("resource_title", "Untitled")
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


def update_myst_yml(myst_path: Path, section_title: str, file_entry: str) -> bool:
    """Append a file entry to the correct section in myst.yml.

    Returns True if the entry was added, False if the section wasn't found.
    """
    content = myst_path.read_text()
    lines = content.split("\n")

    # Find the section by matching `- title: <section_title>`
    target = f"- title: {section_title}"
    section_idx = None
    for i, line in enumerate(lines):
        if line.strip() == target:
            section_idx = i
            break

    if section_idx is None:
        return False

    # Find the `children:` line immediately after the section title
    children_idx = None
    for i in range(section_idx + 1, min(section_idx + 3, len(lines))):
        if "children:" in lines[i]:
            children_idx = i
            break

    if children_idx is None:
        return False

    # Determine indentation of existing children entries
    indent = ""
    for i in range(children_idx + 1, len(lines)):
        line = lines[i]
        if line.strip().startswith("- file:") or line.strip().startswith("- title:"):
            indent = re.match(r"^(\s*)", line).group(1)
            break

    # Find the last child entry in this section (before next sibling section or end)
    insert_idx = children_idx + 1
    base_indent_len = len(indent)
    for i in range(children_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if not stripped:
            continue
        line_indent = len(lines[i]) - len(lines[i].lstrip())
        if line_indent < base_indent_len and stripped:
            break
        insert_idx = i + 1

    new_line = f"{indent}- file: {file_entry}"
    lines.insert(insert_idx, new_line)
    myst_path.write_text("\n".join(lines))
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-body", required=True)
    parser.add_argument("--output-dir", default="docs/resources")
    parser.add_argument("--myst-yml", default="myst.yml")
    args = parser.parse_args()

    fields = parse_body(args.issue_body)

    title = fields.get("resource_title", "")
    if not title:
        print("ERROR: Could not parse resource title from issue body", file=sys.stderr)
        sys.exit(1)

    slug = slugify(title)
    section = fields.get("suggested_section", "Other / New section")

    # Determine output directory
    if section in SECTION_MAP:
        subdir = SECTION_MAP[section]
        out_dir = Path(args.output_dir) / subdir
    else:
        out_dir = Path("docs/_incoming")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"
    out_path.write_text(generate_page(fields))

    # Update myst.yml if section is known
    myst_path = Path(args.myst_yml)
    file_entry = str(out_path).removesuffix(".md")
    if section in SECTION_MAP and myst_path.exists():
        updated = update_myst_yml(myst_path, section, file_entry)
        if not updated:
            print(
                f"WARNING: Could not find section '{section}' in {myst_path}. "
                "Maintainer must add the entry manually.",
                file=sys.stderr,
            )

    print(str(out_path))


if __name__ == "__main__":
    main()
