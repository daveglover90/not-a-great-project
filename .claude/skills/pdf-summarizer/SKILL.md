---
name: pdf-summarizer
description: Extract and summarize the text of a PDF the user points to. Use when the user wants a quick summary or the key points of a PDF document.
---

# PDF Summarizer

A well-behaved example skill, included so Agent Scan has a clean skill to contrast
against the deliberately risky one.

## Steps

1. Read the PDF text with a local extractor (e.g. `pdfplumber` or `pypdf`).
2. Chunk the text if it is longer than the model context window.
3. Produce a 5-bullet summary plus a one-line TL;DR.
4. Never send the PDF contents to any host other than the configured model provider.

## References

- `references/prompt.md` holds the summarization prompt template.
