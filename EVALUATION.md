# Research Agent Evaluation

I ran five distinct research questions and two simulated page-fetch failure cases. I reviewed the search and fetch traces, the answer structure, and the reported limitations. I also spot-checked three claims against their cited sources and verified that the simulated timeout URL was excluded from the final source list.

## Research queries

| Query | Expected behavior | Observed result | Status |
| --- | --- | --- | --- |
| Compare three open-source vector databases for a RAG startup | Compare three relevant options and cite evidence for the tradeoffs. | The agent read three pages and compared Chroma, Qdrant, and Milvus. It reported high confidence. The cited sources support considering Milvus at 100M+ vectors as a rule of thumb, but the cited passages do not establish a benchmark-backed threshold. | Partial |
| Compare ways to add memory to an AI customer support agent | Adapt the search plan and compare relevant memory approaches. | The agent compared framework memory features and knowledge graphs. It read two pages, disclosed a failed fetch, and noted the lack of deployment-specific performance evidence. | Passed for topic adaptation and failure disclosure |
| What's the best database for my startup? | State workload assumptions or explain what information is needed to make a recommendation. | The agent focused on web-based SaaS and acknowledged that analytics and time-series workloads may need different options. It still recommended Supabase with high confidence despite missing workload details. | Partial |
| When should a help center use keyword search, semantic search, or both? | Explain when to use each approach and cite a relevant example. | The agent read four pages and cited three. It recommended keyword search for identifiers, semantic search for natural-language queries, and hybrid search when both matter. The cited Redis article supports the hybrid search recommendation for help centers. The answer acknowledged the lack of implementation-specific performance metrics. | Passed for the comparison and the spot-checked claim |
| Compare single-agent and multi-agent architectures for customer support automation. | Explain the tradeoffs and when added coordination is justified. | The agent read three pages and disclosed one failed fetch. It distinguished narrow support tasks from requests spanning multiple domains. It reported high confidence and repeated a 73% to 94% accuracy increase. The cited guide reports the figure, but the underlying evaluation could not be verified. | Partial |

## Simulated failure cases

Both cases used the vector database comparison question.

| Case | Expected behavior | Observed result | Status |
| --- | --- | --- | --- |
| First selected page times out | Report the failure, continue reading other pages, and exclude the failed page from citations. | The CLI logged one simulated timeout, read three other pages, and included the failed URL under Limitations. The final Sources section contained two successfully read pages and excluded the failed URL. | Passed |
| Every selected page times out | Return a structured response with low confidence, no findings, and no sources. | All four selected reads were simulated failures. The CLI printed low confidence, no verified findings, and no cited sources. | Passed |

## Citation spot checks

| Claim or check | Source passage or evidence | Result |
| --- | --- | --- |
| Milvus is a fit for workloads with 100M+ vectors. | The **TL;DR** table in the [Rework comparison, S1](https://resources.rework.com/tools/ai-data-infra/chroma-vs-qdrant-vs-milvus) lists 100M+ vectors as a best-fit range. **How to Choose Between Them** in the [Ganglani comparison, S3](https://www.kunalganglani.com/blog/milvus-vs-qdrant) recommends considering Milvus at that scale or for multi-tenant workloads. | Supported as a rule of thumb. A benchmark-backed cutoff was not established by the cited passages. |
| Hybrid search helps when support queries mix exact identifiers and natural language. | The **Customer support & knowledge bases** section in the [Redis article, S4](https://redis.io/blog/hybrid-search-explained/#customer-support-knowledge-bases) explains how hybrid search can match an exact error code and surface troubleshooting guides that describe similar symptoms in different terms. | Supported for the stated use case. |
| A financial-services multi-agent system increased accuracy from 73% to 94%. | The introduction of the [Marín guide, S2](https://www.ginomarin.com/articles/single-vs-multi-agent-ai) reports this result for an unnamed company. It describes a multi-domain support scenario but does not provide a sample size, define accuracy, or link to the original evaluation. A search for the figures and scenario did not locate a matching original study. | Figure confirmed in the cited guide. Original evaluation and accuracy metric unverified. |
| The timed-out page was excluded from the final sources. | The failed AIMultiple URL appeared in the fetch trace and limitations in `samples/first-timeout.txt`. The final Sources section contained only the Rework and Ganglani pages. | Passed |

## What worked well

- Search plans adapted to the topic.
- The workflow continued after failed reads and carried those failures into the answer's limitations.
- The no-evidence run returned the same answer structure with low confidence and empty findings and sources.

## What needs improvement

- **Confidence calibration.** The model reported high confidence for an ambiguous question with missing workload details. Recommendations should be conditional when the answer depends on unknown requirements.
- **Quantitative claims.** The agent repeated an accuracy figure without its evaluation setup. Require enough context to interpret quantitative claims, including the workload, baseline, and metric.
- **Evidence coverage.** Some pages yielded no usable text, and page text is capped before synthesis. Selecting excerpts relevant to each claim could improve coverage.
- **Citation verification.** The workflow checks that cited IDs map to pages it read successfully. The manual checks above cover selected claims. Automated claim-level verification is future work.

## Saved outputs

- [Normal run](samples/normal.txt)
- [First page timeout](samples/first-timeout.txt)
- [No usable pages](samples/no-pages.txt)