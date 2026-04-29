import streamlit as st
import pickle
import os
from datetime import date
import random

# ====================== إعداد الصفحة ======================
st.set_page_config(page_title="My Words", page_icon="🔥", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    body, .stApp { font-family: 'Cairo', sans-serif; background-color: #0f172a; color: white; }
    .big-title { font-size: 2.8rem; font-weight: 700; color: #22d3ee; }
    .stButton>button { height: 70px; font-size: 1.25rem; border-radius: 16px; font-weight: 600; }
    .word-card { 
        background: linear-gradient(135deg, #1e3a8a, #3b82f6); 
        border-radius: 20px; 
        padding: 30px; 
        margin: 15px 0;
        text-align: center;
    }
    .flashcard {
        background: #1e2937;
        border-radius: 20px;
        padding: 40px 20px;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        border: 3px solid #67e8f9;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ====================== بيانات الكلمات ======================
words_data = {
    "beginner": [
        {"id":1, "word":"Hello", "meaning":"مرحبا", "example":"Hello, how are you today?"},
        {"id":2, "word":"Thank you", "meaning":"شكراً", "example":"Thank you for your help."},
        {"id":3, "word":"Please", "meaning":"من فضلك", "example":"Please pass the salt."},
        {"id":4, "word":"Goodbye", "meaning":"وداعاً", "example":"Goodbye, see you tomorrow."},
        {"id":5, "word":"Yes", "meaning":"نعم", "example":"Yes, I understand."},
        {"id":6, "word":"No", "meaning":"لا", "example":"No, thank you."},
        {"id":7, "word":"Apple", "meaning":"تفاحة", "example":"I eat an apple every day."},
        {"id":8, "word":"Book", "meaning":"كتاب", "example":"This book is very interesting."},
        {"id":9, "word":"Water", "meaning":"ماء", "example":"Drink water to stay healthy."},
        {"id":10, "word":"Friend", "meaning":"صديق", "example":"He is my best friend."},
    ],
    "basic": [
        {"id":11, "word":"Happy", "meaning":"سعيد", "example":"I feel happy when I see my family."},
        {"id":12, "word":"Big", "meaning":"كبير", "example":"The elephant is a big animal."},
        {"id":13, "word":"Small", "meaning":"صغير", "example":"This phone is small and light."},
        {"id":14, "word":"Run", "meaning":"يركض", "example":"I run every morning in the park."},
        {"id":15, "word":"Eat", "meaning":"يأكل", "example":"We eat breakfast at 8 o'clock."},
        {"id":16, "word":"Sleep", "meaning":"ينام", "example":"I sleep at 11 PM."},
        {"id":17, "word":"Work", "meaning":"يعمل", "example":"My father works in a bank."},
        {"id":18, "word":"Read", "meaning":"يقرأ", "example":"She likes to read books."},
        {"id":19, "word":"Family", "meaning":"عائلة", "example":"I love my family very much."},
        {"id":20, "word":"House", "meaning":"منزل", "example":"My house is near the school."},
    ],
    "advanced": [
        {"id":21, "word":"Environment", "meaning":"البيئة", "example":"We must protect the environment."},
        {"id":22, "word":"Technology", "meaning":"التكنولوجيا", "example":"Technology has changed our lives."},
        {"id":23, "word":"Success", "meaning":"النجاح", "example":"Success comes with hard work."},
        {"id":24, "word":"Knowledge", "meaning":"المعرفة", "example":"Knowledge is power."},
        {"id":25, "word":"Opportunity", "meaning":"فرصة", "example":"This is a great opportunity for you."},
        {"id":26, "word":"Challenge", "meaning":"تحدي", "example":"Every challenge makes us stronger."},
        {"id":27, "word":"Experience", "meaning":"الخبرة", "example":"Experience is the best teacher."},
        {"id":28, "word":"Future", "meaning":"المستقبل", "example":"The future belongs to those who prepare."},
        {"id":29, "word":"Education", "meaning":"التعليم", "example":"Education is very important."},
        {"id":30, "word":"Culture", "meaning":"الثقافة", "example":"Learning about different cultures is interesting."},
    ]
}

# دمج جميع الكلمات في قاموس واحد للبحث السريع
all_words = {word["id"]: word for level_list in words_data.values() for word in level_list}

levels_dict = {
    "beginner": "أنا حديث في اللغة الإنجليزية 🌱",
    "basic": "أعرف بعض الكلمات البسيطة 📘",
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
                        "password": new_password,
                        "level": None,
                        "xp": 0,
                        "streak": 0,
                        "last_date": None,
                        "seen_words": [],
                        "saved_words": [],
                        "daily_ids": [],
                        "practice_stats": {}
                    }
                    save_users(st.session_state.users)
                    st.success("تم إنشاء الحساب بنجاح!")
                    st.session_state.username = new_username
                    st.rerun()

else:
    username = st.session_state.username
    user = st.session_state.users[username]

    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"<h1 style='color:#67e8f9;'>My Words</h1>", unsafe_allow_html=True)
    with col2:
        st.metric("🔥 Day Streak", user.get("streak", 0))

    st.markdown("### Daily Challenge")
    st.info("أكمل الدرس اليوم واحصل على مكافآت!")

    # الأزرار الرئيسية
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
            st.toast("قسم الاختبارات قيد التطوير...", icon="🚧")

    # Progress
    xp = user.get("xp", 0)
    level = (xp // 100) + 1
    st.markdown(f"**المستوى {level}**")
    st.progress(min((xp % 100) / 100, 1.0))
    st.caption(f"{xp} XP")

    st.divider()

    # ====================== صفحة Lesson ======================
    if st.session_state.get("page") == "lesson":
        st.subheader("📖 Lesson - كلمات اليوم")

        if not user.get("level"):
            selected_level = st.selectbox("اختر مستواك الحالي:", 
                                        options=list(levels_dict.keys()),
                                        format_func=lambda x: levels_dict[x])
            if st.button("تأكيد المستوى", type="primary", use_container_width=True):
                user["level"] = selected_level
                save_users(st.session_state.users)
                st.rerun()
        else:
            st.success(f"مستواك الحالي: **{levels_dict[user['level']]}**")

            today = str(date.today())
            if user.get("last_date") != today:
                available = [w for w in words_data[user["level"]] if w["id"] not in user.get("seen_words", [])]
                if len(available) < 3:
                    user["seen_words"] = []
                    available = words_data[user["level"]]
                
                random.shuffle(available)
                daily = available[:3]
                user["daily_ids"] = [w["id"] for w in daily]
                user["seen_words"].extend(user["daily_ids"])
                user["last_date"] = today
                user["xp"] = user.get("xp", 0) + 30
                user["streak"] = user.get("streak", 0) + 1
                save_users(st.session_state.users)

            for word in [all_words[wid] for wid in user.get("daily_ids", [])]:
                with st.container():
                    st.markdown(f"""
                    <div class="word-card">
                        <h2 style="margin:0;">{word['word']}</h2>
                        <h3 style="color:#a5f3fc;">{word['meaning']}</h3>
                        <p style="font-style:italic;">“{word['example']}”</p>
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

    # ====================== صفحة Practice ======================
    elif st.session_state.get("page") == "practice":
        st.subheader("🎮 Practice - ممارسة الكلمات المحفوظة")

        saved_ids = user.get("saved_words", [])

        if not saved_ids:
            st.warning("لم تقم بحفظ أي كلمات بعد. اذهب إلى **Lesson** وحفظ بعض الكلمات أولاً.")
        else:
            if "practice_queue" not in st.session_state or st.session_state.get("practice_reset", False):
                st.session_state.practice_queue = saved_ids.copy()
                random.shuffle(st.session_state.practice_queue)
                st.session_state.current_index = 0
                st.session_state.show_answer = False
                st.session_state.practice_reset = False

            queue = st.session_state.practice_queue
            idx = st.session_state.current_index

            if idx >= len(queue):
                st.success("🎉 تهانينا! لقد انتهيت من ممارسة جميع الكلمات المحفوظة")
                if st.button("ابدأ جولة جديدة", type="primary"):
                    st.session_state.practice_reset = True
                    st.rerun()
            else:
                current_word = all_words[queue[idx]]

                st.markdown('<div class="flashcard">', unsafe_allow_html=True)
                st.markdown(f"<h1 style='font-size: 3rem; margin-bottom: 20px;'>{current_word['word']}</h1>", unsafe_allow_html=True)

                if st.session_state.show_answer:
                    st.markdown(f"<h2 style='color:#67e8f9;'>{current_word['meaning']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size:1.2rem;'><i>“{current_word['example']}”</i></p>", unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✅ أعرفها جيداً", use_container_width=True):
                            user["xp"] = user.get("xp", 0) + 10
                            save_users(st.session_state.users)
                            st.session_state.current_index += 1
                            st.session_state.show_answer = False
                            st.rerun()
                    with col2:
                        if st.button("🔄 صعبة", use_container_width=True):
                            st.session_state.current_index += 1
                            st.session_state.show_answer = False
                            st.rerun()
                    with col3:
                        if st.button("🔊 استمع", use_container_width=True):
                            speak(current_word["word"])
                else:
                    if st.button("أظهر المعنى والجملة", type="primary", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

                st.progress((idx + 1) / len(queue))
                st.caption(f"الكلمة {idx + 1} من {len(queue)}")

    # زر تسجيل الخروج
    if st.button("🚪 تسجيل خروج"):
        if "username" in st.session_state:
            del st.session_state.username
        st.rerun()

# تشغيل التطبيق
if __name__ == "__main__":
    pass
