#!/usr/bin/env python3
"""Inject the library data and new Library tab into index.html"""
import json, re

with open("library.json") as f:
    library = json.load(f)

# Minify prompt text slightly - remove excessive blank lines
for entry in library:
    entry["promptText"] = re.sub(r'\n{3,}', '\n\n', entry["promptText"])

library_json = json.dumps(library, separators=(",", ":"))

with open("index.html") as f:
    html = f.read()

# 1. Add Library tab to navigation
html = html.replace(
    "x-for=\"tab in ['Ingest','Analyze','Compare','Strategize']\"",
    "x-for=\"tab in ['Library','Ingest','Analyze','Compare','Strategize']\""
)

# 2. Inject Library tab section before Ingest tab
library_section = '''
<!-- ==================== LIBRARY TAB ==================== -->
<section x-show="activeTab === 'Library'" class="fade-in">
  <div class="flex items-center justify-between mb-6">
    <div>
      <h2 class="text-base font-semibold text-white">System Prompt Library</h2>
      <p class="text-xs text-slate-500 mt-1" x-text="promptLibrary.length + ' versioned prompts from ' + [...new Set(promptLibrary.map(p=>p.vendor))].length + ' vendors across ' + [...new Set(promptLibrary.map(p=>p.surface))].length + ' surfaces'"></p>
    </div>
    <div class="flex items-center gap-2">
      <select x-model="libFilter" class="bg-slate-800 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white outline-none">
        <option value="all">All Surfaces</option>
        <option value="ide">IDE</option>
        <option value="web">Web</option>
        <option value="cli">CLI</option>
      </select>
      <button @click="loadAllLibrary()" class="px-3 py-1.5 rounded-lg bg-surface-600 hover:bg-surface-500 text-white text-xs font-medium transition">
        Load All to Compare
      </button>
    </div>
  </div>

  <!-- Library Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
    <template x-for="item in filteredLibrary()" :key="item.id">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition group cursor-pointer"
        @click="libSelected = item.id" :class="libSelected === item.id ? 'border-surface-500 glow' : ''">
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="text-sm font-semibold text-white" x-text="item.product"></h3>
            <p class="text-[10px] text-slate-500 mt-0.5" x-text="item.vendor + ' &middot; ' + item.version"></p>
          </div>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-medium uppercase" :class="surfaceBadge(item.surface)" x-text="item.surface"></span>
        </div>
        <div class="grid grid-cols-4 gap-2 text-xs mb-3">
          <div class="text-center">
            <p class="text-surface-400 font-bold" x-text="item.analysis.toolCount"></p>
            <p class="text-[10px] text-slate-600">tools</p>
          </div>
          <div class="text-center">
            <p class="font-bold" :class="item.analysis.safetyScore > 60 ? 'text-red-400' : 'text-amber-400'" x-text="item.analysis.safetyScore + '%'"></p>
            <p class="text-[10px] text-slate-600">safety</p>
          </div>
          <div class="text-center">
            <p class="text-blue-400 font-bold" x-text="item.analysis.autonomyScore + '%'"></p>
            <p class="text-[10px] text-slate-600">autonomy</p>
          </div>
          <div class="text-center">
            <p class="text-white font-bold" x-text="(item.analysis.tokenCount/1000).toFixed(1) + 'K'"></p>
            <p class="text-[10px] text-slate-600">tokens</p>
          </div>
        </div>
        <!-- Capability pills -->
        <div class="flex flex-wrap gap-1 mb-3">
          <template x-for="cap in item.analysis.capabilities.slice(0,6)" :key="cap.name">
            <span class="px-1.5 py-0.5 rounded text-[9px] bg-slate-800 text-slate-400" x-text="cap.name"></span>
          </template>
          <span x-show="item.analysis.capabilities.length > 6" class="px-1.5 py-0.5 rounded text-[9px] bg-slate-800 text-slate-500" x-text="'+' + (item.analysis.capabilities.length - 6)"></span>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-[10px] text-slate-600" x-text="'Model: ' + item.model"></span>
          <div class="flex gap-1.5 opacity-0 group-hover:opacity-100 transition">
            <button @click.stop="loadLibraryItem(item)" class="px-2 py-1 rounded text-[10px] bg-surface-600/20 text-surface-400 hover:bg-surface-600/40 transition">+ Add to Compare</button>
            <button @click.stop="viewPrompt(item)" class="px-2 py-1 rounded text-[10px] bg-slate-800 text-slate-400 hover:bg-slate-700 transition">View Prompt</button>
          </div>
        </div>
        <div class="mt-2 flex items-center gap-2 text-[10px] text-slate-600">
          <span x-text="'Extracted: ' + item.extractedDate"></span>
          <span>&middot;</span>
          <span x-text="item.source"></span>
        </div>
      </div>
    </template>
  </div>

  <!-- Selected prompt detail view -->
  <template x-if="libSelected && getLibItem(libSelected)">
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-6" x-data="{ showFull: false }">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-sm font-semibold text-white" x-text="getLibItem(libSelected).product + ' System Prompt'"></h3>
          <p class="text-xs text-slate-500" x-text="getLibItem(libSelected).version + ' &middot; ' + getLibItem(libSelected).analysis.charCount.toLocaleString() + ' chars &middot; ' + getLibItem(libSelected).analysis.tokenCount.toLocaleString() + ' tokens'"></p>
        </div>
        <div class="flex gap-2">
          <button @click="showFull = !showFull" class="px-3 py-1.5 rounded-lg text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 transition" x-text="showFull ? 'Collapse' : 'Expand Full Prompt'"></button>
          <button @click="loadLibraryItem(getLibItem(libSelected))" class="px-3 py-1.5 rounded-lg text-xs bg-surface-600 hover:bg-surface-500 text-white transition">Add to Compare</button>
        </div>
      </div>
      <div class="bg-slate-800/50 rounded-lg p-4 font-mono text-xs text-slate-300 leading-relaxed overflow-auto"
        :class="showFull ? 'max-h-[600px]' : 'max-h-48'" style="white-space: pre-wrap; word-break: break-word;">
        <template x-if="showFull">
          <div x-text="getLibItem(libSelected).promptText"></div>
        </template>
        <template x-if="!showFull">
          <div>
            <span x-text="getLibItem(libSelected).promptText.slice(0, 800)"></span>
            <span class="text-slate-600">... (click Expand to see full prompt)</span>
          </div>
        </template>
      </div>
    </div>
  </template>
</section>

'''

