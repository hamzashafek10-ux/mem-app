import streamlit as st
import pickle
import os
from datetime import date
import random

# ================== إعداد الصفحة ==================
st.set_page_config(page_title="كلماتي - تعلم الإنجليزية", page_icon="📚", layout="centered")

# لدعم اللغة العربية (RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Cairo', sans-serif !important; }
    .stApp { direction: rtl; text-align: right; }
    .big-word { font-size: 3.5rem; font-weight: bold; color: #1e40af; }
    </style>
""", unsafe_allow_html=True)

# ================== بيانات الكلمات حسب المستوى ==================
words_data = {
    "beginner": [
        {"id": 1, "word": "Hello", "meaning": "مرحبا", "example": "Hello, my name is Ahmed."},
        {"id": 2, "word": "Goodbye", "meaning": "وداعاً", "example": "Goodbye, see you tomorrow."},
        {"id": 3, "word": "Thank you", "meaning": "شكراً", "example": "Thank you for your help."},
        {"id": 4, "word": "Please", "meaning": "من فضلك", "example": "Please open the door."},
        {"id": 5, "word": "Yes", "meaning": "نعم", "example": "Yes, I like it."},
        {"id": 6, "word": "No", "meaning": "لا", "example": "No, thank you."},
        {"id": 7, "word": "Apple", "meaning": "تفاحة", "example": "I eat an apple every morning."},
        {"id": 8, "word": "Book", "meaning": "كتاب", "example": "This book is very interesting."},
        {"id": 9, "word": "Water", "meaning": "ماء", "example": "Drink water to stay healthy."},
        {"id": 10, "word": "Friend", "meaning": "صديق", "example": "He is my best friend."},
    ],
    "basic": [
        {"id": 11, "word": "Happy", "meaning": "سعيد", "example": "I am happy today."},
        {"id": 12, "word": "Big", "meaning": "كبير", "example": "The building is big."},
        {"id": 13, "word": "Small", "meaning": "صغير", "example": "This box is small."},
        {"id": 14, "word": "Run", "meaning": "يركض", "example": "I run every morning."},
        {"id": 15, "word": "Eat", "meaning": "يأكل", "example": "We eat breakfast at 8 AM."},
        {"id": 16, "word": "Sleep", "meaning": "ينام", "example": "I sleep at night."},
        {"id": 17, "word": "Work", "meaning": "يعمل", "example": "He works in a company."},
        {"id": 18, "word": "Read", "meaning": "يقرأ", "example": "She reads a newspaper."},
        {"id": 19, "word": "Color", "meaning": "لون", "example": "My favorite color is blue."},
        {"id": 20, "word": "Family", "meaning": "عائلة", "example": "I love my family very much."},
    ],
    "advanced": [
        {"id": 21, "word": "Environment", "meaning": "البيئة", "example": "We need to protect the environment."},
        {"id": 22, "word": "Technology", "meaning": "التكنولوجيا", "example": "Modern technology makes life easier."},
        {"id": 23, "word": "Education", "meaning": "التعليم", "example": "Education opens many doors."},
        {"id": 24, "word": "Travel", "meaning": "السفر", "example": "I love to travel to new countries."},
        {"id": 25, "word": "Success", "meaning": "النجاح", "example": "Success comes with hard work."},
        {"id": 26, "word": "Knowledge", "meaning": "المعرفة", "example": "Knowledge is power."},
        {"id": 27, "word": "Challenge", "meaning": "تحدي", "example": "Every challenge makes us stronger."},
        {"id": 28, "word": "Opportunity", "meaning": "فرصة", "example": "This is a great opportunity."},
        {"id": 29, "word": "Experience", "meaning": "الخبرة", "example": "Experience teaches us lessons."},
        {"id": 30, "word": "Future", "meaning": "المستقبل", "example": "The future is full of possibilities."},
    ]
}

levels = {
    "beginner": "أنا حديث في اللغة الإنجليزية",
    "basic": "أعرف بعض الكلمات البسيطة",
    "advanced": "يمكنني الحديث عن موضوعات متعددة"
}

# ================== حفظ وتحميل البيانات ==================
DATA_FILE = "users_data.pkl"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

if "users" not in st.session_state:
    st.session_state.users = load_data()

# ================== دالة النطق ==================
def speak(text):
    try:
        # للنطق في Streamlit (يعمل في بعض البيئات)
        st.markdown(f"""
        <audio autoplay="true">
            <source src="https://api.streamelements.com/kappa/v2/speech?voice=Brian&text={text.replace(' ', '%20')}" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)
    except:
        st.warning("النطق غير متاح حالياً")

