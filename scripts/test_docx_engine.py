"""
Integration test for the DOCX template engine.
Creates one document of each type and saves to output/test/.
"""
import sys
sys.path.insert(0, "/Users/qusaiabushanap/dev/storyboard")

from engine.docx_engine import (
    TestBuilder, ActivityBuilder, VideoBuilder,
    ObjectivesBuilder, SummaryBuilder, InfographicBuilder,
    DiscussionBuilder, AssignmentBuilder,
)

OUTPUT_DIR = "/Users/qusaiabushanap/dev/storyboard/output/test"

# Common project metadata
META = dict(
    project_code="DSAI",
    unit_number=1,
    unit_name="المهارات الرقمية: المشهد التحولي",
    project_name="تطوير 15 مقرر إلكتروني - جامعة نجران",
    institution="جامعة نجران",
    designer="أحمد محمد",
)


def test_objectives():
    print("Building: Learning Objectives...")
    b = ObjectivesBuilder(**META)
    b.set_element_name("الأهداف التعليمية")
    b.set_element_code("DSAI_U01_MLO")
    b.set_content_text(
        "1. يتعرف على مفهوم الذكاء الاصطناعي\n"
        "2. يميز بين أنواع التعلم الآلي\n"
        "3. يشرح تطبيقات الذكاء الاصطناعي في الحياة اليومية"
    )
    b.set_screen_description("إنفوجرافيك يوضح الأهداف التعليمية للوحدة")
    b.set_image_sources("أيقونات تعليمية")
    b.set_detailed_description("-")
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_MLO.docx"
    b.save(path)
    print(f"  Saved: {path}")


def test_summary():
    print("Building: Summary...")
    b = SummaryBuilder(**META)
    b.set_element_name("ملخص الوحدة")
    b.set_element_code("DSAI_U01_Summary")
    b.set_content_text(
        "تناولت هذه الوحدة مفهوم الذكاء الاصطناعي وأنواع التعلم الآلي..."
    )
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_Summary.docx"
    b.save(path)
    print(f"  Saved: {path}")


def test_infographic():
    print("Building: Learning Map (Infographic)...")
    b = InfographicBuilder(**META)
    b.set_element_name("خارطة التعلم")
    b.set_element_code("DSAI_U01_Learning_Map")
    b.set_content_text(
        "لتحقيق الأهداف التعليمية الخاصة بهذه المحاضرة، يرجى اتباع الخطوات التالية:\n"
        "1. مشاهدة فيديو المقدمة\n"
        "2. قراءة المحاضرة التفاعلية\n"
        "3. إكمال الأنشطة التفاعلية\n"
        "4. المشاركة في النقاش\n"
        "5. حل الاختبار البعدي"
    )
    b.set_image_sources(
        "أيقونة اختبار\nأيقونة محتوى تعليمي\nأيقونة نقاش\nأيقونة حل واجب"
    )
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_Learning_Map.docx"
    b.save(path)
    print(f"  Saved: {path}")


def test_discussion():
    print("Building: Discussion...")
    b = DiscussionBuilder(**META)
    b.set_element_name("نقاش الوحدة الأولى")
    b.set_element_code("DSAI_U01_Discussion")
    b.set_content_text(
        "ناقش مع زملائك: كيف يمكن للذكاء الاصطناعي أن يغير مجال التعليم؟"
    )
    b.set_instructions(
        "شارك بمداخلة واحدة على الأقل وعلق على مشاركتين من زملائك"
    )
    b.set_related_objectives(
        "1. يتعرف على مفهوم الذكاء الاصطناعي\n"
        "3. يشرح تطبيقات الذكاء الاصطناعي"
    )
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_Discussion.docx"
    b.save(path)
    print(f"  Saved: {path}")


def test_assignment():
    print("Building: Assignment...")
    b = AssignmentBuilder(**META)
    b.set_element_name("واجب الوحدة الأولى")
    b.set_element_code("DSAI_U01_Assignment")
    b.set_content_text(
        "اكتب مقالة من 500 كلمة عن تطبيق واحد للذكاء الاصطناعي في مجال تخصصك"
    )
    b.set_instructions(
        "يرجى التسليم خلال أسبوع من تاريخ النشر\n"
        "الحد الأدنى: 500 كلمة\n"
        "يجب ذكر المراجع المستخدمة"
    )
    b.set_related_objectives(
        "3. يشرح تطبيقات الذكاء الاصطناعي في الحياة اليومية"
    )
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_Assignment.docx"
    b.save(path)
    print(f"  Saved: {path}")


