# Maintainers Guide

## How resources get added

### Automated flow (issue form)

1. A community member opens a GitHub Issue using the "Suggest a Resource" form
2. A GitHub Action creates a `.md` file in the appropriate section directory, updates `myst.yml`, and opens a Pull Request
3. The maintainer reviews the PR — checks that the file is in the right section, reorders the `myst.yml` entry if needed, and merges
4. A deploy workflow builds and publishes the updated site

For resources submitted as "Other / New section", the file goes to `docs/_incoming/` and `myst.yml` is not modified — the maintainer places it manually.

### Direct PRs

Technical contributors may open PRs with new `.md` files or edits to existing ones. The maintainer adds any new files to `myst.yml` during review.

## Site structure

```
myst.yml                    ← site config + TOC (you control this)
assets/
  logo.png                  ← site logo and static assets
docs/
  intro.md                  ← landing page
  contributing.md
  maintainers.md
  analytical-questions.md
  _incoming/                ← staging area for automation-created files
  resources/                ← all contributed content
    dashboards/             ← one .md file per resource
    epi-parameters/
    outbreak-size-estimates/
    risk-of-spread/
    mobility-data/
    humanitarian-data/
    therapeutics-vaccines/
```

## Managing structure

The site navigation is defined entirely by the `toc:` section in `myst.yml`. You have full control over sections, sub-sections, and ordering.

### Adding a resource to the site

Add one line to `myst.yml` under the appropriate section:

```yaml
- title: Dashboards
  children:
    - file: docs/resources/dashboards/inrb-umie-dashboard
    - file: docs/resources/dashboards/new-resource        # ← add here
```

### Creating a new section

```yaml
- title: New Section Name
  children:
    - file: docs/resources/new-section/first-resource
```

**Important:** When creating a new section, also:
1. Update the section dropdown in `.github/ISSUE_TEMPLATE/new-resource.yml`
2. Add the section mapping in `.github/scripts/parse-issue.py` (`SECTION_MAP`)

### Creating sub-sections

```yaml
- title: Epidemiology
  children:
    - title: Parameters
      children:
        - file: docs/resources/epi-parameters/grepi-perg
    - title: Estimates
      children:
        - file: docs/resources/outbreak-size-estimates/mccabe-imperial
```

### Reordering or moving resources

Rearrange the lines in `myst.yml`. Move `.md` files between directories if you want the file paths to match.

## Local development

```bash
pip install jupyter-book
jupyter-book start
```

The site builds at `http://localhost:3000/`.
