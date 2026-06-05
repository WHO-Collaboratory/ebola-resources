# Contributing

This resource list is maintained by the Ebola Community of Practice. Contributions are welcome from anyone working on the 2026 DRC Ebola Bundibugyo response.

## Ways to contribute

There are three ways to add to this site, depending on your comfort level:

### 1. Submit an issue (no coding needed)

The easiest path. Open a GitHub Issue using our structured form:

[Suggest a Resource](https://github.com/bafnaprincy/ebola-resources/issues/new?template=new-resource.yml){ .md-button .md-button--primary }

Fill in the fields — title, URL, type, section, and a short description. A GitHub Action will automatically create a Pull Request from your issue. A maintainer reviews and merges it. Your resource appears on the site within minutes.

### 2. Edit a section page directly (Markdown)

Each section page (e.g. `docs/dashboards.md`) has a **Community Notes** section at the bottom. You can add narrative context, caveats, related links, or anything that doesn't fit the structured resource format.

1. Click the edit icon (:material-pencil:) on any page
2. Add your content under **Community Notes**
3. Open a Pull Request

This is a good option for adding context like "this dataset pairs well with X" or "requires institutional access."

### 3. Edit the data file directly (YAML)

For technical contributors comfortable with YAML, you can add a resource entry directly to `data/resources.yml`:

```yaml
- title: "Resource Title"
  url: "https://..."
  type: dashboard
  section: dashboards
  authors: "Name, Name"
  organisation: "Org"
  date_added: 2026-06-05
  description: >-
    A short description of the resource.
```

Open a Pull Request with your change. See [field reference](#field-reference) below.

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

If a resource doesn't fit an existing section, mention that in your issue or PR — we can create new sections as the response evolves.

## Field reference

| Field | Required | Values |
|---|---|---|
| `title` | Yes | Display name of the resource |
| `url` | Yes | Link to the resource |
| `type` | Yes | `dashboard`, `report`, `tool`, `dataset`, or `package` |
| `section` | Yes | Section slug (e.g. `dashboards`, `epi-parameters`, `mobility-data`) |
| `authors` | No | Comma-separated author names |
| `organisation` | No | Publishing organisation |
| `date_added` | Yes | Date in YYYY-MM-DD format |
| `description` | Yes | Brief description (1-3 sentences) |
| `notes` | No | Free-form context — access instructions, caveats, related resources |
