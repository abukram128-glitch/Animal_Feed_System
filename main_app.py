import streamlit as st
import pandas as pd
import json
from engine import SmartFeedEngine

# 1. قائمة الاحتياجات الغذائية الشاملة
STANDARDS = {
    "--- اختر نوع الحيوان ---": {"CP": 0.0, "ME": 0.0, "Ca": 0.0, "P": 0.0, "Lys": 0.0, "Met": 0.0},
    "دجاج لاحم - بادئ": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "Lys": 1.10, "Met": 0.50},
    "دجاج لاحم - نامي": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "Lys": 1.00, "Met": 0.45},
    "دجاج بياض - إنتاج": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40, "Lys": 0.85, "Met": 0.38},
    "أبقار حلوب": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "Lys": 0.0, "Met": 0.0},
    "أبقار تسمين": {"CP": 14.0, "ME": 12.0, "Ca": 0.6, "P": 0.35, "Lys": 0.0, "Met": 0.0},
    "ماعز حلوب": {"CP": 16.0, "ME": 11.5, "Ca": 0.6, "P": 0.3, "Lys": 0.0, "Met": 0.0},
    "ماعز تسمين": {"CP": 13.5, "ME": 11.0, "Ca": 0.5, "P": 0.25, "Lys": 0.0, "Met": 0.0},
    "أغنام تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "Lys": 0.0, "Met": 0.0},
    "خيل - فرسات (حوامل)": {"CP": 12.5, "ME": 13.0, "Ca": 0.45, "P": 0.35, "Lys": 0.5, "Met": 0.0},
    "خيل - أمهار (فطام)": {"CP": 15.0, "ME": 13.5, "Ca": 0.7, "P": 0.45, "Lys": 0.7, "Met": 0.0}
}

st.set_page_config(page_title="نظام المهندس عبدالقادر", layout="wide")

# 2. الآلة الحاسبة الجانبية
with st.sidebar:
    st.header("🧮 آلة حاسبة سريعة")
    weight = st.number_input("الكمية (طن)", value=1.0)
    price_unit = st.number_input("سعر الوحدة", value=0.0)
    if st.button("احسب التكلفة"):
        st.write(f"الإجمالي: {weight * price_unit}")
    st.divider()

st.title("🌾 نظام تركيب العلائق المطور")

# 3. عرض المكونات المتوفرة
st.subheader("📦 المكونات المتوفرة في المخزن")
try:
    with open("feeds_db.json", "r", encoding="utf-8") as f:
        db_data = json.load(f)
    df_ingredients = pd.DataFrame([
        {"المادة": i["name"], "بروتين %": i["nutrients"]["CP"]/10 if i["nutrients"]["CP"] > 100 else i["nutrients"]["CP"], "طاقة ME": i["nutrients"]["ME"]} 
        for i in db_data["ingredients"]
    ])
    st.table(df_ingredients)
except:
    st.error("تأكد من وجود ملف feeds_db.json بصيغة صحيحة")

# 4. مدخلات الحساب
st.subheader("🎯 تحديد الأهداف الغذائية")
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

if st.button("🚀 احسب العليقة الأقل تكلفة"):
    engine = SmartFeedEngine("feeds_db.json")
    res = engine.solve(req_cp, req_me, req_ca, req_p, req_lys, req_met)
    st.success(res)
