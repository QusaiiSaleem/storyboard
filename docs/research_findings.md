# Research Findings: AI-Generated PPTX/DOCX with Arabic RTL

> Comprehensive research for the Storyboard Generator template engine.
> Focus: practical, actionable patterns for Claude Code subagents generating Arabic educational documents.

---

## Table of Contents

1. [python-pptx Best Practices](#1-python-pptx-best-practices)
2. [python-docx Best Practices](#2-python-docx-best-practices)
3. [Arabic RTL Specific Challenges](#3-arabic-rtl-specific-challenges)
4. [How AI Systems Generate Reliable Document Output](#4-how-ai-systems-generate-reliable-document-output)
5. [Claude Code Agent Design Patterns](#5-claude-code-agent-design-patterns)
6. [Recommended Architecture for This Project](#6-recommended-architecture-for-this-project)
7. [Common Pitfalls and Solutions](#7-common-pitfalls-and-solutions)

---

## 1. python-pptx Best Practices

### 1.1 Core Architecture

python-pptx operates on the Open XML standard. The hierarchy is:

```
Presentation
  -> SlideMaster(s)
    -> SlideLayout(s)
      -> Slide(s)
        -> Shape(s)
          -> TextFrame
            -> Paragraph(s)
              -> Run(s) (character-level formatting)
```

### 1.2 Positioning and Units

PowerPoint uses **EMU (English Metric Units)**: 914,400 EMU = 1 inch.

python-pptx provides helper classes to avoid raw EMU math:

```python
from pptx.util import Inches, Pt, Cm, Emu

# These are all equivalent ways to specify 1 inch:
Inches(1)       # 914400 EMU
Cm(2.54)        # 914400 EMU
Emu(914400)     # direct

# For font sizes:
Pt(18)          # 18-point font
```

**Best practice**: Always use `Inches()` or `Cm()` — never raw EMU values in builder APIs. Store measurements as descriptive constants.

### 1.3 Creating Slides from Blank Layouts

For template-as-code, create from blank layouts and add shapes programmatically rather than depending on placeholder indices:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
# Use blank layout (index 6) for full control
blank_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_layout)

# Add shapes with exact positioning
left = Inches(0.5)
top = Inches(0.5)
width = Inches(9)
height = Inches(1)

txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame
tf.text = "Title Text"
tf.paragraphs[0].font.size = Pt(24)
tf.paragraphs[0].font.bold = True
tf.paragraphs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
```

### 1.4 Shape Fill and Background Colors

```python
from pptx.dml.color import RGBColor

# Solid fill
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x31, 0x84, 0x9B)  # teal header

# No fill (transparent)
shape.fill.background()

# Gradient fill
shape.fill.gradient()
# Access stops via shape.fill.gradient_stops
```

### 1.5 Tables in python-pptx

```python
rows, cols = 3, 3
x, y, cx, cy = Inches(2), Inches(2), Inches(4), Inches(1.5)
shape = slide.shapes.add_table(rows, cols, x, y, cx, cy)
table = shape.table

# Set column widths
table.columns[0].width = Inches(2.0)
table.columns[1].width = Inches(4.0)

# Set cell text
cell = table.cell(0, 0)
cell.text = 'Header'

# Cell background color
cell.fill.solid()
cell.fill.fore_color.rgb = RGBColor(0x31, 0x84, 0x9B)

# Merge cells
table.cell(0, 0).merge(table.cell(0, 2))  # merge row 0, cols 0-2

# Font in table cells
for paragraph in cell.text_frame.paragraphs:
    for run in paragraph.runs:
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
```

### 1.6 Adding Images

```python
from pptx.util import Inches

# Add with position only (original size)
slide.shapes.add_picture('logo.png', Inches(0.5), Inches(0.5))

# Add with width (height auto-calculated to maintain aspect ratio)
slide.shapes.add_picture('logo.png', Inches(0.5), Inches(0.5), width=Inches(2))

# Add with both dimensions (may distort)
slide.shapes.add_picture('logo.png', Inches(0.5), Inches(0.5),
                         width=Inches(2), height=Inches(1))
```

### 1.7 Text Frame Properties

```python
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN

tf = shape.text_frame

# Margins
tf.margin_left = Inches(0.1)
tf.margin_right = Inches(0.1)
tf.margin_top = Inches(0.05)
tf.margin_bottom = Inches(0.05)

# Vertical alignment
tf.vertical_anchor = MSO_ANCHOR.MIDDLE  # or TOP, BOTTOM

# Word wrap
tf.word_wrap = True

# Auto-size behavior
tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT  # or TEXT_TO_FIT_SHAPE, NONE

# Paragraph alignment
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.RIGHT  # critical for Arabic RTL
```

### 1.8 Slide Dimensions

```python
from pptx.util import Inches

prs = Presentation()
# Standard widescreen (16:9)
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Standard (4:3)
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)
```

---

## 2. python-docx Best Practices

### 2.1 Core Architecture

python-docx operates on the Office Open XML (OOXML) standard for Word:

```
Document
  -> Sections (page layout per section)
    -> Header/Footer
  -> Body
    -> Paragraph(s) or Table(s)
      -> Run(s) (character-level formatting)
```

### 2.2 Document Setup

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, Twips
from docx.enum.section import WD_ORIENT

doc = Document()
section = doc.sections[0]

# Set landscape A4
section.page_width = Cm(29.7)
section.page_height = Cm(21.0)
section.orientation = WD_ORIENT.LANDSCAPE

# Set margins (1 inch all around)
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(2.54)
section.right_margin = Cm(2.54)
```

### 2.3 Table Creation

```python
from docx import Document
from docx.shared import Pt, Twips

doc = Document()

# Create table with specific number of rows and columns
table = doc.add_table(rows=7, cols=2)

# Set table width
table.width = Twips(13950)  # matches template

# Access cells
cell = table.cell(0, 0)
cell.text = 'Label'

# Set column widths
table.columns[0].width = Twips(4050)
table.columns[1].width = Twips(9900)
```

### 2.4 Cell Shading (Background Color) -- CRITICAL WORKAROUND

python-docx does NOT have a built-in API for cell shading. You must manipulate XML directly:

```python
from docx.oxml.ns import nsdecls, qn
from docx.oxml import parse_xml, OxmlElement

def set_cell_shading(cell, color_hex):
    """Set background color on a table cell.

    IMPORTANT: You must create a NEW shading element for each cell.
    Reusing the same element will MOVE it from one cell to another.

    Args:
        cell: python-docx table cell object
        color_hex: hex color string without # (e.g., "31849B")
    """
    shading_elm = parse_xml(
        f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    )
    cell._tc.get_or_add_tcPr().append(shading_elm)


# Usage:
set_cell_shading(table.cell(0, 0), "31849B")  # teal header
set_cell_shading(table.cell(1, 0), "DBE5F1")  # light blue label
set_cell_shading(table.cell(1, 1), "FFFFFF")  # white value cell
```

### 2.5 Cell Borders -- CRITICAL WORKAROUND

python-docx does NOT have a built-in API for cell borders. You must manipulate XML:

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_border(cell, **kwargs):
    """Set cell borders.

    Usage:
        set_cell_border(cell,
            top={"sz": 4, "val": "single", "color": "000000"},
            bottom={"sz": 4, "val": "single", "color": "000000"},
            start={"sz": 4, "val": "single", "color": "000000"},
            end={"sz": 4, "val": "single", "color": "000000"},
        )

    For no border (invisible):
        set_cell_border(cell,
            top={"val": "nil"},
        )

    For thick white borders (invisible separator between cells):
        set_cell_border(cell,
            top={"sz": 18, "val": "single", "color": "FFFFFF"},
        )
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')

    for edge in ('top', 'left', 'bottom', 'right', 'start', 'end'):
        if edge in kwargs:
            edge_data = kwargs[edge]
            element = OxmlElement(f'w:{edge}')
            for attr_name, attr_val in edge_data.items():
                element.set(qn(f'w:{attr_name}'), str(attr_val))
            tcBorders.append(element)

    tcPr.append(tcBorders)
```

### 2.6 Font Formatting

```python
from docx.shared import Pt, RGBColor

paragraph = cell.paragraphs[0]
run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()

# Font name (for Arabic, set both ascii and complex script names)
run.font.name = 'Sakkal Majalla'
run.font.cs_name = 'Sakkal Majalla'  # complex script font (Arabic)

# Size, weight, color
run.font.size = Pt(10)
run.font.bold = True
run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
```

### 2.7 Paragraph Alignment

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH

paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT   # common for Arabic
```

### 2.8 Cell Vertical Alignment

```python
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
```

### 2.9 Merging Cells

```python
# Merge horizontally (same row, multiple columns)
table.cell(0, 0).merge(table.cell(0, 1))

# Merge vertically (same column, multiple rows)
table.cell(0, 0).merge(table.cell(2, 0))

# Merge a block (rows and columns)
table.cell(0, 0).merge(table.cell(2, 1))
```

---

## 3. Arabic RTL Specific Challenges

### 3.1 The Core Problem

Neither python-pptx nor python-docx has complete built-in RTL support. Both require XML-level workarounds for proper Arabic text rendering. This is the single biggest challenge for this project.

### 3.2 python-docx RTL: Paragraph Direction

python-docx does NOT expose a `bidi` property on paragraphs. You must add the XML element manually:

```python
from docx.oxml.parser import OxmlElement

def set_paragraph_rtl(paragraph):
    """Set a paragraph to right-to-left direction.

    This adds <w:bidi/> to the paragraph properties <w:pPr>.
    Required for every paragraph containing Arabic text.
    """
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement("w:bidi")
    pPr.insert_element_before(
        bidi,
        *(
            "w:adjustRightInd",
            "w:snapToGrid",
            "w:spacing",
            "w:ind",
            "w:contextualSpacing",
            "w:mirrorIndents",
            "w:suppressOverlap",
            "w:jc",
            "w:textDirection",
            "w:textAlignment",
            "w:textboxTightWrap",
            "w:outlineLvl",
            "w:divId",
            "w:cnfStyle",
            "w:rPr",
            "w:sectPr",
            "w:pPrChange",
        )
    )
```

### 3.3 python-docx RTL: Table Direction

Setting table direction to RTL uses the built-in API, but it has known bugs:

```python
from docx.enum.table import WD_TABLE_DIRECTION

# The official API:
table.table_direction = WD_TABLE_DIRECTION.RTL

# This adds <w:bidiVisual/> to tblPr, but may not always work.
# If it fails, fall back to XML manipulation:
from docx.oxml import OxmlElement

def set_table_rtl(table):
    """Force RTL direction on a table via direct XML manipulation."""
    tblPr = table._tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        table._tbl.insert(0, tblPr)
    bidiVisual = OxmlElement('w:bidiVisual')
    tblPr.append(bidiVisual)
```

**Additionally**: For full RTL support in tables, you need BOTH:
1. `<w:bidiVisual/>` on the table properties (reverses column order visually)
2. `<w:bidi/>` on each paragraph within cells (sets text direction)
3. `<w:rtl/>` on each run's properties (for proper font selection)

### 3.4 python-docx RTL: Run-level RTL

```python
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_run_rtl(run):
    """Set RTL on a specific run for proper complex script font selection."""
    rPr = run._r.get_or_add_rPr()
    rtl = OxmlElement('w:rtl')
    rPr.append(rtl)
```

### 3.5 python-pptx RTL: Paragraph Direction

python-pptx does NOT have a built-in RTL property. You must access the XML directly:

```python
from lxml import etree

def set_pptx_paragraph_rtl(paragraph):
    """Set RTL direction on a python-pptx paragraph.

    In PowerPoint XML, the paragraph properties element is <a:pPr>
    and the RTL attribute is 'rtl="1"'.
    """
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('rtl', '1')


def set_pptx_paragraph_alignment_right(paragraph):
    """Set right alignment (standard for Arabic RTL text)."""
    from pptx.enum.text import PP_ALIGN
    paragraph.alignment = PP_ALIGN.RIGHT
```

### 3.6 Font Selection for Arabic

**Recommended fonts** (in priority order for this project):

| Font | Type | Availability | Best For |
|------|------|-------------|----------|
| **Sakkal Majalla** | Naskh calligraphy | Windows system font | Body text, tables, formal content |
| **Cairo** | Modern sans-serif | Google Fonts | Headings, modern designs |
| **Tajawal** | Sans-serif, 7 weights | Google Fonts | UI text, bilingual content |
| **Traditional Arabic** | Traditional | Windows system font | Fallback for formal content |
| **Tahoma** | Sans-serif | Cross-platform | Small text, footers |

**Critical font gotcha in python-docx**: When setting RTL=True on a style, the `font.name` property may be ignored. You MUST set `font.cs_name` (complex script font name) separately:

```python
run.font.name = 'Sakkal Majalla'       # Latin/ASCII characters
run.font.cs_name = 'Sakkal Majalla'    # Arabic/complex script characters
```

In python-pptx, set the font name on the run's `font.name` property, and for the complex script face, manipulate the XML:

```python
from lxml import etree

def set_pptx_cs_font(run, font_name):
    """Set the complex script (Arabic) font on a python-pptx run."""
    rPr = run._r.get_or_add_rPr()
    # Create or find the <a:cs> element
    nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    cs_elements = rPr.findall('a:cs', nsmap)
    if cs_elements:
        cs_elements[0].set('typeface', font_name)
    else:
        cs = etree.SubElement(rPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}cs')
        cs.set('typeface', font_name)
```

### 3.7 Bidirectional Text (Mixed Arabic + English)

When mixing Arabic text with English words (like "SCAMPER" or "Bloom"), the Unicode Bidirectional Algorithm handles most cases automatically. However:

- **Numbers in Arabic text**: Usually render correctly without intervention
- **English terms in Arabic**: Usually render correctly when the paragraph direction is RTL
- **Avoid manual reshaping**: Do NOT use `arabic-reshaper` or `python-bidi` for document generation -- these are for image/PDF rendering, not OOXML

### 3.8 Complete RTL Helper Module

For this project, create a unified helper module:

```python
# engine/rtl_helpers.py

from docx.oxml.parser import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
from docx.enum.table import WD_TABLE_DIRECTION
from lxml import etree

# ============ python-docx helpers ============

def docx_set_paragraph_rtl(paragraph):
    """Set paragraph direction to RTL in a Word document."""
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement("w:bidi")
    pPr.insert_element_before(
        bidi,
        *(
            "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
            "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap",
            "w:jc", "w:textDirection", "w:textAlignment",
            "w:textboxTightWrap", "w:outlineLvl", "w:divId",
            "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange",
        )
    )

def docx_set_run_rtl(run):
    """Set RTL on a run for proper complex script font selection."""
    rPr = run._r.get_or_add_rPr()
    rtl = OxmlElement('w:rtl')
    rPr.append(rtl)

def docx_set_table_rtl(table):
    """Set table direction to RTL."""
    try:
        table.table_direction = WD_TABLE_DIRECTION.RTL
    except Exception:
        tblPr = table._tbl.tblPr
        if tblPr is None:
            tblPr = OxmlElement('w:tblPr')
            table._tbl.insert(0, tblPr)
        bidiVisual = OxmlElement('w:bidiVisual')
        tblPr.append(bidiVisual)

def docx_set_cell_shading(cell, color_hex):
    """Set cell background color. Creates a NEW element each time."""
    shading_elm = parse_xml(
        f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    )
    cell._tc.get_or_add_tcPr().append(shading_elm)

def docx_set_cell_borders(cell, **kwargs):
    """Set cell borders. Pass edge names with dicts of attributes."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'start', 'end'):
        if edge in kwargs:
            element = OxmlElement(f'w:{edge}')
            for attr_name, attr_val in kwargs[edge].items():
                element.set(qn(f'w:{attr_name}'), str(attr_val))
            tcBorders.append(element)
    tcPr.append(tcBorders)

# ============ python-pptx helpers ============

def pptx_set_paragraph_rtl(paragraph):
    """Set paragraph direction to RTL in a PowerPoint presentation."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('rtl', '1')

def pptx_set_cs_font(run, font_name):
    """Set the complex script (Arabic) font on a python-pptx run."""
    rPr = run._r.get_or_add_rPr()
    nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    cs_elements = rPr.findall('a:cs', nsmap)
    if cs_elements:
        cs_elements[0].set('typeface', font_name)
    else:
        cs = etree.SubElement(
            rPr,
            '{http://schemas.openxmlformats.org/drawingml/2006/main}cs'
        )
        cs.set('typeface', font_name)
```

---

## 4. How AI Systems Generate Reliable Document Output

### 4.1 Industry Approaches (Gamma, Beautiful.ai, Presenton)

**Gamma.app** uses a prompt-driven workflow:
1. User provides prompt, uploads file, or selects template
2. AI model produces **structured intermediate representation** (slide structure + content)
3. Responsive templates adjust layout automatically
4. Output is web-native (HTML) -- exports to PPTX/PDF as secondary format

**Beautiful.ai** uses smart templates:
1. Users select from pre-designed "smart" slide templates
2. Templates have built-in layout rules (spacing, alignment, hierarchy)
3. As content is added, the template auto-adjusts
4. AI handles formatting; user focuses on content

**Presenton** (open-source, most relevant to us):
1. LLM generates structured slide content (markdown)
2. Content is parsed into intermediate representation
3. HTML/Tailwind templates render the content
4. python-pptx converts rendered output to PPTX

### 4.2 Template-as-Code vs Template-Fill: The Verdict

| Approach | Template-Fill | Template-as-Code |
|----------|--------------|------------------|
| **How it works** | Load .docx/.pptx, find placeholders, replace text | Python code defines the document structure, builds from scratch |
| **Pros** | Quick for simple replacements, visual design in Word/PPT | Full control, reliable, no placeholder misses |
| **Cons** | Fragile placeholders, broken formatting, RTL issues, overlapping text | More upfront code, no visual preview until generated |
| **AI reliability** | LOW -- AI must guess placeholder positions, can't control XML | HIGH -- AI calls builder functions with known parameters |
| **Best for** | Simple mail-merge (name, date replacements) | Complex, structured documents with precise formatting |

**Verdict: Template-as-Code is the clear winner for this project.**

Reasons:
1. Arabic RTL requires XML-level control that template-fill cannot provide
2. AI subagents need deterministic builder APIs, not XML string hunting
3. Template-fill approaches break when templates are modified visually
4. Our templates have complex table structures that need programmatic control

### 4.3 The Intermediate Representation Pattern

The most reliable AI document generation pattern is:

```
AI Agent --> Structured Data (JSON/dict) --> Builder Function --> Document File
```

The AI agent should NEVER directly manipulate XML, write raw python-docx code, or touch file I/O. Instead:

1. **AI produces structured content** as a Python dictionary or JSON
2. **Builder function** validates the data and produces the document
3. **Builder function** handles ALL formatting, RTL, fonts, colors, borders

Example flow:

```python
# What the AI agent produces:
content = {
    "element_code": "DSAI_U01_Pre_Test",
    "project_name": "علم البيانات والذكاء الاصطناعي",
    "unit": "الوحدة الأولى: مقدمة",
    "element_name": "الاختبار القبلي",
    "designer": "المصمم التعليمي",
    "date": "2026-02-08",
    "questions": [
        {
            "number": 1,
            "text": "ما هو الذكاء الاصطناعي؟",
            "type": "multiple_choice",
            "options": ["خوارزمية...", "برنامج...", "مجال علمي...", "لغة برمجة..."],
            "correct": 2
        }
    ]
}

# What the builder function does with it:
from engine.docx_builders import build_test
build_test(content, output_path="output/DSAI/U01/DSAI_U01_Pre_Test.docx")
```

---

## 5. Claude Code Agent Design Patterns

### 5.1 Subagent Tool Design

From the Claude Code documentation and best practices:

**Tool selection by role:**
- **Read-only agents** (analysts, reviewers): `Read, Grep, Glob`
- **Research agents**: `Read, Grep, Glob, WebFetch, WebSearch`
- **Document generators**: `Read, Write, Edit, Bash, Glob, Grep`

**For this project's subagents:**
- `storyboard-analyst`: Read, Grep, Glob (read content, no writing)
- `storyboard-test`: Read, Bash (read content, run builder script)
- `storyboard-video`: Read, Bash (read content, run builder script)
- etc.

### 5.2 Agent Configuration Pattern

Subagents are defined as Markdown files with YAML frontmatter in `.claude/agents/`:

```yaml
---
name: storyboard-test
description: Generates pre-test, post-test, and course exam documents
tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Test Storyboard Generator

You generate test/exam storyboard documents. You:

1. Read the raw course content using Read tool
2. Analyze content and generate questions
3. Structure your output as a Python dictionary
4. Call the builder function via Bash to produce the document

## Output Format

Your output must be a Python dictionary with this exact structure:
{...schema here...}
```

### 5.3 Making Code Self-Documenting for AI Agents

When building the template engine, follow these patterns for maximum AI comprehension:

1. **Explicit function signatures with docstrings**:
```python
def build_test(
    content: dict,
    output_path: str,
    template_type: str = "pre_test",  # "pre_test" | "post_test" | "course_exam"
) -> str:
    """Build a test/exam storyboard document.

    Args:
        content: Dictionary with keys:
            - element_code (str): e.g., "DSAI_U01_Pre_Test"
            - project_name (str): Arabic project name
            - unit (str): Unit number and name
            - element_name (str): Element display name
            - designer (str): Designer name
            - date (str): Date string
            - questions (list[dict]): Each with:
                - number (int): Question number
                - text (str): Question text in Arabic
                - type (str): "multiple_choice" or "true_false"
                - options (list[str]): Answer options
                - correct (int): Index of correct answer (0-based)
        output_path: Full path for the output .docx file
        template_type: Type of test document

    Returns:
        str: The output file path on success
    """
```

2. **Type-safe configuration constants**:
```python
# Colors as named constants, not magic strings
HEADER_BG = "31849B"
LABEL_BG = "DBE5F1"
VALUE_BG = "FFFFFF"
HEADER_TEXT = "FFFFFF"
BODY_TEXT = "000000"

# Font configuration
FONT_BODY = "Sakkal Majalla"
FONT_HEADER = "Sakkal Majalla"
FONT_FOOTER = "Tahoma"
FONT_WATERMARK = "Helvetica Neue"
```

3. **Builder pattern with method chaining** (optional but useful):
```python
class DocxBuilder:
    def __init__(self):
        self.doc = Document()
        self._setup_page()

    def add_metadata_table(self, **kwargs) -> 'DocxBuilder':
        """Add the standard 7-row metadata table."""
        ...
        return self

    def add_content_table(self, headers, rows) -> 'DocxBuilder':
        """Add a content table with formatted rows."""
        ...
        return self

    def save(self, path: str) -> str:
        """Save the document and return the path."""
        self.doc.save(path)
        return path
```

### 5.4 Error Handling for Agent Tools

```python
def build_test(content: dict, output_path: str) -> dict:
    """Returns a result dict that agents can interpret."""
    try:
        # Validate required fields
        required = ["element_code", "project_name", "questions"]
        missing = [f for f in required if f not in content]
        if missing:
            return {
                "success": False,
                "error": f"Missing required fields: {missing}",
                "output_path": None
            }

        # Build document...
        path = _build_document(content, output_path)

        return {
            "success": True,
            "error": None,
            "output_path": path,
            "question_count": len(content["questions"])
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output_path": None
        }
```

---

## 6. Recommended Architecture for This Project

### 6.1 Module Structure

```
engine/
  __init__.py
  constants.py          # Colors, fonts, measurements
  rtl_helpers.py        # All RTL/bidi workaround functions
  docx_base.py          # Base DOCX builder (metadata table, page setup)
  pptx_base.py          # Base PPTX builder (slide setup, branding)
  builders/
    __init__.py
    test_builder.py     # Pre-test, post-test, course exam
    activity_builder.py # Interactive activity
    video_builder.py    # Motion video
    discussion_builder.py
    assignment_builder.py
    objectives_builder.py
    infographic_builder.py
    summary_builder.py
    lecture_builder.py  # Interactive lecture (PPTX)
```

### 6.2 Base DOCX Builder

Every DOCX template shares the same structure:
1. Page setup (A4 landscape, 1-inch margins)
2. Header with watermark text
3. Metadata table (7 rows, 2 columns)
4. Content-specific table(s)
5. Footer with page numbers

The base builder handles steps 1-3 and 5. Each specific builder extends it for step 4.

```python
# engine/docx_base.py

class StoryboardDocxBuilder:
    """Base builder for all DOCX storyboard templates."""

    def __init__(self, config: dict):
        """
        config must contain:
            project_code, project_name, unit, element_name,
            element_code, designer, date, header_title
        """
        self.config = config
        self.doc = Document()
        self._setup_page()

    def _setup_page(self):
        """Configure A4 landscape with 1-inch margins."""
        section = self.doc.sections[0]
        section.page_width = Cm(29.7)
        section.page_height = Cm(21.0)
        section.orientation = WD_ORIENT.LANDSCAPE
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    def add_metadata_table(self):
        """Add the standard 7-row, 2-column metadata table."""
        table = self.doc.add_table(rows=7, cols=2)
        docx_set_table_rtl(table)

        # Row 0: Header (merged)
        header_cell = table.cell(0, 0)
        header_cell.merge(table.cell(0, 1))
        header_cell.text = self.config['header_title']
        set_cell_shading(header_cell, HEADER_BG)
        # ... format text white, bold, centered

        # Rows 1-6: Label-value pairs
        labels = [
            ("رمز العنصر", self.config['element_code']),
            ("اسم المشروع", self.config['project_name']),
            ("رقم/اسم الوحدة", self.config['unit']),
            ("اسم العنصر", self.config['element_name']),
            ("المصمم التعليمي", self.config['designer']),
            ("التاريخ", self.config['date']),
        ]
        for i, (label, value) in enumerate(labels, start=1):
            label_cell = table.cell(i, 0)
            value_cell = table.cell(i, 1)
            label_cell.text = label
            value_cell.text = value
            set_cell_shading(label_cell, LABEL_BG)
            # ... format fonts, alignment, RTL

        return self

    def save(self, output_path: str) -> str:
        self.doc.save(output_path)
        return output_path
```

### 6.3 Specific Builder Example (Test Builder)

```python
# engine/builders/test_builder.py

class TestBuilder(StoryboardDocxBuilder):
    """Builder for pre-test, post-test, and course exam documents."""

    def add_questions(self, questions: list[dict]):
        """Add question tables to the document.

        Each question gets its own table with:
        - Question text row (merged header)
        - Answer options rows
        - Correct answer row
        """
        for q in questions:
            self.doc.add_paragraph()  # spacing between questions
            table = self.doc.add_table(rows=2 + len(q['options']), cols=2)
            docx_set_table_rtl(table)

            # Row 0: Question number + text
            q_cell = table.cell(0, 0)
            q_cell.merge(table.cell(0, 1))
            q_cell.text = f"السؤال {q['number']}: {q['text']}"
            set_cell_shading(q_cell, HEADER_BG)

            # Rows 1-N: Options
            for j, option in enumerate(q['options']):
                label_cell = table.cell(j + 1, 0)
                option_cell = table.cell(j + 1, 1)
                label_cell.text = chr(ord('أ') + j)  # Arabic letters
                option_cell.text = option

            # Last row: Correct answer
            answer_cell = table.cell(len(q['options']) + 1, 0)
            answer_cell.merge(table.cell(len(q['options']) + 1, 1))
            answer_cell.text = f"الإجابة الصحيحة: {q['options'][q['correct']]}"
            set_cell_shading(answer_cell, LABEL_BG)

        return self


def build_test(content: dict, output_path: str) -> dict:
    """Entry point for AI subagent to generate a test document.

    Args:
        content: {
            "element_code": str,
            "project_name": str,
            "unit": str,
            "element_name": str,
            "designer": str,
            "date": str,
            "header_title": str,  # e.g., "قالب سيناريو الاختبار القبلي"
            "questions": [
                {
                    "number": int,
                    "text": str,
                    "type": "multiple_choice" | "true_false",
                    "options": list[str],
                    "correct": int  # 0-based index
                }
            ]
        }
        output_path: str - full path to save the .docx file

    Returns:
        dict: {"success": bool, "output_path": str|None, "error": str|None}
    """
    try:
        builder = TestBuilder(content)
        builder.add_metadata_table()
        builder.add_questions(content['questions'])
        path = builder.save(output_path)
        return {"success": True, "output_path": path, "error": None}
    except Exception as e:
        return {"success": False, "output_path": None, "error": str(e)}
```

### 6.4 PPTX Builder (Interactive Lecture)

The PPTX builder follows the same pattern but for PowerPoint:

```python
# engine/pptx_base.py

class StoryboardPptxBuilder:
    """Base builder for PPTX storyboard templates (interactive lecture)."""

    def __init__(self, config: dict):
        self.config = config
        self.prs = Presentation()
        self._setup_slide_size()

    def _setup_slide_size(self):
        """Set slide dimensions to match template."""
        self.prs.slide_width = Inches(13.333)  # widescreen 16:9
        self.prs.slide_height = Inches(7.5)

    def add_title_slide(self, title: str, subtitle: str = ""):
        """Add a title slide with RTL Arabic text."""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        # Add background shape
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0), Inches(0),
            self.prs.slide_width, self.prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(0x31, 0x84, 0x9B)

        # Add title text box
        txBox = slide.shapes.add_textbox(
            Inches(1), Inches(2.5), Inches(11), Inches(2)
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.RIGHT
        pptx_set_paragraph_rtl(p)
        run = p.runs[0]
        run.font.size = Pt(36)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.name = 'Sakkal Majalla'
        pptx_set_cs_font(run, 'Sakkal Majalla')

        return slide

    def add_content_slide(self, title: str, content_text: str):
        """Add a content slide with header and body text."""
        # ... implementation
        pass

    def save(self, output_path: str) -> str:
        self.prs.save(output_path)
        return output_path
```

---

## 7. Common Pitfalls and Solutions

### 7.1 Pitfall: Reusing XML Elements Across Cells

**Problem**: When you create a shading element and append it to multiple cells, it MOVES from the first cell to the second instead of being copied.

**Solution**: Always create a NEW element for each cell:
```python
# WRONG:
shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="31849B"/>')
cell1._tc.get_or_add_tcPr().append(shading)
cell2._tc.get_or_add_tcPr().append(shading)  # This REMOVES it from cell1!

# RIGHT:
for cell in [cell1, cell2]:
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="31849B"/>')
    cell._tc.get_or_add_tcPr().append(shading)
```

### 7.2 Pitfall: RTL Font Name Disappears

**Problem**: Setting RTL=True on a style causes `font.name` to be ignored. The text renders in a default font instead of the specified one.

**Solution**: Always set BOTH `font.name` (Latin) and `font.cs_name` (complex script/Arabic):
```python
run.font.name = 'Sakkal Majalla'
run.font.cs_name = 'Sakkal Majalla'
```

### 7.3 Pitfall: Text Overlapping in Template-Fill Approach

**Problem**: When replacing placeholder text in templates, the new text may overflow its container, overlapping with adjacent shapes.

**Solution**: Use template-as-code. Create shapes with known dimensions that fit the content.

### 7.4 Pitfall: Paragraph Runs Splitting

**Problem**: python-docx/python-pptx may split text into multiple runs even when you set it as a single string. This happens when formatting changes mid-text.

**Solution**: Always set ALL formatting on the paragraph first, then add text via a single run:
```python
# WRONG (may create multiple runs):
paragraph.text = "Some text"
paragraph.runs[0].font.bold = True

# RIGHT (guaranteed single run):
paragraph.clear()
run = paragraph.add_run("Some text")
run.font.bold = True
run.font.name = 'Sakkal Majalla'
run.font.cs_name = 'Sakkal Majalla'
```

### 7.5 Pitfall: Table Width Not Respected

**Problem**: Setting column widths doesn't always produce the expected result because Word auto-adjusts based on content.

**Solution**: Set the table's autofit behavior and use explicit widths:
```python
from docx.shared import Twips

table.autofit = False
table.columns[0].width = Twips(4050)
table.columns[1].width = Twips(9900)

# Also set preferred width on each cell for certainty:
for row in table.rows:
    row.cells[0].width = Twips(4050)
    row.cells[1].width = Twips(9900)
```

### 7.6 Pitfall: Header/Footer Complexity

**Problem**: python-docx headers and footers are tricky -- they have their own paragraph and run objects, and RTL settings must be applied separately.

**Solution**: Access header/footer through the section and format carefully:
```python
section = doc.sections[0]
header = section.header
header.is_linked_to_previous = False

# Add header paragraph
p = header.paragraphs[0]
p.clear()
run = p.add_run("Header text")
run.font.name = 'Helvetica Neue'
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x00, 0x7A, 0x37)
```

### 7.7 Pitfall: Merged Cell Text Access

**Problem**: After merging cells, only the merge-origin cell (top-left) retains text. Accessing text in spanned cells returns empty strings.

**Solution**: Always work with the merge-origin cell:
```python
cell = table.cell(0, 0)
cell.merge(table.cell(0, 2))
# Now cell (0,0) is the merge origin -- set text here
cell.text = "Merged header text"
# table.cell(0, 1) and table.cell(0, 2) are spanned -- don't set text on them
```

---

## Summary of Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | Template-as-code | Full control over RTL, formatting, and structure |
| Document library | python-docx + python-pptx | Standard, well-supported, sufficient for OOXML |
| RTL approach | XML-level workarounds via helper module | Neither library has complete RTL support natively |
| AI interface | Structured dict -> Builder function | AI produces data, builder handles formatting |
| Font | Sakkal Majalla (primary) | Windows system font, Naskh calligraphy, matches templates |
| Module structure | Base builder + specific builders | DRY code, consistent formatting across all 13 types |
| Error handling | Return dict with success/error | Agents can parse and report errors clearly |

---

## References

- [python-pptx documentation](https://python-pptx.readthedocs.io/en/latest/)
- [python-pptx quickstart](https://python-pptx.readthedocs.io/en/latest/user/quickstart.html)
- [python-pptx working with text](https://python-pptx.readthedocs.io/en/latest/user/text.html)
- [python-pptx tables](https://python-pptx.readthedocs.io/en/latest/user/table.html)
- [python-pptx shape fills](https://python-pptx.readthedocs.io/en/latest/dev/analysis/dml-fill.html)
- [python-pptx XML access (issue #626)](https://github.com/scanny/python-pptx/issues/626)
- [python-docx RTL bidi workaround (issue #1411)](https://github.com/python-openxml/python-docx/issues/1411)
- [python-docx RTL font bug (issue #430)](https://github.com/python-openxml/python-docx/issues/430)
- [python-docx table direction RTL (issue #1227)](https://github.com/python-openxml/python-docx/issues/1227)
- [python-docx cell borders workaround (issue #433)](https://github.com/python-openxml/python-docx/issues/433)
- [python-docx cell shading (issue #434)](https://github.com/python-openxml/python-docx/issues/434)
- [python-docx bidi PR #307](https://github.com/python-openxml/python-docx/pull/307/files)
- [python-docx WD_TABLE_DIRECTION API](https://python-docx.readthedocs.io/en/latest/api/enum/WdTableDirection.html)
- [Presenton open-source AI presentation generator](https://github.com/presenton/presenton)
- [PPTAgent agentic framework](https://github.com/icip-cas/PPTAgent)
- [PptxGenJS RTL support (issue #73)](https://github.com/gitbrent/PptxGenJS/issues/73)
- [Claude Code subagent docs](https://code.claude.com/docs/en/sub-agents)
- [Claude Code subagent best practices](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)
- [Sakkal Majalla font (Microsoft)](https://learn.microsoft.com/en-us/typography/font-list/sakkal-majalla)
- [Tajawal font (Google Fonts)](https://fonts.google.com/specimen/Tajawal)
