const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
        Header, Footer, PageNumber, HeadingLevel, PageBreak } = require('docx');

// ============================================================
// PROJECT METADATA
// ============================================================
const projectCode = "NJR01";
const projectName = "تطوير مقررات الكترونية - جامعة نجران";
const institution = "جامعة نجران - كلية علوم الحاسب ونظم المعلومات";
const unitNumber = "02";
const unitName = "الذهنية الرقمية وممارسات الابتكار التقني";
const designerName = "فريق التصميم التعليمي";
const date = "2026-02-07";
const elementCode = `${projectCode}_U${unitNumber}_Objectives`;

// ============================================================
// BLOOM'S TAXONOMY LEARNING OBJECTIVES (8 objectives)
// Covering all 9 topics from content analysis across 6 Bloom's levels
// ============================================================
const objectives = [
  {
    number: 1,
    level: "تذكر",
    objective: "ان يعدد المتعلم عناصر الابتكار الثلاثة (ايجاد حلول جديدة، تحسين العمليات، استخدام تقنيات ابداعية) وتقنيات العصف الذهني الاساسية",
    topic: "ما هو الابتكار / اهمية توليد الافكار"
  },
  {
    number: 2,
    level: "فهم",
    objective: "ان يوضح المتعلم مفهوم ريادة الاعمال وعلاقتها بالابتكار التقني مع بيان المتطلبات العقلية لرائد الاعمال",
    topic: "ما هي ريادة الاعمال / عقلية الابتكار التقني"
  },
  {
    number: 3,
    level: "فهم",
    objective: "ان يشرح المتعلم المراحل الخمس للتفكير التصميمي (التعاطف، التحديد، التصور، النمذجة، الاختبار) ودور كل مرحلة في حل المشكلات",
    topic: "التفكير التصميمي"
  },
  {
    number: 4,
    level: "تطبيق",
    objective: "ان يطبق المتعلم طريقة SCAMPER لتوليد افكار ابداعية جديدة انطلاقا من منتج او خدمة قائمة",
    topic: "اهمية توليد الافكار / تقنيات العصف الذهني"
  },
  {
    number: 5,
    level: "تطبيق",
    objective: "ان يستخدم المتعلم مراحل التفكير التصميمي لتحديد احتياجات المستخدم وبناء نموذج اولي لحل مشكلة رقمية واقعية",
    topic: "التفكير التصميمي / النمذجة والتجريب"
  },
  {
    number: 6,
    level: "تحليل",
    objective: "ان يحلل المتعلم العلاقة بين التكنولوجيا وملاءمة السوق ويميز بين انواع النماذج الاولية (ورقية، رقمية، مادية) واستخداماتها",
    topic: "التكنولوجيا وملاءمة السوق"
  },
  {
    number: 7,
    level: "تقييم",
    objective: "ان يقيم المتعلم فرص العمل الريادية بناء على معايير احتياجات العملاء ودراسة الجدوى وقابلية التوسع مع تحديد تحديات الابتكار وحلولها",
    topic: "المرونة والتكيف / التغلب على تحديات الابتكار"
  },
  {
    number: 8,
    level: "ابداع",
    objective: "ان يصمم المتعلم حلا ابتكاريا لمشكلة رقمية واقعية باستخدام مراحل التفكير التصميمي وادوات العقلية الريادية (Lean Startup, Business Model Canvas)",
    topic: "بناء عقلية ريادية / التفكير التصميمي"
  }
];

// ============================================================
// STYLING CONSTANTS
// ============================================================
const PRIMARY_COLOR = "1F4E79";    // Dark blue for headers
const SECONDARY_COLOR = "2E75B6";  // Medium blue for sub-headers
const LIGHT_BG = "D6E4F0";        // Light blue background
const HEADER_BG = "1F4E79";       // Dark blue header background
const WHITE = "FFFFFF";
const BLACK = "000000";
const LIGHT_GRAY = "F2F2F2";

