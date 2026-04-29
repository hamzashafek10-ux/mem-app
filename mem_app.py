import streamlit as st
import pickle
import os
from datetime import date, timedelta
import random

# ====================== إعداد الصفحة ======================
st.set_page_config(page_title="My Words", page_icon="🔥", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    body, .stApp {
        font-family: 'Cairo', sans-serif;
        background-color: #f8fafc;
        color: #0f172a;
    }
    .big-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #2563eb;
    }
    .stButton>button {
        height: 70px;
        font-size: 1.25rem;
        border-radius: 16px;
        font-weight: 600;
    }
    .word-card {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
        border-radius: 20px;
        padding: 30px;
        margin: 15px 0;
        text-align: center;
        color: #1e293b;
    }
    .flashcard {
        background: #ffffff;
        border-radius: 20px;
        padding: 40px 20px;
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        border: 3px solid #3b82f6;
        margin: 20px 0;
        color: #0f172a;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ====================== بيانات الكلمات ======================
words_data = {
    "beginner": [
        {"id":1,  "word":"Hello",     "meaning":"مرحبا",      "example":"Hello, how are you today?"},
        {"id":2,  "word":"Thank you", "meaning":"شكراً",      "example":"Thank you for your help."},
        {"id":3,  "word":"Please",    "meaning":"من فضلك",    "example":"Please pass the salt."},
        {"id":4,  "word":"Goodbye",   "meaning":"وداعاً",     "example":"Goodbye, see you tomorrow."},
        {"id":5,  "word":"Yes",       "meaning":"نعم",        "example":"Yes, I understand."},
        {"id":6,  "word":"No",        "meaning":"لا",         "example":"No, thank you."},
        {"id":7,  "word":"Apple",     "meaning":"تفاحة",      "example":"I eat an apple every day."},
        {"id":8,  "word":"Book",      "meaning":"كتاب",       "example":"This book is very interesting."},
        {"id":9,  "word":"Water",     "meaning":"ماء",        "example":"Drink water to stay healthy."},
        {"id":10, "word":"Friend",    "meaning":"صديق",       "example":"He is my best friend."},
    ],
    "basic": [
        {"id":11, "word":"Happy",  "meaning":"سعيد",   "example":"I feel happy when I see my family."},
        {"id":12, "word":"Big",    "meaning":"كبير",   "example":"The elephant is a big animal."},
        {"id":13, "word":"Small",  "meaning":"صغير",   "example":"This phone is small and light."},
        {"id":14, "word":"Run",    "meaning":"يركض",   "example":"I run every morning in the park."},
        {"id":15, "word":"Eat",    "meaning":"يأكل",   "example":"We eat breakfast at 8 o'clock."},
        {"id":16, "word":"Sleep",  "meaning":"ينام",   "example":"I sleep at 11 PM."},
        {"id":17, "word":"Work",   "meaning":"يعمل",   "example":"My father works in a bank."},
        {"id":18, "word":"Read",   "meaning":"يقرأ",   "example":"She likes to read books."},
        {"id":19, "word":"Family", "meaning":"عائلة",  "example":"I love my family very much."},
        {"id":20, "word":"House",  "meaning":"منزل",   "example":"My house is near the school."},
    ],
    "advanced": [
        {"id":21, "word":"Environment", "meaning":"البيئة",      "example":"We must protect the environment."},
        {"id":22, "word":"Technology",  "meaning":"التكنولوجيا", "example":"Technology has changed our lives."},
        {"id":23, "word":"Success",     "meaning":"النجاح",      "example":"Success comes with hard work."},
        {"id":24, "word":"Knowledge",   "meaning":"المعرفة",     "example":"Knowledge is power."},
        {"id":25, "word":"Opportunity", "meaning":"فرصة",        "example":"This is a great opportunity for you."},
        {"id":26, "word":"Challenge",   "meaning":"تحدي",        "example":"Every challenge makes us stronger."},
        {"id":27, "word":"Experience",  "meaning":"الخبرة",      "example":"Experience is the best teacher."},
        {"id":28, "word":"Future",      "meaning":"المستقبل",    "example":"The future belongs to those who prepare."},
        {"id":29, "word":"Education",   "meaning":"التعليم",     "example":"Education is very important."},
        {"id":30, "word":"Culture",     "meaning":"الثقافة",     "example":"Learning about different cultures is interesting."},
    ]
}

all_words = {word["id"]: word for level_list in words_data.values() for word in level_list}

levels_dict = {
    "beginner": "أنا حديث في اللغة الإنجليزية 🌱",
    "basic":    "أعرف بعض الكلمات البسيطة 📘",
    "advanced": "يمكنني الحديث عن موضوعات متعددة 🚀"
}

# ====================== حفظ البيانات ======================
DATA_FILE = "mywords_users.pkl"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(users, f)

if "users" not in st.session_state:
    st.session_state.users = load_users()

# ====================== دالة النطق ======================
def speak(word):
    try:
        st.markdown(f'''
        <audio autoplay="true">
            <source src="https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={word.replace(" ", "%20")}" type="audio/mpeg">
        </audio>
        ''', unsafe_allow_html=True)
        st.toast(f"جاري النطق: {word}", icon="🔊")
    except:
        st.toast("النطق غير متاح حالياً", icon="⚠️")

# ====================== الصفحة الرئيسية ======================
if "username" not in st.session_state:
    st.markdown("<h1 class='big-title' style='text-align:center;'>My Words</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.3rem; color:#67e8f9;'>تعلم كلمات إنجليزية يوميًا بذكاء</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "✨ إنشاء حساب جديد"])

    with tab1:
        username = st.text_input("اسم المستخدم", key="login_u")
        password = st.text_input("كلمة المرور", type="password", key="login_p")
        if st.button("دخول", type="primary", use_container_width=True):
            if username in st.session_state.users and st.session_state.users[username]["password"] == password:
                st.session_state.username = username
                # FIX #3: Clear any leftover page state from a previous session
                st.session_state.pop("page", None)
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

    with tab2:
        new_username = st.text_input("اسم المستخدم الجديد", key="reg_u")
        new_password = st.text_input("كلمة المرور", type="password", key="reg_p")
        if st.button("إنشاء الحساب", type="primary", use_container_width=True):
            if new_username and new_password:
                if new_username in st.session_state.users:
                    st.error("هذا الاسم مستخدم بالفعل")
                else:
                    st.session_state.users[new_username] = {
                        "password":   new_password,
                        "level":      None,
                        "xp":         0,
                        "streak":     0,
                        "last_date":  None,
                        "seen_words": [],
                        "saved_words":[],
                        "daily_ids":  [],
                    }
                    save_users(st.session_state.users)
                    st.success("تم إنشاء الحساب بنجاح!")
                    st.session_state.username = new_username
                    st.session_state.pop("page", None)
                    st.rerun()

else:
    username = st.session_state.username
    user     = st.session_state.users[username]

    # ---- الصفحة الرئيسية ----
    if not st.session_state.get("page"):

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("<h1 style='color:#67e8f9;'>My Words</h1>", unsafe_allow_html=True)
        with col2:
            st.metric("🔥 Day Streak", user.get("streak", 0))

        st.markdown("### Daily Challenge")
        st.info("أكمل الدرس اليوم واحصل على مكافآت!")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📖 Lesson", use_container_width=True):
                st.session_state.page = "lesson"
                st.rerun()
        with c2:
            if st.button("🎮 Practice", use_container_width=True):
                st.session_state.page = "practice"
                st.rerun()
        with c3:
            if st.button("🏆 Quiz", use_container_width=True):
                st.session_state.page = "quiz"
                st.rerun()

        xp         = user.get("xp", 0)
        XP_PER_LVL = 50
        level      = (xp // XP_PER_LVL) + 1
        st.markdown(f"**المستوى {level}**")
        st.progress(min((xp % XP_PER_LVL) / XP_PER_LVL, 1.0))
        st.caption(f"{xp} XP · {XP_PER_LVL - (xp % XP_PER_LVL)} XP للمستوى التالي")
        st.divider()

        # FIX #7: تسجيل الخروج ينظّف حالة الصفحة أيضاً
        if st.button("🚪 تسجيل خروج"):
            st.session_state.pop("username", None)
            st.session_state.pop("page", None)
            # FIX #5: استخدام pop بدلاً من del لتجنب KeyError
            for key in ["practice_queue","practice_reset","current_index",
                        "show_answer","quiz_questions","quiz_index",
                        "quiz_score","answered","quiz_xp_given"]:
                st.session_state.pop(key, None)
            st.rerun()

    # ====================== صفحة Lesson ======================
    elif st.session_state.get("page") == "lesson":
        # FIX #6: زر الرجوع للرئيسية
        if st.button("← رجوع"):
            st.session_state.page = None
            st.rerun()

        st.subheader("📖 Lesson - كلمات اليوم")

        if not user.get("level"):
            selected_level = st.selectbox(
                "اختر مستواك الحالي:",
                options=list(levels_dict.keys()),
                format_func=lambda x: levels_dict[x]
            )
            if st.button("تأكيد المستوى", type="primary", use_container_width=True):
                user["level"] = selected_level
                save_users(st.session_state.users)
                st.rerun()
        else:
            col_lvl, col_change = st.columns([3, 1])
            with col_lvl:
                st.success(f"مستواك الحالي: **{levels_dict[user['level']]}**")
            # FIX #7: خيار تغيير المستوى
            with col_change:
                if st.button("تغيير المستوى"):
                    user["level"]     = None
                    user["last_date"] = None  # force daily words to regenerate
                    user["daily_ids"] = []
                    save_users(st.session_state.users)
                    st.rerun()

            today = str(date.today())
            if user.get("last_date") != today:
                # FIX #2: إعادة تعيين السلسلة إذا فاتت يوم أو أكثر
                last = user.get("last_date")
                if last:
                    yesterday = str(date.today() - timedelta(days=1))
                    if last != yesterday:
                        user["streak"] = 0   # كُسرت السلسلة

                available = [w for w in words_data[user["level"]] if w["id"] not in user.get("seen_words", [])]
                if len(available) < 3:
                    user["seen_words"] = []
                    available = words_data[user["level"]]

                random.shuffle(available)
                daily = available[:3]
                user["daily_ids"]  = [w["id"] for w in daily]
                user["seen_words"].extend(user["daily_ids"])
                user["last_date"]  = today
                user["xp"]         = user.get("xp", 0) + 30
                user["streak"]     = user.get("streak", 0) + 1
                save_users(st.session_state.users)

            for word in [all_words[wid] for wid in user.get("daily_ids", [])]:
                with st.container():
                    st.markdown(f"""
                    <div class="word-card">
                        <h2 style="margin:0;">{word['word']}</h2>
                        <h3 style="color:#a5f3fc;">{word['meaning']}</h3>
                        <p style="font-style:italic;">"{word['example']}"</p>
                    </div>
                    """, unsafe_allow_html=True)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("🔊 استمع", key=f"listen_{word['id']}"):
                            speak(word["word"])
                    with col_b:
                        if word["id"] not in user.get("saved_words", []):
                            if st.button("💾 حفظ الكلمة", key=f"save_{word['id']}"):
                                if "saved_words" not in user:
                                    user["saved_words"] = []
                                user["saved_words"].append(word["id"])
                                save_users(st.session_state.users)
                                st.success("تم الحفظ بنجاح!")
                                st.rerun()
                        else:
                            st.success("✓ محفوظة")

    # ====================== صفحة Practice ======================
    elif st.session_state.get("page") == "practice":
        # FIX #6: زر الرجوع
        if st.button("← رجوع"):
            st.session_state.page = None
            for key in ["practice_queue","practice_reset","current_index","show_answer"]:
                st.session_state.pop(key, None)
            st.rerun()

        st.subheader("🎮 Practice - ممارسة الكلمات المحفوظة")

        saved_ids = user.get("saved_words", [])
        if not saved_ids:
            st.warning("لم تقم بحفظ أي كلمات بعد. اذهب إلى **Lesson** وحفظ بعض الكلمات أولاً.")
        else:
            if "practice_queue" not in st.session_state or st.session_state.get("practice_reset", False):
                st.session_state.practice_queue  = saved_ids.copy()
                random.shuffle(st.session_state.practice_queue)
                st.session_state.current_index   = 0
                st.session_state.show_answer     = False
                st.session_state.practice_reset  = False

            queue = st.session_state.practice_queue
            idx   = st.session_state.current_index

            if idx >= len(queue):
                st.success("🎉 تهانينا! لقد انتهيت من ممارسة جميع الكلمات المحفوظة")
                if st.button("ابدأ جولة جديدة", type="primary"):
                    st.session_state.practice_reset = True
                    st.rerun()
            else:
                current_word = all_words[queue[idx]]

                # FIX: flashcard rendered as a plain HTML block (non-wrapping)
                st.markdown(f"""
                <div class="flashcard">
                    <h1 style="font-size:3rem; margin-bottom:10px;">{current_word['word']}</h1>
                    {"<h2 style='color:#67e8f9;'>" + current_word['meaning'] + "</h2><p style='font-size:1.2rem;'><i>\"" + current_word['example'] + "\"</i></p>" if st.session_state.show_answer else ""}
                </div>
                """, unsafe_allow_html=True)

                if st.session_state.show_answer:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✅ أعرفها جيداً", use_container_width=True):
                            user["xp"] = user.get("xp", 0) + 10
                            save_users(st.session_state.users)
                            st.session_state.current_index += 1
                            st.session_state.show_answer   = False
                            st.rerun()
                    with col2:
                        if st.button("🔄 صعبة", use_container_width=True):
                            st.session_state.current_index += 1
                            st.session_state.show_answer   = False
                            st.rerun()
                    with col3:
                        if st.button("🔊 استمع", use_container_width=True):
                            speak(current_word["word"])
                else:
                    if st.button("أظهر المعنى والجملة", type="primary", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()

                st.progress((idx + 1) / len(queue))
                st.caption(f"الكلمة {idx + 1} من {len(queue)}")

    # ====================== صفحة Quiz ======================
    elif st.session_state.get("page") == "quiz":
        # FIX #6: زر الرجوع
        if st.button("← رجوع"):
            st.session_state.page = None
            for key in ["quiz_questions","quiz_index","quiz_score","answered","quiz_xp_given"]:
                st.session_state.pop(key, None)
            st.rerun()

        st.subheader("🏆 Quiz - اختبر نفسك")

        source_ids = user.get("saved_words", [])
        if not source_ids:
            source_ids = [w["id"] for w in words_data[user.get("level", "beginner")]]

        if len(source_ids) < 3:
            st.warning("لا يوجد كلمات كافية لبدء الاختبار (على الأقل 3 كلمات)")
        else:
            if "quiz_questions" not in st.session_state:
                st.session_state.quiz_questions = random.sample(source_ids, min(5, len(source_ids)))
                st.session_state.quiz_index     = 0
                st.session_state.quiz_score     = 0
                st.session_state.answered       = False
                # FIX #1: علم لمنع إضافة XP أكثر من مرة
                st.session_state.quiz_xp_given  = False

            q_ids  = st.session_state.quiz_questions
            q_idx  = st.session_state.quiz_index

            if q_idx >= len(q_ids):
                score = st.session_state.quiz_score
                total = len(q_ids)
                st.success(f"🎉 خلصت الكويز!\n\nالنتيجة: {score} / {total}")

                # FIX #1: XP يُضاف مرة واحدة فقط بعد انتهاء الكويز
                if not st.session_state.quiz_xp_given:
                    xp_gain = score * 10
                    user["xp"] += xp_gain
                    save_users(st.session_state.users)
                    st.session_state.quiz_xp_given = True
                    st.info(f"حصلت على {xp_gain} XP 🔥")

                if st.button("إعادة الاختبار", type="primary"):
                    # FIX #5: pop أكثر أماناً من del
                    for key in ["quiz_questions","quiz_index","quiz_score","answered","quiz_xp_given"]:
                        st.session_state.pop(key, None)
                    st.rerun()
            else:
                current_word = all_words[q_ids[q_idx]]
                st.markdown("### ما معنى هذه الكلمة؟")
                st.markdown(f"<h1 style='text-align:center;'>{current_word['word']}</h1>", unsafe_allow_html=True)

                correct      = current_word["meaning"]
                all_meanings = [w["meaning"] for w in all_words.values() if w["meaning"] != correct]
                options      = random.sample(all_meanings, 3) + [correct]
                random.shuffle(options)

                selected = st.radio("اختر الإجابة:", options, key=f"quiz_{q_idx}")

                if not st.session_state.answered:
                    if st.button("تأكيد الإجابة", type="primary"):
                        st.session_state.answered = True
                        if selected == correct:
                            st.session_state.quiz_score += 1
                            st.success("إجابة صحيحة ✅")
                        else:
                            st.error(f"خطأ ❌ الإجابة الصحيحة: {correct}")
                else:
                    if st.button("السؤال التالي ➡️"):
                        st.session_state.quiz_index += 1
                        st.session_state.answered   = False
                        st.rerun()

                st.progress((q_idx + 1) / len(q_ids))
                st.caption(f"السؤال {q_idx + 1} من {len(q_ids)}")
