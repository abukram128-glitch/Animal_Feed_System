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

    def solve(self, req_cp, req_me, req_ca, req_p, animal_type):
        if not self.ingredients: return "❌ قاعدة البيانات غير متوفرة"
        
        names = list(self.ingredients.keys())
        prices = [self.ingredients[n].get('price', 1) for n in names]
        
        # مصفوفة القيود
        A_ub = [
            [-self.ingredients[n]['nutrients']['CP'] for n in names],
            [-self.ingredients[n]['nutrients']['ME'] for n in names],
            [-self.ingredients[n]['nutrients']['Ca'] for n in names],
            [-self.ingredients[n]['nutrients']['P'] for n in names]
        ]
        b_ub = [-req_cp, -req_me, -req_ca, -req_p]
        
        # قيد المجموع 100%
        A_eq, b_eq = [[1 for _ in names]], [1]
        
        # حدود مهنية (تمنع الحجر الجيري العالي الظاهر في صورك)
        bounds = []
        for n in names:
            if animal_type == "poultry":
                if "حجر جيري" in n: bounds.append((0.01, 0.10))
                else: bounds.append((0, 1))
            else:
                if "حجر جيري" in n: bounds.append((0, 0.02))
                else: bounds.append((0, 1))
                
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = f"✅ التركيبة المعتمدة لـ {animal_type}:\n"
            for i, val in enumerate(res.x):
                if val > 0.001:
                    output += f"- {names[i]}: {round(val*100, 2)}%\n"
            return output
        return "❌ لا توجد تركيبة تحقق هذه الشروط، جرب تعديل المدخلات."
