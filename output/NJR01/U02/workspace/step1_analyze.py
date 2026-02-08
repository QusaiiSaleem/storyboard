#!/usr/bin/env python3
"""Step 1: Analyze the interactive lecture template."""
import subprocess, sys, os, json

SKILLS = "/Users/qusaiabushanap/.claude/plugins/cache/anthropic-agent-skills/document-skills/00756142ab04/skills/pptx"
TEMPLATE = "/Users/qusaiabushanap/dev/storyboard/templates/قالب المحاضرة التفاعلية- عربي.pptx"
WS = "/Users/qusaiabushanap/dev/storyboard/output/NJR01/U02/workspace"
os.makedirs(WS, exist_ok=True)

# 1. Extract text
print("=== Extracting text ===")
r = subprocess.run([sys.executable, "-m", "markitdown", TEMPLATE], capture_output=True, text=True)
with open(f"{WS}/template-content.md", "w") as f:
    f.write(r.stdout)
print(f"Extracted {len(r.stdout)} chars")

# 2. Create thumbnails
print("\n=== Creating thumbnails ===")
r = subprocess.run([sys.executable, f"{SKILLS}/scripts/thumbnail.py", TEMPLATE, f"{WS}/template-thumbs", "--cols", "4"], capture_output=True, text=True)
print(r.stdout or "Done")
if r.stderr: print(r.stderr[:300])

# 3. Run inventory on template
print("\n=== Running inventory ===")
r = subprocess.run([sys.executable, f"{SKILLS}/scripts/inventory.py", TEMPLATE, f"{WS}/template-inventory.json"], capture_output=True, text=True)
print(r.stdout or "Done")
if r.stderr: print(r.stderr[:300])

print("\n=== Step 1 Complete ===")
