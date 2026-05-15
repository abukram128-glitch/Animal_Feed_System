import streamlit as st
import pandas as pd
import json
from engine import SmartFeedEngine

# إعدادات الصفحة
st.set_page_config(page_title="نظام المهندس عبدالقادر لإدارة التغذية", layout="wide")

# 1. تعريف الثوابت والاحتياجات الغذائية
STANDARDS = {
    "--- اختر نوع الحيوان ---": {"CP": 0.0, "ME": 0.0, "Ca": 0.0, "P": 0.0, "Lys": 0.0, "Met": 0.0},
    "أبقار حلوب": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "Lys": 0.0, "Met": 0.0},
    "أبقار تسمين": {"CP": 14.0, "ME": 12.0, "Ca": 0.6, "P": 0.35, "Lys": 0.0, "Met": 0.0},
    "ماعز/أغنام تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "Lys": 0.0, "Met": 0.0},
    "دجاج لاحم - نامي": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "Lys": 1.00, "Met": 0.45}
}

PREMIX_DOSES = {
    "أبقار حلوب (200 جرام)": 200,
    "أبقار تسمين (120 جرام)": 120,
    "أغنام/ماعز (35 جرام)": 35,
    "خيل (80 جرام)": 80
}

st.title("🌾 نظام تركيب العلائق المطور وإدارة التغذية")
st.info("تم تطوير هذا النظام بواسطة المهندس عبدالقادر إسماعيل")

# القسم الأول: بيانات الحيوان الميدانية
st.header("⚖️ إدارة التغذية الميدانية")
col_w1, col_w2 = st.columns(2)
with col_w1:
    animal_weight = st.number_input("وزن الحيوان الحي (كجم)", value=500, step=50)
    selected_premix = st.selectbox("نوع العليقة المصححة (Premix):", list(PREMIX_DOSES.keys()))
with col_w2:
    dmi_percent = st.slider("معدل استهلاك المادة الجافة (% من الوزن)", 2.0, 5.0, 3.0)
    ratio_conc = st.slider("نسبة المركز المستهدفة في العليقة الكلية (%)", 20, 60, 40)

total_dm_daily = animal_weight * (dmi_percent / 100)
st.warning(f"💡 إجمالي احتياج الرأس الواحد: {total_dm_daily:.2f} كجم مادة جافة يومياً.")

# القسم الثاني: الأهداف الغذائية للتركيبة المركزية
st.divider()
st.header("🎯 تحديد أهداف التركيبة المركزية")
choice = st.selectbox("اختر نوع العليقة:", list(STANDARDS.keys()))
std = STANDARDS[choice]

col1, col2, col3 = st.columns(3)
with col1:
    req_cp = st.number_input("البروتين المطلوب (%)", value=float(std["CP"]))
    req_me = st.number_input("الطاقة المطلوبة (ME)", value=float(std["ME"]))
with col2:
    req_ca = st.number_input("الكالسيوم المطلوب (%)", value=float(std["Ca"]))
    req_p = st.number_input("الفسفور المطلوب (%)", value=float(std["P"]))
with col3:
    req_lys = st.number_input("الليسين المطلوب (%)", value=float(std["Lys"]))
    req_met = st.number_input("الميثيونين المطلوب (%)", value=float(std["Met"]))

# القسم الثالث: الحساب والنتائج
if st.button("🚀 احسب البرنامج الغذائي المتكامل"):
    engine = SmartFeedEngine("feeds_db.json")
    
    # 1. حل مشكلة التركيبة المركزية
    chem_result = engine.solve(req_cp, req_me, req_ca, req_p, req_lys, req_met)
    
    if "✅" in chem_result:
        st.success(chem_result)
        
        # 2. حساب جدول التغذية اليومي
        premix_val = PREMIX_DOSES[selected_premix]
        schedule = engine.generate_feeding_schedule(total_dm_daily, ratio_conc, premix_val)
        st.markdown(schedule)
    else:
        st.error(chem_result)
