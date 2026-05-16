# filename: main.py
import pprint
from engine import SmartFeedEngine 

# قاعدة بيانات الخامات والأسعار التي أرسلتها
data = {
  "ingredients": [
    {"name": "ذرة صفراء (حبوب)", "nutrients": {"CP": 8.8, "ME": 3370, "Ca": 0.02, "P": 0.27, "Lys": 0.24, "Met": 0.18}, "price": 400},
    {"name": "شعير (حبوب)", "nutrients": {"CP": 11.5, "ME": 2910, "Ca": 0.08, "P": 0.38, "Lys": 0.36, "Met": 0.17}, "price": 420},
    {"name": "كسب صويا 44%", "nutrients": {"CP": 44.0, "ME": 2240, "Ca": 0.28, "P": 0.66, "Lys": 2.85, "Met": 0.64}, "price": 850},
    {"name": "كسب عباد الشمس (مقشور)", "nutrients": {"CP": 36.0, "ME": 2100, "Ca": 0.40, "P": 0.90, "Lys": 1.10, "Met": 0.70}, "price": 600},
    {"name": "نخالة قمح (ردة)", "nutrients": {"CP": 15.5, "ME": 1300, "Ca": 0.14, "P": 1.15, "Lys": 0.65, "Met": 0.22}, "price": 320},
    {"name": "برسيم جاف (دريس)", "nutrients": {"CP": 16.5, "ME": 1950, "Ca": 1.45, "P": 0.24, "Lys": 0.75, "Met": 0.28}, "price": 450},
    {"name": "مسحوق سمك (60%)", "nutrients": {"CP": 60.0, "ME": 2850, "Ca": 5.0, "P": 3.0, "Lys": 4.5, "Met": 1.8}, "price": 1500},
    {"name": "حجر جيري (مسحوق)", "nutrients": {"CP": 0.0, "ME": 0, "Ca": 38.0, "P": 0.0, "Lys": 0.0, "Met": 0.0}, "price": 50}
  ]
}

# تحديد الاحتياجات الغذائية المطلوبة للحيوان أو الطائر
poultry_broiler_req = {
    'cp_min': 23.0,
    'me_min': 3000,
    'ca_min': 0.90,
    'ca_max': 1.10,
    'p_min': 0.45,
    'p_max': 0.60,
    'lys_min': 1.10,
    'met_min': 0.50
}

# تشغيل المحرك
engine = SmartFeedEngine(data["ingredients"])
result = engine.create_formulation(poultry_broiler_req, animal_type="دواجن تسمين")

print("--- نتيجة تشغيل البرنامج التجريبية ---")
pprint.pprint(result)
