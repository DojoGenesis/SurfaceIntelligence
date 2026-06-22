---
license: apache-2.0
task_categories:
  - text-classification
  - text-generation
language:
  - en
tags:
  - ai-safety
  - system-prompts
  - behavioral-analysis
  - llm-alignment
  - prompt-engineering
  - competitive-intelligence
pretty_name: Surface Intelligence — AI System Prompt Corpus
size_categories:
  - n<1K
---

# Surface Intelligence — AI System Prompt Corpus

**A 2025–26 study of how AI products are instructed across deployment surfaces.**

Surface Intelligence is a research corpus and analysis platform that collects, normalizes, and compares system prompts from production AI products. The dataset documents how vendors shape model behavior through prompting — revealing product strategy, surface-specific constraints, and behavioral differentiation that is otherwise opaque to researchers and practitioners.

## Dataset Overview

| Attribute | Value |
|-----------|-------|
| Total prompt entries | 71 |
| Unique products | 49 |
| Unique vendors | 35 |
| Deployment surfaces | 6 (ide, web, cli, desktop, api, mobile) |
| Date range | 2024–2026 |
| Primary language | English |
| Repo license | Apache 2.0 |

These counts reflect the corpus as described in the repository README. The `library.json` file is populated by the build pipeline (`build-full-library.py`) against a local `system-prompts-collection` directory; counts should be reverified after any build run.

## Surface Taxonomy

A "surface" is the deployment context where users interact with an AI product. The same underlying model behaves differently depending on the surface.

| Surface | What it covers | Entries |
|---------|---------------|---------|
| `ide` | IDE assistants: Cursor, Copilot variants, Kiro, Zed, Windsurf, Xcode AI, etc. | 38 |
| `web` | Web chatbots and SaaS products: Claude.ai, ChatGPT, Gemini, Linear, etc. | 18 |
| `cli` | Command-line tools: Claude Code, Gemini CLI, Codex CLI, Warp, etc. | 7 |
| `desktop` | Native desktop apps: Claude desktop, Cluely, dia, etc. | 4 |
| `api` | API platform and model-level prompts | 2 |
| `mobile` | iOS and Android AI apps | 2 |

## What Each Entry Contains

Each entry in `library.json` includes:

- `id` — stable slug (`lib-{product}-{surface}-{version}`)
- `product` — product name
- `vendor` — company or organization
- `surface` — one of: ide, web, cli, desktop, api, mobile
- `version` — variant label or date string
- `model` — underlying model at time of collection
- `extractedDate` — date the prompt was captured
- `source` — upstream repository or disclosure source
- `sourceUrl` — URL pointing to the source
- `promptHash` — MD5 prefix for change detection without full text comparison
- `promptText` — full system prompt text
- `analysis` — derived metrics: token count, tool count, tool density, safety score, autonomy score, capability detection (file ops, shell, git, web search, MCP, etc.)
- `createdAt` — ISO timestamp of library entry creation

## Vendor Coverage

The corpus spans vendors across the AI tooling spectrum as of 2025–2026, including (non-exhaustive): Anthropic, Google, OpenAI, GitHub/Microsoft, Anysphere (Cursor), AWS (Kiro), JetBrains (Junie), Apple (Xcode AI), ByteDance (Trae), Augment, Codeium (Windsurf), Vercel (v0), StackBlitz (Bolt.new), Notion, Perplexity, Manus, and various open-source tools (Cline, RooCode, Bolt.new, Gemini CLI, Codex CLI).

Multi-version entries exist for several products (Cursor, Copilot variants, Kiro, Claude Code, Qoder, Traycer, Xcode AI), enabling longitudinal comparison.

## Key Findings

**IDE prompts are 3–5x longer than web prompts.** IDE surfaces require detailed tool descriptions, workspace context, and file operation instructions. Web surfaces optimize for conciseness.

