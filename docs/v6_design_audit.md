# PPTX Engine v6 — Comprehensive Design Audit

**File:** `engine/pptx_engine.py` (2,581 lines)
**Auditor:** Claude Opus 4.6 (senior graphic designer lens)
**Date:** 2026-02-08
**Slide dimensions:** 12,192,000 x 6,858,000 EMU (33.87 x 19.05 cm, 16:9 widescreen)

---

## Executive Summary

| Metric | Count |
|--------|-------|
| **Critical Bugs** | 5 |
| **Design Problems** | 14 |
| **Enhancement Opportunities** | 21 |
| **Overall Quality Score** | **5.5 / 10** |

The engine produces functional slides but has several critical overflow bugs that cause content to render off-screen. Beyond that, there are systematic design issues around vertical centering, missing overflow guards, inconsistent spacing, and a lack of adaptive layout logic. The code works well for "happy path" content volumes but breaks badly when real-world content arrives in larger-than-expected quantities.

---

## Top 5 Priority Fixes

1. **CRITICAL: Objectives slide overflows at 6+ objectives** — Row positioning is unbounded; 6 objectives push 236K EMU past the slide bottom, 8 objectives push 1.9M EMU past.
2. **CRITICAL: Click-reveal slide overflows at 7+ items** — Vertical list layout hits slide bottom at 7 items (666K EMU overflow).
3. **CRITICAL: Drag-drop slide overflows at 5+ items** — Both draggable items AND drop zones overflow at 5 items (551K EMU overflow).
4. **CRITICAL: Dropdown slide overflows at 6+ items** — No maximum item guard; 6 rows push 270K EMU past the bottom.
5. **HIGH: Section divider title/subtitle not vertically centered** — Title sits at 6.0cm but the blue background card extends from 2.0cm to 17.05cm, making the visual center 9.53cm. Content appears pushed up, not centered.

---

## 1. `add_title_slide()`

### Bugs
- None found. All elements stay within slide bounds.

### Problems
- **Hand cursor icon barely fits.** Bottom edge at 6,641,008 EMU leaves only 217K EMU (~0.6cm) margin to the slide bottom. On some renderers, anti-aliasing or scaling could clip this.
- **`auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT`** on the title/subtitle textbox means an unusually long title could push the text frame downward and overlap the button. No maximum height guard.
- **Play icon placement is absolute** (hard-coded at left=9476078). If the button text is shorter or longer than the default, the icon will not stay visually aligned with the button edge.
- **Institution name at Pt(24) ExtraBold is the same size as the lecture title** (also Pt(24) ExtraBold). There is no visual hierarchy distinction between these two text elements. The institution name should either be smaller or use a lighter weight.

### Enhancement Opportunities
- Add a thin decorative line between institution name and title to visually separate them.
- Consider dimming the institution name color (e.g., use a lighter shade of blue) to create hierarchy.
- Add a maximum character length guard or use `MSO_AUTO_SIZE.NONE` with word wrap to prevent title overflow.

---

## 2. `add_objectives_slide()` -- CRITICAL OVERFLOW BUG

### Bugs
- **CRITICAL: Content overflows slide bottom at 6+ objectives.**
  - 6 objectives: last row bottom = 7,094,319 EMU (236K past slide edge)
  - 7 objectives: last row bottom = 7,930,060 EMU (1.07M past slide edge)
  - 8 objectives: last row bottom = 8,765,801 EMU (1.9M past slide edge)
  - The `row_spacing` of 835,741 EMU (~2.32cm) is too generous. With `row_top_start` at 2,315,612 and `row_height` of 600,002, the maximum number of objectives that fit is **5**.
  - The target icon images (`target_icon.png`) placed at each row also overflow along with the rows.
- **No maximum item count guard.** The method accepts any length list without checking if it will fit.

