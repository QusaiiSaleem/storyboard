# Storyboard Generator

AI-powered system that transforms raw client course content into production-ready educational storyboard documents (DOCX/PPTX) for Arabic e-learning courses.

## Architecture

```
User provides raw content (PDF, DOCX, PPTX, images)
  → Main agent COORDINATES (never generates content directly)
    → Specialized subagents produce content
      → Template engine builds formatted documents
        → Output: production-ready DOCX/PPTX files
```

### Core Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Template Engine | `engine/docx_engine.py`, `engine/pptx_engine.py` | Builds documents from scratch matching template designs |
| Engine Skill | `.claude/skills/storyboard-templates/` | API reference for the engine (preloaded by agents) |
| Subagents (10) | `.claude/agents/storyboard-*.md` | Specialized content producers |
| Coordinator | `.claude/commands/storyboard.md` | Orchestration workflow (`/storyboard`) |
| Project Configs | `projects/[code]/config.json` | Per-project metadata and branding |
| Visual References | `templates/` | Original template files (visual reference ONLY, not edited) |

### How Document Generation Works

The engine uses a **"template-as-code"** approach:
- Python builders construct DOCX/PPTX documents from scratch
- All formatting, RTL, fonts, colors, and borders are handled automatically
- Agents produce CONTENT and call engine builders via `python3 -c "..."`
- Agents DO NOT open or edit template files directly
- Each agent preloads the `storyboard-templates` skill for engine API reference

## Non-Negotiable Rules

1. **COORDINATOR ONLY** — The main agent orchestrates. NEVER produce storyboard content directly. Always delegate to specialized subagents.
2. **ONE AT A TIME** — Generate each storyboard type individually with user review between each.
3. **ENGINE BUILDS DOCUMENTS** — All documents are built by the template engine (`engine/`). Never manipulate template files. Agents call builders via Bash.
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

## 12 Storyboard Types

| # | Type | Agent | Engine Builder |
|---|------|-------|----------------|
| 1 | فيديو موشن (Motion Video) | storyboard-video | VideoBuilder (DOCX) |
| 2 | نشاط تفاعلي (Interactive Activity) | storyboard-activity | ActivityBuilder (DOCX) |
| 3 | محاضرة تفاعلية (Interactive Lecture) | storyboard-lecture | LectureBuilder (PPTX) |
| 4 | محاضرة PDF (PDF Lecture) | storyboard-lecture (Mode 2) | LectureBuilder (PPTX) |
| 5 | إنفوجرافيك (Learning Map) | storyboard-infographic | InfographicBuilder (DOCX) |
| 6 | اختبار قبلي (Pre-Test) | storyboard-test | TestBuilder (DOCX) |
| 7 | اختبار بعدي (Post-Test) | storyboard-test | TestBuilder (DOCX) |
| 8 | نقاش (Discussion) | storyboard-discussion | DiscussionBuilder (DOCX) |
| 9 | واجب (Assignment) | storyboard-assignment | AssignmentBuilder (DOCX) |
| 10 | اختبار المقرر (Course Exam) | storyboard-test | TestBuilder (DOCX) |
| 11 | أهداف تعليمية (Learning Objectives) | storyboard-objectives | ObjectivesBuilder (DOCX) |
| 12 | ملخص (Summary) | storyboard-summary | SummaryBuilder (DOCX) |

## Project Setup

When starting a new project, collect:
- Project code (e.g., `NJR01`)
- Project name, client name, institution
- Client logo + header image file paths
- Designer name
- Unit count and names

Save to: `projects/[project-code]/config.json`

When starting a unit, user provides:
- File paths to raw content
- Which storyboard types and counts needed
- Unit number and name

## File Naming Convention

```
[PROJECT_CODE]_U[UNIT_NUMBER]_[Element_Type]
```
Examples: `NJR01_U02_Pre_Test.docx`, `NJR01_U02_Activity2.1.docx`

## Output Location

```
output/[project-code]/U[XX]/
```

## Test Rules

### Pre-Test
- 3-5 questions only
- Multiple choice or True/False

### Post-Test
- 7-10 questions
- Multiple choice or True/False

### Course Exam
- Question count per client agreement (stored in project config)

## Content Input
- User shares **file paths** -- read them directly using Read tool
- Content can be: .pptx, .docx, .pdf, images, .txt
- Each content share = one complete unit

## Branding
- Per-project branding (different logos, headers per client)
- Stored in `projects/[project-code]/branding/`
