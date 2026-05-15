import streamlit as st
from engine import SmartFeedEngine

# إعدادات الهوية المهنية
st.set_page_config(page_title="نظام المهندس عبدالقادر إسماعيل", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #1b5e20; color: white; border-radius: 10px; font-size: 18px; }
    .expert-header { color: #2e7d32; text-align: center; border-bottom: 2px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

# الهيدر والشعار
col_l, col_r = st.columns([1, 4])
with col_l: st.markdown("<h1>🌾</h1>", unsafe_allow_html=True)
with col_r:
    st.markdown("<h2 class='expert-header'>نظام الإدارة الغذائية المتكامل</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'><b>اختصاصي تغذية الحيوان: عبدالقادر إسماعيل تاور</b></p>", unsafe_allow_html=True)

# المكتبة العلمية المحدثة
INTERNAL_LIBRARY = {
    "قسم المجترات (أبقار، أغنام، ماعز)": {
        "أبقار حلابة": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "type": "ruminant"},
        "أبقار تسمين": {"CP": 14.0, "ME": 12.0, "Ca": 0.6, "P": 0.35, "type": "ruminant"},
        "أغنام/ماعز حلوب": {"CP": 16.0, "ME": 11.5, "Ca": 0.6, "P": 0.3, "type": "ruminant"},
        "أغنام/ماعز تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "type": "ruminant"}
    },
    "قسم الدواجن (لاحم وبياض)": {
        "بادي (0-10 أيام)": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "type": "poultry"},
        "نامي (11-24 يوم)": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "type": "poultry"},
        "ناهي (25-تسويق)": {"CP": 19.0, "ME": 3200, "Ca": 0.85, "P": 0.30, "type": "poultry"},
        "دجاج بياض": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40, "type": "poultry"}
    }
}

cat = st.selectbox("اختر فئة الحيوان:", list(INTERNAL_LIBRARY.keys()))
sub_cat = st.selectbox("اختر الصنف الإنتاجي:", list(INTERNAL_LIBRARY[cat].keys()))
target = INTERNAL_LIBRARY[cat][sub_cat]

st.divider()
c1, c2 = st.columns(2)
with c1:
    count = st.number_input("العدد الكلي:", value=100 if "الدواجن" in cat else 1)
    weight = st.number_input("الوزن (كجم):", value=500 if "أبقار" in sub_cat else 45)
with c2:
    if "الدواجن" in cat: age = st.number_input("العمر (أيام):", value=20)
    else: prod = st.number_input("الإنتاج (حليب/نمو):", value=15.0)

if st.button("🚀 تشغيل الخوارزمية العلمية"):
    engine = SmartFeedEngine()
    res = engine.solve(target["CP"], target["ME"], target["Ca"], target["P"], target["type"])
    
    if "✅" in res:
        st.success(res)
        if target["type"] == "poultry":
            st.info(f"📍 علف القطيع اليومي: {(age * 5.5 / 1000) * count:.2f} كجم")
        else:
            st.info(f"📍 احتياج المادة الجافة للرأس: {weight * 0.03:.2f} كجم")
    else: st.error(res)