### Problems
- **Objective text font at Pt(16) is too small for Arabic readability.** Arabic characters have more complex shapes than Latin and generally need 20%+ larger sizes. At Pt(16), text may appear cramped and hard to read on projected presentations. The rest of the engine uses Pt(18)+ for body text.
- **Fixed row spacing regardless of item count.** Unlike `add_content_with_cards()` which calculates card width dynamically, this method uses a fixed `row_spacing` that doesn't adapt.

### Enhancement Opportunities
- Implement adaptive row spacing: calculate `row_spacing` dynamically based on `len(objectives)` so that all rows fit between `row_top_start` and a safe bottom boundary (e.g., 6,400,000 EMU to leave room for page number).
- Increase objective text to Pt(18) for consistency with the rest of the engine.
- Add a maximum item count of 8 with auto-pagination (split into two slides) if exceeded.
- Consider adding a numbering indicator (e.g., "1.", "2.") to help learners reference specific objectives.

---

## 3. `add_content_slide()`

### Bugs
- None found. Content card bottom at 6,048,000 EMU is within bounds.

### Problems
- **Content card background (`#F5F7FA`) is added ONLY for bullet lists, not for paragraphs.** If the slide uses `paragraphs` instead of `bullets`, there is no visual container, making the slide look inconsistent with other slides.
- **Image placeholder area at Cm(9) x Cm(9)** is a fixed square. Real images are rarely square; this placeholder gives a misleading impression of the available space.
- **Content height at Cm(11.5)** with `MSO_AUTO_SIZE.NONE` means long bullet lists will be silently clipped without any warning. There is no overflow detection.
- **When image is present, content width shrinks to Cm(18).** Combined with large Pt(20) font and Arabic text that is naturally wider, this can cause severe wrapping that makes 3+ bullet points unreadable.

### Enhancement Opportunities
- Apply the content card background consistently for both bullets and paragraphs.
- Add text overflow detection: if the estimated text height exceeds the container, either reduce font size or split into a second slide.
- Make image placeholder aspect ratio configurable (16:9, 4:3, square).

---

## 4. `add_content_with_cards()`

### Bugs
- None found. Card bottom at 5,220,000 EMU is well within bounds.

### Problems
- **Card shadow is a flat colored rectangle, not a real shadow.** The shadow shape at `+Cm(0.1)` offset with `SHADOW_COLOR (#E0E0E0)` looks like a separate shape rather than a natural drop shadow. It would be more professional with a proper PowerPoint shadow effect.
- **Card body text height at Cm(5.5)** with `MSO_AUTO_SIZE.NONE` will silently clip long content. No overflow handling.
- **Only 3 default card colors** (`PRIMARY_BLUE`, `ACCENT1_BLUE`, `CARD_DARK2`). For 4 cards, the 4th card reuses `PRIMARY_BLUE`, making cards 1 and 4 visually identical. This breaks the "each card should be visually distinct" design principle.
- **All three default colors are dark blue shades.** There is insufficient color variation between the cards. The colors `#2D588C`, `#156082`, and `#0E2841` are all in the same blue family and would be hard to distinguish at a glance, especially on a projector.
- **Card accent bar at Cm(1.2) height** occupies 13.3% of the card. For a card that is Cm(9) tall, this is visually heavy and reduces the usable content area.

### Enhancement Opportunities
- Use python-pptx's built-in shadow effect instead of a manual offset rectangle.
- Add more diverse accent colors (e.g., teal, amber, green) while staying within a professional palette.
- Implement text truncation or font-size reduction for long card body text.
- Add an icon or number indicator to each card for visual interest.

---

## 5. `add_section_divider()`

### Bugs
- None found. All elements within slide bounds.

