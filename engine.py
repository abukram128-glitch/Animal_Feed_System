import json
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.ingredients = {i['name']: i for i in data['ingredients']}
        except Exception as e:
            self.ingredients = {}

    def solve(self, req_cp, req_me, req_ca, req_p, req_lys, req_met):
        if not self.ingredients:
            return "❌ خطأ: تعذر قراءة قاعدة البيانات. تأكد من سلامة ملف feeds_db.json"

        names = list(self.ingredients.keys())
        # مصفوفة التكاليف
        prices = [self.ingredients[n].get('price', 1) for n in names]
        
        # مصفوفة القيود الغذائية (المتطلبات الدنيا)
        A_ub = []
        # البروتين، الطاقة، الكالسيوم، الفسفور، الليسين، الميثيونين
        A_ub.append([-self.ingredients[n]['nutrients']['CP'] for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['ME'] for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['Ca'] for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['P'] for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['Lys'] for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['Met'] for n in names])
        
        b_ub = [-req_cp, -req_me, -req_ca, -req_p, -req_lys, -req_met]
        
        # قيد المجموع الكلي (يجب أن يساوي 100%)
        A_eq = [[1 for _ in names]]
        b_eq = [1]
        
        # --- إضافة القيود الفنية (المنطق المهني) ---
        bounds = []
        for n in names:
            if "حجر جيري" in n or "ملح" in n:
                bounds.append((0, 0.02))  # لا يتجاوز 2% بأي حال
            elif "DCP" in n:
                bounds.append((0, 0.015)) # لا يتجاوز 1.5%
            elif "مركز" in n:
                bounds.append((0, 0.10))  # لا يتجاوز 10% لضبط التكلفة والجودة
            elif "ذرة" in n:
                bounds.append((0.40, 0.80)) # الذرة يجب أن تكون بين 40% و 80% لضمان الهيكل
            elif "صناعي" in n:
                bounds.append((0, 0.005)) # الأحماض الصناعية بجرعات دقيقة جداً
            else:
                bounds.append((0, 1.0))   # بقية المواد مرنة
        
        # تنفيذ عملية التحسين الرياضي
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = "✅ التركيبة المهنية المكتشفة (النسب المئوية):\n"
            output += "------------------------------------------\n"
            for i, val in enumerate(res.x):
                if val > 0.0001:
                    output += f"📍 {names[i]}: {round(val*100, 2)}%\n"
            
            # حساب القيم الغذائية الفعلية للتركيبة الناتجة للتأكد
            actual_cp = sum(res.x[i] * self.ingredients[names[i]]['nutrients']['CP'] for i in range(len(names)))
            actual_me = sum(res.x[i] * self.ingredients[names[i]]['nutrients']['ME'] for i in range(len(names)))
            output += "------------------------------------------\n"
            output += f"📊 التحليل المتوقع: بروتين {round(actual_cp, 2)}% | طاقة {round(actual_me, 2)}"
            return output
        else:
            return "⚠️ تعذر الوصول لتركيبة تحقق كافة الشروط. جرب تقليل نسبة البروتين المطلوبة أو إضافة مكونات جديدة."
