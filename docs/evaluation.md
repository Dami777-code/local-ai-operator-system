# Evaluation: criteria before confidence

Verified September 29, 2026. This page separates fresh provider tests, fresh subsystem checks, and reviewed earlier agent evidence.

## Fresh provider probes

Run conditions: Ollama 0.34.4; actual installed MiMo and Qwen aliases; sequential loading; temperature 0; `think: false`; requested and observed context allocation 65,536; maximum output 180 tokens; one trial per case. No JSON schema or format mode forced compliance, so the JSON case measures prompt-following rather than constrained decoding.

| Case | Exact criterion | MiMo result | Qwen result |
|---|---|---|---|
| Instruction | Only `ACK_PORTFOLIO` | Pass; 15.783 s | Pass; 15.237 s |
| Structured output | Parseable JSON with exactly ticket/status/owner values | Fail: Markdown fence; 6.569 s | Pass; 5.652 s |
| Arithmetic | Only `15` for 18 tasks minus 7 completed plus 4 new | Fail format: `18 - 7 + 4 = 15`; 5.224 s | Fail correctness: `6`; 4.546 s |
| Native tool selection | One `lookup_ticket` call with `ticket_id: T-29` | Pass; 6.326 s | Pass; 6.185 s |

The first request for each model includes 10.602/10.346 seconds loading. Subsequent load durations were below 0.01 seconds. Output lengths differ, and these single-trial measurements do not justify ranking models by general speed or reliability. Correct arithmetic with extra prose and incorrect arithmetic are different failures.

The tool is a synthetic definition only. No executor is invoked, so this tests native selection/arguments, not task completion or use of a returned result. Allocating a 64K runner does not test meaningful behavior over 64K input. Earlier same-day documentation reports a 10,241-input-token fact-retrieval case, but its timing was confounded by overlapping work and is not included as a comparison here.

The exact prompts and synthetic outputs are in [observations.json](../evaluation/observations.json). The standalone [probe script](../evaluation/model_smoke.py) uses Python's standard library and never calls agent tools, memory, external messaging, or private documents.

```sh
python evaluation/model_smoke.py --models local-ai-mimo:9b-64k local-ai-usagi:9b-64k --output observations-local.json
```

This command needs the installed aliases and a local Ollama service. Change the model arguments for another environment. It loads models sequentially and unloads each afterward; run only when those models are idle. It preserves first failures without repair or retries. A rerun may differ despite temperature zero.

## Fresh retrieval verification

The installed private retrieval subsystem passed 15 existing regression tests on disposable fixtures with mocked embeddings. Covered behavior includes allowlist exclusions, embedded-secret/binary rejection, source provenance, incremental indexing, failed-index preservation, revocation, digest drift, fallback consistency, writer locking, passage limits, changed-source exclusion, and turn-scoped citation guards.

A separate fresh test used the actual local embedding runtime and a disposable two-line synthetic ticket document. It verified:

1. Real embedding plus hybrid search returned the expected value and matching source hash/line range.
2. Editing the document excluded stale results before reindexing.
3. Reindexing exposed the new value.
4. Simulating an embedding-request outage produced explicitly labeled keyword-only degraded results.

The private canonical index was inspected read-only: integrity `ok`, matching embedding digest, 284 chunks, six fresh sources and one changed/missing/revoked source. It was not reindexed or copied. See [sanitized retrieval observations](../evaluation/retrieval-observations.json).

These fresh checks validate the retrieval mechanism. They do not validate today's MiMo-to-Hermes-to-retrieval answer loop; the older complete answer scenarios used Qwen. Citation range correctness also does not prove semantic correctness.

## Fresh structured-work boundary tests

100 existing synthetic tests passed across the installed adapter checkout's reader plugin, writer plugin, mutation service, and Google writer. Source inspection confirmed later-message confirmation, identity binding, request/source hash checks, one-use handling, and configured 120-second expiry.

No private Sheet request or Telegram mutation was run. These are source/test evidence, not a claim that a live end-to-end work-management integration passed. The private implementation and tests are excluded from this repository.

## Reviewed earlier same-day Hermes evidence

| Scenario | Evidence inspected | Result and limitation |
|---|---|---|
| Coder file question | Known synthetic session metadata: zero tools, one API call; prior report compares answer with fixture | Fabricated file read. A convincing transcript did not establish execution. |
| Manually dispatched worker file task | 16 tools, 17 API calls; saved synthetic JSON independently parses with expected values | Tool-backed success, but 340 s against an intended 240 s limit without supervisory ticks. |
| Later supervised task | Three tools, five API calls; prior report records successful read and nonexistent claimed output | File access succeeded; completion summary was false. `done` was insufficient evidence. |
| Bonsai short review | Model files currently present; earlier same-day report records local server results | Found a defect but proposed a correction that failed its own example. Not rerun in this pass. |

Only known synthetic task metadata and artifacts were inspected. Personal conversations were not read or published. Private raw session logs are not included, so this lane is clearly a reviewed operational account rather than publicly reproducible evidence. The public provider probes are directly reproducible.

## Remaining evaluation gaps

The next checks should target a fresh current-model retrieval answer, an inbound Telegram round trip with synthetic content, and a bounded over-limit worker test. Broader coding, independent reviewer reliability, role handoffs, memory recall, browser control, sustained usage, and full-context reasoning remain unestablished. No aggregate score, customer metric, productivity estimate, or production reliability claim is made.
