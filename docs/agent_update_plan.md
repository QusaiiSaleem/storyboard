# Agent Update Plan: Migrating Subagents to Template Engine

> Prepared by: Research Agent
> Status: DRAFT -- do NOT edit agent files until engine APIs are finalized
> Date: 2026-02-08

---

## Overview

All 9 document-producing subagents currently instruct the AI to create documents using the `/docx` or `/pptx` skills directly, treating template files as the base. This approach is fragile and produces broken RTL, overlapping text, and unreplaced placeholders.

The new approach: **agents produce structured content data, then call engine builder functions** to create the documents. The engine handles all formatting, RTL, fonts, colors, and borders.

---

## Global Changes (Apply to ALL 9 document-producing agents)

### 1. Remove Template File References

**Current pattern** (in every agent):
```
Create a [type] storyboard following the template at `templates/[template].docx`
```

**New pattern**:
```
Generate the structured content data, then use the engine builder to create the document.
```

### 2. Change Tool List

**Current**: `tools: Read, Write, Edit, Glob, Skill`
**New**: `tools: Read, Bash, Glob, Grep`

Rationale:
- **Remove `Write, Edit`**: Agents should NOT write files directly. The engine does that.
- **Remove `Skill`**: No longer using `/docx` or `/pptx` skills for document creation.
- **Add `Bash`**: Needed to run the engine builder script via Python.
- **Keep `Read, Glob, Grep`**: Agents still need to read raw content and project config.

### 3. Replace Output Section

**Current pattern** (in every agent):
```
## Output
- Use `/docx` skill to create the document from template
- Save to: `output/[project-code]/U[XX]/[filename].docx`
```

**New pattern**:
```
## Output

1. Structure your content as a Python dictionary (see Content Schema below)
2. Write the content dict to a temporary JSON file
3. Run the engine builder via Bash:

\`\`\`bash
python3 -c "
import json, sys
sys.path.insert(0, '/Users/qusaiabushanap/dev/storyboard')
from engine.docx_engine import [BuilderName]

with open('/tmp/storyboard_content.json') as f:
    content = json.load(f)

builder = [BuilderName](content)
result = builder.build('output/[project-code]/U[XX]/[filename].docx')
print(json.dumps(result))
"
\`\`\`

4. Check the result for `{"success": true}` before reporting completion
```

### 4. Add Content Schema Section

Every agent gets a new section defining the exact JSON/dict schema the engine expects. This is the contract between the agent (content producer) and the engine (document producer).

### 5. Add Explicit Separation of Concerns

Add to every agent:
```
## IMPORTANT: Separation of Concerns

You are a CONTENT PRODUCER, not a document formatter.

- DO: Read raw content, analyze it, generate educational content in Arabic
- DO: Structure your output as a Python dictionary matching the Content Schema
- DO: Ensure all Arabic text is correct, educational, and well-written
- DO NOT: Worry about fonts, colors, cell shading, borders, or RTL formatting
- DO NOT: Try to manipulate .docx or .pptx files directly
- DO NOT: Use the /docx or /pptx skills

The engine handles ALL formatting automatically.
```

---

## Agent-by-Agent Change Plan

### 1. storyboard-analyst.md

**Changes needed**: MINIMAL

This agent is a read-only content analyzer. It does not produce documents, so it does not need engine integration. It stays mostly the same.

**Specific changes**:
- Remove `Skill` from tools (it references `/docx` and `/pptx` skills for reading, but `Read` + `Bash` can handle this)
- Update tools to: `tools: Read, Glob, Grep, Bash`
- Keep the rest as-is -- its output is a text analysis, not a formatted document

---

### 2. storyboard-objectives.md

**Changes needed**: MODERATE

**Current approach**: Reads content analysis, generates objectives, uses `/docx` skill to fill the objectives template.

