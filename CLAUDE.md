# Storyboard Generator

AI-powered system that transforms raw client course content into production-ready educational storyboard documents (docx/pptx).

## Non-Negotiable Rules

1. **COORDINATOR ONLY** — The main agent is an orchestrator. NEVER produce storyboard content directly. Always delegate to specialized subagents.
2. **ONE AT A TIME** — Generate each storyboard type individually with user review between each.
3. **EXACT TEMPLATE MATCH** — Output documents must be visually identical to template files. Use templates as base, fill in content.
4. **ARABIC RTL** — All content in Arabic, right-to-left. No tashkeel/diacritics needed.
5. **USER DECIDES** — AI suggests (activity types, content distribution), user approves before proceeding.

## Workflow (Every Unit)

```
Phase 1: Content Analysis
  → User shares file paths to raw content + specifies storyboard types/counts
  → Delegate to storyboard-analyst agent
  → Present analysis summary for user review

Phase 2: Learning Objectives
  → Delegate to storyboard-objectives agent
  → Generate Bloom's Taxonomy-aligned objectives
  → Present for user review

Phase 3: Individual Storyboards (one at a time)
  → Delegate to the appropriate specialized agent
  → Present each document for user review
  → Move to next type after approval
```

### Suggested Storyboard Order
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

## Project Setup

When starting a new project, collect:
- Project code (e.g., `DSAI`)
- Project name, client name, institution
- Client logo + header image file paths
- Designer name
- Unit count and names

Save to: `projects/[project-code]/config.json`

When starting a unit, user provides:
- File paths to raw content
- Which storyboard types and counts needed
- Unit number and name

## 13 Storyboard Types

| # | Type | Template | Agent |
|---|------|----------|-------|
| 1 | فيديو موشن (Motion Video) | قالب فيديو.docx | storyboard-video |
| 2 | نشاط تفاعلي (Interactive Activity) | قالب النشاط.docx | storyboard-activity |
| 3 | محاضرة تفاعلية (Interactive Lecture) | قالب المحاضرة التفاعلية- عربي.pptx | storyboard-lecture |
| 4 | محاضرة PDF (PDF Lecture) | Same as #3, export PDF, no interactive commands | storyboard-lecture |
| 6 | إنفوجرافيك (Learning Map) | قالب خارطة التعلم.docx | storyboard-infographic |
| 7 | اختبار قبلي (Pre-Test) | قالب الاختبارات.docx | storyboard-test |
| 8 | اختبار بعدي (Post-Test) | قالب الاختبارات.docx | storyboard-test |
| 9 | نقاش (Discussion) | قالب النقاش.docx | storyboard-discussion |
| 10 | واجب (Assignment) | قالب الواجب.docx | storyboard-assignment |
| 11 | اختبار المقرر (Course Exam) | قالب الاختبارات.docx | storyboard-test |
| 12 | أهداف تعليمية (Learning Objectives) | قالب الأهداف التعليمية.docx | storyboard-objectives |
| 13 | ملخص (Summary) | قالب الملخص.docx | storyboard-summary |

## File Naming Convention

```
[PROJECT_CODE]_U[UNIT_NUMBER]_[Element_Type]
```
Examples: `DSAI_U01_Pre_Test.docx`, `DSAI_U01_Activity1.1.docx`

## Output Location

```
output/[project-code]/U[XX]/
```

## Key Commands

- Use `/docx` skill for all .docx file creation and editing
- Use `/pptx` skill for all .pptx file creation and editing
- Template files are at: `templates/`
- Project configs at: `projects/[project-code]/config.json`

## Test Rules

### Pre-Test
- 3–5 questions only
- Multiple choice or True/False

### Post-Test
- 7–10 questions
- Multiple choice or True/False

### Course Exam
- Question count per client agreement (stored in project config)

## Content Input
- User shares **file paths** — read them directly using Read, /docx, /pptx tools
- Content can be: .pptx, .docx, .pdf, images, .txt
- Each content share = one complete unit

## Branding
- Per-project branding (different logos, headers per client)
- Stored in `projects/[project-code]/branding/`
- Apply to every generated document
