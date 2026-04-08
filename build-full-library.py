#!/usr/bin/env python3
"""Build complete library from system-prompts-collection repo + /tmp originals."""
import json, re, os, hashlib, glob

BASE = "/Users/alfonsomorales/ZenflowProjects/system-prompts-collection"

# Define all prompts with metadata
# Format: (file_path, product, surface, version, model, vendor)
CATALOG = [
    # === ANTHROPIC ===
    (f"{BASE}/Anthropic/Claude-Code/Prompt.txt", "Claude Code", "cli", "v1.0", "Claude 3.5 Sonnet", "Anthropic"),
    (f"{BASE}/Anthropic/Claude-Code-2.0.txt", "Claude Code", "cli", "v2.0 (2026)", "Claude Sonnet 4.6", "Anthropic"),
    (f"{BASE}/Anthropic/Sonnet-4.5-Prompt.txt", "Claude Sonnet 4.5", "api", "4.5", "Claude Sonnet 4.5", "Anthropic"),
    (f"{BASE}/Anthropic/Sonnet-4.6-Prompt.txt", "Claude Sonnet 4.6", "api", "4.6", "Claude Sonnet 4.6", "Anthropic"),
    (f"{BASE}/Anthropic/Claude-Chrome/Prompt.txt", "Claude for Chrome", "desktop", "Extension", "Claude", "Anthropic"),

    # === CURSOR ===
    (f"{BASE}/Cursor/Agent-Prompt-2.0.txt", "Cursor", "ide", "Agent 2.0", "GPT-4.1", "Anysphere"),
    (f"{BASE}/Cursor/Agent-Prompt-2025-09-03.txt", "Cursor", "ide", "Agent Sep 2025", "GPT-5", "Anysphere"),
    (f"{BASE}/Cursor/Agent-CLI-Prompt-2025-08-07.txt", "Cursor CLI", "cli", "CLI Aug 2025", "GPT-5", "Anysphere"),
    (f"{BASE}/Cursor/Chat-Prompt.txt", "Cursor Chat", "ide", "Chat Mode", "GPT-4.1", "Anysphere"),

    # === VSCODE / COPILOT ===
    (f"{BASE}/VSCode-Agent/Prompt.txt", "GitHub Copilot Agent", "ide", "VSCode Base", "GPT-4.1", "GitHub/Microsoft"),
    (f"{BASE}/VSCode-Agent/gpt-5.txt", "Copilot Agent (GPT-5)", "ide", "GPT-5 variant", "GPT-5", "GitHub/Microsoft"),
    (f"{BASE}/VSCode-Agent/gpt-5-mini.txt", "Copilot Agent (GPT-5 Mini)", "ide", "GPT-5-mini variant", "GPT-5 Mini", "GitHub/Microsoft"),
    (f"{BASE}/VSCode-Agent/gpt-4.1.txt", "Copilot Agent (GPT-4.1)", "ide", "GPT-4.1 variant", "GPT-4.1", "GitHub/Microsoft"),
    (f"{BASE}/VSCode-Agent/gpt-4o.txt", "Copilot Agent (GPT-4o)", "ide", "GPT-4o variant", "GPT-4o", "GitHub/Microsoft"),
    (f"{BASE}/VSCode-Agent/claude-sonnet-4.txt", "Copilot Agent (Claude 4)", "ide", "Claude Sonnet 4 variant", "Claude Sonnet 4", "GitHub/Microsoft"),
    (f"{BASE}/VSCode-Agent/gemini-2.5-pro.txt", "Copilot Agent (Gemini)", "ide", "Gemini 2.5 Pro variant", "Gemini 2.5 Pro", "GitHub/Microsoft"),

    # === GOOGLE ===
    (f"{BASE}/Google/Antigravity/Fast-Prompt.txt", "Google Antigravity", "ide", "Fast Mode", "Gemini", "Google"),
    (f"{BASE}/Google/Antigravity/planning-mode.txt", "Google Antigravity", "ide", "Planning Mode", "Gemini", "Google"),
    (f"{BASE}/Google/Gemini/AI-Studio-vibe-coder.txt", "Gemini AI Studio", "web", "Vibe Coder", "Gemini 2.5 Pro", "Google"),
    (f"{BASE}/OpenSource/Gemini-CLI/system-prompt.txt", "Gemini CLI", "cli", "2025", "Gemini", "Google"),

    # === OPENAI ===
    (f"{BASE}/OpenSource/Codex-CLI/Prompt.txt", "OpenAI Codex CLI", "cli", "v1", "GPT-4.1", "OpenAI"),
    (f"{BASE}/OpenSource/Codex-CLI/system-prompt-20250820.txt", "OpenAI Codex CLI", "cli", "Aug 2025", "GPT-4.1", "OpenAI"),

    # === AWS / JETBRAINS ===
    (f"{BASE}/Kiro/Mode-Classifier-Prompt.txt", "Kiro (AWS)", "ide", "Mode Classifier", "Claude", "AWS"),
    (f"{BASE}/Kiro/Spec-Prompt.txt", "Kiro (AWS)", "ide", "Spec Mode", "Claude", "AWS"),
    (f"{BASE}/Kiro/Vibe-Prompt.txt", "Kiro (AWS)", "ide", "Vibe Mode", "Claude", "AWS"),
    (f"{BASE}/Junie/Prompt.txt", "Junie (JetBrains)", "ide", "2025", "Multi-model", "JetBrains"),

    # === AUGMENT ===
    (f"{BASE}/Augment-Code/claude-4-sonnet-agent-prompts.txt", "Augment Code", "ide", "Claude 4 Sonnet", "Claude Sonnet 4", "Augment"),
    (f"{BASE}/Augment-Code/gpt-5-agent-prompts.txt", "Augment Code", "ide", "GPT-5", "GPT-5", "Augment"),

    # === BYTEDANCE ===
    (f"{BASE}/Trae/Builder-Prompt.txt", "Trae (ByteDance)", "ide", "Builder Mode", "Multi-model", "ByteDance"),
    (f"{BASE}/Trae/Chat-Prompt.txt", "Trae (ByteDance)", "ide", "Chat Mode", "Multi-model", "ByteDance"),

    # === WEB BUILDERS ===
    (f"{BASE}/Leap-new/Prompts.txt", "Leap.new", "web", "2025", "Claude", "Leap"),
    (f"{BASE}/Same-dev/Prompt.txt", "Same.dev", "web", "2025", "Claude", "Same"),
    (f"{BASE}/Emergent/Prompt.txt", "Emergent", "web", "2025", "Multi-model", "Emergent"),

    # === MANUS ===
    (f"{BASE}/Manus/Prompt.txt", "Manus AI", "web", "Core Prompt", "Claude", "Manus"),
    (f"{BASE}/Manus/Agent-loop.txt", "Manus AI", "web", "Agent Loop", "Claude", "Manus"),
    (f"{BASE}/Manus/Modules.txt", "Manus AI", "web", "Modules", "Claude", "Manus"),

    # === PRODUCTIVITY / OTHER ===
    (f"{BASE}/NotionAI/Prompt.txt", "Notion AI", "web", "2025", "Multi-model", "Notion"),
    (f"{BASE}/Perplexity/Prompt.txt", "Perplexity", "web", "2025", "Multi-model", "Perplexity"),
    (f"{BASE}/Warp-dev/Prompt.txt", "Warp Terminal", "cli", "2025", "Multi-model", "Warp"),
    (f"{BASE}/Comet-Assistant/System-Prompt.txt", "Comet Assistant", "web", "2025", "Multi-model", "Comet"),
    (f"{BASE}/dia/Prompt.txt", "dia (Browser Co)", "desktop", "2025", "Multi-model", "The Browser Company"),

    # === IDE ASSISTANTS ===
    (f"{BASE}/CodeBuddy/Chat-Prompt.txt", "CodeBuddy", "ide", "Chat Mode", "Multi-model", "CodeBuddy"),
    (f"{BASE}/CodeBuddy/Craft-Prompt.txt", "CodeBuddy", "ide", "Craft Mode", "Multi-model", "CodeBuddy"),
    (f"{BASE}/Traycer-AI/phase-mode-prompts.txt", "Traycer AI", "ide", "Phase Mode", "Multi-model", "Traycer"),
    (f"{BASE}/Traycer-AI/plan-mode-prompts.txt", "Traycer AI", "ide", "Plan Mode", "Multi-model", "Traycer"),
    (f"{BASE}/Qoder/prompt.txt", "Qoder", "ide", "Main Prompt", "Multi-model", "Qoder"),
    (f"{BASE}/Qoder/Quest-Action.txt", "Qoder", "ide", "Quest Action", "Multi-model", "Qoder"),
    (f"{BASE}/Qoder/Quest-Design.txt", "Qoder", "ide", "Quest Design", "Multi-model", "Qoder"),
    (f"{BASE}/Z-ai-Code/prompt.txt", "Z.ai Code", "ide", "2025", "Multi-model", "Z.ai"),

    # === OPEN SOURCE ===
    (f"{BASE}/OpenSource/RooCode/Prompt.txt", "RooCode", "ide", "Open Source", "Multi-model", "RooCode (OSS)"),
    (f"{BASE}/OpenSource/Lumo/Prompt.txt", "Lumo", "web", "Open Source", "Multi-model", "Lumo (OSS)"),

    # === MISC ===
    (f"{BASE}/Cluely/Default-Prompt.txt", "Cluely", "desktop", "Default", "Multi-model", "Cluely"),
    (f"{BASE}/Cluely/Enterprise-Prompt.txt", "Cluely", "desktop", "Enterprise", "Multi-model", "Cluely"),
    (f"{BASE}/Orchids-app/System-Prompt.txt", "Orchids App", "mobile", "System Prompt", "Multi-model", "Orchids"),
    (f"{BASE}/Orchids-app/Decision-making-prompt.txt", "Orchids App", "mobile", "Decision Making", "Multi-model", "Orchids"),

    # === APPLE ===
    (f"{BASE}/Xcode/System.txt", "Xcode AI", "ide", "System", "Apple Intelligence", "Apple"),
    (f"{BASE}/Xcode/ExplainAction.txt", "Xcode AI", "ide", "Explain Action", "Apple Intelligence", "Apple"),
    (f"{BASE}/Xcode/DocumentAction.txt", "Xcode AI", "ide", "Document Action", "Apple Intelligence", "Apple"),
    (f"{BASE}/Xcode/PlaygroundAction.txt", "Xcode AI", "ide", "Playground Action", "Apple Intelligence", "Apple"),
    (f"{BASE}/Xcode/MessageAction.txt", "Xcode AI", "ide", "Message Action", "Apple Intelligence", "Apple"),
    (f"{BASE}/Xcode/PreviewAction.txt", "Xcode AI", "ide", "Preview Action", "Apple Intelligence", "Apple"),

    # === POKE (multi-part) ===
    (f"{BASE}/Poke/Poke-agent.txt", "Poke", "web", "Agent", "Multi-model", "Poke"),
    (f"{BASE}/Poke/Poke_p1.txt", "Poke", "web", "Part 1", "Multi-model", "Poke"),

    # === FROM /tmp (original downloads, deduplicated) ===
    ("/tmp/devin_prompt.txt", "Devin", "web", "2025", "Claude 3.5 Sonnet", "Cognition"),
    ("/tmp/lovable_prompt.txt", "Lovable", "web", "2025", "Claude 3.5 Sonnet", "Lovable"),
    ("/tmp/replit_prompt.txt", "Replit Agent", "web", "2025", "Multi-model", "Replit"),
    ("/tmp/cline_prompt.txt", "Cline", "ide", "Open Source 2025", "Multi-model", "Cline (OSS)"),
    ("/tmp/copilot_prompt.txt", "GitHub Copilot Chat", "ide", "Sep 2024", "GPT-4o", "GitHub/Microsoft"),
    ("/tmp/bolt_prompt.txt", "Bolt.new", "web", "Open Source 2025", "Claude 3.5 Sonnet", "StackBlitz"),
    ("/tmp/v0_prompt.txt", "v0", "web", "Mar 2026", "Claude 3.5 Sonnet", "Vercel"),
    ("/tmp/windsurf_prompt.txt", "Windsurf", "ide", "Cascade Wave 11", "GPT-4.1", "Codeium"),
]

