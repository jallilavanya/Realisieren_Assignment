# AI Usage

AI assistance was used during development, as explicitly permitted by the assignment.

## Tool

**ChatGPT**

## Uses

- Interpreting the assignment requirements.
- Designing the common data model.
- Suggesting a modular scraper architecture.
- Reviewing pagination and error-handling approaches.
- Designing unit-test cases.
- Improving README structure and documenting assumptions.
- Reviewing duplicate-detection logic and edge cases.

## Representative prompts

1. "Design a medium-level Python web scraping pipeline with separate source scrapers, cleaning, validation, deduplication and CSV/JSON outputs."
2. "Review a duplicate-detection strategy that normalizes whitespace and capitalization without incorrectly merging records from different sources."
3. "Suggest unit tests for a Python scraping data-processing pipeline."
4. "Review error handling so one failed source does not unnecessarily stop the remaining pipeline."

## AI-assisted areas

AI assistance contributed to the initial architecture, code scaffolding, test ideas and documentation.

## Human review

The final implementation should be reviewed and executed by the candidate. In particular, the candidate should verify:

- The current HTML selectors on both practice websites.
- Pagination reaches the final page.
- Output record counts.
- Price and rating parsing.
- Duplicate counts.
- Failure behavior.
- Unit-test results.

## Important verification principle

AI-generated code is not treated as authoritative. Any implementation detail that depends on the live website should be verified by actually running the scraper against the public source.

## Testing performed

The included unit tests cover the processing layer. The full scraping pipeline should be run in a network-enabled environment before submission, and the generated `output/` and `logs/` files should be inspected.
