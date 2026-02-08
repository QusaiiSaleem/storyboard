"""
Test script for the DOCX engine after gap-analysis fixes.
Generates one document per builder type to verify all fixes are applied.
"""

import sys
sys.path.insert(0, "/Users/qusaiabushanap/dev/storyboard")

from engine.docx_engine import (
    ObjectivesBuilder,
    SummaryBuilder,
    InfographicBuilder,
    DiscussionBuilder,
    AssignmentBuilder,
    TestBuilder,
    ActivityBuilder,
    VideoBuilder,
)

OUTPUT_DIR = "/Users/qusaiabushanap/dev/storyboard/output/NJR01/U02"

# Common project info for all builders
PROJECT_ARGS = dict(
    project_code="NJR01",
    unit_number=2,
    unit_name="الذهنية الرقمية وممارسات الابتكار التقني",
    project_name="تطوير مقررات إلكترونية – جامعة نجران",
    institution="كلية علوم الحاسب ونظم المعلومات",
    designer="مصمم تجريبي",
)


def test_objectives():
    print("Testing ObjectivesBuilder...")
    b = ObjectivesBuilder(**PROJECT_ARGS)
    b.set_element_name("الأهداف التعليمية")
    b.set_element_code("NJR01_U02_MLO")
    b.set_screen_description("شاشة توضيحية لأهداف الوحدة")
    b.set_content_text(
        "1. يتعرف على مفهوم الذهنية الرقمية\n"
        "2. يفهم ممارسات الابتكار التقني\n"
        "3. يطبق التفكير التصميمي"
    )
    b.set_image_sources("صور من مصادر مفتوحة")
    b.set_detailed_description("وصف تفصيلي للأهداف")
    b.build()
    path = f"{OUTPUT_DIR}/test_objectives.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


def test_summary():
    print("Testing SummaryBuilder...")
    b = SummaryBuilder(**PROJECT_ARGS)
    b.set_element_name("ملخص الوحدة")
    b.set_element_code("NJR01_U02_Summary")
    b.set_content_text("ملخص المحتوى التعليمي للوحدة الثانية")
    b.build()
    path = f"{OUTPUT_DIR}/test_summary.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


def test_infographic():
    print("Testing InfographicBuilder...")
    b = InfographicBuilder(**PROJECT_ARGS)
    b.set_element_name("خارطة التعلم")
    b.set_element_code("NJR01_U02_Learning_Map")
    b.set_screen_description("إنفوجرافيك يوضح خارطة التعلم")
    b.set_content_text("المحتوى العلمي")
    b.build()
    path = f"{OUTPUT_DIR}/test_infographic.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


def test_discussion():
    print("Testing DiscussionBuilder...")
    b = DiscussionBuilder(**PROJECT_ARGS)
    b.set_element_name("نقاش الوحدة الثانية")
    b.set_element_code("NJR01_U02_Discussion")
    b.set_screen_description("شاشة النقاش")
    b.set_content_text(
        "ناقش مع زملائك دور العقلية الرقمية في تعزيز الابتكار التقني "
        "وكيف يمكن تطبيق ممارسات التفكير التصميمي في حل المشكلات الرقمية "
        "المعاصرة. قدم أمثلة واقعية من حياتك اليومية."
    )
    b.set_instructions("شارك رأيك في المنتدى وعلق على مشاركة زميل واحد على الأقل")
    b.set_related_objectives("1. يتعرف على مفهوم الذهنية الرقمية")
    b.build()
    path = f"{OUTPUT_DIR}/test_discussion.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


def test_assignment():
    print("Testing AssignmentBuilder...")
    b = AssignmentBuilder(**PROJECT_ARGS)
    b.set_element_name("واجب الوحدة الثانية")
    b.set_element_code("NJR01_U02_Assignment")
    b.set_screen_description("شاشة الواجب")
    b.set_content_text("اكتب مقالة عن تطبيق التفكير التصميمي في حل مشكلة رقمية")
    b.set_instructions("يرجى التسليم خلال أسبوع من تاريخ النشر")
    b.set_related_objectives("1. يطبق التفكير التصميمي")
    b.build()
    path = f"{OUTPUT_DIR}/test_assignment.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


