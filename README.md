# Surface Intelligence

71 AI system prompts from 49 products across 6 surfaces. Statistical comparison, multi-surface pattern analysis, searchable browser.

A living dataset and analysis platform for understanding how AI products position themselves through their system prompts.

## What's Here

- **71 system prompts** from products including Claude, Cursor, Kiro (AWS), Gemini, Copilot, Linear, and more
- **49 unique products** spanning IDE assistants, web chatbots, API platforms, mobile apps, CLIs, and desktop tools
- **6 surfaces**: `ide`, `web`, `api`, `cli`, `mobile`, `desktop`
- **Statistical comparison** — length, structure, tone, behavioral constraints across surfaces
- **Multi-surface strategy** — how the same vendor approaches different distribution surfaces

## The Browser

`index.html` is a self-contained web app (Alpine.js + Chart.js + Tailwind CSS, no build step) that loads `library.json` at runtime. Deploy to any static host, or open directly in a browser.

```bash
# Cloudflare Workers (wrangler)
npx wrangler deploy

# Local — no server needed
open index.html
```

## Library Format

Each entry in `library.json`:

```json
{
  "id": "lib-product-surface-version",
  "product": "Product Name",
  "surface": "ide|web|api|cli|mobile|desktop",
  "version": "Variant name",
  "source": "source repository or disclosure",
  "sourceUrl": "https://...",
  "extractedDate": "2025-01-01",
  "model": "Claude|GPT-4|Gemini|etc",
  "vendor": "Vendor name",
  "promptHash": "70080dcf473c",
  "promptText": "..."
}
```

## Adding Entries

1. Add the entry object to `library.json`
2. Run `python3 build-library.py` to rebuild search indexes
3. Open `index.html` and verify the new prompt appears correctly

## Project Structure

```
SurfaceIntelligence/
├── index.html          # Self-contained browser app (Alpine.js + Chart.js)
├── library.json        # 71 system prompt entries (1.5MB)
├── worker.js           # Cloudflare Worker entry point
├── wrangler.toml       # CF Workers deploy config
├── build-library.py    # Rebuild search index from library.json
└── build.sh            # Full build pipeline
```

## Use Cases

- **Competitive intelligence** — what does Cursor's system prompt reveal about its product strategy?
- **Surface analysis** — how does Claude's IDE prompt differ from its web prompt?
- **Behavioral constraints** — what guardrails do products bake into their base instructions?
- **Prompt engineering research** — patterns across 71 prompts from 49 production AI systems

## License

MIT

*Data sourced from public disclosures and community research. See individual `sourceUrl` fields for attribution.*
