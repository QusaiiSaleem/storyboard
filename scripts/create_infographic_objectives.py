#!/usr/bin/env python3
"""
Step 1: Unpack the template and convert to markdown to see its structure.
This is a discovery script - we'll read the output and then create the real script.
"""
import subprocess
import os

SKILL_ROOT = "/Users/qusaiabushanap/.claude/plugins/cache/anthropic-agent-skills/document-skills/00756142ab04/skills/docx"
TEMPLATE = "/Users/qusaiabushanap/dev/storyboard/templates/قالب خارطة التعلم.docx"
UNPACK_DIR = "/tmp/template_learning_map_unpacked"

# Clean up previous unpack
if os.path.exists(UNPACK_DIR):
    import shutil
    shutil.rmtree(UNPACK_DIR)

# Unpack template
result = subprocess.run(
    ["python", f"{SKILL_ROOT}/ooxml/scripts/unpack.py", TEMPLATE, UNPACK_DIR],
    capture_output=True, text=True
)
print("UNPACK STDOUT:", result.stdout)
print("UNPACK STDERR:", result.stderr)

# Convert to markdown
result2 = subprocess.run(
    ["pandoc", TEMPLATE, "-o", "/tmp/template_learning_map.md"],
    capture_output=True, text=True
)
print("PANDOC STDOUT:", result2.stdout)
print("PANDOC STDERR:", result2.stderr)

# Also convert objectives doc
result3 = subprocess.run(
    ["pandoc", "/Users/qusaiabushanap/dev/storyboard/output/NJR01/U02/NJR01_U02_Objectives.docx", "-o", "/tmp/objectives_u02.md"],
    capture_output=True, text=True
)
print("OBJECTIVES PANDOC:", result3.stdout, result3.stderr)

# List unpacked files
for root, dirs, files in os.walk(UNPACK_DIR):
    for f in files:
        path = os.path.join(root, f)
        print(f"FILE: {path}")