**New approach**: Reads content analysis, generates objectives, outputs a structured dict, calls `ObjectivesBuilder`.

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Learning_Objectives",
    "project_name": "...",
    "unit": "...",
    "element_name": "الأهداف التعليمية",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو إنفوجرافيك",
    "objectives": [
        {
            "text": "أن يُعرّف المتعلم مفهوم ...",
            "bloom_level": "تذكر"
        },
        # ... 4-8 objectives
    ]
}
```

**Lines to change**:
- Line 4: `tools: Read, Write, Edit, Glob, Skill` --> `tools: Read, Bash, Glob, Grep`
- Lines 22-24: Remove "Use the template at..." and "Generate the output document using the `/docx` skill"
- Lines 35-37: Replace Output section with engine builder call
- Add: Content Schema section
- Add: Separation of Concerns section

**Keep unchanged**: Bloom's Taxonomy rules (lines 15-21), objective writing rules (lines 27-32), Arabic text rules (lines 39-43)

---

### 3. storyboard-test.md

**Changes needed**: MODERATE

**Current approach**: Reads content, generates test questions, uses `/docx` skill to fill the test template.

**New approach**: Reads content, generates questions, outputs structured dict, calls `TestBuilder`.

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Pre_Test",
    "project_name": "...",
    "unit": "...",
    "element_name": "الاختبار القبلي",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو اختبار",
    "test_type": "pre_test",  # "pre_test" | "post_test" | "course_exam"
    "description": "وصف الاختبار والغرض منه",
    "guidelines": "المحاولات المتاحة: 1\nفرص متابعة الاختبار: لا\nحفظ الإجابات: تلقائي",
    "questions": [
        {
            "number": 1,
            "text": "ما هو الذكاء الاصطناعي؟",
            "type": "multiple_choice",  # "multiple_choice" | "true_false"
            "options": ["خيار أ", "خيار ب", "خيار ج", "خيار د"],
            "correct": 2,  # 0-based index
            "image_ref": "---"
        }
    ]
}
```

**Lines to change**:
- Line 4: Tools
- Line 12: Remove "following the template at `templates/...`"
- Lines 70-72: Replace Output section
- Add: Content Schema, Separation of Concerns

**Keep unchanged**: Test type rules (lines 43-60), question quality rules (lines 62-68), template structure description (used as content guidance, not formatting guidance)

---

### 4. storyboard-activity.md

**Changes needed**: MODERATE

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Activity1.1",
    "project_name": "...",
    "unit": "...",
    "element_name": "نشاط تفاعلي: ...",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو نشاط تفاعلي",
    "scenes": [
        {
            "number": 1,
            "description": "وصف المشهد",
            "elements": "عناصر المشهد",
            "image_description": "وصف الصور",
            "motion_graphic": "",  # optional
            "sound_effects": "",   # optional
            "screen_text": "نص يظهر على الشاشة",
            "question": {
                "text": "...",
                "options": ["...", "..."],
                "correct_feedback": "التغذية الراجعة للإجابة الصحيحة",
                "incorrect_feedback": "التغذية الراجعة للإجابة الخاطئة",
                "exhausted_feedback": "التغذية الراجعة بعد نفاذ المحاولات",
                "correct_answer": "الإجابة الصحيحة",
                "max_attempts": 2
            },
            "activity_steps": ["الخطوة 1", "الخطوة 2"],
            "buttons_after_exhausted": ["مراجعة المحتوى", "أعد المحاولة"]
        }
    ],
    "interaction_type": "اختيار من متعدد"
}
```

**Lines to change**:
- Line 4: Tools
- Line 12: Remove template file reference
- Lines 67-69: Replace Output section
- Add: Content Schema, Separation of Concerns

**Keep unchanged**: Scene structure requirements (lines 27-49), interaction types (lines 51-58), quality rules (lines 60-65)

---

### 5. storyboard-video.md

**Changes needed**: MODERATE

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Video",
    "project_name": "...",
    "element_name": "فيديو موشن: ...",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو فيديوهات موشن جرافيك",
    "lecture_reference": "مكان عرض الفيديو في المحاضرة التفاعلية",
    "scenes": [
        {
            "number": 0,  # 0 = title scene
            "title": "مشهد العنوان",
            "screen_description": "شاشة توضيحية للمشهد...",
            "sound_effects": "",
            "narration_text": "النص العلمي المقروء...",
            "onscreen_text": "النصوص التي تظهر في المشاهد...",
            "sync_description": "الوصف التفصيلي للمشهد والتزامن...",
            "image_refs": ["رابط صورة 1"]
        }
    ]
}
```

