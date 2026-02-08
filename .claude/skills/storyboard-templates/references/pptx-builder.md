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

### 3. add_content_slide(title, bullets, paragraphs, image_placeholder, notes)

Main workhorse slide with title banner and body text.

- `title: str` -- Section title
- `bullets: list[str]` -- Bullet points (use this OR paragraphs)
- `paragraphs: list[str]` -- Paragraph text (use this OR bullets)
- `image_placeholder: str` -- Optional image area description
- `notes: str` -- Speaker notes / Storyline instructions

### 4. add_content_with_cards(title, cards, notes)

2-4 cards layout for concepts.

- `title: str` -- Section title
- `cards: list[dict]` -- Each dict: `{"title": "...", "body": "...", "color": RGBColor}` (body and color optional)
- `notes: str` -- Speaker notes

### 5. add_section_divider(section_title, section_subtitle)

Full-color section transition slide.

- `section_title: str` -- Main section title
- `section_subtitle: str` -- Optional subtitle

### 6. add_quiz_slide(question, options, correct_index, quiz_number, total_quizzes)

MCQ quiz with letter badges. Correct answer stored in slide notes.

- `question: str` -- Question text
- `options: list[str]` -- Answer options (2-4)
- `correct_index: int` -- Zero-based index of correct answer
- `quiz_number: int` -- Quiz number (default: 1)
- `total_quizzes: int` -- Total quizzes (default: 5)

### 7. add_drag_drop_slide(question, items, correct_order, quiz_number)

Drag-and-drop classification activity.

- `question: str` -- Instruction text
- `items: list[str]` -- Draggable item strings
- `correct_order: list[str]` -- Correct classification for each item
- `quiz_number: int` -- Activity number

### 8. add_two_column_slide(title, left_title, left_points, right_title, right_points, notes)

Side-by-side comparison (RTL: right column appears first).

- `title: str` -- Section title
- `left_title: str` -- Left column title
- `left_points: list[str]` -- Left column bullets
- `right_title: str` -- Right column title
- `right_points: list[str]` -- Right column bullets
- `notes: str` -- Speaker notes

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
