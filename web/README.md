# MiniHouse · Web & OpenRouter Free SDK Integration

This directory houses the interactive web client and agent harness for the **MiniHouse (6 × 3 m Steel + Reclaimed Wood)** project, adapted from `deepseek-ai/chat-demo` and `deepseek-ai/deepseek-harness` to run exclusively on **OpenRouter's Free API (`openrouter/free` and `:free` models)** via the official **`@openrouter/sdk`**.

## Packages

| Path | Upstream Base | Adaptation Summary |
| --- | --- | --- |
| [`web/chat-demo/`](chat-demo/README.md) | [`deepseek-ai/chat-demo`](https://github.com/deepseek-ai/chat-demo) | Replaces `api.deepseek.com` with `@openrouter/sdk` (`src/services/api/openrouter-client.ts`), enforces zero-cost model guardrails (`openrouter/free`, `deepseek/deepseek-r1:free`, `deepseek/deepseek-chat-v3-0324:free`), adds a live free-model picker in Settings, uses browser-native Web Speech TTS, and injects MiniHouse traceability rules (`[CONCEPTUAL]` / `[CALCULADO]` / `[ENSAYADO]` / `[LIBERADO]`). |
| [`web/deepseek-harness/packages/llm/llm-openrouter-free/`](deepseek-harness/packages/llm/llm-openrouter-free/src/index.ts) | [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) | Custom Cordis LLM plugin (`@minihouse/dsh-llm-openrouter-free`) using `@openrouter/sdk` with live zero-cost model discovery (`pricing.prompt == "0" && pricing.completion == "0"`) and MiniHouse rule injection. |
| [`web/deepseek-harness/profiles/minihouse-openrouter.yaml`](deepseek-harness/profiles/minihouse-openrouter.yaml) | `dsh` profile | Disables paid `@deepseek-ai/dsh-llm-deepseek` and mounts `.agents/skills/minihouse-*` and `.agents/agents/*` with `@minihouse/dsh-llm-openrouter-free`. |

## Quick Start

### 1. Run the MiniHouse Chat Web App (`web/chat-demo`)
```powershell
Set-Location .\web\chat-demo
pnpm install
pnpm dev
```
Open `http://localhost:8090`, enter your free **OpenRouter API Key** (`sk-or-v1-...` from [openrouter.ai/settings/keys](https://openrouter.ai/settings/keys)), and select any `:free` model or `openrouter/free` in **Settings → General**.

### 2. Run Tests & Production Build
```powershell
Set-Location .\web\chat-demo
pnpm test
pnpm build

Set-Location ..\deepseek-harness\packages\llm\llm-openrouter-free
pnpm test
pnpm build
```
