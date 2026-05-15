import streamlit as st
from engine import SmartFeedEngine

st.set_page_config(page_title="نظام المهندس عبدالقادر إسماعيل", layout="centered")

# لمسات جمالية وألوان
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f4; }
    .stButton>button { width: 100%; background-color: #2e7d32; color: white; border-radius: 10px; height: 3.5em; font-weight: bold; }
    .expert-title { color: #1b5e20; text-align: center; border-right: 8px solid #1b5e20; padding-right: 15px; background: white; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='expert-title'><h1>🌾 نظام الإدارة الغذائية الذكي</h1><p><b>اختصاصي تغذية الحيوان: عبدالقادر إسماعيل تاور</b></p></div>", unsafe_allow_html=True)

# المكتبة العلمية المدمجة
INTERNAL_LIBRARY = {
    "قسم الخيول": {
        "فرسات حوامل": {"CP": 12.5, "ME": 13.0, "Ca": 0.45, "P": 0.35, "type": "horse"},
        "أمهار فطام": {"CP": 15.0, "ME": 13.5, "Ca": 0.7, "P": 0.45, "type": "horse"},
        "حصين رياضة": {"CP": 11.0, "ME": 14.5, "Ca": 0.3, "P": 0.2, "type": "horse"}
    },
    "قسم الدواجن": {
        "بادي (0-10 أيام)": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "type": "poultry"},
        "نامي (11-24 يوم)": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "type": "poultry"},
        "ناهي (25-تسويق)": {"CP": 19.0, "ME": 3200, "Ca": 0.85, "P": 0.30, "type": "poultry"}
    },
    "قسم المجترات": {
        "أبقار حلابة": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "type": "ruminant"},
        "تسمين": {"CP": 14.0, "ME": 12.0, "Ca": 0.6, "P": 0.35, "type": "ruminant"}
    }
}

cat = st.selectbox("1. اختر فئة الحيوان:", list(INTERNAL_LIBRARY.keys()))
sub_cat = st.selectbox("2. اختر الصنف الإنتاجي:", list(INTERNAL_LIBRARY[cat].keys()))
target = INTERNAL_LIBRARY[cat][sub_cat]

st.divider()
c1, c2 = st.columns(2)
with c1:
    count = st.number_input("العدد:", value=100 if "الدواجن" in cat else 1)
    weight = st.number_input("الوزن (كجم):", value=500 if "أبقار" in sub_cat or "الخيول" in cat else 45)
with c2:
    if "الدواجن" in cat: age = st.number_input("العمر (أيام):", value=15)
    else: prod = st.number_input("الإنتاج (حليب/نمو):", value=15.0)

if st.button("🚀 تشغيل الخوارزمية العلمية"):
    engine = SmartFeedEngine()
    res = engine.solve(target["CP"], target["ME"], target["Ca"], target["P"], target["type"])
    if "✅" in res:
        st.success(res)
    else: st.error(res)
