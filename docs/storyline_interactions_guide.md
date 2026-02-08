# Storyline Interactions Guide: PPTX to Articulate Storyline 360

A comprehensive reference for adding PowerPoint features (via python-pptx) that Articulate Storyline 360 recognizes when importing PPTX files.

**Last Updated:** 2026-02-08

---

## Table of Contents

1. [What Storyline Imports from PowerPoint](#1-what-storyline-imports-from-powerpoint)
2. [PowerPoint Animations and Storyline](#2-powerpoint-animations-and-storyline)
3. [Hyperlinks and Navigation](#3-hyperlinks-and-navigation)
4. [Speaker Notes and Storyline](#4-speaker-notes-and-storyline)
5. [Shape Naming Conventions](#5-shape-naming-conventions)
6. [Grouping and Layers](#6-grouping-and-layers)
7. [Quiz / Assessment Interactions](#7-quiz--assessment-interactions)
8. [python-pptx Capabilities for Interactions](#8-python-pptx-capabilities-for-interactions)
9. [Practical Implementation Plan by Slide Type](#9-practical-implementation-plan-by-slide-type)
10. [Code Examples](#10-code-examples)
11. [Priority Implementation Roadmap](#11-priority-implementation-roadmap)

---

## 1. What Storyline Imports from PowerPoint

### Features That ARE Preserved

| Feature | Status | Notes |
|---------|--------|-------|
| **Shapes** (rectangles, ovals, etc.) | Preserved | Become editable Storyline objects |
| **Text formatting** | Preserved | Font, size, color, bold, italic carry over |
| **Images** | Preserved | PNG, JPG import correctly |
| **Hyperlinks** (web URLs) | Preserved | External URLs import as triggers |
| **Speaker notes** | Preserved | Appear in Storyline's Notes panel |
| **Slide master** | Preserved | Imported as Storyline slide master |
| **Shape positions/sizes** | Preserved | Coordinates transfer accurately |
| **Simple groups** (single level) | Preserved | Group remains editable |
| **Supported animations** | Preserved | See Section 2 for the complete list |
| **Supported transitions** | Preserved | See Section 2 for the complete list |
| **SmartArt** (converted to shapes first) | Preserved | Must convert to shapes in PPT before importing |
| **Tables** | Partially preserved | Formatting may shift |

### Features That Are LOST or Changed

| Feature | What Happens |
|---------|-------------|
| **Emphasis animations** | Completely dropped (not imported at all) |
| **Unsupported entrance/exit animations** | Converted to Fade |
| **Unsupported motion paths** | Dropped entirely |
| **Nested groups** (groups within groups) | Flattened into a single image (not editable) |
| **VBA macros** | Dropped (but must be enabled for import to work) |
| **Some complex shapes** (curved arrows, etc.) | Converted to images |
| **Audio embedded in slides** | May not import; depends on format |
| **Video embedded in slides** | May not import reliably |
| **Custom fonts** (not installed on Storyline machine) | Substituted with fallback fonts |
| **Morph transitions** (with images) | Partially supported; images may not morph correctly |

### Critical Best Practices for Import

1. **Match slide size** -- Set Storyline story size to match your PPTX slide dimensions BEFORE importing. Our templates use 16:9 widescreen (12192000 x 6858000 EMU / 33.87cm x 19.05cm).
2. **Avoid nested groups** -- Only use single-level grouping. If you have groups inside groups, ungroup everything and regroup as a flat group.
3. **Convert SmartArt** -- Right-click SmartArt, choose "Convert to Shapes" before importing into Storyline.
4. **Use supported animations only** -- Stick to the 15 entrance/exit animations Storyline supports (see Section 2).
5. **Install fonts** -- Ensure all fonts used in the PPTX are installed on the machine running Storyline.
6. **Save as .pptx** -- Always use the .pptx format (not .ppt or .pptm).

### Sources

- [Import PowerPoint Slides into Storyline 360](https://community.articulate.com/articles/articulate-storyline-360-user-guide-how-to-import-slides-from-powerpoint)
- [Storyline 360: Tips for Importing Microsoft PowerPoint and Articulate Presenter Content](https://articulate.com/support/article/Storyline-360-Tips-for-Importing-Microsoft-PowerPoint-and-Articulate-Presenter-Content)
- [How to convert PowerPoint to Storyline 360: 5 top tips (BrightCarbon)](https://www.brightcarbon.com/blog/convert-powerpoint-to-storyline-360/)
- [3 Tips for Importing PowerPoint Slides Into Storyline (Tim Slade)](https://timslade.com/blog/importing-powerpoint-slides-into-storyline/)

---

## 2. PowerPoint Animations and Storyline

### Storyline's 15 Supported Entrance/Exit Animations

These are the ONLY animations that survive a PowerPoint import. Any other animation type is either converted to Fade or dropped entirely.

| # | Animation Name | Type | PowerPoint Equivalent | OOXML Filter Value |
|---|---------------|------|----------------------|-------------------|
| 1 | **Fade** | Entrance/Exit | Fade | `fade` |
| 2 | **Fly In / Fly Out** | Entrance/Exit | Fly In / Fly Out | `blinds(horizontal)` or positional anim |
| 3 | **Float In / Float Out** | Entrance/Exit | Float In / Float Out | Positional + opacity anim |
| 4 | **Split** | Entrance/Exit | Split | `barn(inVertical)` |
| 5 | **Wipe** | Entrance/Exit | Wipe | `wipe(down)` |
| 6 | **Grow / Shrink** | Entrance/Exit | Grow & Turn variant | Scale transform |
| 7 | **Spin & Grow** | Entrance/Exit | Custom combo | Rotation + scale |
| 8 | **Grow & Spin** | Entrance/Exit | Custom combo | Scale + rotation |
| 9 | **Zoom** | Entrance/Exit | Zoom | `wheel(1)` or scale |
| 10 | **Swivel** | Entrance/Exit | Swivel | 3D rotation |
| 11 | **Bounce** | Entrance/Exit | Bounce | Positional with bounce easing |
| 12 | **Wheel** | Entrance/Exit | Wheel | `wheel(N)` |
| 13 | **Random Bars** | Entrance/Exit | Random Bars | `randombar(horizontal)` |
| 14 | **Shape** | Entrance/Exit | Shape | `box(in)` |
| 15 | **Spin** | Entrance/Exit | Spin | Rotation transform |

### What Happens to Unsupported Animations

- **Unsupported entrance/exit animations** --> Converted to **Fade**
- **Emphasis animations** --> **Completely removed** (Storyline does not support emphasis animations on import)
- **Unsupported motion paths** --> **Completely removed**
- **Supported motion paths** --> May import, but only the final path is preserved if multiple paths exist on one object

### Animation Timing Import

| PowerPoint Timing | Storyline Behavior |
|------------------|-------------------|
| **On Click** | Becomes a timeline cue; object appears when timeline reaches that point. User can convert to trigger. |
| **With Previous** | Starts at same timeline position as previous animation |
| **After Previous** | Starts after previous animation ends |
| **Duration** | Preserved (maps to animation duration on timeline) |
| **Delay** | Preserved (maps to delay before animation starts) |

### Supported Slide Transitions

Storyline 360 supports importing these PowerPoint slide transitions:

| Transition | Preserved? |
|-----------|-----------|
| **Fade** | Yes |
| **Push** | Yes |
| **Wipe** | Yes |
| **Split** | Yes |
| **Morph** | Yes (but images may not morph correctly; best added directly in Storyline) |
| **None** | Yes (no transition) |
| **All others** | Converted to Fade or removed |

### Recommendation for Our Engine

**Use only Fade and Wipe animations** in our generated PPTX files. These are:
- The most reliably imported
- The most professional-looking
- Universally supported across Storyline versions
- Simple enough to implement via OOXML XML manipulation

### Sources

- [Import PowerPoint Animations into Storyline 360](https://community.articulate.com/articles/articulate-storyline-360-user-guide-how-powerpoint-animations-transitions-are-imported)
- [Storyline 360: Understanding How PowerPoint Animations and Transitions Are Imported](https://community.articulate.com/kb/user-guides/storyline-360-understanding-how-powerpoint-animations-and-transitions-are-import/1098363)
- [Storyline 360: Adding Animations](https://community.articulate.com/kb/user-guides/storyline-360-adding-animations/1121958)
- [Storyline 360: Emphasis Animations (Jan 2024 Update)](https://blog.iconlogic.com/weblog/2024/01/articulate-storyline-360-january-2024-update-includes-library-of-entrance-animations.html)

---

## 3. Hyperlinks and Navigation

### What Imports

| Hyperlink Type | Storyline Behavior |
|---------------|-------------------|
| **External URL** (https://...) | Becomes a trigger: "Jump to URL/File" |
| **Internal slide link** (jump to slide N) | Becomes a trigger: "Jump to Slide" referencing the imported slide |
| **Action buttons** (Next, Previous, etc.) | Import as shapes; actions may need to be re-created as triggers |
| **mailto: links** | Imported but may need adjustment |

### Important Limitations

- Hyperlinks on shapes import more reliably than hyperlinks on text runs.
- Internal slide jumps depend on slide order being preserved during import.
- After import, all navigation is managed through Storyline's trigger system, so hyperlinks become starting points that the developer will refine.

### python-pptx Hyperlink Capabilities

python-pptx fully supports:
- **Shape-level hyperlinks** via `shape.click_action.hyperlink.address`
- **Internal slide jumps** via `shape.click_action.target_slide = slide_object`
- **Action types**: Next Slide, Previous Slide, First Slide, Last Slide, Named Slide

This is one of the **highest-value features** we can add because:
1. It is fully supported by python-pptx (no XML workarounds needed)
2. It imports reliably into Storyline
3. It saves the Storyline developer significant setup time

### Sources

- [Shape hyperlink - python-pptx 1.0.0 docs](https://python-pptx.readthedocs.io/en/latest/dev/analysis/shp-hyperlink.html)
- [Click Action-related Objects - python-pptx 1.0.0 docs](https://python-pptx.readthedocs.io/en/latest/api/action.html)
- [Import PowerPoint Slides into Storyline 360](https://community.articulate.com/articles/articulate-storyline-360-user-guide-how-to-import-slides-from-powerpoint)

---

## 4. Speaker Notes and Storyline

### How Notes Import

When PowerPoint slides are imported into Storyline 360:
- **Speaker notes** from PowerPoint appear in Storyline's **Notes panel** (bottom of the editor, next to Timeline and States tabs)
- Notes can be displayed in the published course by enabling "Notes" in the Storyline Player settings
- Notes can also be used as a **script for text-to-speech** narration (Storyline has a "Copy From Slide Notes" button)

### Our Engine Already Supports This

Our `pptx_engine.py` already has a `_add_notes()` method:

```python
def _add_notes(self, slide, notes_text: str):
    notes_slide = slide.notes_slide
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = notes_text
```

### Strategic Use of Notes

We should use speaker notes for structured metadata that helps the Storyline developer:

```
=== STORYLINE INSTRUCTIONS ===
Slide Type: Quiz - Multiple Choice
Correct Answer: B
Feedback (Correct): احسنت! الاجابة صحيحة
Feedback (Incorrect): للاسف، الاجابة غير صحيحة. حاول مرة اخرى
Points: 10
Attempts: 2

=== NARRATOR SCRIPT ===
في هذا السؤال، اختر الاجابة الصحيحة من الخيارات المتاحة

=== IMAGE LINKS ===
Background: https://example.com/image.png
```

This structured format means:
1. The Storyline developer gets clear instructions
2. The narrator script is ready for text-to-speech
3. Asset links are easily accessible

### Sources

- [Storyline 360: Adding Slide Notes](https://community.articulate.com/kb/user-guides/storyline-360-adding-slide-notes/1078897)
- [Storyline 360: Converting Text to Speech](https://community.articulate.com/articles/storyline-360-converting-text-to-speech)
- [Working with Notes Slides - python-pptx](https://python-pptx.readthedocs.io/en/latest/user/notes.html)

---

## 5. Shape Naming Conventions

### Why Shape Names Matter

When PowerPoint shapes are imported into Storyline, Storyline uses the shape names from PowerPoint in its **Timeline panel**. Well-named shapes make the Storyline developer's life much easier because:

1. They can quickly identify which shape is which (instead of "Rectangle 47", they see "btn_check_answer")
2. They can create triggers referencing shapes by meaningful names
3. It reduces errors when building interactivity

### python-pptx Supports Shape Naming

The `shape.name` property is **read/write** in python-pptx:

```python
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
shape.name = "btn_check_answer"  # This name appears in Storyline's timeline
```

### Recommended Naming Convention

We should use a prefix-based naming system:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `btn_` | Button (clickable) | `btn_next`, `btn_check`, `btn_reveal_1` |
| `txt_` | Text content area | `txt_question`, `txt_feedback_correct` |
| `img_` | Image placeholder | `img_hero`, `img_diagram` |
| `card_` | Content card | `card_1`, `card_2`, `card_3` |
| `opt_` | Quiz option/choice | `opt_a`, `opt_b`, `opt_c`, `opt_d` |
| `drop_` | Drop zone (drag-drop) | `drop_zone_1`, `drop_zone_2` |
| `drag_` | Draggable item | `drag_item_1`, `drag_item_2` |
| `reveal_` | Hidden content (click to reveal) | `reveal_content_1`, `reveal_content_2` |
| `header_` | Header/banner area | `header_bar`, `header_title` |
| `nav_` | Navigation element | `nav_back`, `nav_next`, `nav_menu` |
| `bg_` | Background element | `bg_card`, `bg_overlay` |
| `icon_` | Icon or small graphic | `icon_check`, `icon_arrow` |
| `label_` | Label text | `label_step_1`, `label_category` |
| `divider_` | Visual divider | `divider_horizontal` |
| `num_` | Page/slide number | `num_page` |
| `group_` | Group container | `group_question_1` |

### Naming by Slide Type

| Slide Type | Shape Names |
|-----------|-------------|
| **Title Slide** | `bg_title`, `txt_course_title`, `txt_subtitle`, `img_logo`, `btn_start` |
| **Objectives Slide** | `header_objectives`, `txt_obj_1`, `txt_obj_2`, `icon_obj_1`, `icon_obj_2` |
| **Content Slide** | `header_content`, `txt_body`, `img_illustration` |
| **Quiz Slide** | `txt_question`, `opt_a`, `opt_b`, `opt_c`, `opt_d`, `btn_check`, `txt_feedback` |
| **Click-Reveal** | `btn_reveal_1`, `btn_reveal_2`, `reveal_content_1`, `reveal_content_2` |
| **Drag-Drop** | `drag_item_1`, `drag_item_2`, `drop_zone_1`, `drop_zone_2`, `btn_submit` |
| **Cards** | `card_1`, `card_2`, `card_3`, `card_4`, `txt_card_1_title`, `txt_card_1_body` |
| **Section Divider** | `bg_divider`, `txt_section_title`, `txt_section_number` |
| **Summary** | `header_summary`, `txt_summary_1`, `txt_summary_2` |

### Sources

- [Shapes - python-pptx 1.0.0 docs](https://python-pptx.readthedocs.io/en/latest/api/shapes.html)
- [Feature: setters for Shape.id and .name - python-pptx GitHub Issue #95](https://github.com/scanny/python-pptx/issues/95)

---

## 6. Grouping and Layers

### How Groups Import into Storyline

| Group Type | Storyline Behavior |
|-----------|-------------------|
| **Single-level group** | Preserved as an editable group |
| **Nested groups** (group within group) | Flattened into a single uneditable **image** |
| **Ungrouped shapes** | Each shape imports as an individual object |

### Storyline Layers vs PowerPoint Groups

**Important**: PowerPoint groups do NOT become Storyline layers. Layers in Storyline are a completely separate concept (they are like additional slides that overlay the base slide). There is no PowerPoint feature that directly maps to Storyline layers.

However, we can **prepare shapes for easy layer creation** by:
1. Naming shapes with layer-indicating prefixes (e.g., `layer1_txt_content`, `layer1_img_diagram`)
2. Including instructions in speaker notes about which shapes should be moved to which layer
3. Positioning "layer content" shapes in consistent locations

### python-pptx Group Shape Support

python-pptx supports creating group shapes:

```python
group = slide.shapes.add_group_shape()
# Add shapes to the group via group.shapes
shape1 = group.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
shape2 = group.shapes.add_shape(MSO_SHAPE.RECTANGLE, left2, top2, width2, height2)
```

### Recommendations

1. **Use single-level groups only** -- never nest groups
2. **Group related interactive elements** -- e.g., group a button shape with its label text
3. **Name the group** -- `group.name = "group_quiz_option_a"`
4. **Use notes for layer instructions** -- tell the Storyline developer which shapes to move to layers

### Sources

- [5 FAQs About Using Grouped Objects in Storyline 360](https://community.articulate.com/blog/articles/5-faqs-about-using-grouped-objects-in-storyline-360/1096971)
- [Storyline 360: Working with Layers](https://community.articulate.com/kb/user-guides/storyline-360-working-with-layers/1137567)
- [Group Shape - python-pptx 1.0.0 docs](https://python-pptx.readthedocs.io/en/latest/dev/analysis/shp-group-shape.html)

---

## 7. Quiz / Assessment Interactions

### Can PowerPoint Quizzes Import as Storyline Quiz Slides?

**No.** Storyline quiz slides (Multiple Choice, True/False, Drag-and-Drop, etc.) are a native Storyline feature. There is no PowerPoint structure that automatically becomes a Storyline quiz slide on import.

However, we can **prepare quiz content** so that the Storyline developer can quickly convert our slides to quiz interactions:

### Strategy: Freeform Conversion

Storyline 360 has a powerful feature called **"Convert to Freeform"** that lets a developer take any regular slide and turn it into a graded quiz interaction. Our job is to make that conversion as easy as possible.

#### For Multiple Choice Questions

Create the slide with well-named shapes:

```
Shape: txt_question     --> "ما هو الذكاء الاصطناعي؟"
Shape: opt_a            --> "أ. علم الحاسوب فقط"
Shape: opt_b            --> "ب. محاكاة الذكاء البشري"  (correct)
Shape: opt_c            --> "ج. لغة برمجة"
Shape: opt_d            --> "د. نوع من الأجهزة"
Shape: btn_check        --> "تحقق من الإجابة"
```

Then in the notes:
```
=== QUIZ CONFIGURATION ===
Type: Multiple Choice
Correct Answer: B (opt_b)
Points: 10
Attempts: 2
Feedback Correct: احسنت! الذكاء الاصطناعي هو محاكاة الذكاء البشري
Feedback Incorrect: الاجابة غير صحيحة. الذكاء الاصطناعي يشير الى محاكاة الذكاء البشري
=== FREEFORM INSTRUCTIONS ===
1. Insert > Convert to Freeform > Pick One
2. Assign opt_a, opt_b, opt_c, opt_d as choices
3. Set opt_b as correct answer
4. Set to 2 attempts with "Try Again" layer
```

#### For True/False Questions

```
Shape: txt_question     --> "الذكاء الاصطناعي يمكنه التعلم من البيانات"
Shape: opt_true         --> "صحيح"  (correct)
Shape: opt_false        --> "خطأ"
```

#### For Drag-and-Drop

```
Shape: drag_item_1      --> "التعلم العميق"
Shape: drag_item_2      --> "التعلم الآلي"
Shape: drag_item_3      --> "معالجة اللغة"
Shape: drop_zone_1      --> "فرع من الذكاء الاصطناعي"
Shape: drop_zone_2      --> "تطبيقات عملية"
```

### Sources

- [Storyline 360: Converting an Existing Slide to a Freeform Interaction](https://community.articulate.com/kb/user-guides/storyline-360-converting-an-existing-slide-to-a-freeform-interaction/1141102)
- [Create Quizzes and Results Slides in Storyline](https://community.articulate.com/kb/storyline-360-onboarding/create-quizzes-and-results-slides-in-storyline/1210800)

---

## 8. python-pptx Capabilities for Interactions

### Capability Matrix

| Feature | python-pptx Support | Implementation Method |
|---------|--------------------|-----------------------|
| **Shape naming** | Full support | `shape.name = "btn_next"` |
| **External hyperlinks** | Full support | `shape.click_action.hyperlink.address = "https://..."` |
| **Internal slide jumps** | Full support | `shape.click_action.target_slide = slide_obj` |
| **Speaker notes** | Full support | `slide.notes_slide.notes_text_frame.text = "..."` |
| **Group shapes** | Full support | `slide.shapes.add_group_shape()` |
| **Entrance animations** | NOT supported natively | Requires direct XML manipulation |
| **Exit animations** | NOT supported natively | Requires direct XML manipulation |
| **Emphasis animations** | NOT supported natively | Not worth implementing (Storyline drops them) |
| **Motion paths** | NOT supported natively | Not worth implementing (unreliable import) |
| **Slide transitions** | NOT supported natively | Requires direct XML manipulation |
| **Action buttons** | Partial | Via click_action, but no built-in action button shapes |

### What We CAN Do Easily (Priority 1 -- No XML Hacking)

1. **Shape naming** -- Assign meaningful names to every shape
2. **Hyperlinks** -- Add click actions to buttons and navigation elements
3. **Internal navigation** -- Link buttons to jump to specific slides
4. **Speaker notes** -- Embed structured Storyline instructions
5. **Group shapes** -- Group related interactive elements

### What We CAN Do With XML Workarounds (Priority 2 -- Moderate Effort)

6. **Slide transitions** -- Add `<p:transition>` elements to slide XML
7. **Fade entrance animations** -- Add timing/animation XML to slides

### What We Should NOT Try (Not Worth the Effort)

8. Emphasis animations (Storyline drops them)
9. Complex motion paths (unreliable import)
10. Morph transitions (better added in Storyline directly)

### Sources

- [python-pptx 1.0.0 documentation](https://python-pptx.readthedocs.io/en/latest/)
- [Animation control - python-pptx GitHub Issue #400](https://github.com/scanny/python-pptx/issues/400)
- [python-pptx API: Shapes](https://python-pptx.readthedocs.io/en/latest/api/shapes.html)
- [python-pptx API: Action](https://python-pptx.readthedocs.io/en/latest/api/action.html)

---

## 9. Practical Implementation Plan by Slide Type

### Title Slide

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name shapes: `txt_course_title`, `txt_subtitle`, `img_logo`, `btn_start` | `shape.name = ...` | P1 |
| Add Fade transition to this slide | XML workaround | P2 |
| Add "Start Course" hyperlink to button | `click_action.target_slide` | P1 |
| Notes: course metadata, narrator welcome script | `_add_notes()` | P1 |

### Objectives Slide

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name shapes: `header_objectives`, `txt_obj_1` through `txt_obj_N` | `shape.name = ...` | P1 |
| Notes: learning objectives for Storyline developer reference | `_add_notes()` | P1 |

### Content Slide (Standard)

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name shapes: `header_content`, `txt_body`, `img_illustration` | `shape.name = ...` | P1 |
| Notes: narrator script for text-to-speech | `_add_notes()` | P1 |

### Content with Cards

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name each card: `card_1`, `card_2`, etc. | `shape.name = ...` | P1 |
| Name card titles/bodies: `txt_card_1_title`, `txt_card_1_body` | `shape.name = ...` | P1 |
| Notes: instructions to set up card flip or click-reveal in Storyline | `_add_notes()` | P1 |

### Quiz Slide (Multiple Choice)

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name question: `txt_question` | `shape.name = ...` | P1 |
| Name options: `opt_a`, `opt_b`, `opt_c`, `opt_d` | `shape.name = ...` | P1 |
| Name check button: `btn_check` | `shape.name = ...` | P1 |
| Notes: correct answer, feedback text, freeform conversion instructions | `_add_notes()` | P1 |
| Hyperlink on check button (placeholder -- Storyline developer will replace) | `click_action` | P2 |

### Click-Reveal Slide

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name reveal buttons: `btn_reveal_1`, `btn_reveal_2`, etc. | `shape.name = ...` | P1 |
| Name hidden content: `reveal_content_1`, `reveal_content_2`, etc. | `shape.name = ...` | P1 |
| Notes: layer setup instructions for each reveal | `_add_notes()` | P1 |
| Hyperlink on reveal buttons (placeholder triggers) | `click_action` | P2 |

### Drag-Drop Slide

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name draggable items: `drag_item_1`, `drag_item_2`, etc. | `shape.name = ...` | P1 |
| Name drop zones: `drop_zone_1`, `drop_zone_2`, etc. | `shape.name = ...` | P1 |
| Name submit button: `btn_submit` | `shape.name = ...` | P1 |
| Notes: correct pairings, freeform drag-drop conversion instructions | `_add_notes()` | P1 |

### Section Divider

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name shapes: `bg_divider`, `txt_section_title`, `txt_section_number` | `shape.name = ...` | P1 |
| Add Fade or Wipe transition | XML workaround | P2 |

### Summary Slide

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name shapes: `header_summary`, `txt_summary_1` through `txt_summary_N` | `shape.name = ...` | P1 |
| Notes: narrator wrap-up script | `_add_notes()` | P1 |

### Slider Slide

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name slider track: `slider_track` | `shape.name = ...` | P1 |
| Name slider thumb: `slider_thumb` | `shape.name = ...` | P1 |
| Name value labels: `label_min`, `label_max`, `label_current` | `shape.name = ...` | P1 |
| Notes: slider interaction setup instructions | `_add_notes()` | P1 |

### Dropdown Slide

| Enhancement | Method | Priority |
|------------|--------|----------|
| Name dropdown trigger: `btn_dropdown_1`, `btn_dropdown_2` | `shape.name = ...` | P1 |
| Name dropdown options: `dropdown_opt_1a`, `dropdown_opt_1b` | `shape.name = ...` | P1 |
| Notes: dropdown interaction setup instructions | `_add_notes()` | P1 |

---

## 10. Code Examples

### 10.1 Setting Shape Names

This is the simplest and highest-value change. After creating any shape, immediately set its name.

```python
# Current code (no name):
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)

# Enhanced code (with name):
shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
shape.name = "btn_check_answer"
```

For textboxes:
```python
txBox = slide.shapes.add_textbox(left, top, width, height)
txBox.name = "txt_question"
```

### 10.2 Adding Hyperlinks to Shapes

#### External URL hyperlink:
```python
# Make a shape link to a web page
button_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
button_shape.name = "btn_external_link"
button_shape.click_action.hyperlink.address = "https://example.com"
```

#### Internal slide jump:
```python
# Make a button jump to another slide in the same presentation
button_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
button_shape.name = "btn_next_section"

# target_slide must be an actual Slide object from the presentation
target_slide = prs.slides[5]  # Jump to slide 6 (0-indexed)
button_shape.click_action.target_slide = target_slide
```

#### Next/Previous slide navigation:
```python
from pptx.enum.action import PP_ACTION

# "Next slide" button
btn_next = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
btn_next.name = "nav_next"
# For next/previous, you set the action type directly:
btn_next.click_action.hyperlink.address = None  # Clear any existing
# Note: python-pptx does not have direct PP_ACTION.NEXT_SLIDE setter,
# but you can set target_slide to the next slide object:
current_index = list(prs.slides).index(slide)
if current_index + 1 < len(prs.slides):
    btn_next.click_action.target_slide = prs.slides[current_index + 1]
```

### 10.3 Structured Speaker Notes

```python
def _add_storyline_notes(self, slide, slide_type, **kwargs):
    """
    Add structured speaker notes with Storyline instructions.

    Args:
        slide: The slide object
        slide_type: Type of slide (e.g., "quiz_mc", "click_reveal", "content")
        **kwargs: Additional metadata (correct_answer, feedback, narrator_script, etc.)
    """
    notes_parts = []

    # Storyline instructions section
    notes_parts.append("=== STORYLINE INSTRUCTIONS ===")
    notes_parts.append(f"Slide Type: {slide_type}")

    if "correct_answer" in kwargs:
        notes_parts.append(f"Correct Answer: {kwargs['correct_answer']}")
    if "feedback_correct" in kwargs:
        notes_parts.append(f"Feedback (Correct): {kwargs['feedback_correct']}")
    if "feedback_incorrect" in kwargs:
        notes_parts.append(f"Feedback (Incorrect): {kwargs['feedback_incorrect']}")
    if "points" in kwargs:
        notes_parts.append(f"Points: {kwargs['points']}")
    if "attempts" in kwargs:
        notes_parts.append(f"Attempts: {kwargs['attempts']}")
    if "layer_instructions" in kwargs:
        notes_parts.append(f"\n=== LAYER SETUP ===")
        for instruction in kwargs['layer_instructions']:
            notes_parts.append(f"- {instruction}")

    # Narrator script section
    if "narrator_script" in kwargs:
        notes_parts.append(f"\n=== NARRATOR SCRIPT ===")
        notes_parts.append(kwargs['narrator_script'])

    # Image/asset links
    if "image_links" in kwargs:
        notes_parts.append(f"\n=== IMAGE LINKS ===")
        for name, url in kwargs['image_links'].items():
            notes_parts.append(f"{name}: {url}")

    notes_text = "\n".join(notes_parts)
    notes_slide = slide.notes_slide
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = notes_text
```

### 10.4 Adding Slide Transitions via XML

python-pptx does not have a built-in API for transitions, but we can add them by directly manipulating the slide's XML. This uses the same pattern as our RTL helpers in `rtl_helpers.py`.

```python
from lxml import etree

# XML namespace for PresentationML
_PML_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
_PML_NSMAP = {"p": _PML_NS}


def add_slide_transition(slide, transition_type="fade", speed="med",
                         advance_on_click=True, advance_after_ms=None):
    """
    Add a slide transition to a slide via direct XML manipulation.

    This works because python-pptx preserves unknown XML elements when saving,
    so our manually-added <p:transition> element will survive the save process.

    Args:
        slide: A python-pptx Slide object
        transition_type: One of "fade", "push", "wipe", "split", "dissolve"
        speed: One of "slow", "med", "fast"
        advance_on_click: Whether clicking advances to next slide
        advance_after_ms: Auto-advance after N milliseconds (None = no auto-advance)

    Supported transition_type values and their OOXML elements:
        "fade"     -> <p:fade/>
        "push"     -> <p:push dir="l"/>  (push from left, good for RTL)
        "wipe"     -> <p:wipe dir="r"/>  (wipe from right, good for RTL)
        "split"    -> <p:split orient="horz" dir="out"/>
        "dissolve" -> <p:dissolve/>
    """
    sld_element = slide._element

    # Remove any existing transition element
    existing = sld_element.findall(f"{{{_PML_NS}}}transition")
    for elem in existing:
        sld_element.remove(elem)

    # Build the <p:transition> element
    transition_attribs = {"spd": speed}
    if advance_on_click:
        transition_attribs["advClick"] = "1"
    else:
        transition_attribs["advClick"] = "0"
    if advance_after_ms is not None:
        transition_attribs["advTm"] = str(advance_after_ms)

    transition_elem = etree.SubElement(
        sld_element,
        f"{{{_PML_NS}}}transition",
        attrib=transition_attribs,
    )

    # Add the transition type child element
    type_map = {
        "fade":     (f"{{{_PML_NS}}}fade", {}),
        "push":     (f"{{{_PML_NS}}}push", {"dir": "l"}),
        "wipe":     (f"{{{_PML_NS}}}wipe", {"dir": "r"}),
        "split":    (f"{{{_PML_NS}}}split", {"orient": "horz", "dir": "out"}),
        "dissolve": (f"{{{_PML_NS}}}dissolve", {}),
    }

    if transition_type in type_map:
        tag, attribs = type_map[transition_type]
        etree.SubElement(transition_elem, tag, attrib=attribs)


# Usage:
# add_slide_transition(slide, "fade", speed="med")
# add_slide_transition(slide, "wipe", speed="fast", advance_after_ms=3000)
```

**Important note on XML element ordering**: In OOXML, the `<p:transition>` element must appear after `<p:clrMapOvr>` and before `<p:timing>` in the slide XML. The `etree.SubElement` approach appends to the end, which may work in practice but could potentially cause validation issues. A more robust approach would insert at the correct position:

```python
def add_slide_transition_robust(slide, transition_type="fade", speed="med",
                                advance_on_click=True, advance_after_ms=None):
    """
    Robust version that inserts the transition element at the correct XML position.
    """
    sld_element = slide._element

    # Remove any existing transition element
    existing = sld_element.findall(f"{{{_PML_NS}}}transition")
    for elem in existing:
        sld_element.remove(elem)

    # Build the <p:transition> element
    transition_attribs = {"spd": speed}
    if advance_on_click:
        transition_attribs["advClick"] = "1"
    else:
        transition_attribs["advClick"] = "0"
    if advance_after_ms is not None:
        transition_attribs["advTm"] = str(advance_after_ms)

    transition_elem = etree.Element(
        f"{{{_PML_NS}}}transition",
        attrib=transition_attribs,
        nsmap=_PML_NSMAP,
    )

    # Add the transition type child element
    type_map = {
        "fade":     (f"{{{_PML_NS}}}fade", {}),
        "push":     (f"{{{_PML_NS}}}push", {"dir": "l"}),
        "wipe":     (f"{{{_PML_NS}}}wipe", {"dir": "r"}),
        "split":    (f"{{{_PML_NS}}}split", {"orient": "horz", "dir": "out"}),
        "dissolve": (f"{{{_PML_NS}}}dissolve", {}),
    }

    if transition_type in type_map:
        tag, attribs = type_map[transition_type]
        etree.SubElement(transition_elem, tag, attrib=attribs)

    # Insert at the correct position (after clrMapOvr, before timing)
    # Find the timing element to insert before it
    timing_elem = sld_element.find(f"{{{_PML_NS}}}timing")
    if timing_elem is not None:
        sld_element.insert(list(sld_element).index(timing_elem), transition_elem)
    else:
        sld_element.append(transition_elem)
```

### 10.5 Adding Fade Entrance Animation via XML

This is the most complex XML workaround. A Fade entrance animation requires building the full OOXML timing tree.

```python
from lxml import etree

_PML_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
_A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def add_fade_entrance_animation(slide, shape, delay_ms=0, duration_ms=500,
                                 trigger="onClick"):
    """
    Add a Fade entrance animation to a shape on a slide.

    WARNING: This is complex XML manipulation. Test thoroughly with your
    target version of Storyline before relying on it.

    Args:
        slide: A python-pptx Slide object
        shape: A python-pptx Shape object (must be on this slide)
        delay_ms: Delay before animation starts (milliseconds)
        duration_ms: Duration of the animation (milliseconds)
        trigger: "onClick", "withPrev", or "afterPrev"

    The OOXML structure for a fade animation is:
        <p:timing>
          <p:tnLst>
            <p:par>                              <!-- root timing node -->
              <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
                <p:childTnLst>
                  <p:seq concurrent="1" nextAc="seek">   <!-- click sequence -->
                    <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
                      <p:childTnLst>
                        <p:par>                  <!-- animation group -->
                          <p:cTn id="3" fill="hold">
                            <p:stCondLst>
                              <p:cond delay="0"/>
                            </p:stCondLst>
                            <p:childTnLst>
                              <p:par>            <!-- individual animation -->
                                <p:cTn id="4" presetID="10" presetClass="entr"
                                       presetSubtype="0" fill="hold">
                                  <p:stCondLst>
                                    <p:cond delay="0"/>
                                  </p:stCondLst>
                                  <p:childTnLst>
                                    <p:set>      <!-- visibility: hidden -> visible -->
                                      <p:cBhvr>
                                        <p:cTn id="5" dur="1" fill="hold">
                                          <p:stCondLst>
                                            <p:cond delay="0"/>
                                          </p:stCondLst>
                                        </p:cTn>
                                        <p:tgtEl>
                                          <p:spTgt spid="SHAPE_ID"/>
                                        </p:tgtEl>
                                        <p:attrNameLst>
                                          <p:attrName>style.visibility</p:attrName>
                                        </p:attrNameLst>
                                      </p:cBhvr>
                                      <p:to><p:strVal val="visible"/></p:to>
                                    </p:set>
                                    <p:animEffect transition="in" filter="fade">
                                      <p:cBhvr>
                                        <p:cTn id="6" dur="500"/>
                                        <p:tgtEl>
                                          <p:spTgt spid="SHAPE_ID"/>
                                        </p:tgtEl>
                                      </p:cBhvr>
                                    </p:animEffect>
                                  </p:childTnLst>
                                </p:cTn>
                              </p:par>
                            </p:childTnLst>
                          </p:cTn>
                        </p:par>
                      </p:childTnLst>
                    </p:cTn>
                    <p:prevCondLst>...</p:prevCondLst>
                    <p:nextCondLst>...</p:nextCondLst>
                  </p:seq>
                </p:childTnLst>
              </p:cTn>
            </p:par>
          </p:tnLst>
        </p:timing>
    """
    # Get the shape ID from the shape's XML element
    shape_id = str(shape.shape_id)

    sld = slide._element
    nsmap = {
        "p": _PML_NS,
        "a": _A_NS,
    }

    # Remove existing timing if present
    existing_timing = sld.findall(f"{{{_PML_NS}}}timing")
    for elem in existing_timing:
        sld.remove(elem)

    # Build the timing tree
    p = lambda tag: f"{{{_PML_NS}}}{tag}"

    timing = etree.SubElement(sld, p("timing"))
    tnLst = etree.SubElement(timing, p("tnLst"))

    # Root par
    par_root = etree.SubElement(tnLst, p("par"))
    cTn1 = etree.SubElement(par_root, p("cTn"),
                            attrib={"id": "1", "dur": "indefinite",
                                    "restart": "never", "nodeType": "tmRoot"})
    childTnLst1 = etree.SubElement(cTn1, p("childTnLst"))

    # Main sequence
    seq = etree.SubElement(childTnLst1, p("seq"),
                           attrib={"concurrent": "1", "nextAc": "seek"})
    cTn2 = etree.SubElement(seq, p("cTn"),
                            attrib={"id": "2", "dur": "indefinite",
                                    "nodeType": "mainSeq"})
    childTnLst2 = etree.SubElement(cTn2, p("childTnLst"))

    # Animation group par
    par_group = etree.SubElement(childTnLst2, p("par"))
    cTn3 = etree.SubElement(par_group, p("cTn"),
                            attrib={"id": "3", "fill": "hold"})
    stCondLst3 = etree.SubElement(cTn3, p("stCondLst"))
    etree.SubElement(stCondLst3, p("cond"), attrib={"delay": "0"})
    childTnLst3 = etree.SubElement(cTn3, p("childTnLst"))

    # Individual animation par
    par_anim = etree.SubElement(childTnLst3, p("par"))
    cTn4 = etree.SubElement(par_anim, p("cTn"),
                            attrib={"id": "4", "presetID": "10",
                                    "presetClass": "entr", "presetSubtype": "0",
                                    "fill": "hold"})
    stCondLst4 = etree.SubElement(cTn4, p("stCondLst"))
    cond_delay = str(delay_ms)
    etree.SubElement(stCondLst4, p("cond"), attrib={"delay": cond_delay})
    childTnLst4 = etree.SubElement(cTn4, p("childTnLst"))

    # Set element (visibility: hidden -> visible)
    set_elem = etree.SubElement(childTnLst4, p("set"))
    cBhvr_set = etree.SubElement(set_elem, p("cBhvr"))
    cTn5 = etree.SubElement(cBhvr_set, p("cTn"),
                            attrib={"id": "5", "dur": "1", "fill": "hold"})
    stCondLst5 = etree.SubElement(cTn5, p("stCondLst"))
    etree.SubElement(stCondLst5, p("cond"), attrib={"delay": "0"})
    tgtEl_set = etree.SubElement(cBhvr_set, p("tgtEl"))
    etree.SubElement(tgtEl_set, p("spTgt"), attrib={"spid": shape_id})
    attrNameLst = etree.SubElement(cBhvr_set, p("attrNameLst"))
    attrName = etree.SubElement(attrNameLst, p("attrName"))
    attrName.text = "style.visibility"
    to_elem = etree.SubElement(set_elem, p("to"))
    strVal = etree.SubElement(to_elem, p("strVal"), attrib={"val": "visible"})

    # animEffect (the actual fade)
    animEffect = etree.SubElement(childTnLst4, p("animEffect"),
                                  attrib={"transition": "in", "filter": "fade"})
    cBhvr_anim = etree.SubElement(animEffect, p("cBhvr"))
    cTn6 = etree.SubElement(cBhvr_anim, p("cTn"),
                            attrib={"id": "6", "dur": str(duration_ms)})
    tgtEl_anim = etree.SubElement(cBhvr_anim, p("tgtEl"))
    etree.SubElement(tgtEl_anim, p("spTgt"), attrib={"spid": shape_id})

    # Sequence navigation conditions
    prevCondLst = etree.SubElement(seq, p("prevCondLst"))
    etree.SubElement(prevCondLst, p("cond"), attrib={"evt": "onPrev", "delay": "0"})
    nextCondLst = etree.SubElement(seq, p("nextCondLst"))
    etree.SubElement(nextCondLst, p("cond"), attrib={"evt": "onNext", "delay": "0"})
```

**Important caveats for animation XML:**
- This code creates a single Fade animation for one shape. Adding multiple animations to the same slide requires extending the timing tree (not replacing it).
- The `presetID="10"` corresponds to Fade. Other IDs: Appear=1, Fly In=2, Blinds=3, Box=4, etc.
- This is fragile code. Always test the generated PPTX by opening it in PowerPoint first, then importing into Storyline.
- For production use, consider creating a reference PPTX file with the desired animations in PowerPoint, then examining its XML to get the exact structure.

### 10.6 Enhancing the _add_shape Method with Naming

Here is how we would modify the existing `_add_shape` helper in our engine:

```python
def _add_shape(
    self,
    slide,
    shape_type,
    left: int,
    top: int,
    width: int,
    height: int,
    fill_color: RGBColor = None,
    border_color: RGBColor = None,
    border_width=None,
    name: str = None,             # NEW parameter
):
    """
    Add a shape to a slide with optional fill, border, and name.
    """
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)

    # Set the shape name for Storyline identification
    if name:
        shape.name = name

    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color

    if border_color:
        shape.line.color.rgb = border_color
        if border_width:
            shape.line.width = border_width
    else:
        shape.line.fill.background()

    return shape
```

Similarly for `_add_arabic_textbox`:

```python
def _add_arabic_textbox(
    self,
    slide,
    left, top, width, height,
    text, font_name, font_size, bold, color,
    alignment=PP_ALIGN.RIGHT,
    name: str = None,             # NEW parameter
):
    """
    Add an Arabic RTL textbox with optional naming.
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)

    # Set the shape name for Storyline identification
    if name:
        txBox.name = name

    # ... rest of existing implementation ...
```

---

## 11. Priority Implementation Roadmap

### Phase 1: Quick Wins (Estimated: 1-2 hours)
These require NO XML workarounds, use fully supported python-pptx APIs.

| # | Task | Impact | Effort |
|---|------|--------|--------|
| 1 | **Add `name` parameter to `_add_shape()`** | High | Very Low |
| 2 | **Add `name` parameter to `_add_arabic_textbox()`** | High | Very Low |
| 3 | **Name all shapes in `add_quiz_slide()`** | Very High | Low |
| 4 | **Name all shapes in `add_click_reveal_slide()`** | Very High | Low |
| 5 | **Name all shapes in `add_drag_drop_slide()`** | Very High | Low |
| 6 | **Name all shapes in `add_content_with_cards()`** | High | Low |
| 7 | **Enhance `_add_notes()` with structured format** | High | Low |

### Phase 2: Navigation & Interactivity (Estimated: 2-3 hours)
These use python-pptx's click_action API (fully supported).

| # | Task | Impact | Effort |
|---|------|--------|--------|
| 8 | **Add "Start" button hyperlink on title slide** | Medium | Low |
| 9 | **Add navigation buttons (Next/Previous) to content slides** | Medium | Medium |
| 10 | **Add quiz check button click action** | Medium | Low |
| 11 | **Add structured Storyline instructions in notes for ALL slide types** | Very High | Medium |

### Phase 3: Transitions (Estimated: 2-3 hours)
These require XML workarounds but are well-understood patterns.

| # | Task | Impact | Effort |
|---|------|--------|--------|
| 12 | **Create `add_slide_transition()` helper function** | Medium | Medium |
| 13 | **Add Fade transitions to title and section divider slides** | Low | Low |
| 14 | **Add Wipe transitions to content slides** | Low | Low |

### Phase 4: Animations (Estimated: 4-6 hours)
These are complex XML manipulations. Only attempt after Phases 1-3 are stable.

| # | Task | Impact | Effort |
|---|------|--------|--------|
| 15 | **Create `add_fade_entrance_animation()` helper** | Medium | High |
| 16 | **Add Fade entrance to bullet points on content slides** | Medium | High |
| 17 | **Add Fade entrance to cards on card slides** | Medium | High |
| 18 | **Test all animations by importing into Storyline** | Critical | Medium |

### NOT Recommended (Skip These)

| Task | Why Skip |
|------|----------|
| Emphasis animations | Storyline drops them completely on import |
| Complex motion paths | Unreliable import; only final path kept |
| Morph transitions | Better added directly in Storyline |
| Action buttons (built-in PPT shapes) | Storyline may not recognize them; use regular shapes with click actions instead |

---

## Summary: The 80/20 Rule

**80% of the value comes from these 3 things:**

1. **Shape naming** -- Costs almost nothing to implement, saves the Storyline developer hours of work renaming "Rectangle 1", "Rectangle 2", etc.

2. **Structured speaker notes** -- Already have the `_add_notes()` method. Just need to use it strategically with Storyline instructions, correct answers, narrator scripts, and layer setup guides.

3. **Click actions / hyperlinks** -- Fully supported by python-pptx. Adding navigation and "check answer" triggers gives the Storyline developer a head start on building interactivity.

The remaining 20% (transitions, animations) is nice-to-have but requires XML manipulation and careful testing. Implement it only after the first three are stable and proven.

---

## References

### Articulate Storyline Documentation
- [Import PowerPoint Slides into Storyline 360](https://community.articulate.com/articles/articulate-storyline-360-user-guide-how-to-import-slides-from-powerpoint)
- [Understanding How PowerPoint Animations and Transitions Are Imported](https://community.articulate.com/kb/user-guides/storyline-360-understanding-how-powerpoint-animations-and-transitions-are-import/1098363)
- [Tips for Importing PowerPoint and Presenter Content](https://articulate.com/support/article/Storyline-360-Tips-for-Importing-Microsoft-PowerPoint-and-Articulate-Presenter-Content)
- [Storyline 360: Adding Animations](https://community.articulate.com/kb/user-guides/storyline-360-adding-animations/1121958)
- [Storyline 360: Converting an Existing Slide to a Freeform Interaction](https://community.articulate.com/kb/user-guides/storyline-360-converting-an-existing-slide-to-a-freeform-interaction/1141102)
- [Storyline 360: Working with Layers](https://community.articulate.com/kb/user-guides/storyline-360-working-with-layers/1137567)
- [5 FAQs About Using Grouped Objects in Storyline 360](https://community.articulate.com/blog/articles/5-faqs-about-using-grouped-objects-in-storyline-360/1096971)
- [Storyline 360: Adding Slide Notes](https://community.articulate.com/kb/user-guides/storyline-360-adding-slide-notes/1078897)
- [Storyline 360: Converting Text to Speech](https://community.articulate.com/articles/storyline-360-converting-text-to-speech)

### python-pptx Documentation
- [python-pptx 1.0.0 docs](https://python-pptx.readthedocs.io/en/latest/)
- [Shapes API](https://python-pptx.readthedocs.io/en/latest/api/shapes.html)
- [Click Action-related Objects](https://python-pptx.readthedocs.io/en/latest/api/action.html)
- [Shape Hyperlink Analysis](https://python-pptx.readthedocs.io/en/latest/dev/analysis/shp-hyperlink.html)
- [Group Shape Analysis](https://python-pptx.readthedocs.io/en/latest/dev/analysis/shp-group-shape.html)
- [Working with Notes Slides](https://python-pptx.readthedocs.io/en/latest/user/notes.html)
- [Animation Control Issue #400](https://github.com/scanny/python-pptx/issues/400)
- [Shape.name Setter Issue #95](https://github.com/scanny/python-pptx/issues/95)

### OOXML / Open XML Specifications
- [Office Open XML Slide Transitions](http://officeopenxml.com/prSlide-transitions.php)
- [Working with Animation - Open XML SDK](https://learn.microsoft.com/en-us/office/open-xml/presentation/working-with-animation)
- [How to Add Transitions Between Slides - Open XML SDK](https://learn.microsoft.com/en-us/office/open-xml/presentation/how-to-add-transitions-between-slides-in-a-presentation)
- [FadeTransition Class](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.fadetransition?view=openxml-2.8.1)
- [WipeTransition Class](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.wipetransition?view=openxml-2.8.1)
- [PushTransition Class](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.pushtransition?view=openxml-3.0.1)

### Community Resources
- [How to convert PowerPoint to Storyline 360: 5 top tips (BrightCarbon)](https://www.brightcarbon.com/blog/convert-powerpoint-to-storyline-360/)
- [3 Tips for Importing PowerPoint Slides Into Storyline (Tim Slade)](https://timslade.com/blog/importing-powerpoint-slides-into-storyline/)
- [How to Integrate PowerPoint Presentations in Articulate Storyline (GPI)](https://www.globalizationpartners.com/2021/08/19/integrate-powerpoint-presentations-articulate-storyline/)
