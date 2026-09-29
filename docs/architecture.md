# Architecture and execution boundaries

Snapshot: September 29, 2026. Windows owns the active Hermes/Ollama runtime. WSL holds development checkouts and older operating documentation. The system uses existing Hermes Agent and model runtimes; this case study does not claim authorship of those frameworks or model training.

## Authority and profiles

The root configuration is not sufficient to describe every interface. Root/default selects Qwen, while the installed Desktop selects the named `usagi` profile, which currently selects MiMo. Root Telegram is disabled; the named profile's Telegram adapter reports connected. Ignoring profile scope would produce the wrong account of the live system.

| Profile | Model assignment | Intended surface | Evidence boundary |
|---|---|---|---|
| `usagi` | MiMo | Conversation, memory, triage, Kanban, web, local knowledge, Shisa adapters | Configuration and adapter connectivity; full current interface workflow not retested |
| `worker` | MiMo | One supervised file/terminal task | Earlier same-day tool-backed task and mixed completion evidence |
| `coder` | MiMo | Coding tasks | Failed fabricated read and later successful read documented; unattended use unvalidated |
| `researcher` | MiMo | Research task profile with web tools | Assignment verified; no fresh research scenario |
| `reviewer` | Bonsai 2 | On-demand independent review | Separate model files installed; fresh same-card review not run |
| `operator` | Qwen | Restricted legacy inspection fixture | Gated inspection tools, memory disabled; separate from general workers |

Other profiles are retained comparison/alternate assets. Eleven served profiles do not mean eleven active agents. The gateway reported zero active agents at inspection.

## Retrieval

Local knowledge is an independent Python subsystem registered as two Hermes tools: search and status. It uses local `nomic-embed-text` embeddings, SQLite FTS5 keyword ranking, and sqlite-vec cosine search. The configured embedding path requests CPU execution and unloads after use.

Sources are selected through an operator-owned explicit allowlist. The model cannot select arbitrary files, index/rebuild the corpus, or write memory through these tools. Results carry original line ranges and source hashes. Changed, missing, or revoked sources are excluded until resolved. The current private index had 284 chunks, six fresh sources, and one excluded source at inspection.

Citation hooks reject missing or invented line ranges by substituting actual retrieved excerpts. This checks provenance ranges, not the truth of every sentence. Fresh tests verified the mechanism against synthetic data. The prior end-to-end Hermes retrieval scenarios used Qwen; current `usagi` uses MiMo, so that combination still needs a regression test.

## Structured-work adapters

Installed Shisa read and write plugins invoke a separate local service implementation through a bounded wrapper. The write path binds a preview to request/source hashes, identity, and a short-lived confirmation. It requires an exact confirmation in a later inbound message and tracks used confirmations.

Source inspection and 100 synthetic tests establish these adapter behaviors within their tested scope. They do not establish the current live Sheet state, current remote authorization, or a complete Telegram mutation path. No live private-work read or write was made for this case study. Operator Hub's UI is not established as the live AI control plane, and n8n is not part of the verified architecture.

## Execution and resources

Automatic dispatch, automatic decomposition, and automatic review dispatch are disabled at root. The one-worker caps support supervised use. A maximum runtime is enforced through dispatcher maintenance; a worker may exceed it if no tick runs. A foreground supervisor provides maintenance ticks, but current hard-deadline behavior remains unvalidated.

Tool scopes vary by profile. The primary interface does not expose a general file/terminal toolset; a worker does. This is useful separation, not a comprehensive sandbox or universal approval guarantee. Root's broad CLI tool surface still exists, and its loop guard warns without a hard stop.

The 8 GB-class GPU motivates sequential model loading. Bonsai is a separate on-demand server and was stopped during inspection. llama-swap's API is reachable, but its two advertised models have absent configured payloads; they are excluded from the working model layer.

## Source conflicts retained

- Older WSL documentation predates the current role inventory.
- The Kanban manual names an earlier Hermes source revision than the live gateway.
- Old switching scripts reference an absent model alias.
- Historical timeout-cleanup and retrieval-answer tests do not automatically apply to today's revision/model pairing.

These discrepancies are reported rather than silently treated as reconciled. This publication did not modify the live configuration, upgrade packages, repair scripts, or enable automation.
