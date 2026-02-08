# DOCX Template Gap Analysis

Deep comparison of original template XML/PDF vs our `engine/docx_engine.py` output.
Generated: 2026-02-08

---

## Common Elements (All Templates)

### Page Setup

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Page size | w=16840 h=11907 (A4 Landscape) | 29.7cm x 21.0cm | MATCH (equivalent) |
| Orientation | landscape | WD_ORIENT.LANDSCAPE | MATCH |
| Top margin | 1440 twips (2.54cm) | 2.54cm | MATCH |
| Bottom margin | 1440 twips | 2.54cm | MATCH |
| Left margin | 1440 twips | 2.54cm | MATCH |
| Right margin | 1440 twips | 2.54cm | MATCH |
| Footer distance | 397 twips (0.7cm) | 0.7cm | MATCH |
| Header distance | 144 twips (0.25cm) for most; 567 twips (1.0cm) for Activity/Video | 0.25cm always | GAP: Activity and Video templates use header_distance=567 (1.0cm), engine always uses 0.25cm |

### Page Header (Logo Area)

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Structure | Two logos in header: eduArabia (left/anchor) + client logo (right/inline) | No header at all - engine skips header entirely | CRITICAL GAP: Engine does not create page headers with logos |
| eduArabia logo | Anchor positioned, cx=1990090 cy=402590 EMU (~2.2in x 0.4in) | Missing | CRITICAL GAP |
| Client logo | Inline, cx=1073150 cy=832976 EMU (~1.2in x 0.9in) | Missing | CRITICAL GAP |
| Header font | Helvetica Neue, 10pt (sz=20 half-pts), color=#007A37 green | Engine defines FONT_HEADER but never uses it | CRITICAL GAP |
| Header line spacing | 360 (1.5x) | N/A | GAP |
| Header direction | RTL (bidi) | N/A | GAP |

**Note on logos**: The template XML references `image1.png` (eduArabia) and `image2.jpeg` (client). In the Learning Map example PDF, the client logo is Najran University. In the Test/Discussion/Assignment examples, the client logo is Ministry of Education. Logos are per-project branding stored in `projects/[code]/branding/`.

### Page Footer

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Font | Tahoma, sz=16 (8pt) | Tahoma 8pt | MATCH |
| Color | #000000 | #000000 | MATCH |
| Structure | Two paragraphs: 1) top-border line + tabs, 2) "Page X of Y" | Single paragraph "Page X of Y" | GAP: Missing top-border separator line above footer |
| Border | top border: single, sz=4, color=#000000 on first paragraph | No border | GAP: Missing horizontal rule above footer |
| Spacing | before=240 on first paragraph | None | GAP |
| Indent | right=-709, hanging=2 | None | GAP |
| Tab stops | right at pos=10348 | None | GAP |

### Metadata Table (Page 1 - All Types Except Video)

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table width | 13950 dxa | 13950 dxa | MATCH |
| Column 0 width | 4050 dxa | 4050 dxa | MATCH |
| Column 1 width | 9900 dxa | 9900 dxa | MATCH |
| Table indent | -10 dxa | Not set | MINOR GAP |
| Table layout | fixed | Set via autofit=False | MATCH |
| RTL/bidiVisual | Yes | Yes | MATCH |
| Table style | "affff" | Not set (uses defaults) | MINOR (style name irrelevant if borders set correctly) |

#### Metadata Table Borders

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table-level outer | sz=4, black | sz=4, black | MATCH |
| Table-level insideH | sz=18, white | sz=18, white | MATCH |
| Table-level insideV | sz=18, white | sz=18, white | MATCH |
| Row 0 cell borders | top=12, left=12, bottom=8, right=12 (THICK outer frame) | No cell-level borders | GAP: Header row has thicker cell-level borders than table default |
| Rows 1-6 cell borders | all sides sz=8, black | No cell-level borders | GAP: Data rows override table borders with sz=8 black on all sides |

**Important**: The template uses cell-level border overrides on EVERY cell, not just table-level borders. The table-level borders (sz=4 outer, sz=18 white inner) are defaults, but each cell overrides them with sz=8 black. The header row (Row 0) uses even thicker borders: sz=12 on top/left/right, sz=8 on bottom.

#### Metadata Table Row Heights

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Row 0 (header) | trHeight=1400 | Not set (auto-height) | GAP: Header row should have explicit height of 1400 twips |
| Rows 1-6 | trHeight=20 (min height) | Not set | MINOR GAP |

