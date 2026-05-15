import streamlit as st
from engine import SmartFeedEngine

st.set_page_config(page_title="نظام المهندس عبدالقادر المتكامل", layout="wide")

# هيكلة البيانات المقترحة (الدواجن تشمل الناهي الآن)
ANIMAL_DATA = {
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
    }
}

st.title("🚜 المنصة الاستشارية للتغذية - م. عبدالقادر")

# اختيار الفئة والنوع
cat = st.selectbox("اختر فئة الحيوان:", list(ANIMAL_DATA.keys()))
sub_cat = st.selectbox("اختر الصنف الإنتاجي:", list(ANIMAL_DATA[cat].keys()))
target = ANIMAL_DATA[cat][sub_cat]

st.divider()
st.subheader("📋 بيانات الإنتاج")

col1, col2 = st.columns(2)
with col1:
    count = st.number_input("العدد (رأس/طائر):", value=1000 if "الدواجن" in cat else 1)
    if "الدواجن" in cat:
        age = st.number_input("العمر بالأيام:", value=1)
    else:
        weight = st.number_input("وزن الحيوان (كجم):", value=500)

with col2:
    if "حلاب" in sub_cat:
        milk = st.number_input("إنتاج الحليب المستهدف (كجم):", value=20)
    elif "تسمين" in sub_cat or "لاحم" in cat:
        growth = st.number_input("النمو المستهدف (جرام/يوم):", value=1000 if "الأبقار" in cat else 50)

if st.button("🚀 احسب البرنامج الغذائي"):
    engine = SmartFeedEngine("feeds_db.json")
    # حل مشكلة الـ TypeError بإرسال القيم بشكل صريح
    result = engine.solve(target.get("CP", 0), target.get("ME", 0), target.get("Ca", 0), target.get("P", 0), target["type"])
    st.success(result)
    
    # حساب الكميات الكلية (الجرام والكيلو)
    if "الدواجن" in cat:
        total_feed = (age * 5.5 / 1000) * count # كيلو علف للقطيع
        st.info(f"📍 إجمالي العلف المطلوب للقطيع يومياً: {total_feed:.2f} كجم")
    else:
        daily_dm = weight * 0.03 # 3% من الوزن
        st.info(f"📍 إجمالي المادة الجافة للرأس الواحد: {daily_dm:.2f} كجم")
