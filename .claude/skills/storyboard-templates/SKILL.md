---
name: storyboard-templates
description: Template engine API reference for generating DOCX and PPTX educational storyboard documents. Loaded by storyboard agents when generating documents.
---

# Storyboard Template Engine API

This skill documents the complete Python engine that generates production-ready DOCX and PPTX storyboard documents. The engine uses a "template-as-code" approach -- building documents from scratch to match the exact visual design of the original templates.

**NEVER edit template files directly.** Always use the engine builders below.

## Import Paths

```python
import sys
sys.path.insert(0, '/Users/qusaiabushanap/dev/storyboard')

# DOCX builders (8 types)
from engine.docx_engine import (
    TestBuilder,           # Pre-test, post-test, course exam
    ActivityBuilder,       # Interactive activities with scenes
    VideoBuilder,          # Motion video with narration scenes
    ObjectivesBuilder,     # Learning objectives (Group A)
    SummaryBuilder,        # Unit summary (Group A)
    InfographicBuilder,    # Learning map / infographic (Group A)
    DiscussionBuilder,     # Discussion activity (Group B)
    AssignmentBuilder,     # Assignment (Group B)
)

# PPTX builder (1 type)
from engine.pptx_engine import LectureBuilder  # Interactive & PDF lectures
```

## Common Constructor Pattern (All DOCX Builders)

Every DOCX builder inherits from `DocxBuilder` and takes the same constructor parameters:

```python
builder = AnyBuilder(
    project_code="DSAI",          # Short project code
    unit_number=1,                # Integer unit number
    unit_name="المهارات الرقمية",   # Arabic unit name
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",  # Full project name
    institution="جامعة نجران",     # Client/institution name
    designer="أحمد",              # Designer name
)
```

### Common Methods (All DOCX Builders)

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_element_name(name)` | `name: str` | Set element name (e.g. "الاختبار القبلي") |
| `set_element_code(code)` | `code: str` | Set element code (e.g. "DSAI_U01_Pre_Test"). Auto-generated if not called. |
| `set_date(date_str)` | `date_str: str` | Set date (default: today). Format: "YYYY-MM-DD" |
| `build()` | none | Build the complete document (metadata + content + footer). Call AFTER setting all content. |
| `save(output_path)` | `output_path: str` | Save to disk. Creates parent directories automatically. |

### Execution Pattern

Always call methods in this order:
1. Constructor
2. `set_element_name()` + `set_element_code()`
3. Type-specific content methods (see each builder below)
4. `build()`
5. `save()`

Run via Bash: `python3 -c "..."` with the full script.

---

## GROUP A Builders: ObjectivesBuilder, SummaryBuilder, InfographicBuilder

These three builders share an identical infographic-style content table structure.

### Content Methods (Group A)

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_screen_description(value)` | `value: str` | Screen/infographic visual description (row 1) |
| `set_content_text(value)` | `value: str` | Main content text displayed on screen (row 2) |
| `set_image_sources(value)` | `value: str` | Image sources/credits (row 3) |
| `set_detailed_description(value)` | `value: str` | Detailed screen description (row 4) |

### ObjectivesBuilder

Used for: Learning Objectives (الأهداف التعليمية)

```python
from engine.docx_engine import ObjectivesBuilder

builder = ObjectivesBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("الأهداف التعليمية")
builder.set_element_code("DSAI_U01_MLO")
builder.set_screen_description("وصف شاشة الأهداف التعليمية")
builder.set_content_text(
    "1. أن يُعرّف المتعلم مفهوم التقنية الناشئة\n"
    "2. أن يُحدد المتعلم فوائد التقنية الرقمية\n"
)
builder.set_image_sources("أيقونات الأهداف التعليمية")
builder.set_detailed_description("")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Learning_Objectives.docx")
```

### SummaryBuilder

Used for: Unit Summary (الملخص)

```python
from engine.docx_engine import SummaryBuilder

builder = SummaryBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("ملخص الوحدة")
builder.set_element_code("DSAI_U01_Summary")
builder.set_screen_description("شاشة توضيحية للملخص")
builder.set_content_text("ملخص المحتوى التعليمي...")
builder.set_image_sources("")
builder.set_detailed_description("")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Summary.docx")
```

### InfographicBuilder

Used for: Learning Map / Infographic (خارطة التعلم)

