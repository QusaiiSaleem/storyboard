# PPTX LectureBuilder API Reference

Complete API documentation for LectureBuilder in `engine/pptx_engine.py`.

## Constructor

```python
import sys
sys.path.insert(0, '/Users/qusaiabushanap/dev/storyboard')
from engine.pptx_engine import LectureBuilder

builder = LectureBuilder(
    project_code="DSAI",
    unit_number=1,
    unit_name="المهارات الرقمية",
    institution="جامعة نجران - كلية علوم الحاسب ونظم المعلومات",
    designer="أحمد",  # optional
)
```

## 12 Slide Methods

### 1. add_title_slide(title, subtitle, start_button_text)

Opening slide. Sets `builder.lecture_title` used on all subsequent slides.

- `title: str` -- Main lecture title
- `subtitle: str` -- Subtitle (optional, default: "")
- `start_button_text: str` -- Button text (default: "ابدأ المحاضرة")

### 2. add_objectives_slide(objectives)

Numbered objectives with colored background rows.

- `objectives: list[str]` -- List of objective strings (3-5 recommended)

### 3. add_content_slide(title, bullets, paragraphs, image_placeholder, image_path, image_prompt, notes)

Main workhorse slide with title banner and body text. **Automatically cycles between 3 layout variants** (A: full-width card, B: accent stripe + narrower card, C: numbered points) for visual variety. Image mode always uses Variant A.

- `title: str` -- Section title
- `bullets: list[str]` -- Bullet points (use this OR paragraphs)
- `paragraphs: list[str]` -- Paragraph text (use this OR bullets)
- `image_placeholder: str` -- Gray box with text label (fallback)
- `image_path: str` -- **Path to real image file** (takes priority over placeholder). 9x9cm bounding box, left side. Shape name: `img_content`
- `image_prompt: str` -- **AI image generation prompt** (English). Auto-generates image if no image_path. Priority: image_path > image_prompt
- `notes: str` -- Speaker notes / Storyline instructions

### 4. add_content_with_cards(title, cards, notes)

2-4 cards layout for concepts.

- `title: str` -- Section title
- `cards: list[dict]` -- Each dict: `{"title": "...", "body": "...", "color": RGBColor, "image": "/path/to/img.png", "image_prompt": "..."}` (body, color, image, image_prompt optional). When image present, title/body shift down. Shape name: `img_card_N`. Priority: `image` > `image_prompt`
- `notes: str` -- Speaker notes

### 5. add_section_divider(section_title, section_subtitle, section_number, total_sections, image_path, image_prompt)

Full-color section transition slide with decorative corners and optional progress dots.

- `section_title: str` -- Main section title
- `section_subtitle: str` -- Optional subtitle
- `section_number: int` -- Current section number (optional, enables progress dots)
- `total_sections: int` -- Total sections count (optional, enables progress dots)
- `image_path: str` -- Optional background illustration (8x8cm, bottom-left). Shape name: `img_section_bg`
- `image_prompt: str` -- AI image generation prompt (English). Used if no image_path

### 6. add_quiz_slide(question, options, correct_index, quiz_number, total_quizzes, image_path, image_prompt)

MCQ quiz with letter badges. Correct answer stored in slide notes.

- `question: str` -- Question text
- `options: list[str]` -- Answer options (2-4)
- `correct_index: int` -- Zero-based index of correct answer
- `quiz_number: int` -- Quiz number (default: 1)
- `total_quizzes: int` -- Total quizzes (default: 5)
- `image_path: str` -- Optional illustration next to question (7x5cm, left). Shape name: `img_quiz`
- `image_prompt: str` -- AI image generation prompt (English). Used if no image_path

### 7. add_drag_drop_slide(question, items, correct_order, quiz_number)

Drag-and-drop classification activity.

- `question: str` -- Instruction text
- `items: list[str]` -- Draggable item strings
- `correct_order: list[str]` -- Correct classification for each item
- `quiz_number: int` -- Activity number

### 8. add_two_column_slide(title, left_title, left_points, right_title, right_points, notes, right_image, left_image, right_image_prompt, left_image_prompt)

Side-by-side comparison (RTL: right column appears first).

- `title: str` -- Section title
- `left_title: str` -- Left column title
- `left_points: list[str]` -- Left column bullets
- `right_title: str` -- Right column title
- `right_points: list[str]` -- Right column bullets
- `notes: str` -- Speaker notes
- `right_image: str` -- Optional image above right column header (4cm tall). Shape name: `img_col1`
- `left_image: str` -- Optional image above left column header (4cm tall). Shape name: `img_col2`
- `right_image_prompt: str` -- AI image generation prompt for right column. Used if no right_image
- `left_image_prompt: str` -- AI image generation prompt for left column. Used if no left_image

