
# Contributing

This resource list is maintained by the Ebola Community of Practice. Contributions are welcome from anyone working on the 2026 DRC Ebola Bundibugyo response.

## How to suggest a resource

**No coding required.** Open a GitHub Issue using our structured form:

[Suggest a Resource](https://github.com/bafnaprincy/ebola-resources/issues/new?template=new-resource.yml){ .md-button .md-button--primary }

Fill in the fields — title, URL, type, section, and a short description. A maintainer will review and add it to the site.

## What belongs here

We curate resources that are:

- **Relevant** to the 2026 DRC Ebola Bundibugyo outbreak response
- **Publicly accessible** (or with a clear access path)
- **Actionable** — dashboards, datasets, tools, reports, and packages that responders and researchers can use

## Sections

| Section | What goes here |
|---|---|
| Dashboards | Live epi dashboards and situation trackers |
| Epi Parameters | Parameter databases, R packages, systematic reviews |
| Outbreak Size Estimates | Modelling reports on outbreak scale |
| Risk of Spread | Domestic and international spread risk assessments |
| Mobility Data | Population movement and mobility datasets |
| Humanitarian Data | Conflict, displacement, infrastructure datasets |
| Therapeutics & Vaccines | Vaccine and therapeutics guidance, trial data |

If a resource doesn't fit an existing section, mention that in the issue — we can create new sections as the response evolves.

## For maintainers

Resources are stored as YAML in the `data/` directory, one file per section. To add a resource from an approved issue, add an entry to the appropriate `data/<section>.yml` file:

```yaml
- title: "Resource Title"
  url: "https://..."
  type: dashboard  # dashboard | report | tool | dataset | package
  authors: "Name, Name"
  organisation: "Org"
  date_added: 2026-06-05
  description: >-
    A short description of the resource.
```

New sections require adding a `data/<section>.yml` file, a `docs/<section>.md` page, and updating the `nav:` in `mkdocs.yml`.
