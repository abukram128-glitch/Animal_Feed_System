import streamlit as st
from engine import SmartFeedEngine

# إعدادات الهوية المهنية والألوان
st.set_page_config(page_title="نظام المهندس عبدالقادر إسماعيل", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f4; }
    .stButton>button { width: 100%; background-color: #2e7d32; color: white; border-radius: 10px; height: 3.5em; font-weight: bold; }
    .expert-title { color: #1b5e20; text-align: center; border-right: 8px solid #1b5e20; padding-right: 15px; background: white; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='expert-title'><h1>🌾 نظام الإدارة الغذائية الذكي</h1><p><b>اختصاصي تغذية الحيوان: عبدالقادر إسماعيل تاور</b></p></div>", unsafe_allow_html=True)

# المكتبة العلمية الشاملة والمحدثة
INTERNAL_LIBRARY = {
    "قسم الدواجن": {
        "بادي (لاحم)": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "type": "poultry", "prod_type": "growth"},
        "نامي (لاحم)": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "type": "poultry", "prod_type": "growth"},
        "ناهي (لاحم)": {"CP": 19.0, "ME": 3200, "Ca": 0.85, "P": 0.30, "type": "poultry", "prod_type": "growth"},
        "دجاج بياض (إنتاج)": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40, "type": "poultry", "prod_type": "egg"}
    },
    "قسم الأبقار": {
        "أبقار حلابة": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "type": "ruminant", "prod_type": "milk"},
        "عجول تسمين (ذكور)": {"CP": 14.0, "ME": 12.0, "Ca": 0.6, "P": 0.35, "type": "ruminant", "prod_type": "growth"}
    },
    "قسم الأغنام والماعز": {
        "ماعز/أغنام (لبن)": {"CP": 16.0, "ME": 11.5, "Ca": 0.6, "P": 0.3, "type": "ruminant", "prod_type": "milk"},
        "خراف تسمين (ذكور)": {"CP": 14.5, "ME": 11.0, "Ca": 0.4, "P": 0.25, "type": "ruminant", "prod_type": "growth"}
    },
    "قسم الخيول": {
        "خيل رياضة/عمل": {"CP": 11.0, "ME": 14.5, "Ca": 0.3, "P": 0.2, "type": "horse", "prod_type": "work"}
    }
}

cat = st.selectbox("1. اختر فئة الحيوان:", list(INTERNAL_LIBRARY.keys()))
sub_cat = st.selectbox("2. اختر الصنف الإنتاجي:", list(INTERNAL_LIBRARY[cat].keys()))
target = INTERNAL_LIBRARY[cat][sub_cat]

st.divider()
st.subheader("📊 بيانات الإنتاج الميداني")
c1, c2 = st.columns(2)

with c1:
    count = st.number_input("العدد الكلي:", value=100 if "الدواجن" in cat else 1)
    weight = st.number_input("الوزن (كجم):", value=500 if "الأبقار" in cat else 45)

with c2:
    # تمييز الواجهة: إخفاء إنتاج الحليب في حالة التسمين أو الدواجن
    if target["prod_type"] == "milk":
        prod = st.number_input("إنتاج الحليب اليومي (كجم):", value=15.0)
    elif target["prod_type"] == "growth":
        growth = st.number_input("النمو المستهدف (جرام/يوم):", value=1000 if "الأبقار" in cat else 200)
    elif target["prod_type"] == "egg":
        egg_rate = st.slider("نسبة إنتاج البيض %:", 0, 100, 85)
    else:
        st.write("حالة صيانة/رياضة")

if st.button("🚀 تشغيل الخوارزمية العلمية"):
    engine = SmartFeedEngine()
    res = engine.solve(target["CP"], target["ME"], target["Ca"], target["P"], target["type"])
    if "✅" in res:
        st.success(res)
        # حسابات المادة الجافة والعلف
        if target["type"] == "ruminant":
            st.info(f"📍 احتياج المادة الجافة التقريبي للرأس: {weight * 0.03:.2f} كجم/يوم")
    else:
        st.error(res)
