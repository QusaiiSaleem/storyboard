#!/usr/bin/env python3
"""Analyze the interactive lecture template."""
import subprocess, sys, os

SKILLS = "/Users/qusaiabushanap/.claude/plugins/cache/anthropic-agent-skills/document-skills/00756142ab04/skills/pptx"
TEMPLATE = "/Users/qusaiabushanap/dev/storyboard/templates/قالب المحاضرة التفاعلية- عربي.pptx"
WORKSPACE = "/Users/qusaiabushanap/dev/storyboard/output/NJR01/U02/workspace"

os.makedirs(WORKSPACE, exist_ok=True)
os.chdir(SKILLS)

# 1. Extract text with markitdown
print("=== Step 1: Extracting text ===")
result = subprocess.run(
    [sys.executable, "-m", "markitdown", TEMPLATE],
    capture_output=True, text=True
)
with open(f"{WORKSPACE}/template-content.md", "w") as f:
    f.write(result.stdout)
print(f"Text extracted: {len(result.stdout)} chars")
if result.stderr:
    print(f"Warnings: {result.stderr[:500]}")

# 2. Create thumbnails
print("\n=== Step 2: Creating thumbnails ===")
result = subprocess.run(
    [sys.executable, f"{SKILLS}/scripts/thumbnail.py", TEMPLATE, f"{WORKSPACE}/template-thumbs", "--cols", "4"],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print(f"Errors: {result.stderr[:500]}")

# 3. Unpack template
print("\n=== Step 3: Unpacking template ===")
result = subprocess.run(
    [sys.executable, f"{SKILLS}/ooxml/scripts/unpack.py", TEMPLATE, f"{WORKSPACE}/template-unpacked"],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print(f"Errors: {result.stderr[:500]}")

# 4. Run inventory on template
print("\n=== Step 4: Running inventory ===")
result = subprocess.run(
    [sys.executable, f"{SKILLS}/scripts/inventory.py", TEMPLATE, f"{WORKSPACE}/template-inventory.json"],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print(f"Errors: {result.stderr[:500]}")

print("\n=== Done ===")
