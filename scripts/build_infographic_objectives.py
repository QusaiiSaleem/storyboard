#!/usr/bin/env python3
"""
Build the Learning Objectives Infographic document for NJR01 U02.
Creates the .docx file directly using zipfile (a docx is just a zip of XML files).

Usage: python3 scripts/build_infographic_objectives.py
"""
import zipfile
import os

OUTPUT_DIR = "/Users/qusaiabushanap/dev/storyboard/output/NJR01/U02"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "NJR01_U02_Infographic_Objectives.docx")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ====================================================================
# Content Configuration
# ====================================================================
PROJECT_CODE = "NJR01"
UNIT_NUM = "02"
PROJECT_NAME = "تطوير مقررات إلكترونية – جامعة نجران"
INSTITUTION = "جامعة نجران - كلية علوم الحاسب ونظم المعلومات"
UNIT_NAME = "الذهنية الرقمية وممارسات الابتكار التقني"
ELEMENT_CODE = f"{PROJECT_CODE}_U{UNIT_NUM}_Infographic_Objectives"
ELEMENT_NAME = "إنفوجرافيك الأهداف التعليمية"
TODAY = "2026-02-07"

# Bloom levels (top to bottom for pyramid display)
BLOOM_LEVELS = [
    ("ابداع", "Create", "9B59B6"),
    ("تقييم", "Evaluate", "3498DB"),
    ("تحليل", "Analyze", "2ECC71"),
    ("تطبيق", "Apply", "F1C40F"),
    ("فهم", "Understand", "E67E22"),
    ("تذكر", "Remember", "E74C3C"),
]

OBJECTIVES = [
    ("تذكر", "E74C3C", "01", "ان يعدد المتعلم عناصر الابتكار الثلاثة وتقنيات العصف الذهني الاساسية"),
    ("فهم", "E67E22", "02", "ان يوضح المتعلم مفهوم ريادة الاعمال وعلاقتها بالابتكار التقني"),
    ("فهم", "E67E22", "03", "ان يشرح المتعلم المراحل الخمس للتفكير التصميمي ودور كل مرحلة"),
    ("تطبيق", "F1C40F", "04", "ان يطبق المتعلم طريقة SCAMPER لتوليد افكار ابداعية جديدة"),
    ("تطبيق", "F1C40F", "05", "ان يستخدم المتعلم مراحل التفكير التصميمي لبناء نموذج اولي"),
    ("تحليل", "2ECC71", "06", "ان يحلل المتعلم العلاقة بين التكنولوجيا وملاءمة السوق"),
    ("تقييم", "3498DB", "07", "ان يقيم المتعلم فرص العمل الريادية بناء على معايير محددة"),
    ("ابداع", "9B59B6", "08", "ان يصمم المتعلم حلا ابتكاريا لمشكلة رقمية واقعية"),
]

# ====================================================================
# XML Templates for required docx files
# ====================================================================

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
</Types>"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOCUMENT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
</Relationships>"""

SETTINGS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
  <w:characterSpacingControl w:val="doNotCompress"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Sakkal Majalla" w:hAnsi="Sakkal Majalla" w:cs="Sakkal Majalla"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="en-US" w:bidi="ar-SA"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:bidi/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr><w:bidi/></w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Sakkal Majalla" w:hAnsi="Sakkal Majalla" w:cs="Sakkal Majalla"/>
    </w:rPr>
  </w:style>
  <w:style w:type="table" w:styleId="TableGrid">
    <w:name w:val="Table Grid"/>
    <w:basedOn w:val="TableNormal"/>
    <w:tblPr>
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>
      </w:tblBorders>
    </w:tblPr>
  </w:style>
  <w:style w:type="table" w:default="1" w:styleId="TableNormal">
    <w:name w:val="Normal Table"/>
    <w:tblPr>
      <w:tblCellMar>
        <w:top w:w="0" w:type="dxa"/>
        <w:left w:w="108" w:type="dxa"/>
        <w:bottom w:w="0" w:type="dxa"/>
        <w:right w:w="108" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
  </w:style>
</w:styles>"""


# ====================================================================
# XML Builder Helpers
# ====================================================================