def analyze(text):
    t = text.lower()
    cc = len(text)
    tc = round(cc / 3.7)
    tp = [r'function[_\s]?call', r'tool[_\s]?use', r'"name"\s*:\s*"[^"]+"', r'mcp__\w+',
          r'\bBash\b', r'\bRead\b', r'\bWrite\b', r'\bEdit\b', r'\bGrep\b', r'\bGlob\b']
    tm = set()
    for p in tp:
        for m in re.finditer(p, text): tm.add(m.group().strip())
    tool_count = min(len(tm), 200)
    tool_density = round(tool_count / max(tc / 1000, 0.1), 1)

    sk = ['safety','prohibited','never','must not','do not','forbidden','restrict','dangerous',
          'harmful','security','injection','malicious','sensitive','privacy','copyright','confidential']
    sh = sum(len(re.findall(kw, t)) for kw in sk)
    ss = min(round((sh / max(tc / 500, 1)) * 25), 100)

    ak = ['autonomous','independently','without asking','proceed','execute','automatically','on your own','take action','agentic','background']
    ck = ['ask first','confirm','check with','user approval','permission','explicit consent','wait for','do not proceed']
    ah = sum(1 for k in ak if k in t)
    ch = sum(1 for k in ck if k in t)
    aus = min(max(round(((ah - ch*0.5)/8)*50+40),5),95)

    def sc(kws):
        h = sum(1 for k in kws if k in t)
        return min(round((h/len(kws))*100),100)

    cg = sc(['code','function','implementation','refactor','debug','compile','build','test','lint','syntax','commit','diff','merge'])
    sr = sc(['search','find','grep','glob','query','lookup','retrieve','index','web search','documentation'])
    mm = sc(['image','screenshot','visual','diagram','pdf','audio','video','camera','photo','render'])
    ig = sc(['api','webhook','oauth','mcp','plugin','extension','integration','slack','github','database','cloud'])
    ps = sc(['tone','personality','style','voice','concise','friendly','professional','emoji','humor','empathy'])

    caps = []
    ccs = [
        (r'file.*read|read.*file','File Reading','filesystem'),(r'file.*write|write.*file|create.*file','File Writing','filesystem'),
        (r'file.*edit|edit.*file','File Editing','filesystem'),(r'bash|shell|terminal|command','Shell Execution','system'),
        (r'git\b|commit|branch|merge','Git Operations','vcs'),(r'web.*search|search.*web','Web Search','search'),
        (r'screenshot|screen.*capture','Screenshots','multimodal'),(r'browser|chrome|navigate|click','Browser Control','automation'),
        (r'database|sql|query.*db','Database Access','data'),(r'mcp|model context protocol','MCP Support','integration'),
        (r'api.*call|http.*request|fetch','API Calls','integration'),(r'image.*generat|diagram|chart','Image Generation','multimodal'),
        (r'pdf|document.*read','PDF Processing','multimodal'),(r'email|gmail|smtp','Email','communication'),
        (r'slack|messaging|chat','Messaging','communication'),(r'calendar|schedule|event','Calendar','productivity'),
        (r'memory|remember|persist','Memory/Persistence','cognition'),(r'plan|planning|architect','Planning','cognition'),
        (r'notebook|jupyter|ipynb','Notebooks','data'),(r'deploy|cloudflare|worker|serverless','Deployment','devops'),
        (r'test|jest|pytest|mocha','Testing','quality'),(r'lint|format|prettier|eslint','Linting/Formatting','quality'),
        (r'docker|container|kubernetes','Containers','devops'),(r'figma|design|ui.*component','Design Tools','design'),
    ]
    for pat,name,cat in ccs:
        if re.search(pat, text, re.IGNORECASE): caps.append({"name":name,"category":cat})

    return {"toolCount":tool_count,"toolDensity":str(tool_density),"safetyScore":ss,"autonomyScore":aus,
            "codegenScore":cg,"searchScore":sr,"multimodalScore":mm,"integrationScore":ig,"personalityScore":ps,
            "tokenCount":tc,"charCount":cc,"capabilities":caps}