**Lines to change**:
- Line 4: Tools (keep `Grep` since video agent uses it)
- Line 12: Remove template file reference
- Lines 63-66: Replace Output section
- Add: Content Schema, Separation of Concerns

**Keep unchanged**: Scene structure requirements (lines 27-49), quality standards (lines 51-56), image generation section (lines 58-61)

**Special note**: The video agent has `tools: Read, Write, Edit, Glob, Grep, Skill`. It also generates images (line 58-61). The image generation part stays separate from the docx engine -- images are saved to `assets/images/` and referenced by path in the content dict. The agent may still need `Write` for saving images, or this can be handled through `Bash`.

---

### 6. storyboard-discussion.md

**Changes needed**: MODERATE

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Discussion",
    "project_name": "...",
    "unit": "...",
    "element_name": "نقاش: ...",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو نقاش",
    "discussion": {
        "screen_description": "شاشة توضيحية للنقاش...",
        "topic_context": "موضوع النقاش...",
        "question": "سؤال النقاش المفتوح...",
        "guidelines": "تعليمات وإرشادات النقاش...",
        "learning_objectives": ["الهدف 1", "الهدف 2"]
    }
}
```

**Lines to change**:
- Line 4: Tools
- Line 12: Remove template file reference
- Lines 52-54: Replace Output section
- Add: Content Schema, Separation of Concerns

**Keep unchanged**: Discussion quality rules (lines 46-50), template structure description (as content guidance)

---

### 7. storyboard-assignment.md

**Changes needed**: MODERATE

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Assignment",
    "project_name": "...",
    "unit": "...",
    "element_name": "واجب: ...",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو واجب",
    "assignment": {
        "screen_description": "شاشة توضيحية للواجب...",
        "task_text": "النص العلمي المعروض على الشاشة...",
        "guidelines": "تعليمات وإرشادات الواجب...",
        "file_format": "Word",
        "learning_objectives": ["الهدف 1", "الهدف 2"]
    }
}
```

**Lines to change**:
- Line 4: Tools
- Line 12: Remove template file reference
- Lines 52-53: Replace Output section
- Add: Content Schema, Separation of Concerns

**Keep unchanged**: Assignment quality rules (lines 46-49)

---

### 8. storyboard-infographic.md

**Changes needed**: MODERATE

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Learning_Map",
    "project_name": "...",
    "unit": "...",
    "element_name": "خرطة التعلم",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو إنفوجرافيك",
    "infographic": {
        "screen_description": "شاشة توضيحية للانفوجرافيك...",
        "onscreen_text": "النص العلمي المعروض على الشاشة...",
        "image_sources": "مصادر الصور...",
        "detailed_description": "الوصف التفصيلي للشاشة...",
        "journey_steps": [
            {"number": 1, "title": "حل الاختبار القبلي", "icon": "أيقونة اختبار"},
            {"number": 2, "title": "ادرس المحتوى التعليمي", "icon": "أيقونة محتوى تعليمي",
             "sub_items": ["نصوص", "أنشطة تفاعلية"]},
            # ... more steps
        ]
    }
}
```

**Lines to change**:
- Line 4: Tools
- Line 12: Remove template file reference
- Lines 55-57: Replace Output section
- Add: Content Schema, Separation of Concerns

**Keep unchanged**: Customization rules (lines 49-53) -- these are content decisions, not formatting

---

### 9. storyboard-summary.md

**Changes needed**: MODERATE

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Summary",
    "project_name": "...",
    "unit": "...",
    "element_name": "ملخص الوحدة",
    "designer": "...",
    "date": "2026-02-08",
    "header_title": "قالب سيناريو ملخص",
    "summary": {
        "screen_description": "شاشة توضيحية للملخص...",
        "content_text": "النص العلمي المعروض على الشاشة...",
        "key_terms": [
            {"term": "المصطلح", "definition": "التعريف"}
        ],
        "main_takeaways": ["النقطة الرئيسية 1", "النقطة الرئيسية 2"]
    }
}
```