const FONT_AR = "Sakkal Majalla";
const FONT_AR_FALLBACK = "Arial";

const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "BFBFBF" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };
const thickBorder = { style: BorderStyle.SINGLE, size: 2, color: PRIMARY_COLOR };
const headerBorders = { top: thickBorder, bottom: thickBorder, left: thickBorder, right: thickBorder };

// ============================================================
// HELPER: Create a text run with RTL Arabic formatting
// ============================================================
function ar(text, opts = {}) {
  return new TextRun({
    text,
    font: FONT_AR,
    size: opts.size || 24,
    bold: opts.bold || false,
    color: opts.color || BLACK,
    rightToLeft: true,
    ...opts
  });
}

// ============================================================
// HELPER: Create a right-aligned Arabic paragraph
// ============================================================
function arPara(children, opts = {}) {
  const { alignment, spacing, ...rest } = opts;
  return new Paragraph({
    alignment: alignment || AlignmentType.RIGHT,
    bidirectional: true,
    spacing: spacing || { before: 60, after: 60 },
    children: Array.isArray(children) ? children : [children],
    ...rest
  });
}

// ============================================================
// HELPER: Create a table cell
// ============================================================
function cell(children, opts = {}) {
  const paras = Array.isArray(children) ? children : [children];
  return new TableCell({
    borders: opts.borders || cellBorders,
    width: opts.width ? { size: opts.width, type: WidthType.DXA } : undefined,
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    verticalAlign: opts.vAlign || VerticalAlign.CENTER,
    children: paras.map(c => {
      if (c instanceof Paragraph) return c;
      return arPara(c, { alignment: opts.alignment || AlignmentType.CENTER });
    })
  });
}

// ============================================================
// BUILD METADATA TABLE (Project Info)
// ============================================================
function buildMetadataTable() {
  const metaRows = [
    ["رمز العنصر", elementCode],
    ["اسم المشروع", projectName],
    ["المؤسسة", institution],
    ["رقم الوحدة", `الوحدة ${unitNumber}`],
    ["عنوان الوحدة", unitName],
    ["المصمم التعليمي", designerName],
    ["التاريخ", date]
  ];

  return new Table({
    columnWidths: [3000, 6360],
    rows: metaRows.map(([label, value]) =>
      new TableRow({
        children: [
          cell(ar(label, { bold: true, size: 22, color: WHITE }), {
            width: 3000,
            shading: PRIMARY_COLOR,
            borders: headerBorders,
            alignment: AlignmentType.CENTER
          }),
          cell(ar(value, { size: 22 }), {
            width: 6360,
            borders: cellBorders,
            alignment: AlignmentType.CENTER
          })
        ]
      })
    )
  });
}

// ============================================================
// BUILD OBJECTIVES TABLE
// ============================================================
function buildObjectivesTable() {
  // Header row
  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      cell(ar("م", { bold: true, size: 22, color: WHITE }), {
        width: 600,
        shading: PRIMARY_COLOR,
        borders: headerBorders
      }),
      cell(ar("مستوى بلوم", { bold: true, size: 22, color: WHITE }), {
        width: 1400,
        shading: PRIMARY_COLOR,
        borders: headerBorders
      }),
      cell(ar("الهدف التعليمي", { bold: true, size: 22, color: WHITE }), {
        width: 5360,
        shading: PRIMARY_COLOR,
        borders: headerBorders
      }),
      cell(ar("الموضوع المرتبط", { bold: true, size: 22, color: WHITE }), {
        width: 2000,
        shading: PRIMARY_COLOR,
        borders: headerBorders
      })
    ]
  });

  // Data rows
  const dataRows = objectives.map((obj, i) => {
    const rowShading = i % 2 === 0 ? undefined : LIGHT_GRAY;
    return new TableRow({
      children: [
        cell(ar(String(obj.number), { size: 22 }), {
          width: 600,
          shading: rowShading,
          borders: cellBorders
        }),
        cell(ar(obj.level, { size: 22, bold: true, color: SECONDARY_COLOR }), {
          width: 1400,
          shading: rowShading,
          borders: cellBorders
        }),
        cell(
          arPara(ar(obj.objective, { size: 22 }), { alignment: AlignmentType.RIGHT }),
          {
            width: 5360,
            shading: rowShading,
            borders: cellBorders,
            alignment: AlignmentType.RIGHT
          }
        ),
        cell(
          arPara(ar(obj.topic, { size: 20 }), { alignment: AlignmentType.CENTER }),
          {
            width: 2000,
            shading: rowShading,
            borders: cellBorders,
            alignment: AlignmentType.CENTER
          }
        )
      ]
    });
  });

  return new Table({
    columnWidths: [600, 1400, 5360, 2000],
    rows: [headerRow, ...dataRows]
  });
}