**CLI prompts have the highest density of behavioral constraints.** Command-line tools show the most explicit capability boundaries and limitation disclosures.

**Multi-surface vendors show deliberate differentiation.** A vendor's IDE prompt vs. web prompt reveals what they want users to do vs. what they prevent. Behavioral constraint clusters track by surface, not by model.

**Behavioral constraints cluster by surface, not by underlying model.** GPT-4-powered products on the web surface resemble Claude-powered web products more than they resemble GPT-4-powered IDE products.

## Browser Application

A self-contained browser app is included in the repository (`index.html`). No build step is required — open the file directly or deploy to Cloudflare Workers.

The app provides:
- Full-text search across all prompt entries
- Surface and vendor filters
- Statistical comparisons (prompt length, tool density, behavioral constraint counts)
- Side-by-side diff view

The Cloudflare Workers deployment is configured under the name `surface-intelligence` (see `wrangler.toml`). The canonical GitHub repository is `https://github.com/DojoGenesis/SurfaceIntelligence`.

## Data Sources

Prompts in this corpus were collected from public disclosures, community research repositories, and vendor announcements. Primary upstream sources include:

- `x1xhlol/system-prompts-and-models-of-ai-tools` (GitHub)
- `jujumilk3/leaked-system-prompts` (GitHub)
- Official open-source repositories where vendors publish prompts directly (e.g., `cline/cline`, `stackblitz/bolt.new`, `openai/codex`)

Each entry's `source` and `sourceUrl` fields document the specific upstream origin.

## License and Provenance — READ BEFORE USE

The repository code (build scripts, browser app, analysis tooling) is licensed under **Apache 2.0**.

The **prompt texts themselves carry independent provenance** and are not uniformly covered by the repo license. System prompts vary significantly in their redistribution rights:

- Some were disclosed officially by vendors or published in open-source repositories with permissive licenses.
- Some were extracted by community researchers and shared in aggregator repositories without explicit vendor authorization.
- Some may be subject to confidentiality claims, terms of service restrictions, or copyright assertions by the originating vendor.

**Do not assume the Apache 2.0 repo license extends to the prompt text content.**

---

## Publish Checklist

Complete the following steps in order before publishing this dataset to Hugging Face.

### Step 1 — Per-Prompt License and Provenance Audit

This is the most critical gate. Do not upload until complete.

- [ ] For each of the 71 entries, review the `source` and `sourceUrl` fields.
- [ ] Categorize each entry into one of:
  - **T1 — Vendor-disclosed**: Vendor published the prompt in an official repo, blog post, or documentation. Redistribution is generally permissible under the original license.
  - **T2 — Open-source repo, clear license**: Prompt appears in a community aggregator repo that has a permissive license AND the vendor has not contested disclosure. Document the specific license.
  - **T3 — Community-extracted, contested or unclear**: Prompt was extracted by researchers; vendor has not officially sanctioned sharing. Redistribution risk is present.
  - **T4 — Contested or ToS-restricted**: Vendor has issued DMCA, objected publicly, or ToS prohibits redistribution.
- [ ] Exclude any T4 entries from the upload.
- [ ] For T3 entries, make a documented judgment call per entry. Consider consulting with legal counsel if the corpus will be used commercially.
- [ ] For T2 entries, verify the aggregator repo's own license permits redistribution (not all do).
- [ ] Record the tier decision for each entry in a provenance manifest (e.g., `provenance.csv`) that ships alongside the dataset.

### Step 2 — Rebuild the Library

The current `library.json` on this machine is empty (the build pipeline requires prompt source files from a Mac-side path). Before publishing:

- [ ] Run `python3 build-full-library.py` on the machine that has the `system-prompts-collection` directory (Mac, path: `/Users/alfonsomorales/ZenflowProjects/system-prompts-collection`).
- [ ] Verify entry count matches the README claims (71 prompts, 49 products, 35 vendors).
- [ ] Commit the rebuilt `library.json` and push to `DojoGenesis/SurfaceIntelligence` on GitHub.

