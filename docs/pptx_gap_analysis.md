# PPTX Template Gap Analysis

## Deep comparison: Template XML vs Current Engine (`engine/pptx_engine.py`)

---

## 1. Presentation-Level Settings

| Property | Template Value | Engine Value | Match? |
|----------|---------------|--------------|--------|
| Slide Width | 12192000 EMU | 12192000 EMU | YES |
| Slide Height | 6858000 EMU | 6858000 EMU | YES |
| Embedded Fonts | Play, Tajawal ExtraBold, Tajawal Medium, Tajawal | None embedded | **GAP** |
| Default Text RTL | `rtl="0"` (LTR default) | N/A | OK (overridden per paragraph) |
| embedTrueTypeFonts | `"1"` (enabled) | Not set | **GAP** |

### GAP: Font Embedding
The template embeds 7 font files (Play regular/bold, Tajawal regular/bold, Tajawal ExtraBold bold, Tajawal Medium regular/bold). The engine does not embed any fonts. This means on systems without Tajawal installed, text will fall back to Arial.

**Fix**: Consider embedding font files or at minimum documenting font dependency.

---

## 2. Theme Color Scheme

From `ppt/theme/theme1.xml`:

| Theme Color | Hex Value | Engine Equivalent | Match? |
|-------------|-----------|-------------------|--------|
| dk1 (Dark 1) | #000000 | Not used directly | OK |
| lt1 (Light 1) | #FFFFFF | `WHITE` = #FFFFFF | YES |
| dk2 (Dark 2) | #0E2841 | Not defined | **GAP** |
| lt2 (Light 2) | #E8E8E8 | Not defined | **GAP** |
| accent1 | #156082 | Not defined (engine uses #2D588C) | **GAP** |
| accent2 | #E97132 | Not defined | N/A |
| accent3 | #196B24 | Not defined | N/A |
| accent4 | #0F9ED5 | Not defined | N/A |
| accent5 | #A02B93 | Not defined | N/A |
| accent6 | #4EA72E | Not defined | N/A |
| hlink | #467886 | Not defined | N/A |
| folHlink | #96607D | Not defined | N/A |

### GAP: accent1 Mismatch
The theme's accent1 is `#156082`, but the engine uses `PRIMARY_BLUE = #2D588C`. The template slide 1 button uses `<a:schemeClr val="accent1"/>` which resolves to #156082. However, the text colors on the actual slides use explicit `srgbClr val="2D588C"`. So the engine's PRIMARY_BLUE is correct for text, but the button fill should be #156082 (accent1) not #2D588C.

**Fix**: Add `ACCENT1_BLUE = RGBColor(0x15, 0x60, 0x82)` for button fills that reference `schemeClr accent1`.

---

## 3. Slide Layouts (The Critical Architecture)

### Layout 1: "Title Slide" (used by slide 1 only)

Contains a **grouped shape** (`grpSp`) with:
1. **Full-slide background image** (`image24.png`, 2500x1406px) — blue tech/laptop design, positioned at `(0,0)` covering full slide `12192000x6857999 EMU`, **flipped horizontally** (`flipH="1"`)
2. **University logo** (`image1.png`, 736x570px) — positioned at `(2500158, 962015)` with size `1612381x1248719 EMU`, **flipped horizontally back** (`flipH="1"` on group cancels)
3. **Horizontal line** — blue `#2D588C` line, 1.5pt, at y=4048125

### Layout 2: "Title and Content" (used by slides 2-8)

Contains 4 image elements:
1. **Full-slide background image** (`image5.png`, 2500x1435px) — nearly white/transparent, at `(0,0)` full slide size `12192000x6858000 EMU`
2. **Header bar image** (`image22.png`, 2500x192px) — blue gradient rounded bar, at `(1803400, 0)` size `8585200x1007706 EMU`, cropped with `srcRect l="15304" r="15305"` (cropping 15.3% from left and right)
3. **Footer bar image** (`image23.png`, 2500x175px) — blue footer strip with decorative lines, at `(0, 6023222)` size `12192000x853440 EMU`, **flipped horizontally**
4. **University logo** (`image1.png`, 736x570px) — small logo at `(371475, 85756)` size `709767x549684 EMU`

### CRITICAL GAP: Background Images Not Used by Engine