def esc(text):
    """Escape XML special characters."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def run(text, bold=False, color=None, sz=None, font=None, rtl=True):
    """Create a w:r element."""
    rpr = []
    if font:
        rpr.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>')
    if bold:
        rpr.append('<w:b/><w:bCs/>')
    if color:
        rpr.append(f'<w:color w:val="{color}"/>')
    if sz:
        rpr.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    if rtl:
        rpr.append('<w:rtl/>')
    rpr_xml = f"<w:rPr>{''.join(rpr)}</w:rPr>" if rpr else ""
    t = esc(text)
    sp = ' xml:space="preserve"' if t.startswith(' ') or t.endswith(' ') else ''
    return f'<w:r>{rpr_xml}<w:t{sp}>{t}</w:t></w:r>'


def para(runs_xml, align="right", sb=0, sa=0, il=0, bidi=True):
    """Create a w:p element."""
    pp = []
    if bidi:
        pp.append('<w:bidi/>')
    if align == "center":
        pp.append('<w:jc w:val="center"/>')
    elif align == "right":
        pp.append('<w:jc w:val="right"/>')
    elif align == "left":
        pp.append('<w:jc w:val="left"/>')
    if sb or sa:
        pp.append(f'<w:spacing w:before="{sb}" w:after="{sa}"/>')
    if il:
        pp.append(f'<w:ind w:left="{il}"/>')
    ppr = f"<w:pPr>{''.join(pp)}</w:pPr>" if pp else ""
    return f'<w:p>{ppr}{runs_xml}</w:p>'


def cell(content, w=None, shd=None, cs=None, va="center"):
    """Create a w:tc element."""
    tp = []
    if w:
        tp.append(f'<w:tcW w:w="{w}" w:type="dxa"/>')
    if cs and cs > 1:
        tp.append(f'<w:gridSpan w:val="{cs}"/>')
    if shd:
        tp.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{shd}"/>')
    if va:
        tp.append(f'<w:vAlign w:val="{va}"/>')
    tp.append("""<w:tcBorders>
      <w:top w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
      <w:left w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
      <w:bottom w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
      <w:right w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
    </w:tcBorders>""")
    tpr = f"<w:tcPr>{''.join(tp)}</w:tcPr>"
    return f'<w:tc>{tpr}{content}</w:tc>'


def row(cells):
    return f'<w:tr>{cells}</w:tr>'


def tbl(cols, rows_xml):
    grid = "".join(f'<w:gridCol w:w="{c}"/>' for c in cols)
    return f"""<w:tbl>
<w:tblPr>
  <w:tblW w:w="0" w:type="auto"/>
  <w:tblBorders>
    <w:top w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
    <w:left w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
    <w:right w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
    <w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
    <w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>
  </w:tblBorders>
  <w:tblCellMar>
    <w:top w:w="80" w:type="dxa"/>
    <w:left w:w="120" w:type="dxa"/>
    <w:bottom w:w="80" w:type="dxa"/>
    <w:right w:w="120" w:type="dxa"/>
  </w:tblCellMar>
  <w:bidiVisual/>
</w:tblPr>
<w:tblGrid>{grid}</w:tblGrid>
{rows_xml}
</w:tbl>"""


# ====================================================================
# Build the Document Content
# ====================================================================

def build_header_table():
    """Build the metadata header table."""
    r = []
    # Title row
    r.append(row(cell(
        para(run("قالب سيناريو إنفوجرافيك", bold=True, color="FFFFFF", sz=36, font="Sakkal Majalla"),
             align="center", sb=120, sa=120),
        w=9360, shd="1F4E79", cs=2
    )))
    # Metadata rows
    for label, value in [
        ("رمز العنصر", ELEMENT_CODE),
        ("اسم المشروع", PROJECT_NAME),
        ("المؤسسة", INSTITUTION),
        ("رقم/اسم الوحدة", f"الوحدة {UNIT_NUM} - {UNIT_NAME}"),
        ("اسم العنصر", ELEMENT_NAME),
        ("المصمم التعليمي", "(لم يحدد)"),
        ("التاريخ", TODAY),
    ]:
        r.append(row(
            cell(para(run(label, bold=True, color="FFFFFF", sz=24, font="Sakkal Majalla"),
                      align="center", sb=60, sa=60), w=2500, shd="1F4E79") +
            cell(para(run(value, sz=24, font="Sakkal Majalla"),
                      align="center", sb=60, sa=60), w=6860)
        ))
    return tbl([2500, 6860], "\n".join(r))


def build_bloom_table():
    """Build the Bloom's taxonomy objectives table."""
    r = []
    # Header
    r.append(row(
        cell(para(run("مستوى بلوم", bold=True, color="FFFFFF", sz=24, font="Sakkal Majalla"),
                  align="center", sb=80, sa=80), w=1800, shd="1F4E79") +
        cell(para(run("الهدف التعليمي", bold=True, color="FFFFFF", sz=24, font="Sakkal Majalla"),
                  align="center", sb=80, sa=80), w=7000, shd="1F4E79")
    ))
    # Bloom levels
    for lv_ar, lv_en, lv_color in BLOOM_LEVELS:
        objs = [(n, t) for l, c, n, t in OBJECTIVES if l == lv_ar]
        level_xml = (
            para(run(lv_ar, bold=True, color="FFFFFF", sz=26, font="Sakkal Majalla"),
                 align="center", sb=80, sa=20) +
            para(run(lv_en, bold=True, color="FFFFFF", sz=18, font="Arial", rtl=False),
                 align="center", sb=0, sa=80, bidi=False)
        )
        if objs:
            obj_xml = ""
            for n, t in objs:
                obj_xml += para(
                    run(f"{n}  ", bold=True, color=lv_color, sz=24, font="Arial", rtl=False) +
                    run(t, sz=22, font="Sakkal Majalla"),
                    align="right", sb=60, sa=60
                )
        else:
            obj_xml = para(run("---", color="999999", sz=20), align="center")
        r.append(row(
            cell(level_xml, w=1800, shd=lv_color) +
            cell(obj_xml, w=7000)
        ))
    return tbl([1800, 7000], "\n".join(r))


