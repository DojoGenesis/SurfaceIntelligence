#!/usr/bin/env python3
"""Build worker that serves HTML + library JSON from separate routes."""
import json, re

with open("index.html") as f:
    html = f.read()

with open("library.json") as f:
    lib = json.load(f)

# Create a catalog (metadata only, no prompt text) for initial page load
catalog = []
for entry in lib:
    cat_entry = {k: v for k, v in entry.items() if k != "promptText"}
    cat_entry["promptSnippet"] = entry["promptText"][:300] + "..."
    catalog.append(cat_entry)

catalog_json = json.dumps(catalog, separators=(",", ":"))
library_json = json.dumps(lib, separators=(",", ":"))

# Update HTML to load catalog initially, fetch full prompts on demand
# Replace the LIBRARY_DATA script with catalog data + fetch logic
old_lib_script = None
# Find the library data injection point
html = html.replace(
    'const LIBRARY_DATA = ',
    'const LIBRARY_CATALOG = '
)

# Add fetch-on-demand logic
fetch_script = """
// Load catalog immediately, fetch full prompts on demand
const LIBRARY_DATA = LIBRARY_CATALOG;
async function fetchFullPrompt(id) {
  if (window._promptCache && window._promptCache[id]) return window._promptCache[id];
  try {
    const res = await fetch('/api/library');
    const lib = await res.json();
    window._promptCache = {};
    lib.forEach(e => { window._promptCache[e.id] = e.promptText; });
    return window._promptCache[id] || '';
  } catch(e) { return '(Failed to load prompt text)'; }
}
"""

html = html.replace(
    'function surfaceIntel()',
    fetch_script + '\nfunction surfaceIntel()'
)

# Update viewPrompt to fetch full text
html = html.replace(
    "getLibItem(libSelected).promptText",
    "(getLibItem(libSelected)._fullText || getLibItem(libSelected).promptSnippet)"
)

# Add method to load full prompt
load_method = """
    async loadFullPrompt(item) {
      if (item._fullText) return;
      const text = await fetchFullPrompt(item.id);
      item._fullText = text;
      item.promptText = text;
    },
"""
html = html.replace(
    'filteredLibrary()',
    load_method + '    filteredLibrary()'
)

# Update viewPrompt to trigger fetch
html = html.replace(
    "viewPrompt(item) {",
    "async viewPrompt(item) { await this.loadFullPrompt(item);"
)

# Escape for JS template literal
def escape_for_js(s):
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

html_escaped = escape_for_js(html)
catalog_escaped = escape_for_js(catalog_json)
library_escaped = escape_for_js(library_json)

# Build worker
worker = f"""
const HTML = `{html_escaped}`;
const LIBRARY_JSON = `{library_escaped}`;

export default {{
  async fetch(request) {{
    const url = new URL(request.url);

    if (url.pathname === '/api/library') {{
      return new Response(LIBRARY_JSON, {{
        headers: {{
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=86400',
          'Access-Control-Allow-Origin': '*',
        }},
      }});
    }}

    return new Response(HTML, {{
      headers: {{
        'Content-Type': 'text/html;charset=UTF-8',
        'Cache-Control': 'public, max-age=3600',
      }},
    }});
  }},
}};
"""

with open("worker.js", "w") as f:
    f.write(worker)

print(f"Worker: {len(worker):,} chars")
print(f"  HTML portion: {len(html):,} chars")
print(f"  Library JSON: {len(library_json):,} chars")
print(f"  Catalog entries: {len(catalog)}")
