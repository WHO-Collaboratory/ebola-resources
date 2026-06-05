# Maintainers Guide

This page documents how the site works end-to-end and what maintainers need to do.

## How resources get added

### Automated flow (issue form)

1. A community member opens a GitHub Issue using the "Suggest a Resource" form
2. A GitHub Action automatically parses the issue, appends an entry to `data/resources.yml`, creates a branch, and opens a Pull Request
3. The maintainer reviews the PR — the diff shows only the new entry — and merges
4. A second GitHub Action rebuilds and deploys the site to GitHub Pages
5. The original issue closes automatically

The maintainer's role is to **review and merge**. The automation handles everything else.

### Direct PRs

Technical contributors may open PRs that either:

- Add a YAML entry to `data/resources.yml`
- Add narrative content to a section page under **Community Notes**

Review these as normal PRs.

## Site architecture

```
data/resources.yml     ← single file, all resource entries
docs/<section>.md      ← section pages (intro + macro + community notes)
main.py                ← mkdocs-macros hook, loads YAML, provides render_resources()
mkdocs.yml             ← site config, nav, plugins
```

Each section page calls `{{ render_resources("section-slug") }}` which filters `data/resources.yml` by the `section` field and renders the entries.

## Adding a resource manually

Append to `data/resources.yml`:

```yaml
- title: "Resource Title"
  url: "https://..."
  type: report
  section: epi-parameters
  authors: "Name, Name"
  organisation: "Org"
  date_added: 2026-06-05
  description: >-
    A short description of the resource.
  notes: >-
    Optional free-form context.
```

## Creating a new section

Four files need updating:

1. **`data/resources.yml`** — add entries with the new section slug
2. **`docs/<new-section>.md`** — create the page:
    ```markdown
    # Section Title

    Intro prose.

    {{ render_resources("new-section-slug") }}

    ## Community Notes

    <!-- Add free-form content below via PR -->
    ```
3. **`mkdocs.yml`** — add the page to `nav:`
4. **`.github/ISSUE_TEMPLATE/new-resource.yml`** — add the section to the dropdown

## Updating or removing a resource

Edit or delete the entry in `data/resources.yml` and open a PR (or commit directly to `main`).

## Local development

```bash
pip install -r requirements.txt
mkdocs serve
```

The site builds at `http://127.0.0.1:8000/ebola-resources/`. Changes to `data/resources.yml` and `docs/` hot-reload.

## Deployment

Deployment is automatic. Every push to `main` triggers `.github/workflows/deploy.yml` which builds the site and deploys to GitHub Pages.
