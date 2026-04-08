#!/bin/bash
# Build worker.js by inlining the HTML using Base64 to avoid escaping issues
cd "$(dirname "$0")"

python3 -c "
import base64, json

with open('index.html', 'r') as f:
    html = f.read()

# Base64 encode to completely avoid template literal escaping issues
b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')

worker = '''// Surface Intelligence Worker - serves HTML from Base64
const HTML_B64 = \"''' + b64 + '''\";

function b64decode(str) {
  const binStr = atob(str);
  const bytes = new Uint8Array(binStr.length);
  for (let i = 0; i < binStr.length; i++) bytes[i] = binStr.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

let cachedHtml = null;

export default {
  async fetch(request) {
    if (!cachedHtml) cachedHtml = b64decode(HTML_B64);
    return new Response(cachedHtml, {
      headers: {
        \"Content-Type\": \"text/html;charset=UTF-8\",
        \"Cache-Control\": \"public, max-age=3600\",
      },
    });
  },
};'''

with open('worker.js', 'w') as f:
    f.write(worker)

print(f'Built worker.js: {len(worker):,} chars (HTML: {len(html):,}, B64: {len(b64):,})')
"