// ============================================================
// BUILD BLOOM'S TAXONOMY SUMMARY TABLE
// ============================================================
function buildBloomSummaryTable() {
  const bloomLevels = [
    { level: "تذكر (Remember)", count: 1, color: "E8F5E9" },
    { level: "فهم (Understand)", count: 2, color: "E3F2FD" },
    { level: "تطبيق (Apply)", count: 2, color: "FFF3E0" },
    { level: "تحليل (Analyze)", count: 1, color: "FCE4EC" },
    { level: "تقييم (Evaluate)", count: 1, color: "F3E5F5" },
    { level: "ابداع (Create)", count: 1, color: "E0F7FA" }
  ];

  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      cell(ar("مستوى بلوم", { bold: true, size: 22, color: WHITE }), {
        width: 4680,
        shading: PRIMARY_COLOR,
        borders: headerBorders
      }),
      cell(ar("عدد الاهداف", { bold: true, size: 22, color: WHITE }), {
        width: 4680,
        shading: PRIMARY_COLOR,
        borders: headerBorders
      })
    ]
  });

  const dataRows = bloomLevels.map(bl =>
    new TableRow({
      children: [
        cell(ar(bl.level, { size: 22, bold: true }), {
          width: 4680,
          shading: bl.color,
          borders: cellBorders
        }),
        cell(ar(String(bl.count), { size: 22 }), {
          width: 4680,
          shading: bl.color,
          borders: cellBorders
        })
      ]
    })
  );

  return new Table({
    columnWidths: [4680, 4680],
    rows: [headerRow, ...dataRows]
  });
}

