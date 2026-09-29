# Workflow contracts and observed outcomes

These examples use synthetic data. They describe tested mechanisms and supervised practice; they do not authorize unattended execution.

## 1. Compare models on the same criteria

**Input:** one fixed set of exact-instruction, strict-JSON, arithmetic, and native-tool prompts.

Run one installed alias at a time. Keep sampling, context request, and output cap fixed. Save each first output, validate it without repairing it, inspect loaded context, and unload after testing. Keep model loading time separate from warm-response observations.

**Observed:** both aliases complied with the marker and selected the native tool. MiMo fenced its JSON and added prose to the integer-only task. Qwen emitted valid JSON but failed the arithmetic. A useful model-selection decision requires the task's actual criterion, rather than a generic impression of fluency.

The published harness covers this workflow and contains no private data.

## 2. Retrieve bounded evidence

**Input:** an operator-reviewed document allowlist and a query. In the fresh synthetic scenario, a ticket starts `READY`, then changes to `HOLD`.

The operator owns indexing. Search combines local embeddings and keywords, returns bounded passages with line ranges and hashes, and checks current source freshness. After a change, old results are excluded until successful reindexing. If embedding requests fail, keyword results are explicitly labeled degraded.

**Observed:** the disposable live-embedding scenario passed provenance checks, excluded the stale value, returned the reindexed value, and labeled the simulated outage fallback. The current private corpus also excludes one non-fresh source.

**Boundary:** retrieved documents may describe past operational state. They cannot establish today's repository commit, service health, or remote work records. Citation checks constrain source ranges but do not make every model conclusion correct. Current MiMo-mediated answers remain a separate test gap.

## 3. Supervise one file-processing task

**Input:** a synthetic text fixture, an exact workspace and output contract, and one manually selected Kanban task.

Keep automatic dispatch off. Require recorded reads/writes, parse the resulting JSON independently, compare values with the original input, and verify that source content was preserved. Maintain foreground dispatcher ticks when enforcing time limits; inspect the actual task/process state.

**Observed earlier on the same date:** one worker produced a valid synthetic JSON output through real calls. It needed recovery from blocked commands and path errors and exceeded its intended time limit without ticks. A later task read the fixture through real tools but falsely claimed an output file. These outcomes make independent artifact verification part of the workflow.

**Boundary:** a native task's completion status, a model summary, or a path in an event does not prove correctness or copied attachments. The foreground supervisor is best-effort; a current hard-timeout test is still needed.

## Interfaces and proposed structured work

The named Telegram adapter is connected and Desktop is installed. A fresh inbound Telegram exchange and current Desktop task were not run here, so they are not presented as a fourth completed workflow.

Shisa adapters are registered and have tested confirmation boundaries. Their synthetic tests do not establish current live remote reads/writes. n8n and an Operator Hub UI-to-agent workflow are not verified and are omitted from the completed workflows.
