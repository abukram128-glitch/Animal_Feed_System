import streamlit as st
from engine import SmartFeedEngine

# إعدادات الواجهة والألوان
st.set_page_config(page_title="نظام المهندس عبدالقادر إسماعيل", layout="centered")

# إضافة تصميم احترافي وألوان مريحة (Professional UI)
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp { background-color: #f0f4f0; }
    /* تنسيق الأزرار */
    .stButton>button { 
        width: 100%; 
        background-color: #1b5e20; 
        color: white; 
        border-radius: 12px; 
        height: 3.5em; 
        font-weight: bold;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    /* تنسيق العناوين */
    h1, h2, h3 { color: #2e7d32; font-family: 'Cairo', sans-serif; }
    .expert-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 10px solid #1b5e20;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# الهيدر التعريفي
st.markdown(f"""
    <div class="expert-card">
        <h1 style='margin:0;'>🌾 نظام الإدارة الغذائية المتكامل</h1>
        <p style='font-size:18px; margin:0;'><b>اختصاصي تغذية الحيوان: عبدالقادر إسماعيل تاور</b></p>
    </div>
    """, unsafe_allow_html=True)

# المكتبة العلمية المحدثة (إضافة الخيل والدواجن والمجترات)
INTERNAL_LIBRARY = {
    "قسم الخيول": {
        "فرسات حوامل": {"CP": 12.5, "ME": 13.0, "Ca": 0.45, "P": 0.35, "type": "horse"},
        "أمهار فطام": {"CP": 15.0, "ME": 13.5, "Ca": 0.70, "P": 0.45, "type": "horse"},
        "حصين رياضة": {"CP": 11.0, "ME": 14.5, "Ca": 0.30, "P": 0.20, "type": "horse"}
    },
    "قسم الدواجن": {
        "بادي (0-10 أيام)": {"CP": 23.0, "ME": 3025, "Ca": 1.0, "P": 0.45, "type": "poultry"},
        "نامي (11-24 يوم)": {"CP": 21.0, "ME": 3150, "Ca": 0.9, "P": 0.35, "type": "poultry"},
        "ناهي (25-تسويق)": {"CP": 19.0, "ME": 3200, "Ca": 0.85, "P": 0.30, "type": "poultry"},
        "دجاج بياض": {"CP": 17.5, "ME": 2800, "Ca": 3.8, "P": 0.40, "type": "poultry"}
    },
    "قسم المجترات (أبقار وأغنام)": {
        "أبقار حلابة": {"CP": 17.5, "ME": 11.8, "Ca": 0.75, "P": 0.45, "type": "ruminant"},
        "أبقار تسمين": {"CP": 14.0, "ME": 12.0, "Ca": 0.60, "P": 0.35, "type": "ruminant"},
        "أغنام/ماعز تسمين": {"CP": 14.5, "ME": 11.0, "Ca": 0.40, "P": 0.25, "type": "ruminant"}
    }
}

# واجهة الاختيارات
with st.expander("🛠️ إعدادات الفصيلة والهدف", expanded=True):
    cat = st.selectbox("1. اختر فئة الحيوان:", list(INTERNAL_LIBRARY.keys()))
    sub_cat = st.selectbox("2. اختر الصنف الإنتاجي:", list(INTERNAL_LIBRARY[cat].keys()))
    target = INTERNAL_LIBRARY[cat][sub_cat]

st.divider()

# مدخلات الميدان
col1, col2 = st.columns(2)
with col1:
    count = st.number_input("العدد الكلي:", value=100 if "الدواجن" in cat else 1)
    weight = st.number_input("متوسط وزن الرأس (كجم):", value=500 if "أبقار" in sub_cat or "الخيول" in cat else 45)
with col2:
    if "الدواجن" in cat:
        age = st.number_input("العمر (أيام):", value=15)
    else:
        prod = st.number_input("الإنتاج المستهدف (حليب/نمو):", value=15.0)

# تشغيل الخوارزمية
if st.button("🚀 تشغيل الخوارزمية العلمية"):
    engine = SmartFeedEngine()
    # إرسال الاحتياجات للمحرك
    res = engine.solve(target["CP"], target["ME"], target["Ca"], target["P"], target["type"])
    
    if "✅" in res:
        st.success(res)
        # معلومات ميدانية إضافية
        if target["type"] == "poultry":
            st.info(f"📋 علف القطيع اليومي: {(age * 5.5 / 1000) * count:.2f} كجم")
        else:
            st.info(f"📋 احتياج المادة الجافة للرأس: {weight * 0.03:.2f} كجم")
    else:
        st.error(res)
