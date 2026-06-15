# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A MyST (Markedly Structured Text) / Jupyter Book site that curates resources for the 2026 DRC Ebola Bundibugyo outbreak response. Maintained by the Ebola Community of Practice under the WHO Collaboratory. The site is purely content — Markdown pages organized into thematic sections — with no application code.

## Build & Development

```bash
pip install jupyter-book        # install the only dependency
jupyter-book start              # local dev server at http://localhost:3000/
```

There are no tests, linting, or CI workflows configured.

## Architecture

- **`myst.yml`** — The single source of truth for site configuration and navigation. The `toc:` section controls all page ordering and section structure. Any new resource page must be registered here to appear on the site.
- **`assets/`** — Static assets (logo, favicon) kept separate from content.
- **`docs/`** — Site pages (`intro.md`, `contributing.md`, `maintainers.md`, `analytical-questions.md`).
- **`docs/resources/`** — All contributed resource content as `.md` files, grouped into section subdirectories (e.g. `docs/resources/dashboards/`, `docs/resources/epi-parameters/`).
- **`docs/_incoming/`** — Staging directory where GitHub Actions deposit auto-generated draft pages from the issue form workflow (currently empty; workflows in `.github/workflows/` and `.github/scripts/` are not yet implemented).
- **`_build/`** — Generated output (gitignored). Contains the built site including the MyST book-theme template.

## Content Workflow

1. **Adding a resource**: Create a `.md` file in the appropriate `docs/resources/<section>/` directory, then add a `- file: docs/resources/<section>/<slug>` entry to the `toc:` in `myst.yml`.
2. **Automated flow (planned)**: A GitHub Issue form (`.github/ISSUE_TEMPLATE/new-resource.yml`) collects resource metadata. A GitHub Action (not yet wired up) would create a draft `.md` in `docs/_incoming/` and open a PR for maintainer review.
3. **New sections**: Add a new `- title: / children:` block in `myst.yml`, create the corresponding directory under `docs/resources/`, and update the section dropdown in `.github/ISSUE_TEMPLATE/new-resource.yml`.

## Resource Page Format

```markdown
# Resource Title

Type · **Organisation** · Authors

Description of the resource.

[Visit resource](https://...)
```