def build_main_table():
    """Build the main 4-section content table."""
    r = []

    def sec_title(title):
        return row(cell(
            para(run(title, bold=True, color="FFFFFF", sz=28, font="Sakkal Majalla"),
                 align="center", sb=80, sa=80),
            w=9360, shd="2E75B6", cs=2
        ))

    def sec_content(xml):
        return row(cell(xml, w=9360, cs=2))

    # Section 1: Visual mockup
    r.append(sec_title("1. شاشة توضيحية للإنفوجرافيك"))
    s1 = ""
    s1 += para(run("عند الانتهاء من دراسة هذه المحاضرة، يتوقع ان يكون المتعلم قادرا على:",
                    bold=True, sz=24, font="Sakkal Majalla"), align="center", sb=200, sa=200)
    s1 += para("", sb=60, sa=60)
    s1 += build_bloom_table()
    s1 += para("", sb=100, sa=100)
    s1 += para(run("ملاحظة: يتم تصميم الاهداف على شكل هرم بلوم المعرفي بحيث تتدرج المستويات من الاسفل (التذكر) الى الاعلى (الابداع)، مع تخصيص لون مميز لكل مستوى وترقيم الاهداف من 01 الى 08.",
                    sz=20, color="666666", font="Sakkal Majalla"), align="center", sb=60, sa=100)
    r.append(sec_content(s1))

    # Section 2: Scientific text
    r.append(sec_title("2. النص العلمي المعروض على الشاشة"))
    s2 = ""
    s2 += para(run("عند الانتهاء من دراسة هذه المحاضرة، يتوقع ان يكون المتعلم قادرا على:",
                    bold=True, sz=24, font="Sakkal Majalla"), align="right", sb=150, sa=100)
    for i, (lv, clr, num, txt) in enumerate(OBJECTIVES):
        s2 += para(
            run(f"{i+1}. ", bold=True, sz=24, color="2E75B6", font="Sakkal Majalla") +
            run(f"[{lv}] ", bold=True, sz=22, color=clr, font="Sakkal Majalla") +
            run(txt, sz=24, font="Sakkal Majalla"),
            align="right", sb=60, sa=60, il=360
        )
    s2 += para("", sb=80, sa=80)
    r.append(sec_content(s2))

    # Section 3: Image sources
    r.append(sec_title("3. مصادر الصور (إن وجدت)"))
    s3 = para("", sb=80, sa=40)
    for item in [
        "ايقونات مستويات بلوم الستة (تذكر، فهم، تطبيق، تحليل، تقييم، ابداع) بألوان مميزة لكل مستوى",
        "ايقونة هرم تصنيف بلوم المعرفي",
        "ايقونة هدف تعليمي / علم الانجاز",
        "ارقام متسلسلة ملونة (01 الى 08) لترقيم الاهداف",
    ]:
        s3 += para(run(f"- {item}", sz=22, font="Sakkal Majalla"), align="right", sb=40, sa=40, il=360)
    s3 += para("", sb=40, sa=80)
    r.append(sec_content(s3))

    # Section 4: Detailed description
    r.append(sec_title("4. الوصف التفصيلي للشاشة إن لزم"))
    s4 = para("", sb=80, sa=40)
    s4 += para(run("التصميم العام:", bold=True, sz=24, font="Sakkal Majalla"), align="right", sb=80, sa=40)
    s4 += para(run("يعرض الانفوجرافيك الاهداف التعليمية للوحدة الثانية (الذهنية الرقمية وممارسات الابتكار التقني) على شكل هرم تصنيف بلوم المعرفي، حيث يتدرج من المستويات الدنيا (التذكر) في قاعدة الهرم الى المستويات العليا (الابداع) في قمته. يتضمن الانفوجرافيك 8 اهداف تعليمية موزعة على 6 مستويات من تصنيف بلوم.",
                    sz=22, font="Sakkal Majalla"), align="right", sb=40, sa=80, il=360)

    s4 += para(run("توزيع الاهداف على المستويات:", bold=True, sz=24, font="Sakkal Majalla"), align="right", sb=80, sa=40)
    for desc in [
        "مستوى التذكر (1 هدف): يعدد عناصر الابتكار وتقنيات العصف الذهني",
        "مستوى الفهم (2 هدفان): يوضح مفهوم ريادة الاعمال، ويشرح مراحل التفكير التصميمي",
        "مستوى التطبيق (2 هدفان): يطبق طريقة SCAMPER، ويستخدم مراحل التفكير التصميمي",
        "مستوى التحليل (1 هدف): يحلل العلاقة بين التكنولوجيا وملاءمة السوق",
        "مستوى التقييم (1 هدف): يقيم فرص العمل الريادية",
        "مستوى الابداع (1 هدف): يصمم حلا ابتكاريا لمشكلة رقمية",
    ]:
        s4 += para(run(f"- {desc}", sz=22, font="Sakkal Majalla"), align="right", sb=30, sa=30, il=360)

    s4 += para(run("الالوان والعناصر البصرية:", bold=True, sz=24, font="Sakkal Majalla"), align="right", sb=80, sa=40)
    for item in [
        "كل مستوى من مستويات بلوم يمثل بلون مميز (احمر للتذكر، برتقالي للفهم، اصفر للتطبيق، اخضر للتحليل، ازرق للتقييم، بنفسجي للابداع)",
        "الاهداف مرقمة من 01 الى 08 بأرقام ملونة حسب مستوى بلوم المقابل",
        "يظهر عنوان في اعلى الانفوجرافيك: الاهداف التعليمية للوحدة الثانية مع اسم الوحدة",
        "التخطيط من اليمين الى اليسار (RTL) مناسب للغة العربية",
    ]:
        s4 += para(run(f"- {item}", sz=22, font="Sakkal Majalla"), align="right", sb=30, sa=30, il=360)

    s4 += para(run("التفاعل:", bold=True, sz=24, font="Sakkal Majalla"), align="right", sb=80, sa=40)
    s4 += para(run("- لا يوجد تفاعل في هذه الشاشة، هي شاشة عرض ثابتة للأهداف التعليمية",
                    sz=22, font="Sakkal Majalla"), align="right", sb=30, sa=30, il=360)
    s4 += para(run("- يمكن للمتعلم الضغط على كل مستوى لمشاهدة تفاصيل اضافية عن الاهداف المرتبطة به",
                    sz=22, font="Sakkal Majalla"), align="right", sb=30, sa=30, il=360)
    s4 += para("", sb=40, sa=80)
    r.append(sec_content(s4))

    return tbl([2500, 6860], "\n".join(r))


