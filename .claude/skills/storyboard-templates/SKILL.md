---
name: storyboard-templates
description: Template engine API for generating production-ready DOCX and PPTX educational storyboard documents. Provides Python builders for 13 storyboard types (tests, activities, videos, lectures, discussions, assignments, summaries, objectives, infographics). Use when generating storyboard documents, when agents need engine API reference, or when working with the storyboard engine.
---

# Storyboard Template Engine

Python engine that builds production-ready DOCX and PPTX documents from scratch, matching the exact visual design of original templates. Uses a "template-as-code" approach -- no template file manipulation.

Engine files: `engine/docx_engine.py`, `engine/pptx_engine.py`, `engine/rtl_helpers.py`

## Quick Reference

### Import Paths

```python
import sys
sys.path.insert(0, '/Users/qusaiabushanap/dev/storyboard')

# DOCX builders (8 types)
from engine.docx_engine import (
    TestBuilder,           # Pre-test, post-test, course exam
    ActivityBuilder,       # Interactive activities with scenes
    VideoBuilder,          # Motion video with narration scenes
    ObjectivesBuilder,     # Learning objectives
    SummaryBuilder,        # Unit summary
    InfographicBuilder,    # Learning map / infographic
    DiscussionBuilder,     # Discussion activity
    AssignmentBuilder,     # Assignment
)

# PPTX builder (1 type)
from engine.pptx_engine import LectureBuilder  # Interactive & PDF lectures
```

### Common DOCX Pattern

Every DOCX builder takes the same constructor and follows the same lifecycle:

```python
builder = AnyBuilder(
    project_code="DSAI",
    unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران",
    designer="أحمد",
)
builder.set_element_name("...")   # Arabic element name
builder.set_element_code("...")   # e.g. DSAI_U01_Pre_Test
# ... type-specific content methods ...
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Pre_Test.docx")
```

Run via Bash: `python3 -c "..."` with the full script.

### PPTX Quick Start

```python
from engine.pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    institution="جامعة نجران",
)
builder.add_title_slide(title="المحاضرة:", subtitle="المهارات الرقمية")
builder.add_objectives_slide(objectives=["هدف 1", "هدف 2"])
builder.add_content_slide(title="المقدمة", bullets=["نقطة 1", "نقطة 2"])
builder.add_quiz_slide(question="سؤال؟", options=["أ", "ب", "ج"], correct_index=1)
builder.add_summary_slide(["ملخص النقطة 1", "ملخص النقطة 2"])
builder.add_closing_slide(next_steps=["المحاضرة القادمة"])
builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
```

## Detailed API References

For complete method signatures, parameters, and full examples:

- **DOCX builders (8 types)**: See [references/docx-builders.md](references/docx-builders.md)
- **PPTX LectureBuilder (12 slide types)**: See [references/pptx-builder.md](references/pptx-builder.md)

## Builder-to-Storyboard Mapping

| Storyboard Type | Builder | Extension |
|----------------|---------|-----------|
| الأهداف التعليمية (Learning Objectives) | ObjectivesBuilder | .docx |
| خارطة التعلم (Learning Map) | InfographicBuilder | .docx |
| الاختبار القبلي (Pre-Test) | TestBuilder | .docx |
| المحاضرة التفاعلية (Interactive Lecture) | LectureBuilder | .pptx |
| محاضرة PDF (PDF Lecture) | LectureBuilder | .pptx |
| فيديو موشن (Motion Video) | VideoBuilder | .docx |
| نشاط تفاعلي (Interactive Activity) | ActivityBuilder | .docx |
| النقاش (Discussion) | DiscussionBuilder | .docx |
| الواجب (Assignment) | AssignmentBuilder | .docx |
| الاختبار البعدي (Post-Test) | TestBuilder | .docx |
| الملخص (Summary) | SummaryBuilder | .docx |
| اختبار المقرر (Course Exam) | TestBuilder | .docx |

## Output Path Convention

```
output/[project-code]/U[XX]/[CODE]_U[XX]_[Element_Type].[ext]
```

Examples: `DSAI_U01_Pre_Test.docx`, `DSAI_U01_Interactive_Lecture.pptx`, `DSAI_U01_Activity1.1.docx`

## Project Config

Read project config from `projects/[project-code]/config.json` to populate builder constructor parameters.

```json
{
  "projectCode": "DSAI",
  "projectName": "تطوير 15 مقرر إلكتروني – جامعة نجران",
  "clientName": "جامعة نجران",
  "designerName": "تسنيم خالد",
  "branding": {
    "logo": "branding/logo.png",
    "header": "branding/header.png"
  }
}
```

## Image Generation

All builders support AI image generation via `image_prompt` parameter. The engine calls `generate_storyboard_image()` internally (Nano Banana Pro / Gemini 3 Pro) with project visual direction auto-applied from `projects/[code]/config.json` -> `visualDirection`. Priority: `image_path` > `image_prompt` (existing file wins). Write prompts in English; cultural rules are enforced automatically.

For full API, caching, density guidelines, and per-builder usage: See [references/image-gen.md](references/image-gen.md)

## Storyline 360 Compatibility (PPTX)

The PPTX engine is Storyline-import-ready:
- Hidden TOC titles on every slide (Storyline sidebar shows Arabic titles)
- No page numbers (Storyline's player handles navigation)
- Import instructions in title slide speaker notes (fonts, setup, QA checklist)
- Named shapes (`btn_*`, `opt_*`, `txt_*`) for easy trigger setup
- Target story size: 1280x720px

## RTL Notes (for debugging)

The engine handles RTL automatically. Key internals:

- **python-docx**: `<w:bidi/>` on paragraphs, `<w:rtl/>` on runs, `<w:bidiVisual/>` on tables
- **python-pptx**: `pPr.set('rtl', '1')` on paragraphs
- **Font gotcha**: RTL causes `font.name` to be ignored -- must set `font.cs_name` separately
- **Never reuse XML elements** across cells -- they get MOVED not copied
- Shared helpers: `engine/rtl_helpers.py`
