#!/usr/bin/env python3
"""Pre-analyze system prompts and build a versioned JSON library."""
import json, re, os, hashlib
from datetime import datetime

PROMPTS = [
    {
        "file": "/tmp/cursor_latest_prompt.txt",
        "product": "Cursor",
        "surface": "ide",
        "version": "Agent Sep 2025",
        "source": "x1xhlol/system-prompts-and-models-of-ai-tools",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2025-09-03",
        "model": "GPT-5",
        "vendor": "Anysphere",
    },
    {
        "file": "/tmp/v0_prompt.txt",
        "product": "v0",
        "surface": "web",
        "version": "Mar 2026",
        "source": "x1xhlol/system-prompts-and-models-of-ai-tools",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2026-03-08",
        "model": "Claude 3.5 Sonnet",
        "vendor": "Vercel",
    },
    {
        "file": "/tmp/windsurf_prompt.txt",
        "product": "Windsurf",
        "surface": "ide",
        "version": "Cascade Wave 11",
        "source": "x1xhlol/system-prompts-and-models-of-ai-tools",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2025-06-01",
        "model": "GPT-4.1",
        "vendor": "Codeium",
    },
    {
        "file": "/tmp/devin_prompt.txt",
        "product": "Devin",
        "surface": "web",
        "version": "2025",
        "source": "x1xhlol/system-prompts-and-models-of-ai-tools",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2025-06-01",
        "model": "Claude 3.5 Sonnet",
        "vendor": "Cognition",
    },
    {
        "file": "/tmp/lovable_prompt.txt",
        "product": "Lovable",
        "surface": "web",
        "version": "2025",
        "source": "x1xhlol/system-prompts-and-models-of-ai-tools",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2025-06-01",
        "model": "Claude 3.5 Sonnet",
        "vendor": "Lovable",
    },
    {
        "file": "/tmp/replit_prompt.txt",
        "product": "Replit Agent",
        "surface": "web",
        "version": "2025",
        "source": "x1xhlol/system-prompts-and-models-of-ai-tools",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2025-06-01",
        "model": "Unknown",
        "vendor": "Replit",
    },
    {
        "file": "/tmp/cline_prompt.txt",
        "product": "Cline",
        "surface": "ide",
        "version": "Open Source 2025",
        "source": "cline/cline (official)",
        "sourceUrl": "https://github.com/cline/cline",
        "extractedDate": "2025-06-01",
        "model": "Multi-model",
        "vendor": "Cline (OSS)",
    },
    {
        "file": "/tmp/copilot_prompt.txt",
        "product": "GitHub Copilot Chat",
        "surface": "ide",
        "version": "Sep 2024",
        "source": "jujumilk3/leaked-system-prompts",
        "sourceUrl": "https://github.com/jujumilk3/leaked-system-prompts",
        "extractedDate": "2024-09-30",
        "model": "GPT-4o",
        "vendor": "GitHub/Microsoft",
    },
    {
        "file": "/tmp/vscode_agent_prompt.txt",
        "product": "GitHub Copilot Agent",
        "surface": "ide",
        "version": "VSCode Agent 2025",
        "source": "x1xhlol/system-prompts-and-models-of-ai-tools",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2025-06-01",
        "model": "GPT-4.1",
        "vendor": "GitHub/Microsoft",
    },
    {
        "file": "/tmp/bolt_prompt.txt",
        "product": "Bolt.new",
        "surface": "web",
        "version": "Open Source 2025",
        "source": "stackblitz/bolt.new (official)",
        "sourceUrl": "https://github.com/stackblitz/bolt.new",
        "extractedDate": "2025-03-01",
        "model": "Claude 3.5 Sonnet",
        "vendor": "StackBlitz",
    },
]

