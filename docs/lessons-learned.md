# Operational lessons

## Evidence must sit outside the answer

A file-read transcript can be fabricated without any tool call. Conversely, real tool access can be followed by a false completion summary. Check session tool records, input/output content, and artifact existence separately. The earlier same-day successes and failures both support this lesson.

## Evaluate the contract actually needed

MiMo's arithmetic response contained the right number but violated an integer-only contract. Its JSON values were correct inside an unwanted Markdown fence. Qwen passed the JSON criterion but produced the wrong arithmetic result. Preserve these distinctions and use parsers, tests, or independent checks before treating generated output as machine data.

## Runtime settings are not capability guarantees

Both local aliases allocated a 65,536-token runner. That does not establish full-context reasoning quality. A listed model can also be unavailable: the reachable llama-swap API advertised entries whose configured payloads were absent. Inspect actual files and loaded runtime state before making deployment claims.

## Profiles change the source of truth

Root/default selects Qwen; the active primary profile selects MiMo. Root Telegram is disabled while the named profile's adapter reports connected. Documentation that ignores profile scope can misdiagnose a working adapter or misstate the deployed model.

## Time limits depend on their enforcement path

One recorded worker ran for 340 seconds against a 240-second setting when dispatcher ticks were absent. A foreground maintenance loop reduces that gap but has not established a strict current deadline. Keep automatic work disabled until the enforcement and cleanup path is deliberately tested.

## Hardware choices need measured boundaries

The 8 GB-class GPU supports the tested local workloads, with offloading/allocation tradeoffs. Use one heavy workload at a time, observe residency, and unload only the exact idle model involved. The measured short responses and allocations apply to these cases; they do not prove comfortable concurrent operation or a broad performance ranking.

## Operational documents can become stale

Old switching scripts referenced an absent alias, and manuals named earlier roles and source revisions. Keep dated evidence, report conflicts, and resolve live authority before execution. The retrieval system's freshness checks help exclude changed files, but even an unchanged document can describe historical operational facts.

## Practical troubleshooting order

1. Check current process/service state and the named profile rather than only root settings.
2. Confirm actual model inventory and file availability before selecting catalog entries.
3. Inspect recorded tool calls and output artifacts before accepting a task summary.
4. For retrieval, check source freshness, index digest, and the labeled fallback mode.
5. For a stuck task, inspect its owned run/process state and use bounded maintenance rather than terminating unrelated processes.

This case-study pass verified and documented these boundaries. It did not repair stale scripts, modify the live environment, enable automatic dispatch, or publish private operational data.