```python
from engine.docx_engine import InfographicBuilder

builder = InfographicBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("خارطة التعلم")
builder.set_element_code("DSAI_U01_Learning_Map")
builder.set_screen_description("الإرشادات التعليمية...")
builder.set_content_text("خطوات التعلم في هذه الوحدة...")
builder.set_image_sources("أيقونة اختبار\nأيقونة محتوى")
builder.set_detailed_description("")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Learning_Map.docx")
```

---

## GROUP B Builders: DiscussionBuilder, AssignmentBuilder

These two builders share a card-style content table with invisible white inner borders.

### Content Methods (Group B)

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_screen_description(value)` | `value: str` | Screen description (row 1) |
| `set_content_text(value)` | `value: str` | Main content text (row 2) |
| `set_instructions(value)` | `value: str` | Instructions/guidelines (row 3) |
| `set_related_objectives(value)` | `value: str` | Related learning objectives (row 4) |
| `set_content(label_key, value)` | `label_key: str, value: str` | Set content by exact Arabic label key |

### DiscussionBuilder

Used for: Discussion (النقاش)

```python
from engine.docx_engine import DiscussionBuilder

builder = DiscussionBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("نقاش الوحدة الأولى")
builder.set_element_code("DSAI_U01_Discussion")
builder.set_screen_description("شاشة توضيحية تعرض سؤال النقاش")
builder.set_content_text("ناقش مع زملائك: كيف يمكن...")
builder.set_instructions("احترم آراء الجميع وشارك بآراء مدعمة...")
builder.set_related_objectives("1. أن يُحلل المتعلم تأثير التقنية...")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Discussion.docx")
```

### AssignmentBuilder

Used for: Assignment (الواجب)

```python
from engine.docx_engine import AssignmentBuilder

builder = AssignmentBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("واجب الوحدة الأولى")
builder.set_element_code("DSAI_U01_Assignment")
builder.set_screen_description("شاشة توضيحية تعرض الواجب")
builder.set_content_text("اكتب مقالة من 500 كلمة...")
builder.set_instructions("صيغة التسليم: ملف Word\nالموعد النهائي: نهاية الأسبوع")
builder.set_related_objectives("1. أن يُطبق المتعلم مفاهيم التقنية...")
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Assignment.docx")
```

---

## TestBuilder

Used for: Pre-Test (اختبار قبلي), Post-Test (اختبار بعدي), Course Exam (اختبار المقرر)

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `set_test_info(description, instructions)` | `description: str, instructions: str` | Set test description and instructions |
| `add_question(question_text, choices, correct_answer, image_description)` | See below | Add one question. Call multiple times for multiple questions. |

**add_question parameters:**
- `question_text: str` -- The question in Arabic
- `choices: str` -- Answer choices, newline-separated: `"أ) ...\nب) ...\nج) ...\nد) ..."`
- `correct_answer: str` -- Correct answer letter/text (e.g. "ب")
- `image_description: str` -- Optional image link/description (use "" if none)

```python
from engine.docx_engine import TestBuilder

builder = TestBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("الاختبار القبلي")
builder.set_element_code("DSAI_U01_Pre_Test")
builder.set_test_info(
    description="الاختبار القبلي للوحدة الأولى",
    instructions="المحاولات المتاحة: محاولة واحدة"
)
builder.add_question(
    question_text="ما هو الذكاء الاصطناعي؟",
    choices="أ) برنامج حاسوبي\nب) فرع من علوم الحاسب\nج) لغة برمجة\nد) نظام تشغيل",
    correct_answer="ب",
    image_description=""
)
# Add more questions...
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Pre_Test.docx")
```

---

## ActivityBuilder

Used for: Interactive Activity (نشاط تفاعلي)

Each activity has one or more **scenes**. Call `add_scene()` for each scene.

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `add_scene(...)` | See below | Add a scene to the activity. Call multiple times for multi-scene activities. |

**add_scene parameters:**
- `title: str` -- Scene title (e.g. "المشهد الأول")
- `description: str` -- Scene description text (row 2 col 0)
- `elements: str` -- Scene elements content (row 2 col 1)
- `image_desc: str` -- Image descriptions (default: "-")
- `motion_desc: str` -- Motion graphic description (default: "-")
- `sound_effects: str` -- Sound effects description (default: "-")
- `on_screen_text: str` -- Text shown on screen (includes feedback text)
- `steps: str` -- Activity steps
- `correct_answer: str` -- Correct answer text
- `buttons: str` -- Buttons after attempts (default: 'زر "مراجعة المحتوى"\nزر "أعد المحاولة"')

```python
from engine.docx_engine import ActivityBuilder

