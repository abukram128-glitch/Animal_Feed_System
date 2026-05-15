import streamlit as st
import pandas as pd
from engine import SmartFeedEngine

st.set_page_config(page_title="نظام المهندس عبدالقادر المتكامل", layout="wide")

# 1. قاعدة بيانات الأهداف والاحتياجات
ANIMAL_DATA = {
    "الدواجن": {
        "لاحم - بادي": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "type": "poultry"},
        "لاحم - نامي": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "type": "poultry"},
        "دجاج بياض": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40, "type": "poultry"}
    },
    "الخيل": {
        "فرسات (حوامل)": {"CP": 12.5, "ME": 13.0, "Ca": 0.45, "P": 0.35, "type": "equine"},
        "أمهار (فطام)": {"CP": 15.0, "ME": 13.5, "Ca": 0.7, "P": 0.45, "type": "equine"},
        "حصين رياضة": {"CP": 11.0, "ME": 14.5, "Ca": 0.3, "P": 0.2, "type": "equine"}
    },
    "الأبقار": {
        "حلابة": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "type": "ruminant"},
        "تسمين": {"CP": 14.0, "ME": 12.0, "Ca": 0.6, "P": 0.35, "type": "ruminant"},
        "جفاف": {"CP": 12.0, "ME": 10.5, "Ca": 0.5, "P": 0.3, "type": "ruminant"}
    },
    "الأغنام والماعز": {
        "حلوب": {"CP": 16.0, "ME": 11.5, "Ca": 0.6, "P": 0.3, "type": "ruminant"},
        "تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "type": "ruminant"}
    }
}

st.title("🚜 نظام الإدارة الغذائية المتكامل")
st.caption("تطوير المهندس: عبدالقادر إسماعيل - خبير تغذية حيوان")

# القسم الأول: اختيار التصنيف
cat = st.selectbox("1. اختر فئة الحيوان:", list(ANIMAL_DATA.keys()))
sub_cat = st.selectbox("2. اختر النوع:", list(ANIMAL_DATA[cat].keys()))
target = ANIMAL_DATA[cat][sub_cat]

# القسم الثاني: بيانات الإنتاج والميدان
st.divider()
st.header("📊 بيانات الإنتاج والميدان")
col1, col2 = st.columns(2)

with col1:
    count = st.number_input("العدد (رأس/طائر):", value=1, min_value=1)
    if target["type"] == "poultry":
        age = st.number_input("العمر (بالأيام):", value=1)
    else:
        weight = st.number_input("وزن الحيوان (كجم):", value=500)

with col2:
    if "حلاب" in sub_cat or "حلوب" in sub_cat:
        milk_prod = st.number_input("إنتاج الحليب اليومي (كجم/رأس):", value=10.0)
    elif "تسمين" in sub_cat or "لاحم" in sub_cat:
        growth_target = st.number_input("معدل النمو المستهدف (جرام/يوم):", value=1000 if target["type"] != "poultry" else 50)

# القسم الثالث: الحساب
if st.button("🚀 احسب البرنامج الغذائي"):
    engine = SmartFeedEngine("feeds_db.json")
    
    # حساب التركيبة المركزية
    result = engine.solve(target["CP"], target["ME"], target["Ca"], target["P"], 0, 0, target["type"])
    st.success(result)
    
    # حساب الجدول اليومي بناءً على مدخلاتك
    if target["type"] == "poultry":
        daily_feed = (age * 5.5 / 1000) * count # معادلة نمو الدواجن
        st.info(f"📋 إجمالي العلف المطلوب للقطيع: {daily_feed:.2f} كجم يومياً")
    else:
        # معادلة المجترات والخيل بناءً على الوزن والإنتاج
        base_intake = weight * 0.03
        if "حلاب" in sub_cat: base_intake += (milk_prod * 0.3)
        st.info(f"📋 إجمالي المادة الجافة المطلوبة يومياً للرأس: {base_intake:.2f} كجم")