### Problems
- **Title and subtitle are NOT vertically centered in the blue background.** The blue card spans from 2.0cm to 17.05cm (center at 9.53cm), but the title sits at 6.0cm, which is 3.53cm above the visual center. This makes the slide look top-heavy.
- **Decorative line is at a fixed position (Cm(9.2))** that doesn't adjust if the title text wraps to multiple lines. A long title could overlap the line.
- **Decorative line at Cm(10) width is quite short** relative to the slide width (33.87cm). At only 29.5% of slide width, it feels visually insignificant.
- **No lecture title bar at the top**, unlike all other content slide types. This breaks visual consistency — every other slide type has the header bar, but the section divider skips it.

### Enhancement Opportunities
- Center the title vertically within the blue card. Calculate the vertical center dynamically based on whether a subtitle is present.
- Make the decorative line width proportional (e.g., 40-50% of slide width).
- Consider adding a subtle pattern or icon to the blue background to prevent it from looking like a flat color block.
- Add a slide number in white (like the closing slide does).

---

## 6. `add_quiz_slide()`

### Bugs
- **Feedback instruction text bottom at 6,768,000 EMU leaves only 90K EMU (~0.25cm) margin** to the slide bottom. While technically within bounds, this is dangerously close and any font rendering variation could clip it.

### Problems
- **The "Check Answer" button is at Cm(16), which equals 5,760,000 EMU.** With a Cm(1.6) height, the bottom is at 6,336,000 EMU. This is fine, BUT the feedback text below it at Cm(17.8) is at 6,408,000 EMU. Combined with the page number at 6,384,932 EMU, these two elements vertically overlap or nearly overlap.
- **Mixed languages in the feedback text**: `"Storyline: عند النقر على 'تحقق' تظهر التغذية الراجعة"` — mixing English ("Storyline:") and Arabic in the same text run without explicit LTR/RTL segment handling will cause rendering issues. The colon and English word may appear in the wrong position.
- **Right-side accent border at Cm(30.3)** creates a visual accent on the RIGHT side of the option row. In an RTL layout, this accent should arguably be more prominent or on the left (which is the trailing edge in RTL). The accent bar (Cm(0.2) wide) is quite narrow and may not be visible on projectors.
- **No guard for 5+ options.** While 4 options fit comfortably, if someone passes 5 options the 5th option background bottom would be at 6,516,000 EMU (close to limit) and the badge/text would be very tight.

### Enhancement Opportunities
- Move the feedback instruction text to speaker notes instead of on-slide, since it is a development instruction, not learner-facing content.
- Add visual feedback indicators (green checkmark, red X) as decorative elements.
- Guard against more than 4 options by raising a warning or paginating.

---

## 7. `add_drag_drop_slide()` -- CRITICAL OVERFLOW BUG

### Bugs
- **CRITICAL: Content overflows at 5+ items.**
  - 5 items: max bottom = 7,408,800 EMU (551K past slide edge)
  - 6 items: max bottom = 8,308,800 EMU (1.45M past slide edge)
  - 7 items: max bottom = 9,208,800 EMU (2.35M past slide edge)
  - Both the draggable item shapes (left side) AND the drop zone shapes (right side) overflow simultaneously.
  - The shadow shapes behind items also overflow.
- **No maximum item count guard.**

### Problems
- **Fixed item height of Cm(2) and gap of Cm(0.5)** means each item consumes 2.5cm. Starting at Cm(8.5), only 4 items fit before hitting the slide bottom.
- **Instruction text "اسحب العناصر التالية إلى الترتيب الصحيح" is hardcoded** and does not adapt to different activity types (e.g., classification vs. ordering).
- **Draggable items (left) and drop zones (right) have the same height but different widths** (Cm(12) each). With SLIDE_WIDTH of 33.87cm, items at Cm(2.5) and drops at Cm(18), there is a Cm(3.5) gap between them (Cm(2.5) + Cm(12) = Cm(14.5), gap to Cm(18) = Cm(3.5)). This gap is visually large and wastes space.
- **Drop zone number badges are positioned at the FAR RIGHT** of the drop zone. In RTL, this is the leading edge, which is correct, but the number is small (Pt(16)) and easy to miss.

