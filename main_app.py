import streamlit as st
import pandas as pd
from engine import SmartFeedEngine

st.set_page_config(page_title="نظام عبدالقادر الاحترافي", layout="wide")

@st.cache_resource
def init_engine():
    return SmartFeedEngine("feeds_db.json")

engine = init_engine()

st.title("🌱 نظام تركيب العلائق الذكي (مجترات - دواجن - خيل)")
st.markdown("---")

# اختيار نوع الحيوان لتحديد نظام الطاقة
animal_type = st.sidebar.selectbox("اختر نوع الحيوان المستهدف:", ["مجترات", "دواجن", "خيل"])
st.sidebar.info(f"نظام الطاقة المستخدم: {'ME' if animal_type != 'خيل' else 'DE'}")

tab1, tab2 = st.tabs(["📝 المدخلات والأسعار", "📈 النتائج النهائية"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("المكونات المتوفرة")
        selected = st.multiselect("اختر من المكتبة:", list(engine.ingredients.keys()))
        prices = {name: st.number_input(f"سعر {name} (للطن):", value=500.0) for name in selected}
        
    with col2:
        st.subheader("الاحتياجات الغذائية")
        req_cp = st.number_input("البروتين المطلوب (g/kg):", value=180.0)
        req_en = st.number_input(f"الطاقة المطلوبة ({'MJ' if animal_type != 'خيل' else 'Mcal'}/kg):", value=12.0)
        req_ca = st.number_input("الكالسيوم (g/kg):", value=8.0)
        req_p = st.number_input("الفسفور (g/kg):", value=4.0)

with tab2:
    if st.button("احسب التركيبة الأقل تكلفة"):
        if not selected:
            st.error("الرجاء اختيار المكونات أولاً.")
        else:
            reqs = {'CP': req_cp, 'Energy': req_en, 'Ca': req_ca, 'P': req_p}
            res = engine.solve(selected, prices, reqs, animal_type)
            
            if res.success:
                st.success("✅ تم الوصول للحل الأمثل")
                df = pd.DataFrame({
                    "المادة": [selected[i] for i, v in enumerate(res.x) if v > 0.001],
                    "النسبة (%)": [f"{v*100:.2f}%" for v in res.x if v > 0.001],
                    "كجم / طن": [f"{v*1000:.1f}" for v in res.x if v > 0.001]
                })
                st.table(df)
                st.metric("التكلفة الإجمالية للطن", f"{res.fun:.2f}")
            else:
                st.error("❌ لا يمكن تحقيق هذه المواصفات بالمكونات المختارة.")
