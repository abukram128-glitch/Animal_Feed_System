# اسم الملف المقترح: app.py
import streamlit as st
import pandas as pd
# استيراد المحرك الرياضي مباشرة للاعتماد عليه في الخلفية
from engine import SmartFeedEngine 

st.set_page_config(page_title="SmartFeed Engine", layout="wide", page_icon="🌾")

# 1. قاعدة البيانات الافتراضية المدمجة بالواجهة
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
st.markdown("تطبيق تفاعلي لحساب العلائق الأقل تكلفة (Least-Cost Ration Formulation).")

col1, col2 = st.columns([2, 3])

with col1:
    st.header("1. الاحتياجات الغذائية")
    animal_type = st.selectbox("نوع الحيوان / الطائر:", ["دواجن تسمين", "دواجن بياض", "مجترات (تسمين)", "مجترات (حليب)"])
    
    st.markdown("---")
    cp_min = st.number_input("الحد الأدنى للبروتين الخام (CP %)", value=23.0, step=0.5)
    me_min = st.number_input("الحد الأدنى للطاقة (ME kcal/kg)", value=3000, step=50)
    
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        ca_min = st.number_input("أدنى كالسيوم (%)", value=0.90, step=0.05)
        p_min = st.number_input("أدنى فسفور (%)", value=0.45, step=0.05)
        lys_min = st.number_input("أدنى لايسين (%)", value=1.10, step=0.05)
    with sub_col2:
        ca_max = st.number_input("أقصى كالسيوم (%)", value=1.10, step=0.05)
        p_max = st.number_input("أقصى فسفور (%)", value=0.60, step=0.05)
        met_min = st.number_input("أدنى ميثيونين (%)", value=0.50, step=0.05)

with col2:
    st.header("2. إدارة أسعار وتحليل الخامات المتاحة")
    st.markdown("يمكنك تعديل الأسعار أو نسب التحليل الغذائي مباشرة من الجدول:")
    
    df_ingredients = pd.DataFrame(get_default_ingredients())
    # استخدام st.data_editor ليتيح للمستخدم التعديل المباشر أو إضافة خامات جديدة
    edited_df = st.data_editor(df_ingredients, num_rows="dynamic", hide_index=True)

st.markdown("---")
if st.button("🚀 احسب التركيبة المثالية الآن", use_container_width=True):
    
    # تحويل بيانات الجدول المعدل إلى الصيغة المتوافقة مع المحرك الرياضي
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

    # تجهيز قاموس الاحتياجات
    reqs = {
        'cp_min': cp_min, 'me_min': me_min,
        'ca_min': ca_min, 'ca_max': ca_max,
        'p_min': p_min, 'p_max': p_max,
        'lys_min': lys_min, 'met_min': met_min
    }

    # استدعاء المحرك الرياضي وحل المسألة
    engine = SmartFeedEngine(formatted_ingredients)
    res = engine.create_formulation(reqs, animal_type)

    if res["Status"] == "Success":
        st.success("✅ تم العثور على التركيبة الاقتصادية المثالية بنجاح!")
        
        out_col1, out_col2 = st.columns(2)
        with out_col1:
            st.subheader("📊 نسب المكونات في الطن:")
            df_res = pd.DataFrame(list(res["Formulation_Percentage"].items()), columns=['الخامة', 'النسبة (%)'])
            st.dataframe(df_res, hide_index=True, use_container_width=True)
            st.bar_chart(df_res.set_index('الخامة'))
            
        with out_col2:
            st.subheader("🧪 التحليل الغذائي النهائي المحقق:")
            df_nutrients = pd.DataFrame(list(res["Actual_Nutritional_Profile"].items()), columns=['العنصر', 'النسبة المحققة فعلياً'])
            st.dataframe(df_nutrients, hide_index=True, use_container_width=True)
            
            st.metric(label="💰 التكلفة الإجمالية لكل 100 كجم", value=f"{res['Cost_per_100kg']}")
            st.metric(label="🚛 تكلفة الطن الواحد الفصيلية", value=f"{round(res['Cost_per_100kg'] * 10, 2)}")
    else:
        st.error(f"❌ لم يتم العثور على حل مطابق: {res['Message']}")
