---
name: storyboard-templates
description: Template structures, field mappings, and generation patterns for all 13 educational storyboard types. Loaded by storyboard agents when generating documents.
---

# Storyboard Templates Knowledge

This skill contains the complete field mappings and generation rules for all 13 storyboard types.

## Template Files Location
All template files are at: `templates/`

## Common Header Fields (All Types)

| Field (Arabic) | Field (English) | Source |
|----------------|-----------------|--------|
| رمز العنصر | Element Code | Auto-generated: [CODE]_U[XX]_[Type] |
| اسم المشروع | Project Name | From `projects/[code]/config.json` → projectName |
| رقم/اسم الوحدة | Unit Number/Name | From user input per unit |
| اسم العنصر | Element Name | Generated based on content + type |
| المصمم التعليمي | Instructional Designer | From config → designerName |
| التاريخ | Date | Current date (DD-MM-YYYY format) |

## Project Config Schema

```json
{
  "projectCode": "DSAI",
  "projectName": "تطوير 15 مقرر إلكتروني – جامعة نجران",
  "clientName": "جامعة نجران",
  "designerName": "تسنيم خالد",
  "branding": {
    "logo": "branding/logo.png",
    "header": "branding/header.png",
    "colors": { "primary": "#0097A7", "secondary": "#333333", "accent": "#FFB300" }
  },
  "units": [],
  "testConfig": {
    "preTestQuestions": "3-5",
    "postTestQuestions": "7-10",
    "courseExamQuestions": null
  }
}
```

## Element Code Patterns

| Type | Code Pattern | Example |
|------|-------------|---------|
| Learning Objectives | [CODE]_U[XX]_Learning_Objectives | DSAI_U01_Learning_Objectives |
| Learning Map | [CODE]_U[XX]_Learning_Map | DSAI_U01_Learning_Map |
| Pre-Test | [CODE]_U[XX]_Pre_Test | DSAI_U01_Pre_Test |
| Post-Test | [CODE]_U[XX]_Post_Test | DSAI_U01_Post_Test |
| Course Exam | [CODE]_U[XX]_Course_Exam | DSAI_U01_Course_Exam |
| Interactive Lecture | [CODE]_U[XX]_Interactive_lecture | DSAI_U01_Interactive_lecture |
| PDF Lecture | [CODE]_U[XX]_PDF_lecture | DSAI_U01_PDF_lecture |
| Video | [CODE]_U[XX]_Video | DSAI_U08_Interactive_lecture_Video |
| Activity | [CODE]_U[XX]_Activity[U].[N] | DSAI_U01_Activity1.1 |
| Discussion | [CODE]_U[XX]_Discussion | DSAI_U01_Discussion |
| Assignment | [CODE]_U[XX]_Assignment | DSAI_U01_Assignment |
| Summary | [CODE]_U[XX]_Summary | DSAI_U01_Summary |

## Template-to-Type Mapping

| Template File | Used By Types |
|--------------|--------------|
| قالب فيديو.docx | Motion Video |
| قالب النشاط.docx | Interactive Activity |
| قالب المحاضرة التفاعلية- عربي.pptx | Interactive Lecture, PDF Lecture |
| قالب خارطة التعلم.docx | Learning Map / Infographic |
| قالب الاختبارات.docx | Pre-Test, Post-Test, Course Exam |
| قالب النقاش.docx | Discussion |
| قالب الواجب.docx | Assignment |
| قالب الأهداف التعليمية.docx | Learning Objectives |
| قالب الملخص.docx | Summary |

## Bloom's Taxonomy Verbs (Arabic)

### تذكر (Remember)
يُعرّف، يَذكُر، يُحدّد، يَسرُد، يُسمّي، يَصِف

### فهم (Understand)
يُفسّر، يُوضّح، يُلخّص، يُقارن، يشرح، يُصنّف

### تطبيق (Apply)
يُطبّق، يَستخدم، يُنفّذ، يَحُل، يُوظّف، يُنتج

### تحليل (Analyze)
يُحلّل، يُميّز، يَفحص، يُقارن، يَستنتج، يُنظّم

### تقييم (Evaluate)
يُقيّم، يَنتقد، يَحكُم، يُبرّر، يُدافع، يُوصي

### إبداع (Create)
يُصمّم، يَبتكر، يُخطّط، يُنشئ، يُؤلّف، يَقترح

## Activity Interaction Types

| Type (Arabic) | Type (English) | Best For |
|--------------|----------------|----------|
| اختيار من متعدد | Multiple Choice | Knowledge recall, concept identification |
| سحب وإفلات | Drag and Drop | Categorization, matching, ordering |
| مطابقة | Matching | Term-definition pairs, concept connections |
| ترتيب | Sorting/Sequencing | Process steps, chronological order |
| ملء الفراغ | Fill in the Blank | Key term recall, formula application |
| صح/خطأ | True/False | Myth busting, fact verification |
| النقر على الصورة | Hotspot | Diagram labeling, visual identification |
| سيناريو متفرع | Branching Scenario | Decision-making, problem-solving |
