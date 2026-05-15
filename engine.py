import json
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.ingredients = {i['name']: i for i in data['ingredients']}
        except:
            self.ingredients = {}

    def solve(self, req_cp, req_me, req_ca, req_p, req_lys, req_met):
        if not self.ingredients:
            return "❌ خطأ في قراءة ملف feeds_db.json"

        names = list(self.ingredients.keys())
        prices = [self.ingredients[n].get('price', 1) for n in names]
        
        # مصفوفة القيود الكيميائية
        A_ub = [
            [-self.ingredients[n]['nutrients']['CP'] for n in names],
            [-self.ingredients[n]['nutrients']['ME'] for n in names],
            [-self.ingredients[n]['nutrients']['Ca'] for n in names],
            [-self.ingredients[n]['nutrients']['P'] for n in names],
            [-self.ingredients[n]['nutrients']['Lys'] for n in names],
            [-self.ingredients[n]['nutrients']['Met'] for n in names]
        ]
        b_ub = [-req_cp, -req_me, -req_ca, -req_p, -req_lys, -req_met]
        
        A_eq = [[1 for _ in names]]
        b_eq = [1]
        
        # القيود الفنية المهنية
        bounds = []
        for n in names:
            if "حجر جيري" in n: bounds.append((0, 0.02))
            elif "مركز" in n: bounds.append((0, 0.10))
            elif "ذرة" in n: bounds.append((0.40, 0.85))
            elif "ملح" in n: bounds.append((0, 0.005))
            else: bounds.append((0, 1.0))
            
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = "✅ تم حساب التركيبة المركزية المثالية:\n"
            for i, val in enumerate(res.x):
                if val > 0.001:
                    output += f"- {names[i]}: {round(val*100, 2)}%\n"
            return output
        return "❌ تعذر إيجاد حل يحقق هذه القيود الفنية."

    def generate_feeding_schedule(self, total_dm, conc_percent, premix_grams):
        # حساب المادة الجافة للمركز والمالئة
        conc_dm = total_dm * (conc_percent / 100)
        roughage_dm = total_dm - conc_dm
        
        # التحويل لمادة مغذاه (As Fed) برطوبة 10%
        conc_as_fed = conc_dm / 0.9
        roughage_as_fed = roughage_dm / 0.9
        
        return f"""
        ---
        ### 📋 البرنامج التغذوي اليومي (للرأس الواحد)
        * **العليقة المالئة (تبن/برسيم):** {round(roughage_as_fed, 2)} كجم
        * **العليقة المركزية:** {round(conc_as_fed, 2)} كجم
        * **العليقة المصححة (Premix):** {premix_grams} جرام
        
        ⚠️ **تعليمات:** يُنصح بتقديم المادة المالئة أولاً ثم المركز لتجنب اضطرابات الهضم.
        """
