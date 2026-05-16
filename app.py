# filename: app.py
import streamlit as st
import pandas as pd
from engine import SmartFeedEngine 

st.set_page_config(page_title="محرك التغذية الذكية", layout="wide")

@st.cache_data
def get_default_ingredients():
    return [
        {"name": "ذرة صفراء (حبوب)", "CP": 8.8, "ME": 3370, "Ca": 0.02, "P": 0.27, "Lys": 0.24, "Met": 0.18, "price": 400.0},
        {"name": "شعير (حبوب)", "CP": 11.5, "ME": 2910, "Ca": 0.08, "P": 0.38, "Lys": 0.36, "Met": 0.17, "price": 420.0},
        {"name": "كسب صويا 44%", "CP": 44.0, "ME": 2240, "Ca": 0.28, "P": 0.66, "Lys": 2.85, "Met": 0.64, "price": 850.0},
        {"name": "كسب عباد الشمس (مقشور)", "CP": 36.0, "ME": 2100, "Ca": 0.40, "P": 0.90, "Lys": 1.10, "Met": 0.70, "price": 600.0},
        {"name": "نخالة قمح (ردة)", "CP": 15.5, "ME": 1300, "Ca": 0.14, "P": 1.15, "Lys": 0.65, "Met": 0.22, "price": 320.0},
        {"name": "برسيم جاف (دريس)", "CP": 16.5, "ME": 1950, "Ca": 1.45, "P": 0.24, "Lys": 0.75, "Met": 0.28, "price": 450.0},
        {"name": "مسحوق سمك (60%)", "CP": 60.0, "ME": 2850, "Ca": 5.0, "P": 3.0, "Lys": 4.5, "Met": 1.8, "price": 1500.0},
        {"name": "حجر جيري (مسحوق)", "CP": 0.0, "ME": 0, "Ca": 38.0, "P": 0.0, "Lys": 0.0, "Met": 0.0, "price": 50.0}
    ]

st.title("🌾 محرك تركيب الأعلاف الذكي | SmartFeed Engine")
st.markdown("صياغة الحصة التموينية الأقل تكلفة")

col1, col2 = st.columns([2, 3])

with col1:
    st.header("1. الاحتياجات الغذائية للحيوان")
    animal_type = st.selectbox("نوع الحيوان:", ["دواجن تسمين", "دواجن بياض", "مجترات (تسمين)", "مجترات (حليب)"])
    
    st.markdown("---")
    cp_min = st.number_input("الحد للبروتين الخام (CP %)", value=23.0)
    me_min = st.number_input("الحد الصافي للطاقة (ME kcal/kg)", value=3000)
    ca_min = st.number_input("أدنى كالسيوم (%)", value=0.90)

with col2:
    st.header("2. إدارة تحليل أسعار الخام")
    st.markdown("تعديل التحليل والأسعار مباشرة من الجدول التالي:")
    
    df_ingredients = pd.DataFrame(get_default_ingredients())
    edited_df = st.data_editor(df_ingredients, num_rows="dynamic", hide_index=True)

st.markdown("---")
if st.button("🚀 احسب التركيبة المثالية الآن", use_container_width=True):
    
    formatted_ingredients = []
    for _, row in edited_df.iterrows():
        formatted_ingredients.append({
            "name": row['name'],
            "price": row['price'],
            "nutrients": {
                "CP": row['CP'], "ME": row['ME'], "Ca": row['Ca'],
                "P": row['P'], "Lys": row['Lys'], "Met": row['Met']
            }
        })

    reqs = {
        'cp_min': cp_min, 'me_min': me_min,
        'ca_min': ca_min, 'ca_max': ca_min + 0.2,
        'p_min': 0.45, 'p_max': 0.60,
        'lys_min': 1.10, 'met_min': 0.50
    }

    engine = SmartFeedEngine(formatted_ingredients)
    res = engine.create_formulation(reqs, animal_type)

    if res["Status"] == "Success":
        st.success("✔ تم العثور على التركيبة الاقتصادية المثالية")
        
        out_col1, out_col2 = st.columns(2)
        with out_col1:
            st.subheader("📊 المكونات النسبية في طن:")
            df_res = pd.DataFrame(list(res["Formulation_Percentage"].items()), columns=['الخامة', 'النسبة (%)'])
            st.dataframe(df_res, hide_index=True)
            st.bar_chart(df_res.set_index('الخامة'))
            
        with out_col2:
            st.subheader("🧪 التحليل النهائي المحقق:")
            df_nutrients = pd.DataFrame(list(res["Actual_Nutritional_Profile"].items()), columns=['العنصر', 'النسبة'])
            st.dataframe(df_nutrients, hide_index=True)
            
            st.metric(label="💰 التكلفة لكل 100 كجم", value=f"{res['Cost_per_100kg']}")
            st.metric(label="🚛 تكلفة الطن الواحد", value=f"{round(res['Cost_per_100kg'] * 10, 2)}")
    else:
        st.error(f"❌ لم يتم العثور على حل حسب المعايير المطلوبة")