**Lines to change**:
- Line 4: Tools
- Lines 39-41: Replace Output section
- Add: Content Schema, Separation of Concerns

**Keep unchanged**: Summary quality rules (lines 32-37)

---

### 10. storyboard-lecture.md (PPTX)

**Changes needed**: SIGNIFICANT -- this is the only PPTX agent

**Current approach**: Creates PPTX using `/pptx` skill directly.

**New approach**: Outputs structured slide content, calls `LectureBuilder` from the PPTX engine.

**Content Schema to add**:
```python
{
    "element_code": "DSAI_U01_Interactive_Lecture",
    "project_name": "...",
    "unit": "...",
    "element_name": "المحاضرة التفاعلية",
    "designer": "...",
    "date": "2026-02-08",
    "mode": "interactive",  # "interactive" | "pdf"
    "slides": [
        {
            "slide_number": 1,
            "slide_type": "title",  # "title" | "objectives" | "content" | "interaction" | "summary"
            "title": "عنوان الشريحة",
            "body_text": "محتوى الشريحة...",
            "bullet_points": ["نقطة 1", "نقطة 2"],
            "image_description": "",  # optional
            "image_path": "",  # optional, path to actual image
            "speaker_notes": "ملاحظات المقدم...",
            "interaction": {  # only for interactive mode
                "type": "اختيار من متعدد",
                "description": "وصف التفاعل...",
                "question": "...",
                "options": ["...", "..."],
                "correct": 0
            }
        }
    ]
}
```

**Lines to change**:
- Line 4: Tools -- change from `Read, Write, Edit, Glob, Grep, Skill` to `Read, Bash, Glob, Grep`
- Line 12: Remove template file reference
- Lines 51-56: Remove interaction instructions format (engine handles formatting)
- Lines 66-73: Replace Output section entirely
- Add: Content Schema (largest of all agents)
- Add: Separation of Concerns

**Keep unchanged**: Two modes section (lines 16-28), slide structure guidance (lines 30-48), quality standards (lines 58-64)

**Special considerations**:
- The lecture agent is unique because it produces PPTX, not DOCX
- It imports from `engine.pptx_engine` instead of `engine.docx_engine`
- The PDF lecture variant is handled by passing `"mode": "pdf"` to the builder
- The builder strips interaction elements when mode is "pdf"

---

## Dependency: Engine API Must Be Finalized First

Before editing any agent files, we need the final APIs from:

1. **Task #3 (DOCX engine)**: Must expose builder classes for all 8 DOCX types:
   - `ObjectivesBuilder`
   - `TestBuilder`
   - `ActivityBuilder`
   - `VideoBuilder`
   - `DiscussionBuilder`
   - `AssignmentBuilder`
   - `InfographicBuilder`
   - `SummaryBuilder`

2. **Task #4 (PPTX engine)**: Must expose:
   - `LectureBuilder` (already started in `engine/__init__.py`)

Once the APIs are finalized, the content schemas above may need adjustment to match the actual `build()` method signatures.

---

## Implementation Order

Recommended order for editing the agent files:

1. **storyboard-test.md** -- simplest content structure, good first test
2. **storyboard-objectives.md** -- simple content, similar structure
3. **storyboard-summary.md** -- simple content
4. **storyboard-discussion.md** -- simple content
5. **storyboard-assignment.md** -- simple content
6. **storyboard-infographic.md** -- moderate complexity
7. **storyboard-activity.md** -- complex scenes
8. **storyboard-video.md** -- complex scenes + images
9. **storyboard-lecture.md** -- PPTX, most complex, different engine

The analyst agent gets a minor tools-only update at any point.

---

## Validation Checklist

After updating each agent, verify:

- [ ] No references to template files in `templates/`
- [ ] No `/docx` or `/pptx` skill usage
- [ ] No `Write` or `Edit` in tools list (except analyst)
- [ ] Content Schema section is present and matches engine API
- [ ] Separation of Concerns section is present
- [ ] Output section shows the Bash command to call the builder
- [ ] All educational content guidance is preserved (quality rules, Bloom's, etc.)
- [ ] Arabic text requirements are preserved
- [ ] File naming convention is preserved in the builder call path