builder = ActivityBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("النشاط التفاعلي 1.1")
builder.set_element_code("DSAI_U01_Activity1.1")
builder.add_scene(
    title="المشهد الأول",
    description="في هذا المشهد يظهر للطالب سؤال...",
    elements="يظهر السؤال مع أربعة خيارات...",
    image_desc="صورة توضيحية للمفهوم",
    motion_desc="-",
    sound_effects="-",
    on_screen_text="السؤال: ...\nالتغذية الراجعة: ...",
    steps="على الطالب اختيار الإجابة الصحيحة. عدد المحاولات: 2",
    correct_answer="ب) فرع من علوم الحاسب",
    buttons='زر "مراجعة المحتوى"\nزر "أعد المحاولة"',
)
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Activity1.1.docx")
```

---

## VideoBuilder

Used for: Motion Video (فيديو موشن)

**Note:** VideoBuilder has a 6-row metadata table (missing the unit row) and overrides the metadata table method.

Each video has one or more **scenes**. Each scene has **narration segments** (rows in a 4-column grid).

### Content Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `add_scene(...)` | See below | Add a scene with narration segments. Call multiple times. |

**add_scene parameters:**
- `title: str` -- Scene title (e.g. "مشهد العنوان")
- `screen_description: str` -- Visual description for the scene
- `sound_effects: str` -- Special sound effects
- `narration_segments: list[dict]` -- List of narration dicts, each with:
  - `"narration"` -- The narrated/read text
  - `"on_screen_text"` -- Text shown on screen
  - `"scene_description"` -- Detailed scene description with sync timing
  - `"image_links"` -- Image source links/descriptions

```python
from engine.docx_engine import VideoBuilder

