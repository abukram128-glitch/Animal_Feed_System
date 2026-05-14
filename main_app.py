import streamlit as st
import pandas as pd
import json
from engine import SmartFeedEngine

# --- 1. المعايير القياسية ---
STANDARDS = {
    "--- اختر نوع العليقة ---": {"CP": 0.0, "ME": 0.0, "Ca": 0.0, "P": 0.0, "Lys": 0.0, "Met": 0.0},
    "دواجن - بادئ": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "Lys": 1.10, "Met": 0.50},
    "أغنام - تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "Lys": 0.0, "Met": 0.0}
}

st.set_page_config(page_title="نظام المهندس عبدالقادر", layout="wide")

# --- 2. الآلة الحاسبة الجانبية ---
with st.sidebar:
    st.header("🧮 آلة حاسبة سريعة")
    weight = st.number_input("الكمية (طن)", value=1.0)
    price_unit = st.number_input("سعر الوحدة", value=0.0)
    if st.button("احسب التكلفة"):
        st.write(f"الإجمالي: {weight * price_unit}")
    st.divider()

st.title("🌾 نظام تركيب العلائق المطور")

# --- 3. عرض المكونات المتوفرة ---
st.subheader("📦 المكونات في المخزن")
try:
    with open("feeds_db.json", "r", encoding="utf-8") as f:
        db_data = json.load(f)
    df_ingredients = pd.DataFrame([
        {"المادة": i["name"], "بروتين": i["nutrients"]["CP"]/10, "طاقة": i["nutrients"]["ME"]} 
        for i in db_data["ingredients"]
    ])
    st.table(df_ingredients)
except:
    st.error("فشل في تحميل المكونات من feeds_db.json")

# --- 4. مدخلات الحساب ---
st.subheader("🎯 تحديد الأهداف الغذائية")
choice = st.selectbox("اختر المعيار:", list(STANDARDS.keys()))
std = STANDARDS[choice]

col1, col2, col3 = st.columns(3)
with col1:
    req_cp = st.number_input("البروتين (%)", value=float(std["CP"]))
    req_me = st.number_input("الطاقة (ME)", value=float(std["ME"]))
with col2:
    req_ca = st.number_input("الكالسيوم (%)", value=float(std["Ca"]))
    req_p = st.number_input("الفسفور (%)", value=float(std["P"]))
with col3:
    req_lys = st.number_input("الليسين (%)", value=float(std["Lys"]))
    req_met = st.number_input("الميثيونين (%)", value=float(std["Met"]))

if st.button("🚀 احسب العليقة"):
    engine = SmartFeedEngine("feeds_db.json")
    res = engine.solve(req_cp, req_me, req_ca, req_p, req_lys, req_met)
    st.success(res)