### Enhancement Opportunities
- Implement adaptive layout: dynamically calculate `item_height` and `gap` based on `item_count` to fit all items within the safe area (below Cm(8.5), above Cm(17)).
- Set a maximum of 6 items with auto-pagination for larger sets.
- Add a visual arrow or connector between the drag items and drop zones to clarify the interaction model.
- Make the instruction text a parameter rather than hardcoded.

---

## 8. `add_two_column_slide()`

### Bugs
- None found. All elements within bounds.

### Problems
- **Column labels have center alignment while bullets have right alignment.** This creates a visual disconnect — the column title appears centered but bullets hang from the right. For RTL, the title should also be right-aligned, or the bullets should be center-aligned, for consistency.
- **Accent bar under column titles** is at `col_left + Cm(2)` and `col_width - Cm(4)`, which centers it under the title. At Cm(9.5) width for a Cm(13.5) column, this looks reasonable.
- **Vertical divider at Cm(16.2)** is between the two columns. However, the right column starts at Cm(17) and the left column ends at Cm(2.5) + Cm(13.5) = Cm(16). The divider at Cm(16.2) leaves only Cm(0.2) gap from the left column content and Cm(0.8) gap from the right column content. This asymmetry is visually noticeable.
- **No visual container (card/background) behind the columns**, unlike the content slide which has a card background. The columns float on the bare slide layout, which looks less polished.

### Enhancement Opportunities
- Add subtle card backgrounds behind each column (like `CONTENT_CARD_BG`).
- Center the vertical divider between the two columns (at Cm(16.25) or remove it and use the card gap as the visual separator).
- Use different accent colors for the two columns to reinforce the comparison.
- Add optional column icons/emojis for visual interest.

---

## 9. `add_click_reveal_slide()` -- CRITICAL OVERFLOW BUG

### Bugs
- **CRITICAL: Vertical list layout (>4 items) overflows at 7+ items.**
  - 7 items: last row bottom = 7,524,000 EMU (666K past slide edge)
  - 8 items: last row bottom = 8,280,000 EMU (1.42M past slide edge)
  - Row height Cm(1.8) + spacing Cm(0.3) = Cm(2.1) per item. Starting at Cm(6.5), only 6 items fit.
- **6 items just barely fit** (bottom at 6,768,000 EMU, only 90K EMU margin). The page number and any badge elements may clip.

### Problems
- **Description area for horizontal layout (<=4 items)** at `top=Cm(10.5), height=Cm(5)` has its bottom at Cm(15.5) = 5,580,000 EMU. This is comfortably within bounds, but the description text at `top=Cm(11)` only gets Cm(4) of effective height, which may clip longer descriptions.
- **Only the FIRST item's description is placed on-slide** for the horizontal layout. Other descriptions are only in the speaker notes. This means the static PPTX export shows only one description, making the slide look incomplete if viewed as a PDF or printout.
- **No label truncation guard.** Long labels in horizontal tabs will overflow the tab width since `MSO_AUTO_SIZE` is not explicitly set on tab text frames (defaults to `SHAPE_TO_FIT_TEXT` behavior of the text frame).
- **Vertical list layout uses number badges but horizontal layout does not.** This is inconsistent interaction design between the two layouts.

### Enhancement Opportunities
- Implement adaptive vertical spacing for the list layout (like the recommendation for objectives and drag-drop).
- Cap the maximum items at 6 for the list layout with auto-pagination beyond that.
- Add all descriptions to the slide (stacked or in a shared area with "layer X" naming for Storyline).
- Add tab numbers to horizontal tabs for consistency with the vertical layout.

---

## 10. `add_summary_slide()`

### Bugs
- None found. Card bottom at 5,292,000 EMU is safely within bounds.