html = html.replace(
    '<!-- ==================== INGEST TAB ==================== -->',
    library_section + '\n<!-- ==================== INGEST TAB ==================== -->'
)

# 3. Inject library data and methods into the Alpine component
library_data_injection = f'''
    promptLibrary: LIBRARY_DATA,
    libFilter: 'all',
    libSelected: null,
'''

html = html.replace(
    "activeTab: 'Ingest',",
    f"activeTab: 'Library',\n{library_data_injection}"
)

# 4. Add library methods before the UTILITIES section
library_methods = '''
    filteredLibrary() {
      if (this.libFilter === 'all') return this.promptLibrary;
      return this.promptLibrary.filter(p => p.surface === this.libFilter);
    },
    getLibItem(id) { return this.promptLibrary.find(p => p.id === id); },
    loadLibraryItem(item) {
      // Check if already loaded
      if (this.profiles.find(p => p.promptHash === item.promptHash)) return;
      this.profiles.push({
        id: item.id + '-' + Date.now().toString(36),
        product: item.product,
        surface: item.surface,
        version: item.version,
        vendor: item.vendor,
        source: item.source,
        promptSnippet: item.promptText.slice(0, 200),
        promptHash: item.promptHash,
        analysis: item.analysis,
        createdAt: new Date().toISOString()
      });
      this.save();
    },
    loadAllLibrary() {
      this.promptLibrary.forEach(item => this.loadLibraryItem(item));
    },
    viewPrompt(item) {
      this.libSelected = item.id;
      // Scroll to detail view
      this.$nextTick(() => {
        const el = document.querySelector('[x-show="activeTab === \\'Library\\'"] .bg-slate-900.border');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
    },

'''

html = html.replace(
    '// ---- UTILITIES ----',
    library_methods + '    // ---- UTILITIES ----'
)

# 5. Inject the library data as a script block before the main Alpine function
lib_script = f'<script>const LIBRARY_DATA = {library_json};</script>\n<script>'
html = html.replace('<script>\nfunction surfaceIntel()', lib_script + '\nfunction surfaceIntel()')

# 6. Update header counter to include library count
html = html.replace(
    "profiles.length + ' profiles ingested'",
    "profiles.length + ' active / ' + promptLibrary.length + ' in library'"
)

with open("index.html", "w") as f:
    f.write(html)

print(f"Updated index.html: {len(html):,} chars")
print(f"Library data: {len(library_json):,} chars ({len(library)} entries)")