def build_document():
    """Build the complete document XML."""
    body = ""
    # Title
    body += para(run("قالب سيناريو إنفوجرافيك - الأهداف التعليمية",
                      bold=True, color="1F4E79", sz=36, font="Sakkal Majalla"),
                 align="center", sb=0, sa=200)
    body += para(run(f"{UNIT_NAME} | الوحدة {UNIT_NUM}",
                      sz=26, color="666666", font="Sakkal Majalla"),
                 align="center", sb=0, sa=300)
    # Header table
    body += build_header_table()
    # Spacer
    body += para("", sb=300, sa=100)
    # Section header
    body += para(run("الشاشة / الإنفوجرافيك",
                      bold=True, color="1F4E79", sz=32, font="Sakkal Majalla"),
                 align="center", sb=100, sa=200)
    # Main table
    body += build_main_table()
    # Footer
    body += para("", sb=300, sa=100)
    body += para(run(f"{PROJECT_CODE} | {INSTITUTION} | {PROJECT_NAME}",
                      sz=20, color="666666", font="Sakkal Majalla"),
                 align="center", sb=100, sa=100)

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
            xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
            xmlns:o="urn:schemas-microsoft-com:office:office"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
            xmlns:v="urn:schemas-microsoft-com:vml"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:w10="urn:schemas-microsoft-com:office:word"
            xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
            xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
            xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
            xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
            xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
            mc:Ignorable="w14 wp14">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/>
      <w:bidi/>
    </w:sectPr>
  </w:body>
</w:document>"""


# ====================================================================
# Create the .docx file
# ====================================================================

if __name__ == "__main__":
    doc_xml = build_document()

    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('[Content_Types].xml', CONTENT_TYPES)
        zf.writestr('_rels/.rels', RELS)
        zf.writestr('word/_rels/document.xml.rels', DOCUMENT_RELS)
        zf.writestr('word/document.xml', doc_xml)
        zf.writestr('word/styles.xml', STYLES)
        zf.writestr('word/settings.xml', SETTINGS)

    print(f"Document created successfully: {OUTPUT_FILE}")
    print(f"File size: {os.path.getsize(OUTPUT_FILE)} bytes")
