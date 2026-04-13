# Surface Intelligence

71 AI system prompts from 35 vendors across 6 surfaces — statistical comparison, multi-surface pattern analysis, searchable browser.

A living dataset and analysis platform for understanding how AI products position themselves through their system prompts.

## What Is a "Surface"?

A surface is the distribution context where users interact with an AI product. The same underlying model behaves differently depending on whether it's embedded in an IDE, a web chat, a mobile app, or a CLI. Surface Intelligence tracks those differences systematically.

| Surface | What it covers | Entries |
|---------|---------------|---------|
| `ide` | IDE assistants: Cursor, Copilot, Kiro, Zed, Windsurf, etc. | 38 |
| `web` | Web chatbots and SaaS products: Claude.ai, ChatGPT, Gemini, Linear, etc. | 18 |
| `cli` | Command-line tools: Claude Code, Gemini CLI, Codex CLI, etc. | 7 |
| `desktop` | Native desktop apps: Claude desktop, Cursor standalone, etc. | 4 |
| `api` | API platform playgrounds and direct integrations | 2 |
| `mobile` | iOS and Android AI apps | 2 |

## The Dataset

- **71 system prompts** from products including Claude, Cursor, Kiro (AWS), Gemini, Copilot, Linear, and more
- **49 unique products** across IDE assistants, web chatbots, API platforms, mobile apps, CLIs, and desktop tools
- **35 unique vendors** — from Anthropic and Google to startups and independent tools
- **Multi-version entries** — tracks how prompts evolve across product versions
- **Prompt hashes** — detect when prompts change without reading full text

## Quick Start

```bash
git clone https://github.com/DojoGenesis/SurfaceIntelligence.git
cd SurfaceIntelligence

# Open the browser — no server needed
open index.html

# Or deploy to Cloudflare Workers
npx wrangler deploy
```

## The Browser App

`index.html` is a fully self-contained web app (Alpine.js + Chart.js + Tailwind CSS, no build step required). It loads `library.json` at runtime and provides:

- **Full-text search** across all 71 prompts
- **Surface filter** — drill into ide, web, cli, desktop, api, or mobile
- **Vendor filter** — compare prompts from the same company across surfaces
- **Statistical comparisons** — prompt length, structure density, behavioral constraint counts
- **Side-by-side diff** — compare two prompts directly

## Key Findings

**IDE prompts are 3-5x longer than web prompts.** IDE surfaces require detailed tool descriptions, workspace context, and file operation instructions. Web surfaces optimize for conciseness.

**CLI prompts are the most explicit about limitations.** Command-line tools have the highest density of behavioral constraints and capability boundaries.

**Multi-surface vendors show deliberate differentiation.** The same vendor's IDE prompt vs. web prompt reveals product strategy: what they want you to do vs. what they prevent.

**Behavioral constraints cluster by surface, not by model.** GPT-4-powered products on the web surface look more like Claude-powered web products than GPT-4-powered IDE products.

## Adding Entries

1. Add the entry object to `library.json`:

```json
{
  "id": "lib-product-surface-version",
  "product": "Product Name",
  "surface": "ide|web|api|cli|mobile|desktop",
  "version": "Variant name or date",
  "source": "source repository or disclosure",
  "sourceUrl": "https://...",
  "extractedDate": "2025-01-01",
  "model": "Claude|GPT-4|Gemini|etc",
  "vendor": "Vendor name",
  "promptHash": "70080dcf473c",
  "promptText": "Full system prompt text..."
}
```

2. Rebuild the search index:

```bash
python3 build-library.py
```

3. Verify: open `index.html` and confirm the new entry appears and is searchable.

## Build Pipeline

```bash
python3 build-library.py          # Rebuild search index
python3 build-full-library.py     # Full rebuild with all derived outputs
python3 build-worker-split.py     # Split library for Cloudflare Worker edge delivery
python3 inject-library.py         # Inject library data into index.html (for offline use)
bash build.sh                     # Full pipeline in sequence
```

## Project Structure

```
SurfaceIntelligence/
├── index.html            — Self-contained browser (Alpine.js + Chart.js + Tailwind)
├── library.json          — 71 system prompt entries (~1.5MB)
├── worker.js             — Cloudflare Worker entry point
├── wrangler.toml         — CF Workers deploy config
├── build-library.py      — Rebuild search index from library.json
├── build-full-library.py — Full derived output rebuild
├── build-worker-split.py — Split for edge delivery
├── inject-library.py     — Embed library data into index.html
└── build.sh              — Full build pipeline
```

## Use Cases

**Competitive intelligence** — what does Cursor's system prompt reveal about its product strategy relative to Copilot?

**Surface analysis** — how does Claude's IDE prompt differ from its web prompt? What does Anthropic optimize for differently per surface?

**Behavioral constraint research** — which surfaces have the most guardrails baked in? Which give the most latitude?

**Prompt engineering** — patterns across 71 prompts from 49 production AI systems in the wild.

**Vendor strategy** — which vendors have consistent identity across surfaces? Which localize heavily per surface?

**Historical tracking** — multi-version entries let you follow how a product's positioning has shifted over time.

## Requirements

- Python 3.x (for build scripts)
- Any modern browser (for `index.html`)
- Cloudflare account + wrangler (for Workers deploy, optional)

## License

MIT

*Data sourced from public disclosures, community research, and vendor announcements. See individual `sourceUrl` fields for attribution.*

---

*A [Dojo Genesis](https://github.com/DojoGenesis) project by Tres Pies Design.*