### Problems
- **All summary text is in `LINK_BLUE` (#2E6CEC)** regardless of whether it is a link or not. This color signals "clickable link" to users but the text is not interactive. This is misleading UX.
- **No maximum items guard.** With `line_spacing=1.5` and `space_after=Pt(8)`, each item occupies approximately Cm(1.5). The text area is Cm(10) tall, fitting roughly 6-7 items. More items will be silently clipped.
- **The summary text box at Cm(29) width sits inside a Cm(30) wide card** with only Cm(0.5) left padding. The right padding is Cm(1.5) (card at Cm(2), text at Cm(2.5)). This asymmetric internal padding is visually noticeable in RTL where the right edge is the primary reading edge.

### Enhancement Opportunities
- Use `BODY_TEXT` (#333333) for summary text and only use `LINK_BLUE` for actual hyperlinks.
- Add numbered or bulleted markers to summary items for visual structure.
- Equalize internal card padding (both sides should have Cm(0.5) or both Cm(1)).
- Add a subtle icon or decorative element to the summary banner to differentiate it from regular content slides.

---

## 11. `add_closing_slide()`

### Bugs
- None found. All elements within bounds.

### Problems
- **"Thank you" text at Cm(5) top in a white card spanning Cm(3) to Cm(16.05)** is not vertically centered. The card's vertical center is at ~Cm(9.5), but the text is at Cm(5) + Cm(1.25) = Cm(6.25). This looks top-heavy.
- **Next steps text and bullets occupy Cm(10) to Cm(15)**, which is lower than the thank-you text. But with only Cm(1.05) margin to the bottom of the white card, it is tight.
- **No subtitle or additional context.** The closing slide jumps from "Thank you" directly to "Next steps" without the lecture title, unit name, or any other contextual information that would help learners recall what they just completed.
- **Page number is set to white** (`color=WHITE`) on a white background card, making it invisible to the viewer.

### Enhancement Opportunities
- Center "Thank you" and "Next steps" content vertically within the white card.
- Add the unit name or lecture title as a subtitle below "Thank you."
- Fix the page number color to be visible (e.g., `PRIMARY_BLUE` or place it outside the white card on the blue border area).
- Add a decorative element or icon (e.g., graduation cap, checkmark) to make the closing feel like a completion milestone.

---

## 12. `add_dropdown_slide()`

### Bugs
- **CRITICAL: Content overflows at 6+ items.**
  - 6 items: last row bottom = 7,128,000 EMU (270K past slide edge)
  - 7 items: last row bottom = 7,920,000 EMU (1.06M past slide edge)
  - Row spacing of Cm(2.2) with row height Cm(1.8) starting at Cm(7). Maximum 5 items fit.

### Problems
- **Dropdown indicator shows only "down arrow" without any text.** The dropdown shapes contain just a single character. In a static PPTX (non-Storyline), this gives no context about what the learner should select from.
- **No visual container or card background** behind the rows. The statements float on the bare slide, looking less polished than quiz or drag-drop slides.
- **Statement text at Cm(22) width is narrower than other slide types** because the dropdown indicator takes Cm(4). For long Arabic statements, this forces excessive line wrapping.

### Enhancement Opportunities
- Implement adaptive row spacing or pagination for 6+ items.
- Add category labels or hints to the dropdown shapes (e.g., "اختر...").
- Add alternating row backgrounds (like the quiz slide has) for better readability.
- Add a content card background behind all rows.

---

## 13. `_add_bullet_list()`

### Bugs
- None found.

### Problems
- **Bullet marker at Pt(12) is significantly smaller than body text** at Pt(16-20). The Unicode filled circle character at Pt(12) will appear as a tiny dot next to Pt(20) Arabic text. The visual weight is insufficient to serve as a bullet marker.
- **Bullet marker color (`BULLET_MARKER_COLOR` = `#2D588C`)** is the same as `PRIMARY_BLUE`. While this is intentional, the small size + dark color combination makes the marker look like a dot rather than a deliberate design element.
- **No indentation is applied.** The bullet marker and text are in the same run with just a space separator. This means the text after the marker does not have a hanging indent, and multi-line text wraps back to the left edge (right edge in RTL) instead of aligning with the first line of text.
- **`space_after = Pt(16)` creates very large gaps** between items (approximately 5.6mm between each bullet). For a Cm(11.5) container with Pt(20) text, this limits the visible bullets to about 6-7 items before clipping.

### Enhancement Opportunities
- Increase bullet marker to Pt(16) or Pt(18) to be visually proportional to body text.
- Implement hanging indent using `pPr.indent` and `pPr.marL` XML properties for proper multi-line bullet alignment.
- Use python-pptx's built-in bullet list features (`p.level`, `p.bullet`) instead of Unicode characters.
- Consider reducing `space_after` to Pt(10) for tighter but still readable lists.

---

## 14. `_add_section_banner()`

### Bugs
- None found.

### Problems
- **Narrow banner text at Pt(18)** may be too small for long Arabic section titles. The narrow banner text area is only 2,297,266 EMU wide (~6.38cm). A long title like "تأثير التقنية الناشئة على المجتمع العربي" would overflow this width.
- **No text truncation or font-size reduction** for titles that exceed the banner width. With `MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT` (the default from `_add_arabic_textbox`), the text frame may auto-shrink but could become unreadably small.
- **Banner text and banner image are separate elements.** If the text auto-sizes and changes position, it may no longer be visually centered on the banner image.

### Enhancement Opportunities
- Add a maximum character length check for narrow banners and auto-switch to wide banners for long titles.
- Set `MSO_AUTO_SIZE.NONE` with word wrap to prevent auto-shrinking.
- Consider programmatically calculating font size based on text length.

---

## 15. `add_slider_slide()`

### Bugs
- None found. 7 items fit within bounds (last bottom at 6,660,000 EMU, 198K margin).

### Problems
- **No section banner.** This slide type jumps directly to a title/instruction text at Cm(2.5) from the top, skipping the banner that every other content slide type uses. This breaks visual consistency.
- **Number badge at Pt(14)** is the smallest badge font in the engine. Other badges (quiz, drag-drop, click-reveal) use Pt(16). This inconsistency makes the slider badges look smaller than their peers.
- **Item text at Pt(18) in a Cm(1.5) height container** with center-anchored badges at Cm(1.5) height means the text and badge are the same height. Two-line items would overflow the Cm(1.5) height.
- **No visual container behind items.** Unlike quiz options and drag-drop items, slider items are plain text + badge with no background card or alternating rows.

### Enhancement Opportunities
- Add a section banner for consistency.
- Increase badge font to Pt(16) to match other slide types.
- Add alternating row backgrounds or subtle cards behind each item.
- Add a visual slider/track element at the bottom to reinforce the interaction metaphor.

---

## Cross-Cutting Issues

### Issue A: No Adaptive Layout System
The engine uses fixed positions for all dynamic content (objectives, quiz options, drag-drop items, etc.). There is no system to:
- Calculate available space and adjust spacing dynamically
- Split content across multiple slides when it exceeds capacity
- Reduce font sizes gracefully when content is dense

This is the root cause of all 5 overflow bugs.

### Issue B: Inconsistent Slide Structure
Some slides have: header bar + section banner + content + page number. Others skip the banner (slider), skip the header bar (section divider, closing), or have unique layouts. A consistent structural pattern would improve the professional feel.

| Slide Type | Header Bar | Section Banner | Content Card BG | Page Number |
|---|---|---|---|---|
| Title | No | No | No | No |
| Objectives | Yes | Yes (narrow) | No | Yes |
| Content | Yes | Yes (narrow) | Yes (bullets only) | Yes |
| Cards | Yes | Yes (wide) | No | Yes |
| Section Divider | No | No | No | Yes |
| Quiz | Yes | Yes (wide) | No | Yes |
| Drag-Drop | Yes | Yes (wide) | No | Yes |
| Two-Column | Yes | Yes (wide) | No | Yes |
| Click-Reveal | Yes | Yes (wide) | No | Yes |
| Summary | Yes | Yes (wide) | Yes | Yes |
| Closing | No | No | No | Yes (wrong color) |
| Slider | Yes | No | No | Yes |
| Dropdown | Yes | Yes (wide) | No | Yes |

### Issue C: Font Size Inconsistency
The minimum recommended font size for Arabic in presentations is Pt(18). Several elements fall below this:
- Objectives body text: Pt(16)
- Quiz feedback text: Pt(14)
- Bullet markers: Pt(12)
- Slider badge numbers: Pt(14)
- Dropdown arrow: Pt(14)

### Issue D: Missing `MSO_ANCHOR` Vertical Alignment
No text frames in the engine set `tf.vertical_anchor` (e.g., `MSO_ANCHOR.MIDDLE`). This means all text in cards, badges, and buttons defaults to top-aligned, which can look awkward when the text is shorter than the container. Specifically:
- Card titles should be vertically centered
- Badge numbers should be vertically centered
- Button text should be vertically centered
- Drop zone placeholders should be vertically centered

### Issue E: No Branding Integration
The engine has no mechanism to:
- Place a project-specific logo
- Apply client-specific colors
- Insert header/footer branding images
These are stored in `projects/[code]/branding/` per the project spec but are never referenced in the engine.

---

## Overflow Capacity Summary Table

| Slide Type | Max Items Before Overflow | Items Used In Practice |
|---|---|---|
| Objectives | 5 | 3-6 (commonly 5-6) |
| Quiz Options | 5 (tight) | 3-4 |
| Drag-Drop Items | 4 | 3-6 |
| Click-Reveal (vertical) | 6 (tight) | 5-9 |
| Dropdown Rows | 5 | 4-8 |
| Slider Items | 7 (tight) | 3-7 |
| Summary Items | ~6-7 | 3-8 |
| Card Layout | 4 | 2-4 |

Note: "tight" means the last item fits but with less than 1cm margin to the slide bottom.

---

## Detailed Bug Registry

| Bug ID | Severity | Slide Type | Description | First Overflow At |
|---|---|---|---|---|
| BUG-001 | CRITICAL | Objectives | Rows exceed slide bottom | 6 items |
| BUG-002 | CRITICAL | Click-Reveal | Vertical list rows exceed bottom | 7 items |
| BUG-003 | CRITICAL | Drag-Drop | Items + drop zones exceed bottom | 5 items |
| BUG-004 | CRITICAL | Dropdown | Statement rows exceed bottom | 6 items |
| BUG-005 | HIGH | Quiz | Feedback text nearly clips bottom edge | 4+ options |
| BUG-006 | MEDIUM | Closing | Page number invisible (white on white) | Always |
| BUG-007 | LOW | Section Divider | Title not centered in background card | Always |

---

## Recommendations Summary

### Immediate (Must Fix)
1. Add adaptive vertical spacing to objectives, drag-drop, click-reveal, and dropdown slides.
2. Set maximum item counts with overflow-to-next-slide logic.
3. Fix closing slide page number color.

### Short Term (Should Fix)
4. Increase all sub-Pt(18) text to at minimum Pt(18) for Arabic readability.
5. Add `MSO_ANCHOR.MIDDLE` vertical centering to badges, buttons, and card titles.
6. Center section divider content vertically.
7. Add content card backgrounds to all slide types for consistency.
8. Fix summary text color from LINK_BLUE to BODY_TEXT.

### Medium Term (Nice to Have)
9. Implement proper hanging indent for bullet lists.
10. Add branding integration (logo, colors from project config).
11. Create a shared `_calculate_adaptive_spacing()` helper method.
12. Add banner text length validation with auto-switching narrow/wide.
13. Remove on-slide Storyline instructions (move to notes only).
14. Add visual connectors/arrows to drag-drop slides.
