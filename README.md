# Ebola Outbreak Analytics CoP Resources

A curated, community-maintained collection of resources supporting the response to the 2026 DRC Ebola Bundibugyo virus disease outbreak. Maintained by the **Ebola Outbreak Analytics CoP** within the [WHO Collaboratory](https://collaboratory.who.int/).

**Live site:** https://who-collaboratory.github.io/ebola-resources/

## What's here

| Section | What's covered |
|---|---|
| Resources and tools | Dashboards, R packages, epidemiological parameter tools |
| Data | Mobility, humanitarian, and epidemiological datasets |
| Emerging evidence | Outbreak size estimates, risk of spread, therapeutics & vaccines |
| Analytical questions | Key analytical questions for the outbreak response |
| Community meeting materials | Seminars, presentations, and meeting recordings |

## Contributing

The easiest way to add a resource is to [open an issue](https://github.com/WHO-Collaboratory/ebola-resources/issues/new?template=new-resource.yml) using the structured form — no coding needed. A GitHub Action will generate a draft page and open a PR.

You can also open a PR directly. See the [Contributing guide](https://who-collaboratory.github.io/ebola-resources/contributing) for details.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter-book start
```

The site runs at `http://localhost:3000/`.

## Deployment

The site deploys to GitHub Pages automatically on push to `main`. A CI check validates `myst.yml` and builds the site before deploying.
