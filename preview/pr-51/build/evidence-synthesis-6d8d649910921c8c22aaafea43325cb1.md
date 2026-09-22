# Evidence Synthesis

Syntheses of the current BVD evidence base, alongside a live tracker of relevant literature and resources.

:::{important} Beta
This page is in beta and still a work in progress. Please direct feedback to [Collaboratory@who.int](mailto:Collaboratory@who.int). This page is subject to the [disclaimer](#evidence-synthesis-page-bottom) below.
:::

## Synthesized analyses

Curated syntheses organized by question. Each page sets out the underlying analyses, how they compare, and where knowledge gaps persist.

```{tableofcontents}
:context: children
```

This site is maintained by the Ebola Outbreak Analytics Community of Practice (CoP) within the [Collaboratory](https://www.who.int/initiatives/collaboratory).

Pages are updated within one working day of new or revised analyses appearing. Verify figures and interpretations against the referenced analyses before use in operational decisions.

## Methods

These pages are produced by a semi-automated evidence-synthesis pipeline that pairs AI models with human review at each major checkpoint: one model reads each source analysis on its own and grounds every extracted claim in a verbatim quoted passage; a second model takes the resulting structured comparison as input, and drafts the narrative. Human analysts then review and edit the output to ensure accuracy and completeness prior to publishing.

**Identifying analyses.** Analyses are identified through continuous monitoring of preprint servers, peer-reviewed publications, and grey literature. An analysis is included if it directly addresses the 2026 Bundibugyo virus disease (BVD) outbreak and provides a quantitative estimate relevant to a given topic (e.g., outbreak size, risk of spread). Each included source is logged, and if the authors later release an updated version, the newer version supersedes the earlier one.

**Preparing the source text.** Each source text, regardless of source type (e.g., PDF, HTML), is converted to Markdown. A human analyst then curates the converted file and removes sections that carry no evidentiary content, such as references, acknowledgments, author contributions, affiliations, and declarations of interest, to keep extraction focused and reduce the number of input tokens used.

**Extracting structured evidence.** The curated text is split into individually citeable units, one per sentence, and passed to Claude Sonnet 4.6. For each of a fixed set of dimensions (e.g., estimates, methods, limitations), the model answers from that one source alone and must ground every factual claim in a verbatim span of its text.

**Synthesizing the narrative.** OpenAI's GPT-5.5 model reads the dimensions extracted for each analysis and synthesizes the information, covering the state of the evidence, how the estimates compare and why they diverge, the key uncertainties and assumptions shared across analyses, what would most reduce that uncertainty, and what it implies for the response.

**Human review and publication.** Human analysts edit the draft for accuracy, completeness, and tone prior to publishing.

**Limitations.** This pipeline surfaces only publicly available analyses; works that have not been made public are not captured.

## Evidence tracker

A live list of BVD literature and resources for modelers, epidemiologists, public health analysts, and others supporting the response. Peer-reviewed publications, preprints, GitHub repositories, datasets, and tools are captured. Refreshed twice per day.

:::{seealso} Access the live list
[Bundibugyo Ebolavirus Disease Literature](https://docs.google.com/spreadsheets/d/1ryymcAzIfZnQL3H79H2bJBdnIzRTHIFUnyt-6zkC4_U/edit?gid=118635632#gid=118635632)
:::

Records are pulled from the WHO [Epidemic Intelligence from Open Sources (EIOS)](https://www.who.int/initiatives/eios) platform, which aggregates content from bioRxiv, Crossref, DataCite, Europe PMC, medRxiv, OpenAlex, PubMed, Semantic Scholar, and other feeds. Direct community submissions are also included.

Spot something missing? Add it to the [`Community_Submissions`](https://docs.google.com/spreadsheets/d/1ryymcAzIfZnQL3H79H2bJBdnIzRTHIFUnyt-6zkC4_U/edit?usp=sharing) tab, or email <collaboratory@who.int> with additions, corrections, or gaps.

:::{div}
:name: evidence-synthesis-page-bottom
:::
