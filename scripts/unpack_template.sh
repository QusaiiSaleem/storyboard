#!/bin/bash
cd /Users/qusaiabushanap/dev/storyboard

# Unpack template
python /Users/qusaiabushanap/.claude/plugins/cache/anthropic-agent-skills/document-skills/00756142ab04/skills/docx/ooxml/scripts/unpack.py "templates/قالب خارطة التعلم.docx" /tmp/template_learning_map_unpacked

# Convert template to markdown
pandoc "templates/قالب خارطة التعلم.docx" -o /tmp/template_learning_map.md

# Also convert objectives document
pandoc "output/NJR01/U02/NJR01_U02_Objectives.docx" -o /tmp/objectives_u02.md

echo "Done unpacking and converting"
