# Storyboard Generator — Product Specification

> AI-powered system that transforms raw client course content into production-ready educational storyboard documents (docx/pptx), following exact template formatting with per-project branding.

---

## 1. System Overview

### What It Does
Takes raw educational content (mixed files from clients) and produces **formatted storyboard documents** — one for each learning element in a course unit. The storyboards are the planning/documentation layer between raw content and final e-learning production.

### Who Uses It
- **Primary user**: Qusai (product designer at eduArabia) — the instructional design coordinator
- **Clients**: Saudi universities, Ministry of Education, corporate training departments
- **Downstream**: Production teams who build the final e-learning content from these storyboards

### Key Principles
- Arabic-first (RTL) with Cairo font
- Exact template fidelity — output must be visually identical to template files
- Step-by-step workflow with user review at each stage
- Multi-project support with persistent memory
- AI generates content (objectives, scenes, activities) — user reviews and approves

---

## 2. Storyboard Types (13 Total)

| # | Type (Arabic) | Type (English) | Template File | Output Format |
|---|--------------|----------------|---------------|---------------|
| 1 | فيديو موشن | Motion Video | قالب فيديو.docx | .docx |
| 2 | نشاط تفاعلي | Interactive Activity | قالب النشاط.docx | .docx |
| 3 | محاضرة تفاعلية | Interactive Lecture | قالب المحاضرة التفاعلية- عربي.pptx | .pptx |
| 4 | محاضرة PDF | PDF Lecture | Same as #3 but exported as PDF, no interactive instructions | .pptx → .pdf |
| 6 | إنفوجرافيك تفاعلي | Interactive Infographic / Learning Map | قالب خارطة التعلم.docx | .docx |
| 7 | اختبار قبلي | Pre-Test | قالب الاختبارات.docx | .docx |
| 8 | اختبار بعدي | Post-Test | قالب الاختبارات.docx | .docx |
| 9 | نشاط نقاش | Discussion Activity | قالب النقاش.docx | .docx |
| 10 | واجب | Assignment | قالب الواجب.docx | .docx |
| 11 | اختبار المقرر | Course Exam | قالب الاختبارات.docx | .docx |
| 12 | الأهداف التعليمية | Learning Objectives | قالب الأهداف التعليمية.docx | .docx |
| 13 | الملخص | Summary | قالب الملخص.docx | .docx |

> Note: Type #5 intentionally skipped in numbering.

### Type-Specific Rules

#### Pre-Test (#7)
- **3–5 questions** only
- Multiple choice or True/False only

#### Post-Test (#8)
- **7–10 questions**
- Multiple choice or True/False only

#### Course Exam (#11)
- Question count **determined with client** (stored in project config)