builder = VideoBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران", designer="أحمد",
)
builder.set_element_name("فيديو موشن الوحدة 1")
builder.set_element_code("DSAI_U01_Video")
builder.add_scene(
    title="مشهد العنوان",
    screen_description="يظهر العنوان الرئيسي مع شعار الجامعة",
    sound_effects="موسيقى هادئة",
    narration_segments=[
        {
            "narration": "مرحبا بكم في الوحدة الأولى...",
            "on_screen_text": "المهارات الرقمية",
            "scene_description": "بالتزامن مع النص يظهر العنوان...",
            "image_links": "logo.png",
        },
    ]
)
builder.build()
builder.save("output/DSAI/U01/DSAI_U01_Video.docx")
```

---

## LectureBuilder (PPTX)

Used for: Interactive Lecture (محاضرة تفاعلية) and PDF Lecture (محاضرة PDF)

### Constructor

```python
from engine.pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="DSAI",             # Short project code
    unit_number=1,                   # Integer unit number
    unit_name="المهارات الرقمية",      # Arabic unit name
    institution="جامعة نجران",        # Institution name
    designer="أحمد",                 # Designer name (optional)
)
```

### Slide Methods (12 types)

#### 1. add_title_slide(title, subtitle, start_button_text)
Opening slide. Sets `builder.lecture_title` used on all subsequent slides.
- `title: str` -- Main lecture title
- `subtitle: str` -- Subtitle text (optional, default: "")
- `start_button_text: str` -- Button text (default: "ابدأ المحاضرة")

#### 2. add_objectives_slide(objectives)
Numbered objectives with colored background rows.
- `objectives: list[str]` -- List of objective strings (3-5 recommended)

#### 3. add_content_slide(title, bullets, paragraphs, image_placeholder, notes)
Main workhorse slide with title banner and body text.
- `title: str` -- Section title
- `bullets: list[str]` -- Bullet points (use this OR paragraphs)
- `paragraphs: list[str]` -- Paragraph text (use this OR bullets)
- `image_placeholder: str` -- Optional image area description (shifts text right)
- `notes: str` -- Speaker notes / Storyline instructions

#### 4. add_content_with_cards(title, cards, notes)
2-4 cards layout for concepts.
- `title: str` -- Section title
- `cards: list[dict]` -- Each dict has "title", "body" (optional), "color" (optional RGBColor)
- `notes: str` -- Speaker notes

#### 5. add_section_divider(section_title, section_subtitle)
Full-color section transition slide.
- `section_title: str` -- Main section title
- `section_subtitle: str` -- Optional subtitle

#### 6. add_quiz_slide(question, options, correct_index, quiz_number, total_quizzes)
MCQ quiz with letter badges. Correct answer stored in slide notes.
- `question: str` -- Question text
- `options: list[str]` -- Answer options (2-4)
- `correct_index: int` -- Zero-based index of correct answer
- `quiz_number: int` -- Quiz number (default: 1)
- `total_quizzes: int` -- Total quizzes (default: 5)

#### 7. add_drag_drop_slide(question, items, correct_order, quiz_number)
Drag-and-drop classification activity.
- `question: str` -- Instruction text
- `items: list[str]` -- Draggable item strings
- `correct_order: list[str]` -- Correct classification for each item
- `quiz_number: int` -- Activity number

#### 8. add_two_column_slide(title, left_title, left_points, right_title, right_points, notes)
Side-by-side comparison (RTL: right column appears first).
- `title: str` -- Section title
- `left_title: str` -- Left column title
- `left_points: list[str]` -- Left column bullets
- `right_title: str` -- Right column title
- `right_points: list[str]` -- Right column bullets
- `notes: str` -- Speaker notes

#### 9. add_summary_slide(summary_items)
Recap slide with blue text.
- `summary_items: list` -- Either list of strings or list of dicts with "title" and "text"

#### 10. add_closing_slide(next_steps)
Final "thank you" slide.
- `next_steps: list[str]` -- Optional list of next step strings

#### 11. add_slider_slide(title, items, notes)
Slider/scroll interaction.
- `title: str` -- Instruction text
- `items: list` -- List of dicts with "number" and "text", or plain strings
- `notes: str` -- Speaker notes

#### 12. add_dropdown_slide(title, instruction, items, notes)
Dropdown matching activity.
- `title: str` -- Activity title
- `instruction: str` -- Instruction text
- `items: list[dict]` -- Each dict has "text" and "correct"
- `notes: str` -- Speaker notes

### Save

```python
builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
```

### Full Example

```python
import sys
sys.path.insert(0, '/Users/qusaiabushanap/dev/storyboard')
from engine.pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="DSAI", unit_number=1,
    unit_name="المهارات الرقمية",
    institution="جامعة نجران - كلية علوم الحاسب ونظم المعلومات",
)
builder.add_title_slide(title="المحاضرة الأولى:", subtitle="المهارات الرقمية")
builder.add_objectives_slide(objectives=["تعريف ماهي التقنية الناشئة.", "التعرف إلى فوائد التقنيات الرقميّة."])
builder.add_content_slide(title="المقدمة", bullets=["أصبحت التقنية الرقمية جزءاً من حياتنا"])
builder.add_quiz_slide(question="ما هي التقنية الناشئة؟", options=["خيار 1", "خيار 2", "خيار 3"], correct_index=1)
builder.add_summary_slide(["التقنيات الناشئة هي تقنيات في مراحلها الأولى"])
builder.add_closing_slide(next_steps=["مراجعة المحاضرة", "حل النشاط التفاعلي"])
builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
```

---

## RTL Notes

The engine handles RTL automatically. Key internals (for debugging only):

- **python-docx**: `<w:bidi/>` on paragraphs, `<w:rtl/>` on runs, `<w:bidiVisual/>` on tables
- **python-pptx**: `pPr.set('rtl', '1')` on paragraphs
- **Font gotcha**: RTL causes `font.name` to be ignored -- must set `font.cs_name` / `w:rFonts w:cs` separately
- **Never reuse XML elements** across cells -- they get MOVED not copied
- Tables need `autofit = False` + explicit cell widths
- Shared helpers: `engine/rtl_helpers.py`

## Output Path Convention

```
output/[project-code]/U[XX]/[CODE]_U[XX]_[Element_Type].[ext]
```

Examples:
- `output/DSAI/U01/DSAI_U01_Pre_Test.docx`
- `output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx`
- `output/DSAI/U01/DSAI_U01_Activity1.1.docx`

## Builder-to-Storyboard Mapping

| Storyboard Type | Builder | File Extension |
|----------------|---------|---------------|
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

## Project Config

Agents should read project config from `projects/[project-code]/config.json` to populate builder constructor parameters.

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