### 9. add_click_reveal_slide(title, instruction, reveal_items, notes)

Click-to-reveal interaction.

- `title: str` -- Section title
- `instruction: str` -- Instruction text
- `reveal_items: list[dict]` -- Each dict: `{"label": "...", "description": "..."}`
- `notes: str` -- Speaker notes

### 10. add_summary_slide(summary_items)

Recap slide with blue text.

- `summary_items: list` -- List of strings OR list of dicts: `{"title": "...", "text": "..."}`

### 11. add_slider_slide(title, items, notes)

Slider/scroll interaction.

- `title: str` -- Instruction text
- `items: list` -- List of dicts: `{"number": "1", "text": "..."}` or plain strings
- `notes: str` -- Speaker notes

### 12. add_dropdown_slide(title, instruction, items, notes)

Dropdown matching activity.

- `title: str` -- Activity title
- `instruction: str` -- Instruction text
- `items: list[dict]` -- Each dict: `{"text": "...", "correct": "..."}`
- `notes: str` -- Speaker notes

## Save

```python
builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
```

`save()` auto-calls `finalize()` which adds click actions to buttons.

## Storyline 360 Compatibility

The engine automatically handles Storyline import requirements:

- **TOC Titles**: Every slide gets a hidden off-screen title so Storyline's sidebar shows Arabic titles (not "Untitled Slide")
- **No Page Numbers**: Page numbers are omitted — Storyline's player handles navigation
- **Import Instructions**: Title slide speaker notes contain import steps, required fonts, QA checklist, and shape naming guide
- **Shape Names**: All interactive shapes use naming convention (`btn_*`, `opt_*`, `txt_*`, `bg_*`, `icon_*`, `num_*`) for easy Storyline trigger setup
- **Story Size**: Design target is 1280x720 pixels

## Design Features

- **Layout Variants**: Content slides auto-cycle between 3 layouts (A: card, B: accent stripe, C: numbered points)
- **Real Shadows**: Cards use OOXML `outerShdw` effects (not fake offset rectangles)
- **Corner Radius**: Rounded rectangles use context-appropriate radii (0.04 for cards, 0.06 for quiz options, 0.08 for tabs)
- **Progress Dots**: Section dividers can show current position via `section_number`/`total_sections` params
- **Decorative Assets**: Section dividers and closing slides use `corner_tr.png`/`corner_bl.png` template assets

## Full Example

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

builder.add_objectives_slide(objectives=[
    "تعريف ماهي التقنية الناشئة.",
    "التعرف إلى فوائد التقنيات الرقميّة.",
])

builder.add_content_slide(
    title="المقدمة",
    bullets=["أصبحت التقنية الرقمية جزءاً من حياتنا"],
    image_prompt="flat vector of digital technology in daily life",
)

builder.add_content_with_cards(
    title="أمثلة على التقنيات الناشئة",
    cards=[
        {"title": "الذكاء الاصطناعي", "body": "وصف..."},
        {"title": "إنترنت الأشياء", "body": "وصف..."},
    ]
)

builder.add_section_divider(section_title="المحور الثاني", section_subtitle="فوائد التقنية")

builder.add_two_column_slide(
    title="مقارنة",
    right_title="الفوائد", right_points=["تسريع الوصول"],
    left_title="السلبيات", left_points=["الإدمان الرقمي"],
)

builder.add_quiz_slide(
    question="أي العبارات تعبر عن التقنية الناشئة؟",
    options=["خيار 1", "خيار 2", "خيار 3"],
    correct_index=1,
)

builder.add_drag_drop_slide(
    question="صنف: فوائد أم سلبيات؟",
    items=["تسريع الوصول", "الإدمان الرقمي"],
    correct_order=["فائدة", "سلبية"],
)

builder.add_click_reveal_slide(
    title="تأثير التقنية",
    instruction="انقر لاكتشاف المزيد",
    reveal_items=[
        {"label": "التعليم", "description": "أثرت التقنية على التعليم..."},
    ]
)

builder.add_summary_slide(["التقنيات الناشئة هي تقنيات في مراحلها الأولى"])

builder.add_closing_slide(next_steps=["مراجعة المحاضرة", "حل النشاط التفاعلي"])

builder.save("output/DSAI/U01/DSAI_U01_Interactive_Lecture.pptx")
```