#### PDF Lecture (#4)
- Same template as Interactive Lecture (#3)
- Exported as PDF
- **Remove all interactive/instructional commands** — pure content only

#### Motion Video (#1)
- Scene-by-scene with **full production detail**:
  - Screen layouts (split-screen, zoom, transitions)
  - Animation timings and sync with narration
  - Text overlay positions
  - Image/video placement descriptions
- AI generates actual images using **nano-banana-pro** model
- Narration text (النص العلمي المقروء) in plain Arabic — no tashkeel

#### Interactive Activity (#2)
- Each activity includes:
  - Scene description + screenshot mockup description
  - Full question text with all answer options
  - Feedback for correct answer
  - Feedback for incorrect answer
  - Feedback after attempts exhausted
  - Steps (خطوات النشاط)
  - Correct answer
  - Buttons shown after max attempts
- AI **suggests** interaction types; user decides

#### Interactive Lecture (#3)
- Creates **actual PPTX slides** (not just storyboard descriptions)
- Includes:
  - Content with proper layouts
  - Full Storyline-style interactions (click-to-reveal, drag-and-drop, hotspots, branching)
  - PowerPoint native animations where possible
  - Written storyboard instructions ON slides for complex interactions
- This is the most complex deliverable


#### Discussion (#9)
- Discussion topic with context paragraph
- Discussion guidelines and instructions
- Related learning objectives

#### Assignment (#10)
- Assignment text with clear instructions
- Submission guidelines (format, deadline reference)
- Related learning objectives

#### Learning Objectives (#12)
- AI generates from content analysis
- Aligned to **Bloom's Taxonomy** (Remember → Create)
- Formatted per template structure

#### Summary (#13)
- Condensed summary of unit content
- Formatted per template structure

---

## 3. Workflow

### Phase 0: Project Setup (One-time per project)
User provides a **full project brief**:
- Project code (e.g., `DSAI`)
- Project name (e.g., `تطوير 15 مقرر إلكتروني – جامعة نجران`)
- Client name and institution
- Client logo file path
- Header/branding images
- Designer name (e.g., `تسنيم خالد`)
- Color scheme (if different from template defaults)
- Number of units
- Unit names/numbers
- Any special requirements

System saves this as a **persistent project config** at:
```
dev/storyboard/projects/[project-code]/config.json
```

### Phase 1: Content Analysis (Per unit)
1. User shares file paths to raw content (mixed: pptx, docx, pdf, images, text)
2. User specifies which storyboard types and counts for this unit
3. System reads and deeply analyzes all content files
4. System produces an **analysis summary**:
   - Key topics identified
   - Content structure breakdown
   - Suggested content distribution across storyboard types
   - Any gaps or questions about the content

**→ User reviews and approves before proceeding**

### Phase 2: Learning Objectives
1. System generates Bloom's Taxonomy-aligned objectives from content
2. Objectives formatted per template
3. Presented to user for review

**→ User reviews, edits, and approves**

### Phase 3: Individual Storyboard Generation
Each storyboard type is produced **one at a time** in sequence:
1. System generates one storyboard document
2. Presents it to user for review
3. User approves or requests changes
4. Move to next storyboard type

**Suggested order** (adjustable per user preference):
1. Learning Objectives (الأهداف التعليمية)
2. Learning Map / Infographic (خارطة التعلم)
3. Pre-Test (الاختبار القبلي)
4. Interactive Lecture (المحاضرة التفاعلية)
5. PDF Lecture (محاضرة PDF)
6. Motion Video (فيديو موشن)
7. Interactive Activities × N (الأنشطة التفاعلية)
8. Discussion (النقاش)
9. Assignment (الواجب)
10. Post-Test (الاختبار البعدي)
11. Summary (الملخص)
12. Course Exam (if applicable)

### Phase 4: Unit Completion
- All storyboards saved to output folder
- Progress tracked per unit

---

## 4. Input Specification

### Content Input
- **Method**: File paths shared in chat
- **Formats supported**: .pptx, .docx, .pdf, images (.png, .jpg), .txt, any readable format
- **Scope**: Each content share = one complete unit
- **Tools**: Use `/docx` skill for .docx, `/pptx` skill for .pptx, Read tool for .pdf and images

### Project Brief Input
- Provided once per project
- Stored persistently in project config
- Carried across sessions via config file

---

## 5. Output Specification

### File Location
```
dev/storyboard/output/[project-code]/U[XX]/
```
Example:
```
dev/storyboard/output/DSAI/U01/
├── DSAI_U01_Learning_Objectives.docx
├── DSAI_U01_Learning_Map.docx
├── DSAI_U01_Pre_Test.docx
├── DSAI_U01_Interactive_lecture.pptx
├── DSAI_U01_PDF_lecture.pptx
├── DSAI_U01_Video.docx
├── DSAI_U01_Activity1.1.docx
├── DSAI_U01_Activity1.2.docx
├── DSAI_U01_Activity1.3.docx
├── DSAI_U01_Discussion.docx
├── DSAI_U01_Assignment.docx
├── DSAI_U01_Post_Test.docx
├── DSAI_U01_Summary.docx
└── assets/
    └── images/          ← Generated images (nano-banana-pro)
```

### File Naming Convention
```
[PROJECT_CODE]_U[UNIT_NUMBER]_[Element_Type]
```
- Activity numbering: `Activity[Unit].[Sequence]` (e.g., `Activity1.1`, `Activity1.2`)
- Follow the exact pattern from the DSAI examples

### Formatting Requirements
- **EXACT visual match** to template files
- Same tables, colors, fonts, logos, header/footer
- Use template files as base and fill in content
- Per-project branding (logos, header images, institutional colors)
- Arabic RTL throughout

---

## 6. Technical Architecture

### Claude Code Project Structure
```
dev/storyboard/
├── CLAUDE.md                          ← Project instructions (coordinator pattern)
├── .claude/
│   ├── settings.json                  ← Permissions
│   ├── agents/                        ← Specialized subagents
│   │   ├── storyboard-analyst.md      ← Analyzes raw content
│   │   ├── storyboard-objectives.md   ← Generates Bloom's objectives
│   │   ├── storyboard-video.md        ← Video motion storyboard
│   │   ├── storyboard-activity.md     ← Interactive activity storyboard
│   │   ├── storyboard-lecture.md      ← Interactive lecture PPTX
│   │   ├── storyboard-test.md         ← Pre/Post/Course test storyboard
│   │   ├── storyboard-discussion.md   ← Discussion storyboard
│   │   ├── storyboard-assignment.md   ← Assignment storyboard
│   │   ├── storyboard-infographic.md  ← Learning map / infographic
│   │   └── storyboard-summary.md      ← Summary storyboard
│   ├── skills/
│   │   └── storyboard-templates/      ← Template knowledge + examples
│   │       ├── SKILL.md
│   │       └── resources/
│   │           ├── template-structures.md   ← Documented template structures
│   │           └── examples/                ← Analyzed example patterns
│   └── commands/
│       └── storyboard.md              ← /storyboard slash command
│
├── templates/                         ← Copied template files (base for generation)
│   ├── قالب فيديو.docx
│   ├── قالب النشاط.docx
│   ├── قالب المحاضرة التفاعلية- عربي.pptx
│   ├── قالب خارطة التعلم.docx
│   ├── قالب الاختبارات.docx
│   ├── قالب النقاش.docx
│   ├── قالب الواجب.docx
│   ├── قالب الأهداف التعليمية.docx
│   └── قالب الملخص.docx
│
├── projects/                          ← Persistent project configs
│   └── [project-code]/
│       ├── config.json                ← Project metadata, branding, unit structure
│       └── branding/
│           ├── logo.png
│           └── header.png
│
├── output/                            ← Generated storyboard files
│   └── [project-code]/
│       └── U[XX]/
│           ├── [CODE]_U[XX]_[Type].docx/.pptx
│           └── assets/images/
│
└── specs/                             ← This spec + any research docs
    └── SPEC.md
```

### Agent Architecture

#### Main Agent (Coordinator)
- Orchestrates the workflow
- Reads user input, manages project context
- Delegates to specialized agents
- Presents results for review
- NEVER produces storyboard content directly

#### Specialized Agents (10)
Each agent:
- Has deep knowledge of its template structure
- Uses /docx or /pptx skills to generate output
- Receives analyzed content + objectives from coordinator
- Produces one storyboard document at a time

### Skills
- **storyboard-templates**: Contains documented template structures, field mappings, and example patterns for each of the 13 storyboard types
- References nano-banana-pro skill from scorm-projects for image generation

### Persistent Memory
- Project configs saved as JSON files in `projects/[code]/config.json`
- Carries across sessions — system reads config when user references a project
- Stores: project metadata, branding paths, unit progress, designer name, dates

---

## 7. Template Field Mappings

### Common Header Fields (All Types)
| Field (Arabic) | Field (English) | Source |
|----------------|-----------------|--------|
| رمز العنصر | Element Code | Auto-generated: [CODE]_U[XX]_[Type] |
| اسم المشروع | Project Name | From project config |
| رقم/اسم الوحدة | Unit Number/Name | From user input per unit |
| اسم العنصر | Element Name | Generated based on content |
| المصمم التعليمي | Instructional Designer | From project config |
| التاريخ | Date | Current date |

### Video Template Fields
| Field | Description |
|-------|-------------|
| مكان عرض الفيديو | Where video appears in the interactive lecture |
| مشهد العنوان | Title scene (intro) |
| المشهد الأول..N | Numbered scenes |
| شاشة توضيحية للمشهد | Screenshot mockup description (with screen labels) |
| مؤثرات صوتية خاصة | Special sound effects |
| النص العلمي المقروء | Narration text (plain Arabic, no tashkeel) |
| النصوص التي تظهر في المشاهد | On-screen text |
| الوصف التفصيلي للمشهد | Detailed scene description with sync timing |
| روابط الصور | Image links/references |

### Test Template Fields
| Field | Description |
|-------|-------------|
| معلومات الاختبار | Test info (description, instructions) |
| الوصف | Test description |
| الإرشادات | Guidelines (attempts, save progress, etc.) |
| نص السؤال | Question text |
| بدائل السؤال | Answer options (4 for MC, 2 for T/F) |
| الإجابة الصحيحة | Correct answer |
| رابط/وصف الصور | Image link/description (if applicable) |

### Activity Template Fields
| Field | Description |
|-------|-------------|
| وصف المشهد | Scene description |
| عناصر المشهد | Scene elements (with screenshot) |
| وصف الصور | Image descriptions |
| وصف موشن جرافيك | Motion graphic description (if needed) |
| مؤثرات صوتية خاصة | Special sound effects |
| نص يظهر على الشاشة | On-screen text (full question + options + feedback) |
| خطوات النشاط | Activity steps |
| الإجابة الصحيحة | Correct answer |
| الأزرار بعد نفاذ المحاولات | Buttons after attempts exhausted |

### Discussion Template Fields
| Field | Description |
|-------|-------------|
| شاشة توضيحية للنقاش | Discussion screenshot mockup |
| النص العلمي المعروض على الشاشة | Discussion topic text |
| تعليمات وإرشادات النقاش | Discussion guidelines |
| الأهداف التعليمية المرتبطة | Related learning objectives |

### Assignment Template Fields
| Field | Description |
|-------|-------------|
| شاشة توضيحية للواجب | Assignment screenshot mockup |
| النص العلمي المعروض على الشاشة | Assignment text |
| تعليمات وإرشادات الواجب | Assignment guidelines |
| الأهداف التعليمية المرتبطة | Related learning objectives |

### Infographic / Learning Map Fields
| Field | Description |
|-------|-------------|
| شاشة توضيحية للانفوجرافيك | Infographic screenshot mockup |
| النص العلمي المعروض على الشاشة | Learning path instructions |
| مصادر الصور | Image sources (icons per step) |
| الوصف التفصيلي للشاشة | Detailed screen description |

---

## 8. Quality Standards

### Content Quality
- All objectives aligned to Bloom's Taxonomy
- Questions must be well-formed with clear correct answers
- Feedback (correct/incorrect/exhausted) must be educational, not just "right/wrong"
- Discussion topics must encourage critical thinking
- Assignment instructions must be clear and actionable

### Document Quality
- Exact visual match to template files
- All tables properly formatted
- Logos and headers correct per project branding
- Arabic text properly right-aligned
- No broken formatting or empty fields

### Pedagogical Quality
- Activities should use varied interaction types (AI suggests, user decides)
- Pre-test should preview concepts (diagnostic, not graded)
- Post-test should assess against learning objectives
- Content progression should follow logical learning sequence

---

## 9. Dependencies & Integrations

### Required Skills
- `/docx` — For creating and editing Word documents
- `/pptx` — For creating and editing PowerPoint presentations
- `nano-banana-pro` — For generating images (referenced from scorm-projects)

### Template Files Location
```
/Users/qusaiabushanap/Downloads/storyboard template/
```
These will be copied to `dev/storyboard/templates/` during project setup.

### Example Files Location (Reference)
```
/Users/qusaiabushanap/Downloads/storyboard template/example/
```

---

## 10. Constraints & Limitations

- Arabic text: No tashkeel/diacritics needed
- PowerPoint interactions: Full Storyline-style where possible, with written instructions for anything beyond native PPTX capabilities
- Image generation: Uses nano-banana-pro model for actual image creation
- File format: docx must use python-docx compatible structures; pptx must use python-pptx
- Template fidelity: Must preserve original template styling, tables, colors, and branding
- One storyboard at a time with user review between each

---

## 11. Success Criteria

A successful storyboard generation session should:
1. Produce documents that are **visually indistinguishable** from hand-crafted storyboards
2. Content should be **pedagogically sound** (proper Bloom's alignment, varied activities)
3. Video storyboards should have **production-ready** scene descriptions
4. Interactive lecture should be **buildable** from the PPTX + instructions
5. All files properly named, organized, and branded
6. User should need **minimal manual edits** after generation

---

*Specification created: 2026-02-07*
*Based on interview with project owner*
*Templates analyzed: 9 docx + 1 pptx templates, 7 filled example files*
