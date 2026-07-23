# Formatting guide

This page shows what's available when writing resource pages. Everything below is valid MyST Markdown and renders on the site.

---

## Standard metadata header

Every resource page starts with this:

```markdown
# Resource Title

Type · **Organisation** · Authors · Date

Description text.

[Visit resource](https://...)
```

---

## Text formatting

**Bold text**, *italic text*, and `inline code`.

---

## Links

- External: [WHO Collaboratory](https://github.com/WHO-Collaboratory)
- Internal cross-reference: [Contributing](contributing.md)

---

## Lists

Bullet list:

- First item
- Second item
  - Nested item

Numbered list:

1. First step
2. Second step
3. Third step

---

## Tables

| Parameter | Estimate | Source |
|---|---|---|
| Incubation period | 2–21 days | WHO |
| Case fatality rate | 25–34% | McCabe et al. |
| Serial interval | 15.3 days | Epiparameter |

---

## Code blocks

R example with syntax highlighting:

```r
library(epiparameter)
ebola_params <- epiparameter_db(disease = "ebola")
plot(ebola_params)
```

Python example:

```python
import pandas as pd
df = pd.read_csv("outbreak_data.csv")
df.groupby("health_zone")["cases"].sum()
```

---

## Admonitions

:::{note}
Use notes for general information or context.
:::

:::{tip}
Use tips for practical advice — e.g. how to access a dataset or interpret a dashboard.
:::

:::{warning}
Use warnings for caveats — e.g. preliminary data, known limitations, or access restrictions.
:::

:::{important}
Use important for critical context that readers should not miss.
:::

---

## Images

```markdown
![Alt text](path/to/image.png)
```

Images can be placed in an `assets/` directory alongside the resource file or in the top-level `assets/` folder.

---

## Block quotes

> This outbreak represents a significant public health emergency requiring coordinated international response.
>
> — WHO Situation Report, June 2026

---

## Math

Inline math: $R_0 = 1.8$

Display math:

$$
R_t = R_0 \cdot S(t) / N
$$

---

## Footnotes

The case fatality rate varies by setting[^1].

[^1]: See McCabe et al. (2026) for a detailed breakdown by health zone.

---

## Horizontal rules

Use `---` to separate sections visually, as shown throughout this page.