The engine creates slides from a **blank presentation** using `self.prs.slide_layouts[6]` (blank layout). This means:

- **NO background image** on any slide (template has blue tech image on title, subtle texture on content)
- **NO header bar image** (template has a beautiful blue gradient rounded bar PNG)
- **NO footer bar image** (template has a decorative blue strip at bottom)
- **NO university logo** on content slides (template shows logo at top-left corner)
- **NO horizontal line** on title slide

The engine tries to compensate with:
- A plain blue rectangle for the header (line 260-268) — looks flat vs the gradient PNG
- A `ROUNDED_RECTANGLE` shape for the section banner (line 1890-1898) — should use the PNG banner image
- No footer at all on most slides

**This is the single biggest visual gap between engine output and the template.**

---

## 4. Slide-by-Slide Analysis

### Slide 1: Title Slide

**Template structure:**
| Element | Position (EMU) | Size (EMU) | Font | Size | Color | RTL |
|---------|---------------|------------|------|------|-------|-----|
| Institution name | x=6096000, y=3198167 | 5181600x461665 | Tajawal ExtraBold | 24pt | #2D588C | Yes, algn=center |
| Lecture title | x=6096000, y=4257368 | 5181600x1077218 | Tajawal ExtraBold | 24pt/20pt | #2D588C | Yes, algn=center |
| Subtitle | (within lecture title textbox, 3rd para) | same | Tajawal ExtraBold | 20pt | #262626 | Yes, algn=center |
| Start button (roundRect) | x=7398084, y=5599525 | 2773680x665193 | Tajawal | 20pt | lt1 (white) | No (center) |
| Button border | — | — | — | — | #082836, 1.5pt | — |
| Button fill | — | — | — | — | accent1 (#156082) | — |
| Play icon (image3.png) | x=9476078, y=5599525 | 619211x657317 | — | — | — | — |
| Hand cursor (image7.png) | x=7570916, y=5888428 | 724001x752580 | — | — | — | — |
| Background | Layout 1 group | Full slide | — | — | — | — |

**Engine vs Template:**
| Element | Engine | Gap? |
|---------|--------|------|
| Background | Plain blue rectangle at top | **MAJOR GAP** — should be image24.png full-slide bg |
| University logo | Not placed | **GAP** — should be in layout bg |
| Institution name | Correct position + font | OK |
| Lecture title | Position OK, but separate textbox for subtitle | **MINOR** — template uses single textbox with 3 paragraphs |
| Subtitle | Separate textbox at y=4800000 | **GAP** — template puts it at y=4257368 para 3, color #262626 |
| Start button fill | Uses PRIMARY_BLUE (#2D588C) | **GAP** — template uses accent1 (#156082) |
| Play icon | Not added | **GAP** — missing image3.png triangle icon |
| Hand cursor | Not added | **GAP** — missing image7.png hand cursor icon |
| Horizontal line | Not added | **GAP** — template has #2D588C line at y=4048125 |

### Slide 2: Objectives Slide

**Template structure:**
| Element | Position (EMU) | Size (EMU) | Details |
|---------|---------------|------------|---------|
| Header bar text | x=3405034, y=114300 | 5181600x369332 | Tajawal ExtraBold 18pt #333333 |
| Section banner (image19.png) | x=4790969, y=898751 | 2610062x695099 | Light blue/grey rounded rect PNG |
| Banner title text | x=4947367, y=1035917 | 2297266x369332 | Tajawal ExtraBold 18pt #333333 |
| Intro text | x=6280654, y=1830945 | 5361940x369332 | Tajawal Medium 18pt #333333 |
| Objective row bg (image6.png) | x=612770, y=2315612+ | 11029824x600002 | Light blue gradient bar PNG |
| Objective row end (image13.png) | x=10922693, y=2315612+ | 703228x600002 | Target/circle icon PNG |
| Objective text | x=1462617, y=row+offset | 9443403x338554 | Tajawal 16pt #333333, algn=right |
| Page number | x=920559, y=6384932 | 327098x400110 | Tajawal ExtraBold 20pt #2D588C |

**Engine vs Template:**
| Element | Engine | Gap? |
|---------|--------|------|
| Header bar | Text only (correct position) | **GAP** — missing header bar PNG (image22.png from layout) |
| Section banner | Blue ROUNDED_RECTANGLE shape | **MAJOR GAP** — should be image19.png (light grey/blue rounded rect), text should be dark #333333 not white |
| Banner text color | WHITE on blue bg | **GAP** — template shows #333333 on light grey PNG |
| Objective row bg | ROUNDED_RECTANGLE with LIGHT_BLUE_BG | **GAP** — should use image6.png (gradient bar PNG) |
| Row end icon | Not present | **GAP** — missing image13.png target icon |
| Row number badge | Positioned at right side | **MINOR** — template doesn't have number badges, uses image13.png icon instead |
| Footer bar | Not present | **GAP** — layout 2 has footer image23.png |
| University logo | Not present | **GAP** — layout 2 has logo at top-left |

### Slide 3: Content Slide (with image + text)

**Template structure:**
| Element | Position (EMU) | Size (EMU) | Details |
|---------|---------------|------------|---------|
| Header bar text | x=3405034, y=114300 | 5181600x369332 | Tajawal ExtraBold 18pt #333333 |
| Section banner x2 (image19.png) | x=4790969, y=898751 | 2610062x695099 | Banner PNG (appears twice in XML) |
| Section title text | x=4870450, y=1055581 | 2457450x400110 | Tajawal ExtraBold 20pt #333333 |
| Subsection title | x=7675818, y=1836174 (flipH) | 3300157x369332 | Tajawal Medium 18pt #2D588C |
| Text bubble bg (image8.png) | x=6263238, y=2459020 (flipH) | 4712737x2005029 | Light grey rounded rect PNG |
| Top-right corner (image9.png) | x=10489588, y=2438365 (flipH) | 493940x446899 | Blue corner bracket |
| Bottom-left corner (image14.png) | x=6240449, y=4020071 (flipH) | 499476x443978 | Blue corner bracket |
| Body text | x=6288448, y=2615000 (flipH) | 4576235x1077218 | Tajawal 16pt #333333, algn=right |
| Image placeholder (image10.png) | x=1084108, y=1968500 (flipH) | 3222625x3213100 | Blue-bordered rounded square |
| Content image | x=1046008, y=1930400 | 3300157x3286434 | Actual content image (cropped) |
| Hand cursor icon | x=9030651, y=3775180 | 724001x752580 | image7.png |
| Yellow cloud callout | x=10347158, y=183666 | 1844842x1588168 | Cloud shape, yellow #FFFF00 fill, text "يوجد وصف أسفل الشريحة" |
| Page number | x=920559, y=6384932 | 327098x400110 | Same as before |

**Engine vs Template:**
| Element | Engine | Gap? |
|---------|--------|------|
| Section title | Uses banner approach (blue rect) | **MAJOR GAP** — should be PNG banner with dark text |
| Sub-section title | Exists (correct) | **MINOR** — position differences |
| Text bubble | Not present | **MAJOR GAP** — engine puts text directly, template has a decorative grey rounded rect bg with blue corner brackets |
| Corner brackets | Not present | **GAP** — missing decorative elements |
| Image placeholder frame | Not present | **GAP** — template has blue-bordered rounded rect frame for images |
| Yellow cloud note | Not present | **OK** — this is a template instruction callout, not for production output |
| flipH usage | Not used | **NOTE** — many elements have flipH="1" for RTL mirroring |

### Slide 4: Section Divider / Pop-up Slide

**Template structure:**
- Full-slide semi-transparent dark overlay: `(0,0)` full slide, dk1 fill at 43.9% alpha
- White content card: `(953011, 1935480)` size `10321295x3611880`, white fill
- Close button icon (image21.png): `(10676935, 1986685)` size `562053x504895` — red X
- Three card placeholders (image16.png): positioned horizontally at x=912265, x=4849615, x=8781538, all y=2595307, each 2492769x782170
- Card label text: Tajawal 16pt #333333

**Engine equivalent**: `add_section_divider()` — uses colored rectangle background. **MAJOR GAP** — template uses a modal/popup pattern with dark overlay + white card + close button, very different from engine approach.

### Slides 5-7: Activity Slides

**Template structure:**
- Header bar text at standard position
- Activity banner (image15.png): `(3884635, 860142)` size `4422731x695099` — wider light blue/grey rounded rect
- Activity title text: `(3818244, 977750)` size `4555512x400110`, Tajawal ExtraBold 20pt #333333
- Yellow cloud callout (template instructions — not in production output)
- Page number at standard position

**Engine comparison:**
| Element | Engine | Gap? |
|---------|--------|------|
| Activity banner | Blue ROUNDED_RECTANGLE (wide) | **MAJOR GAP** — should be image15.png (light grey/blue) with dark text |
| Banner text | White on blue | **GAP** — should be #333333 on light bg |
| Activity body content | Various (quiz, drag-drop, etc.) | Content structure OK, visual framing wrong |

### Slide 8: Summary Slide

**Template structure:**
- Header bar at standard position
- Activity banner (image15.png) at wide position
- Summary title "ملخص الوحدة الدراسية": Tajawal ExtraBold 20pt #333333
- Summary bullet with colored bullet: indent=-342900, marL=342900, bullet color #2E6CEC, bullet font Arial, bullet char "•"
- Summary text: bold label in #2E6CEC + regular text in #2E6CEC, Tajawal 20pt, line spacing 150%

**Engine comparison:**
| Element | Engine | Gap? |
|---------|--------|------|
| Bullet formatting | Uses standard bullets | **GAP** — template uses colored bullets (#2E6CEC), bold label followed by colon then regular text |
| Line spacing | Not set to 150% | **GAP** — template uses 150% line spacing |
| Summary text color | Uses LINK_BLUE #2E6CEC | OK for color |

---

## 5. Image Asset Inventory

### Images in the Template (must be bundled with engine)

| Image File | Purpose | Size (px) | Used In | Engine Has? |
|------------|---------|-----------|---------|-------------|
| `image24.png` | Title slide background (blue tech laptop) | 2500x1406 | Layout 1 | **NO** |
| `image5.png` | Content slide background (nearly white) | 2500x1435 | Layout 2 | **NO** |
| `image22.png` | Header bar (blue gradient rounded) | 2500x192 | Layout 2 | **NO** |
| `image23.png` | Footer bar (blue strip with lines) | 2500x175 | Layout 2 | **NO** |
| `image1.png` | University logo (Najran) | 736x570 | Layout 1 & 2 | **NO** (per-project) |
| `image19.png` | Section banner (narrow, light grey) | 416x117 | Slides 2-3 | **NO** |
| `image15.png` | Activity banner (wide, light grey) | 416x116 | Slides 5-8 | **NO** |
| `image6.png` | Objective row bar (gradient) | 1728x94 | Slide 2 | **NO** |
| `image13.png` | Target/circle icon (row end) | 109x93 | Slide 2 | **NO** |
| `image16.png` | Card placeholder (with blue connector) | 784x246 | Slide 4 | **NO** |
| `image3.png` | Play button triangle icon | 65x69 | Slide 1 | **NO** |
| `image7.png` | Hand cursor icon | 76x79 | Slides 1, 3 | **NO** |
| `image8.png` | Text bubble bg (light grey rounded) | 1534x1024 | Slide 3 | **NO** |
| `image9.png` | Corner bracket top-right | ~50x50 | Slide 3 | **NO** |
| `image14.png` | Corner bracket bottom-left | ~50x50 | Slide 3 | **NO** |
| `image10.png` | Image frame (blue-bordered square) | ~500x500 | Slide 3 | **NO** |
| `image20.png` | Sample content image | 1534x1024 | Slide 3 | N/A (content) |
| `image21.png` | Close button (red X) | ~50x50 | Slide 4 | **NO** |

### External Background Image
`Picture1.png` (5.7MB) from the downloads — this is the same as `image24.png` in the template (the blue tech laptop image). **It is already embedded in the template's Layout 1.** No need to add it separately.

---

## 6. Font Specifications Summary

| Context | Font | Size | Color | Bold | Used In |
|---------|------|------|-------|------|---------|
| Institution name (title slide) | Tajawal ExtraBold | 24pt | #2D588C | No | Slide 1 |
| Lecture title | Tajawal ExtraBold | 24pt | #2D588C | No | Slide 1 |
| Lecture subtitle | Tajawal ExtraBold | 20pt | #262626 | No | Slide 1 |
| Start button | Tajawal | 20pt | white (lt1) | No | Slide 1 |
| Header bar (top of slide) | Tajawal ExtraBold | 18pt | #333333 | No | Slides 2-8 |
| Section banner title | Tajawal ExtraBold | 18pt or 20pt | #333333 | No | Slides 2-3 |
| Activity banner title | Tajawal ExtraBold | 20pt | #333333 | No | Slides 5-8 |
| Intro/description text | Tajawal Medium | 18pt | #333333 | No | Slide 2 |
| Body text / objectives | Tajawal | 16pt | #333333 | No | Slides 2-3 |
| Subsection title | Tajawal Medium | 18pt | #2D588C | No | Slide 3 |
| Page number | Tajawal ExtraBold | 20pt | #2D588C | No | All slides |
| Summary bullets | Tajawal | 20pt | #2E6CEC | Bold (label) | Slide 8 |
| Yellow cloud note | Arial | 18pt | dk1 (black) | No | Template only |

**Engine Match**: Font names are correct. Sizes and colors match for most elements. The key issue is that banner text uses #333333 on light backgrounds (PNG images), not white on blue shapes.

---

## 7. Prioritized Fix List

### P0 — Critical Visual Gaps (must fix)

1. **Add layout background images** — Extract and bundle template images (image5.png for bg, image22.png for header, image23.png for footer, image1.png for logo). Add them to every content slide via `slide.shapes.add_picture()`.

2. **Replace section banner shapes with PNG images** — Use image19.png (narrow) and image15.png (wide) instead of blue ROUNDED_RECTANGLE. Change banner text color from WHITE to #333333.

3. **Add title slide background** — Use image24.png as full-slide background (flipped horizontally). Add university logo, horizontal line, play icon, and hand cursor.

4. **Replace objective row shapes with PNG images** — Use image6.png gradient bar + image13.png target icon instead of ROUNDED_RECTANGLE shapes.

### P1 — Important Visual Gaps

5. **Add content slide text bubble** — Use image8.png as text area background with corner brackets (image9.png, image14.png).

6. **Fix button fill color** — Change from #2D588C to #156082 (accent1) for the start button.

7. **Add footer bar** — Use image23.png at bottom of content slides.

8. **Add image frame** — Use image10.png as the placeholder frame when content slides have images.

### P2 — Nice to Have

9. **Fix subtitle positioning** — Put subtitle in same textbox as title (3rd paragraph) instead of separate textbox.

10. **Add summary bullet formatting** — Colored bullets #2E6CEC, 150% line spacing, bold labels.

11. **Fix section divider** — Use dark overlay + white card + close button pattern instead of colored rectangle.

12. **Font embedding** — Set `embedTrueTypeFonts="1"` and include font data files.

---

## 8. Recommended Architecture Change

### Current Approach (engine creates from blank)
```
Presentation() → blank layout → add shapes manually
```

### Recommended Approach (use template as base)
```
Presentation(template_path) → use existing layouts → add content shapes
```

**Why**: The template already has layouts with all the background images, header bars, footer bars, and logos correctly positioned. Instead of recreating these from scratch with shapes (which can never match the gradient PNGs), the engine should:

1. Open the template PPTX as the base presentation
2. Use Layout 1 (index 0) for title slides
3. Use Layout 2 (index 1) for all content slides
4. Add only the dynamic content (text boxes, shapes for activities) on top

This eliminates the need to bundle and manually position 10+ image assets, and automatically gets the correct backgrounds, headers, footers, and logos.

**Risk**: The template-as-base approach was previously tried and caused issues with overlapping text and broken RTL. However, the key insight is that the template layouts themselves are clean — the issues arose from trying to fill placeholder shapes. The fix is to use the layouts but add content via `slide.shapes.add_textbox()` rather than modifying existing placeholder shapes.

### Hybrid Approach (safest)
1. Use template as base (gets all layout images automatically)
2. Add blank slides using the template's own layouts
3. Place content with explicit `add_textbox()` / `add_picture()` calls (current engine approach)
4. Never touch placeholder shapes

This combines the best of both worlds: template images from layouts + precise positioning from code.

---

## 9. Image Asset Extraction

All required images are available at: `/tmp/pptx-template/ppt/media/`

They should be copied to: `templates/pptx_assets/`

Key files to copy:
```
image24.png → title_bg.png (title slide background)
image5.png  → content_bg.png (content slide background — nearly white)
image22.png → header_bar.png (blue gradient header)
image23.png → footer_bar.png (blue footer strip)
image1.png  → logo.png (university logo — per-project)
image19.png → banner_narrow.png (section title banner)
image15.png → banner_wide.png (activity title banner)
image6.png  → objective_row.png (objective row background)
image13.png → target_icon.png (objective row end icon)
image16.png → card_placeholder.png (card with blue connector)
image3.png  → play_icon.png (play button triangle)
image7.png  → hand_cursor.png (hand cursor icon)
image8.png  → text_bubble.png (text area background)
image9.png  → corner_tr.png (top-right corner bracket)
image14.png → corner_bl.png (bottom-left corner bracket)
image10.png → image_frame.png (blue-bordered image frame)
image21.png → close_btn.png (red X close button)
```

---

## 10. Position Reference Table (All EMU values from template XML)

### Common Elements (appear on most slides)

| Element | Left | Top | Width | Height |
|---------|------|-----|-------|--------|
| Content bg (layout2) | 0 | 0 | 12192000 | 6858000 |
| Header bar (layout2) | 1803400 | 0 | 8585200 | 1007706 |
| Footer bar (layout2) | 0 | 6023222 | 12192000 | 853440 |
| Logo (layout2) | 371475 | 85756 | 709767 | 549684 |
| Title bar text | 3405034 | 114300 | 5181600 | 369332 |
| Narrow banner img | 4790969 | 898751 | 2610062 | 695099 |
| Narrow banner text | 4947367 | 1035917 | 2297266 | 369332 |
| Wide banner img | 3884635 | 860142 | 4422731 | 695099 |
| Wide banner text | 3818244 | 977750 | 4555512 | 400110 |
| Page number | 920559 | 6384932 | 327098 | 400110 |

### Title Slide Elements

| Element | Left | Top | Width | Height |
|---------|------|-----|-------|--------|
| Title bg (layout1) | 0 | 0 | 12192000 | 6857999 |
| Logo (layout1) | 2500158 | 962015 | 1612381 | 1248719 |
| Blue line | 2500158 | 4048125 | 1538442 | 0 |
| Institution text | 6096000 | 3198167 | 5181600 | 461665 |
| Title+subtitle textbox | 6096000 | 4257368 | 5181600 | 1077218 |
| Start button | 7398084 | 5599525 | 2773680 | 665193 |
| Play icon | 9476078 | 5599525 | 619211 | 657317 |
| Hand cursor | 7570916 | 5888428 | 724001 | 752580 |

### Objectives Slide Elements

| Element | Left | Top | Width | Height |
|---------|------|-----|-------|--------|
| Intro text | 6280654 | 1830945 | 5361940 | 369332 |
| Row 1 bar | 612770 | 2315612 | 11029824 | 600002 |
| Row 1 icon | 10922693 | 2315612 | 703228 | 600002 |
| Row 1 text | 1462617 | 2430947 | 9443403 | 338554 |
| Row spacing | — | 835741 (delta) | — | — |

### Content Slide Elements

| Element | Left | Top | Width | Height | Notes |
|---------|------|-----|-------|--------|-------|
| Subsection title | 7675818 | 1836174 | 3300157 | 369332 | flipH=1 |
| Text bubble bg | 6263238 | 2459020 | 4712737 | 2005029 | flipH=1 |
| Body text | 6288448 | 2615000 | 4576235 | 1077218 | flipH=1 |
| Corner TR | 10489588 | 2438365 | 493940 | 446899 | flipH=1 |
| Corner BL | 6240449 | 4020071 | 499476 | 443978 | flipH=1 |
| Image frame | 1084108 | 1968500 | 3222625 | 3213100 | flipH=1 |
| Content image | 1046008 | 1930400 | 3300157 | 3286434 | — |

### Section Divider Elements

| Element | Left | Top | Width | Height |
|---------|------|-----|-------|--------|
| Dark overlay | -1 | 0 | 12192000 | 6858000 |
| White card | 953011 | 1935480 | 10321295 | 3611880 |
| Close button | 10676935 | 1986685 | 562053 | 504895 |
| Card placeholder | 912265/4849615/8781538 | 2595307 | 2492769 | 782170 |