### Step 3 — Hugging Face Organization Setup

- [ ] Create or confirm the HF organization: `DojoGenesis` (or `TresPies` — decide which org owns this dataset; DojoGenesis is the GitHub org for this repo).
- [ ] Ensure Cruz Romero Morales (`cruz@trespiesdesign.com`) has Owner or Write access to the HF org.
- [ ] Confirm the dataset repo name: `DojoGenesis/surface-intelligence` (or operator's preferred slug).

### Step 4 — Dataset Card Metadata

- [ ] Confirm the license field in the YAML frontmatter. If any prompt texts have non-Apache provenance that restricts redistribution, the dataset-level license declaration should be downgraded to `other` and a custom license explanation added.
- [ ] Set `size_categories` accurately after the rebuild confirms entry count.
- [ ] Add `doi` if you register the dataset with a DOI provider (optional).

### Step 5 — Upload

```bash
# Install HF CLI if not present
pip install huggingface_hub

# Log in (use a token with write access to the DojoGenesis org)
huggingface-cli login

# Upload from the SurfaceIntelligence repo directory
huggingface-cli upload DojoGenesis/surface-intelligence . \
  --repo-type dataset \
  --commit-message "Initial dataset upload — Surface Intelligence v1"
```

Alternatively, create the dataset repo on HF first and push via git:

```bash
# After creating the HF dataset repo at https://huggingface.co/datasets/DojoGenesis/surface-intelligence
git remote add hf https://huggingface.co/datasets/DojoGenesis/surface-intelligence
git push hf main
```

### Step 6 — Wire the Browser App URL

- [ ] After the Cloudflare Workers deployment is active, update this dataset card's "Browser Application" section with the live URL.
- [ ] Add the live URL to the HF dataset card's "Dataset Card" metadata (`homepage` field in the YAML front matter, or a prominent link in the card body).
- [ ] Confirm `wrangler.toml` points to the correct account and the `surface-intelligence` worker is deployed: `npx wrangler deploy` from the repo root.

### Step 7 — Author Attribution

- [ ] Set the dataset card `authors` field (HF YAML) to `[Cruz Romero Morales]` or the DojoGenesis org, per HF conventions.
- [ ] Add a `citation` block if the dataset will be referenced in papers or cited work.

### Step 8 — Post-Publish Verification

- [ ] Confirm the dataset appears at `https://huggingface.co/datasets/DojoGenesis/surface-intelligence`.
- [ ] Load `library.json` directly from the HF raw URL and verify entry count.
- [ ] Open the HF dataset viewer and confirm the JSON structure is recognized.
- [ ] Verify the `DATASET_CARD.md` renders correctly on the HF dataset page (check the README tab).
- [ ] Share the HF URL in the DojoGenesis GitHub repo README under a "Dataset" section.

---

## Use Cases

- **Competitive intelligence** — compare system prompt strategies across vendors and surfaces
- **Behavioral constraint research** — which surfaces impose the most guardrails? Which grant the most latitude?
- **Prompt engineering** — study patterns across 49 production AI systems
- **Alignment research** — how do vendors operationalize safety and autonomy through prompting?
- **Longitudinal tracking** — multi-version entries enable before/after comparison as products evolve

## Citation

If you use this dataset in research, please cite the repository:

```
@dataset{surface_intelligence_2026,
  author    = {Cruz Romero Morales and DojoGenesis},
  title     = {Surface Intelligence: AI System Prompt Corpus 2025--2026},
  year      = {2026},
  publisher = {Hugging Face},
  url       = {https://huggingface.co/datasets/DojoGenesis/surface-intelligence}
}
```

## Contact

Cruz Romero Morales — TresPies LLC / DojoGenesis — cruz@trespiesdesign.com

GitHub: https://github.com/DojoGenesis/SurfaceIntelligence
