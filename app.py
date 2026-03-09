import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display

load_dotenv()

# إعداد الصفحة لتناسب اللغة العربية
st.set_page_config(page_title="Donia Labs - Smart Teacher", layout="wide")
st.markdown("""<style> .main { text-align: right; direction: rtl; } div.stButton > button { width: 100%; } </style>""", unsafe_allow_html=True)

def fix_arabic(text):
    return get_display(reshape(text))

# واجهة التطبيق
st.title("🎓 مختبر DONIA LABS: المعلم الذكي")
st.subheader("توليد تمارين المناهج الجزائرية بدعم LaTeX")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = os.getenv("GROQ_API_KEY")
    level = st.selectbox("الطور", ["التعليم الثانوي", "التعليم المتوسط"])
    grade = st.selectbox("السنة", ["السنة الأولى", "السنة الثانية", "السنة الثالثة (بكالوريا)"])
    subject = st.selectbox("المادة", ["العلوم الطبيعية", "الرياضيات", "الفيزياء"])

lesson = st.text_input("📝 اكتب عنوان الدرس (مثلاً: الانقسام المنصف):")

if st.button("توليد التمرين والحل"):
    if not api_key:
        st.error("⚠️ المفتاح غير موجود في ملف .env")
    else:
        llm = ChatGroq(model_name="llama-3.3-70b-specdec", groq_api_key=api_key)
        with st.spinner("جاري التواصل مع العقل الاصطناعي..."):
            prompt = f"""
            أنت أستاذ جزائري خبير. صمم تمرينًا لـ {level} {grade} في مادة {subject} حول {lesson}.
            قواعد: 
            1. استخدم العربية الفصحى. 
            2. المعادلات العلمية يجب أن تكون بتنسيق LaTeX بين علامتي $.
            3. في نهاية الرد، ضع كود LaTeX الكامل للتمرين داخل صندوق كود.
            """
            try:
                response = llm.invoke(prompt)
                res_text = response.content
                
                # عرض النتيجة
                st.markdown("---")
                st.markdown(res_text)
                
                # خيار تحميل PDF (تجريبي)
                if st.download_button("📥 تحميل كملف PDF", data=res_text.encode('utf-8-sig'), file_name="lesson.txt"):
                    st.success("تم التجهيز!")
            except Exception as e:
                st.error(f"خطأ: {e}")