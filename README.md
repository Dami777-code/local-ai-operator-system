# Local AI Operator System

A case study of running local models, retrieving cited documents, and supervising agent tasks on a consumer laptop.

I configured a Windows environment around Hermes Agent and Ollama to test useful workflows under an 8 GB GPU constraint. The central question was whether an agent's answer matched its recorded tool calls and actual output files.

**Status:** experimental, supervised operation. The published September 29, 2026 snapshot records working mechanisms alongside failures; it does not establish unattended reliability. Hermes, the runtimes, and the models are third-party projects.

## At a glance

- **Model evaluation:** fixed synthetic prompts with explicit pass/fail checks and preserved first outputs.
- **Hermes / Ollama operation:** separate task profiles and inspection of loaded models and runtime settings.
- **Retrieval and provenance:** selected sources, line/hash citations, stale-source exclusion, and a labeled keyword fallback.
- **Supervised agent work:** recorded tool calls and independent output checks, including false completion reports.
- **Consumer hardware:** one heavy model workload at a time, with loading time and memory allocation recorded separately.

Start with the [evaluation method](docs/evaluation.md), inspect the [Python probe](evaluation/model_smoke.py), or read its [saved outputs](evaluation/observations.json). The probe requires a local Ollama service and suitable installed models; its exact prompts are public.

## What the checks found

Four synthetic cases were run once per model, with temperature zero and no repair of failed output.

| Criterion | MiMo | Qwen |
|---|---|---|
| Exact instruction | Pass | Pass |
| Strict JSON, no Markdown | **Fail:** fenced JSON | Pass |
| Only the integer for `18 - 7 + 4` | **Fail:** correct number with extra text | **Fail:** returned `6` |
| Native tool name and exact argument | Pass | Pass |

Tool selection tests do not execute the tool, and these small probes are not a general model ranking.

The retrieval account records source-line/hash checks, changed-source exclusion, reindexing, and a simulated embedding outage. It also reports 15 retrieval regression tests and 100 structured-work adapter tests against synthetic fixtures. Those private subsystem implementations are not included here; the public model probe is independently runnable.

Agent task records were mixed: one task produced a checked file, one fabricated a read without tool calls, and another read its input but claimed an output that did not exist. A worker also exceeded its configured time limit without dispatcher maintenance. Automatic dispatch remains disabled in the documented setup.

## Scope and limitations

The snapshot covers local inference, configured profiles, and synthetic retrieval/adapter checks. Current-model retrieval answers, Telegram round trips, reliable handoffs, strict worker deadlines, and unattended operation remain unvalidated. A connected adapter or configured role is not proof of a completed workflow.

This repository publishes documentation and synthetic probes. Runtime configuration, private source, conversations, and user data are excluded.

## Technical detail

- [Architecture, profiles, models, and hardware](docs/architecture.md)
- [Evaluation method, results, and reproduction](docs/evaluation.md)
- [Workflow contracts and observed outcomes](docs/workflows.md)
- [Operational lessons and troubleshooting](docs/lessons-learned.md)
