import streamlit as st
import json
from engine import SmartFeedEngine

# إعدادات الواجهة
st.set_page_config(page_title="نظام المهندس عبدالقادر - النسخة الاحترافية", layout="wide")

# استايل التنسيق
st.markdown("""
    <style>
    .stMultiSelect [data-baseweb="tag"] { background-color: #2e7d32; }
    .reportview-container { background: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌾 نظام تركيب الأعلاف الذكي (نسخة البدائل المحلية)")
st.info("أهلاً يا بشمهندس عبدالقادر. يمكنك الآن اختيار المكونات المتاحة في منطقتك من القائمة أدناه.")

# تحميل المكتبة العلمية (التي استخلصناها من صورك)
try:
    with open('feeds_db.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
        all_ingredients = db['ingredients']
except:
    st.error("يرجى التأكد من رفع ملف feeds_db.json المحدث")
    st.stop()

# 1. اختيار المكونات المتوفرة ميدانياً
st.subheader("1️⃣ حدد المكونات المتوفرة في منطقتك حالياً:")
available_names = [i['name'] for i in all_ingredients]
selected_names = st.multiselect("اختر المكونات (سيتم استبعاد غير المختارة من الحسابات):", 
                               available_names, 
                               default=[n for n in available_names if "ذرة" in n or "صويا" in n or "نخالة" in n])

# تصفية المكتبة بناءً على اختيارك
selected_ingredients = [i for i in all_ingredients if i['name'] in selected_names]

# 2. تحديد الاحتياجات الغذائية (بناءً على جداول NRC/ARC المرفقة)
st.subheader("2️⃣ الأهداف الغذائية للقطيع:")
col1, col2, col3, col4 = st.columns(4)
with col1: req_cp = st.number_input("البروتين الخام (CP %):", 10.0, 30.0, 18.0)
with col2: req_me = st.number_input("الطاقة التمثيلية (ME):", 1500, 3500, 2850)
with col3: req_ca = st.number_input("الكالسيوم (Ca %):", 0.1, 5.0, 1.0)
with col4: req_p = st.number_input("الفسفور المتاح (P %):", 0.1, 2.0, 0.45)

animal_type = st.radio("نوع الحيوان لضبط قيود الأمان:", ["ruminant", "poultry"])

if st.button("🚀 حساب التركيبة الأقل تكلفة بالبدائل المختارة"):
    if not selected_ingredients:
        st.warning("يرجى اختيار مكون واحد على الأقل.")
    else:
        engine = SmartFeedEngine(selected_ingredients)
        requirements = {'cp': req_cp, 'me': req_me, 'ca': req_ca, 'p': req_p}
        result = engine.create_formulation(requirements, animal_type)
        
        if result.success:
            st.success("✅ تم العثور على التركيبة المثالية:")
            for i, val in enumerate(result.x):
                if val > 0.001:
                    st.write(f"**- {selected_names[i]}:** {val*100:.2f} %")
            st.metric("التكلفة الإجمالية للطن:", f"{result.fun:,.2f}")
        else:
            st.error("❌ لا يمكن تحقيق هذه الاحتياجات بالمكونات المختارة. حاول إضافة بدائل بروتينية أو طاقة إضافية.")
