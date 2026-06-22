# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A MyST / Jupyter Book v2 site that curates resources for the 2026 DRC Ebola Bundibugyo outbreak response. Maintained by the Ebola Outbreak Analytics CoP under the WHO Collaboratory. The site is purely content — Markdown pages organized into thematic sections — with no application code.

- **Repo:** `WHO-Collaboratory/ebola-resources`
- **Live site:** https://who-collaboratory.github.io/ebola-resources/
- **Local directory** is named `ebola-resources-jb` but the remote repo is `ebola-resources`

## Build & Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter-book start              # local dev server at http://localhost:3000/
jupyter-book build --html       # static build to _build/html
```

## Architecture

- **`myst.yml`** — Site config and TOC. The TOC references only top-level pages and section index files (not individual resources). The `base_url` must be under `site.options` (not directly under `site`).
- **`assets/`** — Static assets (logo, favicon).
- **`docs/`** — Top-level site pages: `intro.md`, `contributing.md`, `formatting-guide.md`, `maintainers.md`, `analytical-questions.md`.
- **`docs/resources/*-index.md`** — Section index files that use `{include}` directives to pull in individual resource files. Each renders as one continuous page in the sidebar.
- **`docs/resources/<section>/`** — Individual resource `.md` files, grouped by subdirectory (e.g. `dashboards/`, `epi-parameters/`, `outbreak-size-estimates/`).
- **`docs/_incoming/`** — Staging directory for resources submitted as "Other / New section" via the issue form.
- **`_build/`** — Generated output (gitignored).

## Site Sections

The sidebar is structured as:
- Home, How to contribute, Formatting guide, Maintainers
- **Resources and tools** — dashboards, R packages, epi parameter tools
- **Data** — mobility, humanitarian, epidemiological datasets
- **Emerging evidence** — with sub-sections: Outbreak Size, Risk of Spread, Therapeutics & Vaccines
- **Analytical questions** — placeholder for community questions
- **Community meeting materials** — seminars, recordings

## Content Workflow

### Adding a resource (two files)
1. Create a `.md` file in `docs/resources/<section>/`
2. Add an `{include}` directive to the section's index file (e.g. `docs/resources/tools-index.md`)

### Automated flow (issue form)
- A contributor fills in the [issue form](https://github.com/WHO-Collaboratory/ebola-resources/issues/new?template=new-resource.yml)
- `.github/workflows/create-resource.yml` triggers on `opened` and `labeled` events
- `.github/scripts/parse-issue.py` parses the issue body, generates the `.md` file, and appends an `{include}` directive to the section's index file
- A PR is created on branch `resource/issue-<number>` using a PAT (`RESOURCE_BOT_TOKEN` secret) since org-level GitHub Actions PR permissions are disabled
- For "Other / New section" submissions, the file goes to `docs/_incoming/` and no index file is modified
- To retrigger a failed run: remove and re-add the `new-resource` label

### Adding a new section
1. Create a `docs/resources/<name>-index.md` with a title and `{include}` directives
2. Add `- file: docs/resources/<name>-index.md` to `myst.yml`
3. Create directory under `docs/resources/`
4. Update section dropdown in `.github/ISSUE_TEMPLATE/new-resource.yml`
5. Update `SECTION_MAP` in `.github/scripts/parse-issue.py`

## Resource Page Format

```markdown
# Title

Type · **Organisation** · Authors · Date

Description of the resource.

[Visit resource](https://...)
```

All metadata fields (title, type, organisation, authors, date, link, description) are mandatory. See `docs/formatting-guide.md` for MyST features available in page body (admonitions, code blocks, tables, math, etc).

## CI/CD

- **`.github/workflows/build.yml`** — Reusable workflow: validates YAML, checks TOC file references exist, builds with `jupyter-book build --html`. Sets `BASE_URL=/ebola-resources` env var for correct GitHub Pages subpath.
- **`.github/workflows/check.yml`** — Runs `build.yml` on PRs.
- **`.github/workflows/deploy.yml`** — Runs `build.yml` on push to main, then deploys to GitHub Pages.
- **`.github/workflows/create-resource.yml`** — Creates resource PRs from issue form submissions.

## Key Gotchas

- Jupyter Book v2 requires `--html` flag for static builds (not just `jupyter-book build .`)
- `BASE_URL` must be set as an **environment variable** during build for GitHub Pages subpath — the `myst.yml` config alone is not sufficient
- `base_url` in `myst.yml` belongs under `site.options`, not directly under `site`
- TOC entries need explicit `.md` extensions to avoid inference warnings
- GitHub Actions PR creation requires a PAT (`RESOURCE_BOT_TOKEN`), not `GITHUB_TOKEN`