library = []
seen_hashes = set()
ok = 0
skip = 0

for filepath, product, surface, version, model, vendor in CATALOG:
    if not os.path.exists(filepath):
        print(f"  MISS: {filepath}")
        skip += 1
        continue
    with open(filepath) as f:
        text = f.read()
    if len(text.strip()) < 50:
        print(f"  TINY: {filepath} ({len(text)} chars)")
        skip += 1
        continue

    text = re.sub(r'\n{3,}', '\n\n', text)
    h = hashlib.md5(text.encode()).hexdigest()[:12]
    if h in seen_hashes:
        print(f"  DUPE: {product} ({version}) - {filepath}")
        skip += 1
        continue
    seen_hashes.add(h)

    analysis = analyze(text)
    slug = re.sub(r'[^a-z0-9]+', '-', product.lower()).strip('-')
    vid = re.sub(r'[^a-z0-9]+', '-', version.lower()).strip('-')

    entry = {
        "id": f"lib-{slug}-{surface}-{vid}",
        "product": product,
        "surface": surface,
        "version": version,
        "source": "system-prompts-collection",
        "sourceUrl": "https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools",
        "extractedDate": "2025-09-01",
        "model": model,
        "vendor": vendor,
        "promptHash": h,
        "promptText": text,
        "analysis": analysis,
        "createdAt": "2026-04-07T00:00:00.000Z",
    }
    library.append(entry)
    ok += 1
    print(f"  OK: {product:30s} {surface:8s} {version:25s} {analysis['tokenCount']:>6,}tok  safety={analysis['safetyScore']:>3}  auto={analysis['autonomyScore']:>3}")

# Sort: by vendor, then product, then version
library.sort(key=lambda x: (x["vendor"], x["product"], x["version"]))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.json")
with open(out, "w") as f:
    json.dump(library, f, separators=(",", ":"))

sz = os.path.getsize(out)
products = len(set(e["product"] for e in library))
vendors = len(set(e["vendor"] for e in library))
surfaces = len(set(e["surface"] for e in library))

print(f"\n{'='*60}")
print(f"Library: {len(library)} entries ({products} products, {vendors} vendors, {surfaces} surfaces)")
print(f"File: {sz:,} bytes ({sz/1024:.0f} KB)")
print(f"Skipped: {skip}")