def analyze(text):
    t = text.lower()
    char_count = len(text)
    token_count = round(char_count / 3.7)
    lines = text.split('\n')

    # Tool detection
    tool_patterns = [
        r'function[_\s]?call', r'tool[_\s]?use', r'tool[_\s]?name',
        r'"name"\s*:\s*"[^"]+"', r'def\s+\w+\(', r'fn\s+\w+\(',
        r'mcp__\w+', r'\bBash\b', r'\bRead\b', r'\bWrite\b', r'\bEdit\b',
        r'\bGrep\b', r'\bGlob\b',
    ]
    tool_matches = set()
    for p in tool_patterns:
        for m in re.finditer(p, text):
            tool_matches.add(m.group().strip())
    tool_count = min(len(tool_matches), 200)
    tool_density = round(tool_count / (token_count / 1000), 1) if token_count > 0 else 0

    # Safety score
    safety_kw = ['safety', 'prohibited', 'never', 'must not', 'do not', 'forbidden', 'restrict', 'dangerous',
        'harmful', 'security', 'injection', 'malicious', 'sensitive', 'privacy', 'copyright', 'confidential']
    safety_hits = sum(len(re.findall(kw, t)) for kw in safety_kw)
    safety_score = min(round((safety_hits / (token_count / 500)) * 25), 100)

    # Autonomy score
    auto_kw = ['autonomous', 'independently', 'without asking', 'proceed', 'execute', 'automatically',
        'on your own', 'take action', 'agentic', 'background']
    constraint_kw = ['ask first', 'confirm', 'check with', 'user approval', 'permission',
        'explicit consent', 'wait for', 'do not proceed']
    auto_hits = sum(1 for kw in auto_kw if kw in t)
    constraint_hits = sum(1 for kw in constraint_kw if kw in t)
    autonomy_score = min(max(round(((auto_hits - constraint_hits * 0.5) / 8) * 50 + 40), 5), 95)

    def score(keywords):
        h = sum(1 for kw in keywords if kw in t)
        return min(round((h / len(keywords)) * 100), 100)

    codegen = score(['code', 'function', 'implementation', 'refactor', 'debug', 'compile', 'build', 'test', 'lint', 'syntax', 'commit', 'diff', 'merge'])
    search = score(['search', 'find', 'grep', 'glob', 'query', 'lookup', 'retrieve', 'index', 'web search', 'documentation'])
    multimodal = score(['image', 'screenshot', 'visual', 'diagram', 'pdf', 'audio', 'video', 'camera', 'photo', 'render'])
    integration = score(['api', 'webhook', 'oauth', 'mcp', 'plugin', 'extension', 'integration', 'slack', 'github', 'database', 'cloud'])
    personality = score(['tone', 'personality', 'style', 'voice', 'concise', 'friendly', 'professional', 'emoji', 'humor', 'empathy'])

    # Capabilities
    caps = []
    cap_checks = [
        (r'file.*read|read.*file', 'File Reading', 'filesystem'),
        (r'file.*write|write.*file|create.*file', 'File Writing', 'filesystem'),
        (r'file.*edit|edit.*file', 'File Editing', 'filesystem'),
        (r'bash|shell|terminal|command', 'Shell Execution', 'system'),
        (r'git\b|commit|branch|merge', 'Git Operations', 'vcs'),
        (r'web.*search|search.*web', 'Web Search', 'search'),
        (r'screenshot|screen.*capture', 'Screenshots', 'multimodal'),
        (r'browser|chrome|navigate|click', 'Browser Control', 'automation'),
        (r'database|sql|query.*db', 'Database Access', 'data'),
        (r'mcp|model context protocol', 'MCP Support', 'integration'),
        (r'api.*call|http.*request|fetch', 'API Calls', 'integration'),
        (r'image.*generat|diagram|chart', 'Image Generation', 'multimodal'),
        (r'pdf|document.*read', 'PDF Processing', 'multimodal'),
        (r'email|gmail|smtp', 'Email', 'communication'),
        (r'slack|messaging|chat', 'Messaging', 'communication'),
        (r'calendar|schedule|event', 'Calendar', 'productivity'),
        (r'memory|remember|persist', 'Memory/Persistence', 'cognition'),
        (r'plan|planning|architect', 'Planning', 'cognition'),
        (r'notebook|jupyter|ipynb', 'Notebooks', 'data'),
        (r'deploy|cloudflare|worker|serverless', 'Deployment', 'devops'),
        (r'test|jest|pytest|mocha', 'Testing', 'quality'),
        (r'lint|format|prettier|eslint', 'Linting/Formatting', 'quality'),
        (r'docker|container|kubernetes', 'Containers', 'devops'),
        (r'figma|design|ui.*component', 'Design Tools', 'design'),
    ]
    for pattern, name, category in cap_checks:
        if re.search(pattern, text, re.IGNORECASE):
            caps.append({"name": name, "category": category})

    return {
        "toolCount": tool_count,
        "toolDensity": str(tool_density),
        "safetyScore": safety_score,
        "autonomyScore": autonomy_score,
        "codegenScore": codegen,
        "searchScore": search,
        "multimodalScore": multimodal,
        "integrationScore": integration,
        "personalityScore": personality,
        "tokenCount": token_count,
        "charCount": char_count,
        "capabilities": caps,
    }

library = []
for p in PROMPTS:
    if not os.path.exists(p["file"]):
        print(f"SKIP: {p['file']} not found")
        continue

    with open(p["file"], "r") as f:
        text = f.read()

    analysis = analyze(text)
    prompt_hash = hashlib.md5(text.encode()).hexdigest()[:12]

    entry = {
        "id": f"lib-{p['product'].lower().replace(' ', '-').replace('.', '')}-{p['surface']}",
        "product": p["product"],
        "surface": p["surface"],
        "version": p["version"],
        "source": p["source"],
        "sourceUrl": p["sourceUrl"],
        "extractedDate": p["extractedDate"],
        "model": p["model"],
        "vendor": p["vendor"],
        "promptHash": prompt_hash,
        "promptText": text,
        "analysis": analysis,
        "createdAt": datetime.now().isoformat(),
    }
    library.append(entry)
    print(f"OK: {p['product']} ({p['surface']}) - {analysis['toolCount']} tools, {analysis['tokenCount']}tok, safety={analysis['safetyScore']}, autonomy={analysis['autonomyScore']}")

out = os.path.join(os.path.dirname(__file__), "library.json")
with open(out, "w") as f:
    json.dump(library, f, separators=(",", ":"))

print(f"\nLibrary: {len(library)} entries, {os.path.getsize(out):,} bytes")
