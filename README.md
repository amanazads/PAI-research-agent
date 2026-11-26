# Research Agent

A Python CLI that plans web research, selects and reads sources, and produces a structured answer with citations. Gemini handles planning, source selection, and synthesis. Tavily provides web search and page extraction.

## Setup

Install Python 3.12. From the project root, run:

```zsh
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install -r requirements.txt
```

Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey) and a Tavily API key in the [Tavily dashboard](https://app.tavily.com/home). In zsh, use these hidden prompts to load the keys for the current terminal session:

```zsh
read -rs 'GEMINI_API_KEY?Paste your Gemini API key: '
export GEMINI_API_KEY
printf '\n'

read -rs 'TAVILY_API_KEY?Paste your Tavily API key: '
export TAVILY_API_KEY
printf '\n'
```

## Run

```zsh
question="Compare three open-source vector databases for a RAG startup"
python -m research_agent "$question"
```

The CLI prints the plan, searches, selected sources, and fetch outcomes. The final report includes the question, short answer, key findings, sources, confidence, limitations, and suggested next steps.

## Demonstrate page-fetch failures

```zsh
python -m research_agent --demo first-timeout "$question"
python -m research_agent --demo no-pages "$question"
```

Both modes use live planning and search. `first-timeout` simulates a timeout on the first selected page and continues with the remaining pages. `no-pages` simulates timeouts on all selected pages and returns a low-confidence response with empty findings and sources.

## Architecture

```text
Question → Plan → Search → Select sources → Read pages → Synthesize → Validate citations
```

| File | Responsibility |
| --- | --- |
| `research_agent/__main__.py` | Parses arguments and prints the trace and answer. |
| `research_agent/workflow.py` | Coordinates planning, source selection, retrieval, synthesis, and citation checks. |
| `research_agent/tools.py` | Implements `search_web()` for finding candidates and `read_page()` for extracting page text. |
| `research_agent/schemas.py` | Defines and validates the plan, source selection, evidence, and answer. |

The agentic approach lets the model choose research queries and sources based on each question. Python bounds the execution to three search queries and four selected pages. Selection uses IDs from actual search results. A page receives a citation ID only after a successful read, and the workflow rejects unknown citation IDs in the final findings.

## Reliability and tradeoffs

- **Partial results.** Research requests have timeouts. The workflow records search or page-read failures and continues where possible. With no usable page text, it returns low confidence and an empty source list.
- **Input and output checks.** The workflow checks tool response shapes and uses Pydantic to validate model output. The synthesis prompt tells the model to treat retrieved text as evidence and ignore instructions embedded in it. The synthesis call has no research tools.
- **Latency and evidence coverage.** Bounding searches, reads, and page text keeps the amount of work predictable. Sequential calls add latency, and truncation can remove relevant context.
- **Confidence and citations.** The model assigns confidence and can overstate it when evidence is weak. Citation validation confirms that the page was read. The evaluation spot-checks whether specific passages support the claims.
- **Production improvements.** Add bounded retries for transient failures, retrieve more relevant excerpts, and verify claims against cited passages. Monitor latency by stage, tool error rates, empty-evidence runs, invalid citations, and cost per completed run.

## Evaluation and samples

[EVALUATION.md](EVALUATION.md) documents five distinct research queries, two simulated failure cases, and citation spot checks.

- [Normal run](samples/normal.txt)
- [First page timeout](samples/first-timeout.txt)
- [No usable pages](samples/no-pages.txt)