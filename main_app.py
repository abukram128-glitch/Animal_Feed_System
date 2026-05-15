import streamlit as st
import pandas as pd
from engine import SmartFeedEngine

# إعدادات الصفحة وهوية النظام
st.set_page_config(page_title="نظام المهندس عبدالقادر إسماعيل", layout="wide")

# عرض الشعار والاسم المهني
col_h1, col_h2 = st.columns([1, 6])
with col_h1:
    # شعار سنبلة القمح
    st.image("https://img.icons8.com/ios-filled/100/40C057/wheat.png", width=80)
with col_h2:
    st.title("نظام الإدارة الغذائية الذكي")
    st.subheader("اختصاصي تغذية الحيوان: عبدالقادر إسماعيل تاور")

# المكتبة البرمجية المدمجة لضمان استقرار النظام
INTERNAL_LIBRARY = {
    "الدواجن (لاحم)": {
        "بادي (0-10 أيام)": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "type": "poultry"},
        "نامي (11-24 يوم)": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "type": "poultry"},
        "ناهي (25-تسويق)": {"CP": 19.0, "ME": 3200, "Ca": 0.85, "P": 0.30, "type": "poultry"}
    },
    "الدواجن (بياض)": {
        "بياض إنتاج": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40, "type": "poultry"}
    },
    "الأبقار": {
        "حلابة": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "type": "ruminant"},
        "تسمين": {"CP": 14.0, "ME": 12.0, "Ca": 0.6, "P": 0.35, "type": "ruminant"},
        "جفاف": {"CP": 12.0, "ME": 10.5, "Ca": 0.5, "P": 0.3, "type": "ruminant"}
    },
    "الخيل": {
        "فرسات حوامل": {"CP": 12.5, "ME": 13.0, "type": "equine"},
        "أمهار فطام": {"CP": 15.0, "ME": 13.5, "type": "equine"},
        "حصين رياضة": {"CP": 11.0, "ME": 14.5, "type": "equine"}
    },
    "الأغنام والماعز": {
        "حلوب": {"CP": 16.0, "ME": 11.5, "Ca": 0.6, "P": 0.3, "type": "ruminant"},
        "تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "type": "ruminant"}
    }
}

# واجهة المدخلات
cat = st.selectbox("1. اختر فئة الحيوان:", list(INTERNAL_LIBRARY.keys()))
sub_cat = st.selectbox("2. اختر الصنف الإنتاجي:", list(INTERNAL_LIBRARY[cat].keys()))
target = INTERNAL_LIBRARY[cat][sub_cat]

st.divider()
st.header("📊 بيانات الميدان والإنتاج")
c1, c2 = st.columns(2)

with c1:
    count = st.number_input("العدد الكلي:", value=1000 if "الدواجن" in cat else 1)
    if "الدواجن" in cat:
        age = st.number_input("العمر (أيام):", value=1, min_value=1)
    else:
        weight = st.number_input("وزن الحيوان (كجم):", value=500)

with c2:
    if "حلاب" in sub_cat or "حلوب" in sub_cat:
        milk = st.number_input("إنتاج الحليب (كجم/يوم):", value=15.0)
    elif "تسمين" in sub_cat or "لاحم" in cat:
        target_growth = st.number_input("النمو المستهدف (جرام/يوم):", value=1000 if "الأبقار" in cat else 50)

if st.button("🚀 تشغيل خوارزمية التغذية"):
    engine = SmartFeedEngine("feeds_db.json")
    # حل مشكلة TypeError بضمان إرسال جميع القيم
    res = engine.solve(target.get("CP",0), target.get("ME",0), target.get("Ca",0), target.get("P",0), target["type"])
    st.success(res)
    
    # حساب البرنامج الميداني
    if "الدواجن" in cat:
        feed_per_bird = (age * 5.5) / 1000 
        st.info(f"📍 إجمالي علف القطيع المطلوب: {feed_per_bird * count:.2f} كجم يومياً")
    else:
        daily_dm = weight * 0.03
        st.info(f"📍 إجمالي المادة الجافة للرأس: {daily_dm:.2f} كجم يومياً")

st.sidebar.markdown("---")
st.sidebar.info(f"المستخدم الحالي: م. عبدالقادر إسماعيل")