# ================== الصفحة الرئيسية ==================
def main():
    st.title("📚 كلماتي")
    st.subheader("تعلم 3 كلمات إنجليزية جديدة كل يوم")

    # التحقق من تسجيل الدخول
    if "username" not in st.session_state:
        auth_page()
    else:
        user_page()

def auth_page():
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])

    with tab1:
        st.subheader("تسجيل الدخول")
        username = st.text_input("اسم المستخدم", key="login_user")
        password = st.text_input("كلمة المرور", type="password", key="login_pass")
        if st.button("دخول", type="primary"):
            users = st.session_state.users
            if username in users and users[username]["password"] == password:
                st.session_state.username = username
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_user = st.text_input("اسم المستخدم الجديد", key="reg_user")
        new_pass = st.text_input("كلمة المرور", type="password", key="reg_pass")
        if st.button("إنشاء الحساب", type="primary"):
            if new_user and new_pass:
                if new_user in st.session_state.users:
                    st.error("هذا الاسم مستخدم بالفعل")
                else:
                    st.session_state.users[new_user] = {
                        "password": new_pass,
                        "level": None,
                        "seen_words": [],
                        "saved_words": [],
                        "last_daily_date": None,
                        "daily_ids": []
                    }
                    save_data(st.session_state.users)
                    st.success("تم إنشاء الحساب بنجاح! يمكنك تسجيل الدخول الآن")
            else:
                st.warning("يرجى ملء جميع الحقول")

def user_page():
    username = st.session_state.username
    user = st.session_state.users[username]

    # Sidebar
    with st.sidebar:
        st.success(f"مرحباً، {username} 👋")
        if st.button("تسجيل خروج"):
            del st.session_state.username
            st.rerun()

    # اختيار المستوى إذا لم يتم اختياره
    if not user["level"]:
        st.header("ما هو مستواك الحالي في اللغة الإنجليزية؟")
        level_choice = st.selectbox(
            "اختر مستواك",
            options=list(levels.keys()),
            format_func=lambda x: levels[x]
        )
        if st.button("تأكيد المستوى", type="primary"):
            user["level"] = level_choice
            save_data(st.session_state.users)
            st.rerun()
        return

    st.header(f"مستواك: **{levels[user['level']]}**")

    # كلمات اليوم
    today = str(date.today())

    if user.get("last_daily_date") != today:
        available = [w for w in words_data[user["level"]] if w["id"] not in user["seen_words"]]
        if len(available) < 3:
            user["seen_words"] = []  # إعادة تعيين
            available = words_data[user["level"]]

        random.shuffle(available)
        daily_words = available[:3]
        user["daily_ids"] = [w["id"] for w in daily_words]
        user["seen_words"].extend(user["daily_ids"])
        user["last_daily_date"] = today
        save_data(st.session_state.users)

    # عرض الكلمات اليومية
    st.subheader("🌟 كلمات اليوم")
    daily_words = [w for w in words_data[user["level"]] if w["id"] in user.get("daily_ids", [])]

    cols = st.columns(3)
    for i, word in enumerate(daily_words):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"<p class='big-word'>{word['word']}</p>", unsafe_allow_html=True)
                st.subheader(word["meaning"])
                st.write(f"**مثال:** {word['example']}")
                
                if st.button("🔊 استمع", key=f"speak_{word['id']}"):
                    speak(word["word"])
                
                if word["id"] not in user["saved_words"]:
                    if st.button("💾 حفظ الكلمة", key=f"save_{word['id']}"):
                        user["saved_words"].append(word["id"])
                        save_data(st.session_state.users)
                        st.success("تم الحفظ!")
                        st.rerun()

    # عرض الكلمات المحفوظة
    st.subheader("📖 كلماتي المحفوظة")
    saved = [w for w in words_data[user["level"]] if w["id"] in user.get("saved_words", [])]
    
    if not saved:
        st.info("لم تحفظ أي كلمات بعد")
    else:
        for word in saved:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{word['word']}** — {word['meaning']}")
                st.caption(word['example'])
            with col2:
                if st.button("🔊", key=f"spk_{word['id']}"):
                    speak(word['word'])
            with col3:
                if st.button("🗑️", key=f"del_{word['id']}"):
                    user["saved_words"].remove(word["id"])
                    save_data(st.session_state.users)
                    st.rerun()

# ================== تشغيل التطبيق ==================
if __name__ == "__main__":
    main()