import streamlit as st
import pandas as pd
from engine import SmartFeedEngine

# 1. قاعدة بيانات الاحتياجات القياسية المحدثة
STANDARDS = {
    "--- اختر من القائمة ---": {"CP": 0.0, "ME": 0.0, "Ca": 0.0, "P": 0.0, "Lys": 0.0, "Met": 0.0},
    "دواجن - بادئ تسمين": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "Lys": 1.10, "Met": 0.50},
    "دواجن - نامي تسمين": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "Lys": 1.00, "Met": 0.45},
    "دواجن - بياض إنتاج": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40, "Lys": 0.85, "Met": 0.38},
    "أغنام - تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "Lys": 0.0, "Met": 0.0},
    "بقر - حلاب": {"CP": 17.0, "ME": 11.5, "Ca": 0.7, "P": 0.4, "Lys": 0.0, "Met": 0.0},
    "خيل - رياضة": {"CP": 11.5, "ME": 12.5, "Ca": 0.35, "P": 0.25, "Lys": 0.0, "Met": 0.0}
}

# 2. التحقق من كلمة المرور
if not st.session_state.get("password_correct", False):
    st.title("🔐 نظام المهندس عبدالقادر")
    pwd = st.text_input("أدخل كود الدخول:", type="password")
    if st.button("دخول"):
        if pwd == st.secrets["password"]:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("⚠️ الكود غير صحيح")
    st.stop()

# 3. واجهة التطبيق
st.title("🌱 نظام تركيب العلائق المتطور")

selected_std = st.selectbox("اختر نوع الحيوان والعليقة:", list(STANDARDS.keys()))
std_data = STANDARDS[selected_std]

# عرض الخانات (تشمل الأحماض الأمينية الآن)
col1, col2, col3 = st.columns(3)
with col1:
    req_cp = st.number_input("البروتين (%)", value=float(std_data["CP"]))
    req_en = st.number_input("الطاقة (ME)", value=float(std_data["ME"]))
with col2:
    req_ca = st.number_input("الكالسيوم (%)", value=float(std_data["Ca"]))
    req_p = st.number_input("الفسفور (%)", value=float(std_data["P"]))
with col3:
    req_lys = st.number_input("الليسين (%)", value=float(std_data["Lys"]))
    req_met = st.number_input("الميثيونين (%)", value=float(std_data["Met"]))

# 4. محرك الحساب
@st.cache_resource
def init_engine():
    return SmartFeedEngine("feeds_db.json")

engine = init_engine()

# زر الحساب وتوليد النتائج
if st.button("احسب العليقة الأقل تكلفة"):
    # هنا يتم استدعاء المحرك مع كافة المعايير بما فيها الأحماض
    results = engine.solve(req_cp, req_en, req_ca, req_p, req_lys, req_met)
    st.success("تم الحساب بنجاح!")
    st.write(results)