// ============================================================
// BUILD THE DOCUMENT
// ============================================================
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: FONT_AR, size: 24, rightToLeft: true }
      }
    },
    paragraphStyles: [
      {
        id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 40, bold: true, color: PRIMARY_COLOR, font: FONT_AR },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER }
      },
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: PRIMARY_COLOR, font: FONT_AR },
        paragraph: { spacing: { before: 360, after: 200 }, alignment: AlignmentType.RIGHT }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: SECONDARY_COLOR, font: FONT_AR },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.RIGHT }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        size: { width: 12240, height: 15840 }
      },
      bidi: true
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { after: 0 },
            children: [
              ar(institution, { size: 18, color: "666666" }),
              ar("  |  ", { size: 18, color: "999999" }),
              ar(projectName, { size: 18, color: "666666" })
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              ar(`${elementCode}  -  `, { size: 16, color: "999999" }),
              new TextRun({ children: [PageNumber.CURRENT], font: FONT_AR, size: 16, color: "999999" })
            ]
          })
        ]
      })
    },
    children: [
      // ============================================================
      // DOCUMENT TITLE
      // ============================================================
      new Paragraph({
        alignment: AlignmentType.CENTER,
        bidirectional: true,
        spacing: { before: 400, after: 100 },
        children: [ar("الاهداف التعليمية", { size: 40, bold: true, color: PRIMARY_COLOR })]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        bidirectional: true,
        spacing: { before: 0, after: 100 },
        children: [ar("Learning Objectives", { size: 28, color: SECONDARY_COLOR })]
      }),

      // Separator line
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 100, after: 300 },
        children: [ar("ـــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ", { color: SECONDARY_COLOR, size: 16 })]
      }),

      // ============================================================
      // SECTION 1: PROJECT METADATA
      // ============================================================
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        bidirectional: true,
        spacing: { before: 200, after: 200 },
        children: [ar("اولا: بيانات المشروع", { size: 28, bold: true, color: PRIMARY_COLOR })]
      }),

      buildMetadataTable(),

      // Spacer
      new Paragraph({ spacing: { before: 400, after: 100 }, children: [new TextRun("")] }),

      // ============================================================
      // SECTION 2: LEARNING OBJECTIVES TABLE
      // ============================================================
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        bidirectional: true,
        spacing: { before: 200, after: 200 },
        children: [ar("ثانيا: الاهداف التعليمية للوحدة", { size: 28, bold: true, color: PRIMARY_COLOR })]
      }),

      new Paragraph({
        alignment: AlignmentType.RIGHT,
        bidirectional: true,
        spacing: { before: 0, after: 200 },
        children: [ar(`عنوان الوحدة: ${unitName}`, { size: 22, color: "333333" })]
      }),

      new Paragraph({
        alignment: AlignmentType.RIGHT,
        bidirectional: true,
        spacing: { before: 0, after: 200 },
        children: [ar("بنهاية هذه الوحدة يتوقع ان يكون المتعلم قادرا على:", { size: 22, bold: true, color: "333333" })]
      }),

      buildObjectivesTable(),

      // Spacer
      new Paragraph({ spacing: { before: 400, after: 100 }, children: [new TextRun("")] }),

      // ============================================================
      // SECTION 3: BLOOM'S TAXONOMY DISTRIBUTION
      // ============================================================
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        bidirectional: true,
        spacing: { before: 200, after: 200 },
        children: [ar("ثالثا: توزيع الاهداف على مستويات تصنيف بلوم", { size: 28, bold: true, color: PRIMARY_COLOR })]
      }),

      buildBloomSummaryTable(),

      // Spacer
      new Paragraph({ spacing: { before: 400, after: 100 }, children: [new TextRun("")] }),

      // ============================================================
      // SECTION 4: NOTES
      // ============================================================
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        bidirectional: true,
        spacing: { before: 200, after: 200 },
        children: [ar("رابعا: ملاحظات", { size: 28, bold: true, color: PRIMARY_COLOR })]
      }),

      arPara(ar("تم صياغة الاهداف التعليمية وفق تصنيف بلوم المعدل (Bloom's Revised Taxonomy) لتغطي المستويات المعرفية الستة.", { size: 22 })),
      arPara(ar("تغطي الاهداف جميع الموضوعات الرئيسية التسعة الواردة في محتوى الوحدة.", { size: 22 })),
      arPara(ar("صيغت الاهداف بصورة قابلة للقياس باستخدام افعال سلوكية محددة.", { size: 22 })),
      arPara(ar("تتدرج الاهداف من المستويات الدنيا (التذكر والفهم) الى المستويات العليا (التقييم والابداع) لضمان تنمية مهارات التفكير العليا.", { size: 22 })),
      arPara(ar("تم ربط كل هدف بالموضوع المقابل له في المحتوى لتسهيل عملية التصميم التعليمي والتقييم.", { size: 22 })),
    ]
  }]
});

// ============================================================
// EXPORT
// ============================================================
const outputDir = `/Users/qusaiabushanap/dev/storyboard/output/NJR01/U02`;
fs.mkdirSync(outputDir, { recursive: true });
const outputPath = path.join(outputDir, "NJR01_U02_Objectives.docx");

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log(`Document saved to: ${outputPath}`);
}).catch(err => {
  console.error('Error generating document:', err);
  process.exit(1);
});
