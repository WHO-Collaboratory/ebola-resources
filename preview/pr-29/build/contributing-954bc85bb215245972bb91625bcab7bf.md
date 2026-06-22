# Contributing

This resource list is maintained by the Ebola Outbreak Analytics CoP. Contributions are welcome from anyone working on the 2026 DRC Ebola Bundibugyo response.

## Ways to contribute

### 1. Submit an issue (no coding needed)

Open a GitHub Issue using our structured form:

[Suggest a Resource](https://github.com/WHO-Collaboratory/ebola-resources/issues/new?template=new-resource.yml)

Fill in the fields — title, URL, type, section, authors, organisation, date, and a short description. A GitHub Action will create a draft page and open a Pull Request. A maintainer will review, adjust placement if needed, and merge.

### 2. Open a Pull Request directly

Create a `.md` file in the appropriate section directory (e.g. `docs/resources/dashboards/my-resource.md`) and add an `{include}` directive to the section's index file (e.g. `docs/resources/tools-index.md`). Use the format below.

## Resource page format

Every resource page should include these mandatory metadata fields in a standardized header:

```markdown
# Resource Title

Type · **Organisation** · Authors · Date

Description of the resource — as much or as little as needed.

[Visit resource](https://...)
```

| Field | Required | Example |
|---|---|---|
| Title | Yes | `# INRB UMIE Dashboard` |
| Type | Yes | Dashboard, Report, Tool, Dataset, Package |
| Organisation | Yes | Imperial College London |
| Authors | Yes | Ruth McCabe et al. |
| Date | Yes | 2026-05-20 |
| Link | Yes | `[Visit resource](https://...)` |
| Description | Yes | Free-text Markdown |

Beyond the header, the page body is free-text Markdown. See the [Formatting guide](formatting-guide.md) for examples of tables, code blocks, admonitions, math, and more.

## What belongs here

We curate resources that are:

- **Relevant** to the 2026 DRC Ebola Bundibugyo outbreak response
- **Publicly accessible** (or with a clear access path)
- **Actionable** — dashboards, datasets, tools, reports, and packages that responders and researchers can use

## Sections

| Section | What goes here |
|---|---|
| Resources and tools | Dashboards, R packages, epidemiological parameter tools |
| Data | Mobility, humanitarian, and epidemiological datasets |
| Emerging evidence | Outbreak size estimates, risk of spread, therapeutics & vaccines |
| Analytical questions | Key analytical questions for the outbreak response |
| Community meeting materials | Seminars, presentations, and meeting recordings |

If a resource doesn't fit an existing section, mention that in your issue or PR — we can create new sections as the response evolves.