def test_test():
    print("Testing TestBuilder (Pre-Test)...")
    b = TestBuilder(**PROJECT_ARGS)
    b.set_element_name("الاختبار القبلي")
    b.set_element_code("NJR01_U02_Pre_Test")
    b.set_test_info(
        description="اختبار قبلي لقياس المعرفة السابقة للطلاب",
        instructions="المحاولات المتاحة: محاولة واحدة\nالوقت: 10 دقائق"
    )
    b.add_question(
        question_text="ما هو التفكير التصميمي؟",
        choices="أ) منهجية لحل المشكلات\nب) لغة برمجة\nج) نظام تشغيل\nد) قاعدة بيانات",
        correct_answer="أ",
        image_description=""
    )
    b.add_question(
        question_text="أي مما يلي يعتبر من ممارسات الابتكار التقني؟",
        choices="أ) النسخ واللصق\nب) التعلم الآلي\nج) الطباعة\nد) القراءة",
        correct_answer="ب",
        image_description="صورة توضيحية للتعلم الآلي"
    )
    b.add_question(
        question_text="الذهنية الرقمية تتطلب:",
        choices="أ) مهارات تقنية فقط\nب) تفكير نقدي وإبداعي\nج) حفظ المعلومات\nد) لا شيء مما سبق",
        correct_answer="ب",
        image_description=""
    )
    b.build()
    path = f"{OUTPUT_DIR}/test_pretest.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


def test_activity():
    print("Testing ActivityBuilder...")
    b = ActivityBuilder(**PROJECT_ARGS)
    b.set_element_name("النشاط التفاعلي 2.1")
    b.set_element_code("NJR01_U02_Activity2.1")
    b.add_scene(
        title="المشهد الأول",
        description="في هذا المشهد يظهر للطالب سؤال حول مراحل التفكير التصميمي",
        elements="النص التالي يظهر على الشاشة مع صورة توضيحية",
        image_desc="صورة لمراحل التفكير التصميمي الخمس",
        motion_desc="-",
        sound_effects="-",
        on_screen_text="رتب مراحل التفكير التصميمي التالية بالترتيب الصحيح",
        steps="1. اقرأ المراحل المعروضة\n2. اسحب كل مرحلة إلى الترتيب الصحيح\n3. اضغط تحقق",
        correct_answer="التعاطف -> التعريف -> التصور -> النموذج الأولي -> الاختبار",
        buttons='زر "مراجعة المحتوى"\nزر "أعد المحاولة"',
    )
    b.build()
    path = f"{OUTPUT_DIR}/test_activity.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


def test_video():
    print("Testing VideoBuilder...")
    b = VideoBuilder(**PROJECT_ARGS)
    b.set_element_name("فيديو موشن الوحدة 2")
    b.set_element_code("NJR01_U02_Video")
    b.add_scene(
        title="مشهد العنوان",
        screen_description="شاشة العنوان الرئيسي",
        sound_effects="موسيقى هادئة في الخلفية",
        narration_segments=[
            {
                "narration": "مرحبا بكم في الوحدة الثانية: الذهنية الرقمية وممارسات الابتكار التقني",
                "on_screen_text": "الذهنية الرقمية وممارسات الابتكار التقني",
                "scene_description": "يظهر عنوان الوحدة مع انيميشن للنص",
                "image_links": "",
            },
        ]
    )
    b.add_scene(
        title="المشهد الأول",
        screen_description="",
        sound_effects="-",
        narration_segments=[
            {
                "narration": "في هذا الفيديو سنتعرف على مفهوم الذهنية الرقمية",
                "on_screen_text": "ما هي الذهنية الرقمية؟",
                "scene_description": "يظهر السؤال مع رسوم متحركة",
                "image_links": "digital_mindset.png",
            },
            {
                "narration": "الذهنية الرقمية هي القدرة على التفكير النقدي في العصر الرقمي",
                "on_screen_text": "التعريف",
                "scene_description": "يظهر التعريف مع أيقونات توضيحية",
                "image_links": "definition_icons.png",
            },
        ]
    )
    b.build()
    path = f"{OUTPUT_DIR}/test_video.docx"
    b.save(path)
    print(f"  -> Saved: {path}")


if __name__ == "__main__":
    print("=" * 60)
    print("DOCX Engine Test — Post Gap-Analysis Fixes")
    print("=" * 60)

    tests = [
        test_objectives,
        test_summary,
        test_infographic,
        test_discussion,
        test_assignment,
        test_test,
        test_activity,
        test_video,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
