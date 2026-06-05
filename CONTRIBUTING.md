# Contributing to Ebola Resources

Thank you for helping build this resource collection for the Ebola Community of Practice.

## Suggesting a resource (no coding needed)

1. Go to [**New Issue → Suggest a Resource**](https://github.com/bafnaprincy/ebola-resources/issues/new?template=new-resource.yml)
2. Fill in the form: title, URL, type, section, and a short description
3. Submit — a maintainer will review and add it to the site

## For maintainers: adding a resource

Resources live as YAML entries in `data/<section>.yml`. Each entry has these fields:

| Field | Required | Description |
|---|---|---|
| `title` | Yes | Display name of the resource |
| `url` | Yes | Link to the resource |
| `type` | Yes | One of: `dashboard`, `report`, `tool`, `dataset`, `package` |
| `authors` | No | Comma-separated author names |
| `organisation` | No | Publishing organisation |
| `date_added` | Yes | Date added in YYYY-MM-DD format |
| `description` | Yes | Brief description (1-3 sentences) |

### Adding to an existing section

Add a new YAML entry to the appropriate `data/<section>.yml` file.

### Creating a new section

1. Create `data/<new-section>.yml` with at least one entry
2. Create `docs/<new-section>.md` using the same Jinja template as other section pages
3. Add the page to `nav:` in `mkdocs.yml`
4. Update the section dropdown in `.github/ISSUE_TEMPLATE/new-resource.yml`

## Local development

```bash
pip install -r requirements.txt
mkdocs serve
```
