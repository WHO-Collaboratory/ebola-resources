# Maintainers Guide

## How resources get added

### Automated flow (issue form)

1. A community member opens a GitHub Issue using the "Suggest a Resource" form
2. A GitHub Action creates a `.md` file in the appropriate section directory, appends an `{include}` directive to the section's index file, and opens a Pull Request
3. The maintainer reviews the PR — checks that the file is in the right section and the `{include}` is placed correctly — and merges
4. A deploy workflow builds and publishes the updated site

For resources submitted as "Other / New section", the file goes to `docs/_incoming/` and no index file is modified — the maintainer places it manually.

### Direct PRs

Technical contributors may open PRs with new `.md` files or edits to existing ones. The maintainer adds an `{include}` directive to the appropriate section index file during review.

## Site structure

```
myst.yml                    ← site config + TOC (references index files only)
assets/
  logo.png                  ← site logo and static assets
docs/
  intro.md                  ← landing page
  contributing.md
  maintainers.md
  analytical-questions.md
  _incoming/                ← staging area for automation-created files
  resources/                ← all contributed content
    tools-index.md          ← section index: Resources and tools
    data-index.md           ← section index: Data
    emerging-evidence-index.md  ← section index: Emerging evidence
    community-meetings-index.md ← section index: Community meeting materials
    dashboards/             ← one .md file per resource
    epi-parameters/
    outbreak-size-estimates/
    risk-of-spread/
    mobility-data/
    humanitarian-data/
    therapeutics-vaccines/
```

## How section pages work

Each section has an **index file** (e.g. `tools-index.md`) that uses `{include}` directives to pull in individual resource files. This means:

- All resources in a section render as **one continuous page** in the sidebar
- Individual resource files stay **separate** for easy editing and version control
- The sidebar shows **one entry per section**, not one per resource

## Managing structure

### Adding a resource to the site

1. Create the `.md` file in the appropriate subdirectory (e.g. `docs/resources/dashboards/my-resource.md`)
2. Append an include block to the section's index file:

```markdown
---

```{include} dashboards/my-resource.md
```
```

Include paths are relative to the `docs/resources/` directory where the index files live.

### Creating a new section

1. Create a new index file (e.g. `docs/resources/new-section-index.md`):

```markdown
# New Section Name

Brief description of the section.

---

```{include} new-section/first-resource.md
```
```

2. Add it to `myst.yml`:

```yaml
- file: docs/resources/new-section-index.md
```

**Important:** When creating a new section, also:
1. Update the section dropdown in `.github/ISSUE_TEMPLATE/new-resource.yml`
2. Add the section mapping in `.github/scripts/parse-issue.py` (`SECTION_MAP`)

### Reordering or moving resources

Rearrange the `{include}` directives in the section's index file. Move `.md` files between directories if you want the file paths to match.

## Local development

```bash
pip install jupyter-book
jupyter-book start
```

The site builds at `http://localhost:3000/`.
