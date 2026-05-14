import streamlit as st
import pandas as pd
STANDARDS = {
    "--- اختر من القائمة ---": {"CP": 0.0, "ME": 0.0, "Ca": 0.0, "P": 0.0, "Lys": 0.0, "Met": 0.0},
    "دواجن - بادئ تسمين": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "Lys": 1.10, "Met": 0.50},
    "دواجن - نامي تسمين": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "Lys": 1.00, "Met": 0.45},
    "أغنام - تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "Lys": 0.0, "Met": 0.0},
    "بقر - حلاب": {"CP": 17.0, "ME": 11.5, "Ca": 0.7, "P": 0.4, "Lys": 0.0, "Met": 0.0},
    "خيل - رياضة": {"CP": 11.5, "ME": 12.5, "Ca": 0.35, "P": 0.25, "Lys": 0.0, "Met": 0.0}
}

from engine import SmartFeedEngine

# 1. قاعدة بيانات الاحتياجات القياسية (التي طلبتها)
STANDARDS = {
    "--- اختر من القائمة ---": {"CP": 0.0, "ME": 0.0, "Ca": 0.0, "P": 0.0},
    "دواجن - بادئ تسمين": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45},
    "دواجن - نامي تسمين": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35},
    "دواجن - بياض إنتاج": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40},
    "أغنام - تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25},
    "نعاج - مرضعة": {"CP": 15.0, "ME": 10.5, "Ca": 0.5, "P": 0.3},
    "بقر - حلاب عالي الإنتاج": {"CP": 17.0, "ME": 11.5, "Ca": 0.7, "P": 0.4},
    "عجول - تسمين ناهي": {"CP": 12.5, "ME": 12.0, "Ca": 0.5, "P": 0.3},
    "خيل - رياضة": {"CP": 11.5, "ME": 12.5, "Ca": 0.35, "P": 0.25},
    "خيل - أمهار نمو": {"CP": 16.0, "ME": 12.0, "Ca": 0.8, "P": 0.55}
}

def check_password():
    if st.session_state.get("password_correct", False):
        return True
    st.title("🔐 قفل الأمان - المهندس عبدالقادر")
    pwd = st.text_input("أدخل كود الدخول الخاص بك:", type="password")
    if st.button("دخول"):
        if pwd == st.secrets["password"]:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("⚠️ الكود غير صحيح!")
    return False

if not check_password():
    st.stop()

# --- واجهة التطبيق الرئيسية ---
st.title("🌱 نظام المهندس عبدالقادر لتركيب العلائق")

# إضافة قسم اختيار نوع الحيوان والعليقة
st.subheader("📋 اختيار المعايير القياسية")
selected_std = st.selectbox("اختر نوع الحيوان ونوع العليقة المطلوبة:", list(STANDARDS.keys()))

# استخراج البيانات بناءً على الاختيار
std_data = STANDARDS[selected_std]

col1, col2 = st.columns(2)
with col1:
    req_cp = st.number_input("البروتين المطلوب (%)", value=float(std_data["CP"]))
    req_en = st.number_input("الطاقة المطلوبة", value=float(std_data["ME"]))

with col2:
    req_ca = st.number_input("الكالسيوم المطلوب (%)", value=float(std_data["Ca"]))
    req_p = st.number_input("الفسفور المطلوب (%)", value=float(std_data["P"]))

# بقية الكود الخاص بمحرك الحساب (Engine) يتبع هنا...
@st.cache_resource
def init_engine():
    return SmartFeedEngine("feeds_db.json")

engine = init_engine()
# (سيقوم النظام الآن باستخدام هذه القيم لحساب العليقة الأقل تكلفة)