def test_pretest():
    print("Building: Pre-Test...")
    b = TestBuilder(**META)
    b.set_element_name("الاختبار القبلي")
    b.set_element_code("DSAI_U01_Pre_Test")
    b.set_test_info(
        description="الاختبار القبلي للوحدة الأولى (المهارات الرقمية: المشهد التحولي)",
        instructions=(
            "المحاولات المتاحة: غير مسموح بالمحاولات المتعددة — يمكن إجراء الاختبار مرة واحدة فقط\n"
            "المدة: 10 دقائق\n"
            "عدد الأسئلة: 3"
        ),
    )
    b.add_question(
        question_text="ما هو الذكاء الاصطناعي؟",
        choices="أ) برنامج حاسوبي بسيط\nب) فرع من علوم الحاسب يحاكي الذكاء البشري\nج) لغة برمجة\nد) نظام تشغيل",
        correct_answer="ب",
        image_description="",
    )
    b.add_question(
        question_text="أي مما يلي يعد من تطبيقات الذكاء الاصطناعي؟",
        choices="أ) الآلة الحاسبة\nب) المساعدات الصوتية مثل سيري\nج) الطابعة\nد) لوحة المفاتيح",
        correct_answer="ب",
        image_description="",
    )
    b.add_question(
        question_text="التعلم العميق هو نوع من أنواع:",
        choices="أ) البرمجة\nب) قواعد البيانات\nج) التعلم الآلي\nد) أنظمة التشغيل",
        correct_answer="ج",
        image_description="",
    )
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_Pre_Test.docx"
    b.save(path)
    print(f"  Saved: {path}")


def test_activity():
    print("Building: Interactive Activity...")
    b = ActivityBuilder(**META)
    b.set_element_name("النشاط التفاعلي 1.1")
    b.set_element_code("DSAI_U01_Activity1.1")
    b.add_scene(
        title="المشهد الأول",
        description="في هذا المشهد يظهر للطالب الصفحة الأولى والتي تحتوى على النص التالي مع خيارات متعددة",
        elements="سؤال اختيار من متعدد مع 4 خيارات",
        image_desc="صورة توضيحية للمفهوم الرئيسي",
        motion_desc="-",
        sound_effects="-",
        on_screen_text=(
            "التغذية الراجعة للإجابة الصحيحة:\nأحسنت! الإجابة صحيحة.\n\n"
            "التغذية الراجعة للإجابة الخاطئة:\nإجابة خاطئة. حاول مرة أخرى."
        ),
        steps=(
            "على الطالب اختيار الإجابة الصحيحة، ثم النقر على زر إرسال.\n"
            "عند الإجابة الصحيحة: تظهر التغذية الراجعة الإيجابية\n"
            "عند الإجابة الخاطئة: تظهر التغذية الراجعة مع إتاحة المحاولة مرة أخرى"
        ),
        correct_answer="الاجابة الصحيحة هي: ب) فرع من علوم الحاسب",
        buttons='زر "مراجعة المحتوى"\nزر "أعد المحاولة"',
    )
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_Activity1.1.docx"
    b.save(path)
    print(f"  Saved: {path}")


def test_video():
    print("Building: Motion Video...")
    b = VideoBuilder(**META)
    b.set_element_name("فيديو موشن: مقدمة في الذكاء الاصطناعي")
    b.set_element_code("DSAI_U01_Video")
    b.add_scene(
        title="مشهد العنوان",
        screen_description="شاشة العنوان مع شعار الجامعة",
        sound_effects="موسيقى هادئة في الخلفية",
        narration_segments=[
            {
                "narration": "مرحباً بكم في مقرر علوم الحاسب ونظم المعلومات",
                "on_screen_text": "علوم الحاسب ونظم المعلومات\nالوحدة الأولى: المهارات الرقمية",
                "scene_description": "يظهر شعار الجامعة مع عنوان المقرر ثم ينتقل لعنوان الوحدة",
                "image_links": "شعار الجامعة",
            },
        ],
    )
    b.add_scene(
        title="المشهد الأول",
        screen_description="",
        sound_effects="-",
        narration_segments=[
            {
                "narration": "الذكاء الاصطناعي هو فرع من فروع علوم الحاسب...",
                "on_screen_text": "تعريف الذكاء الاصطناعي",
                "scene_description": "يظهر تعريف الذكاء الاصطناعي مع رسوم متحركة توضيحية",
                "image_links": "رسم توضيحي للدماغ والشبكة العصبية",
            },
            {
                "narration": "ويشمل عدة مجالات مثل التعلم الآلي ومعالجة اللغة الطبيعية",
                "on_screen_text": "مجالات الذكاء الاصطناعي:\n- التعلم الآلي\n- معالجة اللغة الطبيعية\n- الرؤية الحاسوبية",
                "scene_description": "تظهر أيقونات لكل مجال مع نص توضيحي",
                "image_links": "أيقونات المجالات",
            },
        ],
    )
    b.build()
    path = f"{OUTPUT_DIR}/DSAI_U01_Video.docx"
    b.save(path)
    print(f"  Saved: {path}")


if __name__ == "__main__":
    print("=" * 60)
    print("DOCX Template Engine Integration Test")
    print("=" * 60)

    test_objectives()
    test_summary()
    test_infographic()
    test_discussion()
    test_assignment()
    test_pretest()
    test_activity()
    test_video()

    print("\n" + "=" * 60)
    print("All 8 document types created successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)