#### Metadata Table Content Formatting

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Header text (Row 0) | Sakkal Majalla, bold (b+bCs), white (#FFFFFF), CENTER, default size (12pt from docDefaults sz=24) | Sakkal Majalla, bold, white, CENTER, 10pt body | GAP: Engine uses FONT_SIZE_BODY=10pt, template uses docDefaults 12pt (sz=24 half-pts) |
| Label cells (col 0) | Sakkal Majalla, bold (b+bCs), black, RTL, default size 12pt | Bold, black, RTL, 10pt | GAP: Font size should be 12pt (default) not 10pt |
| Value cells (col 1) | Sakkal Majalla, bold (b+bCs), default size 12pt | Bold, no explicit size | GAP: Should be 12pt |
| Label shading | #DBE5F1 | #DBE5F1 | MATCH |
| Value shading rows 2-4 | #FFFFFF | #FFFFFF | MATCH |
| Value shading rows 1,5,6 | No explicit shading (transparent) | Row 1: None, Row 5-6: None | MATCH |
| Vertical alignment | center on all cells | center on header and row 1 only | GAP: All rows should have vAlign=center |
| Paragraph indent | hanging=2 on label cells | Not set | MINOR GAP |

### Default Font Size Issue

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| docDefaults sz | 24 half-pts = 12pt | Engine uses FONT_SIZE_BODY=10pt | CRITICAL GAP: The template's default font is 12pt, NOT 10pt. All text without explicit size inherits 12pt. Engine hardcodes 10pt. |
| docDefaults szCs | 24 half-pts = 12pt | Not set explicitly in engine | GAP |
| docDefaults font | Times New Roman (overridden per-cell to Sakkal Majalla) | Sakkal Majalla | OK (engine sets it per-run) |

---

## Type-Specific Analysis

### 1. Test Template (Pre-Test / Post-Test / Course Exam)

#### Metadata Table
Same as common metadata table above. Title: "قالب سيناريو اختبار"

#### Test Info Table (Page 2, Table 2)

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table width | 14175 dxa | 14175 dxa | MATCH |
| Column 0 | 3018 dxa | 3018 dxa | MATCH |
| Column 1 | 11157 dxa | 11157 dxa | MATCH |
| Table style | "affff4" | N/A | OK |
| Borders | all sides sz=4, black (outer + inside) | all sz=4, black | MATCH |
| Header row (R0) | merged, shading=#DBE5F1 (theme accent1 tint 33) | merged, #DBE5F1 | MATCH |
| Header text | "معلومات الاختبار", sz=28 (14pt), bCs (not b), center | sz=14pt, color black, center | GAP: Template uses bCs only (bold complex-script), engine uses generic bold. Both render as bold for Arabic, but XML differs |
| Label cells (R1-R2 C0) | sz=28 (14pt), bCs, shading=#DBE5F1 | sz=14pt, #DBE5F1 | MATCH (close enough) |
| Value cells (R1-R2 C1) | default size (12pt), bold, black | bold, black, no size | GAP: Value text should be 12pt |
| Paragraph spacing | before=240, after=240 on ALL cells | Not set | GAP: Missing paragraph spacing in test info cells |

#### Questions Table (Page 3+, Table 3)

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table width | 14678 dxa | 14678 dxa | MATCH |
| Table indent | -714 dxa | Not set | GAP: Questions table has negative indent to extend into margins |
| Column widths | 3240, 4433, 4050, 2955 | 3240, 4433, 4050, 2955 | MATCH |
| Borders | all sides sz=4, black | all sz=4, black | MATCH |
| Header row (R0) | shading=#DBE5F1, sz=28 (14pt), bCs, center | #DBE5F1, 14pt, center | MATCH |
| Header 4th col text | "رابط/وصف الصور (إن وجد)" | "رابط/وصف الصور (إن وجد)" | MATCH |
| Data row spacing | before=240, after=240 | Not set | GAP: All question rows need paragraph spacing |
| Data row paragraph indent | hanging=3 on col 0, hanging=3 on other cols | Not set | MINOR GAP |

### 2. Activity Template (Interactive Activity)

#### Metadata Table
Same as common. Title: "قالب سيناريو نشاط تفاعلي"
Header distance: 567 twips (1.0cm) - different from other templates.

#### Activity Scene Table (Page 2+)

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table width | 13950 dxa | 13950 dxa | MATCH |
| Column 0 | 4050 dxa | 4050 dxa | MATCH |
| Column 1 | 9900 dxa | 9900 dxa | MATCH |
| Table outer borders | sz=12, black (THICK) | sz=12, black | MATCH |
| Inside borders | sz=18, white (invisible) | sz=18, white | MATCH |
| Row 0 (scene title) | merged, #DBE5F1, bold (b+bCs), center, vAlign=center | merged, #DBE5F1, bold, center | MATCH |
| Row 1 C0 | "وصف المشهد", #DBE5F1, bold, center, vAlign=center | same | MATCH |
| Row 1 C1 | "عناصر المشهد", #DBE5F1, bold, center, vAlign=center | same | MATCH |
| Row 2 C0 | Description text, NO shading, bold (b+bCs for content text), default align | Not bold in engine | GAP: Row 2 C0 (scene description) should be bold |
| Rows 3-6 C0 | Label text, NO shading, NOT bold | Not bold | MATCH |
| Rows 7-9 C0 | Label text, #FFFFFF shading, NOT bold | No shading | GAP: Rows 7-9 label cells have explicit white (#FFFFFF) shading in template |
| Row 6 C1 | on_screen_text, bold | Not bold | GAP: on_screen_text content in col 1 should be bold |
| Row 7 C1 | steps, bold | Not bold | GAP: Steps content should be bold |

### 3. Video Template (Motion Video)

#### Metadata Table (6 rows, NOT 7)

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Row count | 6 (no unit row) | 6 | MATCH |
| Row 0 height | 1898 twips | Not set | GAP: Should set explicit height |
| Header text size | sz=28 (14pt), bold | 14pt, bold | MATCH |
| Cell borders | ALL cells sz=8, black (including header) | Table-level sz=4 outer, sz=18 white inner | GAP: Video metadata uses cell-level sz=8 borders everywhere; engine only sets table-level borders |
| Label cells (R1-5 C0) | NOT bold (no b or bCs), default 12pt | Not bold, no size | GAP: Missing font size (should be 12pt default) |
| Value cells (R1-5 C1) | NOT bold, default 12pt | Not bold, no size | MATCH behavior but GAP on size |
| Header distance | 567 twips (1.0cm) | 0.25cm | GAP |

#### Video Scene Table

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table width | 13960 dxa | 13960 dxa | MATCH |
| Column widths | 3490, 3002, 4418, 3050 | 3490, 3002, 4418, 3050 | MATCH |
| ALL borders | sz=8, black (inside + outside) | sz=8, black | MATCH |
| Scene header (R0) | merged 4 cols, #CFE2F3 | merged, #CFE2F3 | MATCH |
| R1 label | "شاشة توضيحية للمشهد", no shading, center | center | MATCH |
| R1 value | merged cols 1-3 | merged | MATCH |
| R2 label | "مؤثرات صوتية خاصة", no shading, center | center | MATCH |
| R3 sub-headers | 4 individual cells, no shading, center | center | MATCH |
| Sub-header text R3 C2 | "الوصف التفصيلي للمشهد والتزامن مع النص المقروء والصور" | Same (but missing space before والصور) | VERY MINOR |
| Sub-header text R3 C3 | "روابط الصور" | "روابط الصور" | MATCH |

### 4. Learning Map / Infographic (Group A)

#### Content Table (Page 2)

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table width | 14175 dxa | 14175 dxa | MATCH |
| Column 0 | 3015 dxa | 3015 dxa | MATCH |
| Column 1 | 11160 dxa | 11160 dxa | MATCH |
| ALL borders | sz=4, black (inside + outside) | sz=4, black | MATCH |
| Row 0 (header) | merged, #DBE5F1, "الشاشة / الانفوجرافيك", bCs (bold CS), center | merged, #DBE5F1, center | MATCH |
| Row 0 spacing | before=240, after=240 | Not set | GAP: Should have paragraph spacing |
| Col 0 shading (R1-R4) | #FFFFFF (explicit white) | #FFFFFF | MATCH |
| Col 0 alignment | center | center | MATCH |
| Col 0 font weight | R1: bold (b+bCs), R2: bold, R3: NOT bold (bCs only), R4: NOT bold (bCs only) | All bold | GAP: R3 "مصادر الصور" and R4 "الوصف التفصيلي" should be bCs only (not b) |
| Col 0 vertical align | R1: none, R2: none, R3: center, R4: center | R1: center, R4: center | GAP: R3 should have vAlign=center; R1 should NOT |
| Col 1 alignment | R1: center, R2-R4: right (RTL default) | R1: center, R2-R4: right | MATCH |
| Paragraph indent | ind hanging=3 on some label cells | Not set | MINOR GAP |

### 5. Objectives Template (Group A - same structure as Infographic)

Same as Learning Map/Infographic above. Title: "قالب سيناريو إنفوجرافيك"
No structural differences from Learning Map template.

### 6. Summary Template (Group A - same structure)

Same structure. Title: "قالب سيناريو إنفوجرافيك"

Content table borders differ slightly:
| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Inside borders | sz=4, black | sz=4, black | MATCH |

### 7. Discussion Template (Group B)

#### Content Table

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Table width | 13950 dxa | 13950 dxa | MATCH |
| Column 0 | 3330 dxa | 3330 dxa | MATCH |
| Column 1 | 10620 dxa | 10620 dxa | MATCH |
| Outer borders | sz=4, black | sz=4, black | MATCH |
| Inside borders | sz=18, white | sz=18, white | MATCH |
| Row 0 header | "نقاش 1", merged, #DBE5F1, bold (b+bCs), center | bold, #DBE5F1, center | MATCH |
| Col 0 labels (R1-R4) | All #DBE5F1, bold (b+bCs), center | All #DBE5F1, bold, center | MATCH |
| Col 1 R1 | align=center (for image area) | right | GAP: Discussion screen description cell should be CENTER aligned |
| Col 1 R2-R4 | align=both (justify) | right | GAP: Content cells should use JUSTIFY alignment, not RIGHT |

### 8. Assignment Template (Group B)

Same structure as Discussion. Title: "قالب سيناريو واجب"

| Property | Template (XML) | Engine | Gap |
|----------|---------------|--------|-----|
| Col 1 R1 | align=center | right | GAP: Same as Discussion |
| Col 1 R2-R4 | align=default (right) | right | MATCH (Assignment uses default/right unlike Discussion's justify) |

---

## Priority Gap Summary

### CRITICAL (Visible, affects every document)

1. **No page header with logos** - Engine produces no header. Templates have eduArabia logo (left) + client logo (right) on every page. This is the most visible difference.

2. **Default font size is 12pt, not 10pt** - Template docDefaults uses sz=24 (12pt). Engine hardcodes FONT_SIZE_BODY=10pt. All text appears smaller than intended.

3. **Missing cell-level borders on metadata table** - Template has cell-level border overrides (sz=8 on data rows, sz=12 on header row). Engine only sets table-level borders (sz=4 outer, sz=18 white inner). Visual result: borders appear thinner than template.

### HIGH (Noticeable visual differences)

4. **Missing footer top border** - Template footer has a horizontal line (top border sz=4) above "Page X of Y". Engine footer has no separator.

5. **Missing paragraph spacing in test tables** - Test info and questions tables use before=240/after=240 paragraph spacing. Engine doesn't set this, making cells look cramped.

6. **Missing metadata table header row height** - Template header row has explicit height=1400 twips. Engine uses auto-height. The teal header bar appears shorter than template.

7. **Questions table missing negative indent** - Template questions table has tblInd=-714 to extend into left margin. Engine doesn't set this, so questions table is narrower visually.

8. **Discussion content cells should use JUSTIFY alignment** - Template uses `jc=both` for content cells. Engine uses RIGHT.

### MEDIUM (Minor visual differences)

9. **Header distance varies by template type** - Activity and Video templates use 567 twips (1.0cm), others use 144 twips (0.25cm). Engine always uses 0.25cm.

10. **Group A col 0 bold/vAlign inconsistencies** - Rows 3-4 labels should use bCs-only (not full bold). Vertical alignment varies per row.

11. **Activity template: missing bold on some content cells** - Row 2 C0 (description), Row 6 C1 (on_screen_text), and Row 7 C1 (steps) should be bold.

12. **Video metadata: borders should be sz=8 cell-level** - Not table-level defaults.

### LOW (Negligible)

13. Table indent -10 on metadata table (barely visible)
14. Paragraph hanging indent on label cells (minimal visual impact)
15. Video sub-header minor spacing difference

---

## Recommended Fix Order

1. Fix default font size: change FONT_SIZE_BODY from 10 to 12
2. Add page header with logo support (requires logo image paths in builder constructor)
3. Add cell-level border overrides on metadata table (sz=12 header, sz=8 data)
4. Set explicit header row height (1400 twips)
5. Add footer top border separator
6. Add paragraph spacing (before=240, after=240) to test table cells
7. Set questions table indent to -714
8. Fix Discussion content cell alignment to JUSTIFY
9. Fix Group A bold/vAlign per-row differences
10. Fix Activity template bold inconsistencies
