import json
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.ingredients = {i['name']: i for i in data['ingredients']}
        except: self.ingredients = {}

    def solve(self, req_cp, req_me, req_ca, req_p, req_lys, req_met, animal_type):
        if not self.ingredients: return "❌ خطأ في قاعدة البيانات"
        
        names = list(self.ingredients.keys())
        prices = [self.ingredients[n].get('price', 1) for n in names]
        
        A_ub = [
            [-self.ingredients[n]['nutrients']['CP'] for n in names],
            [-self.ingredients[n]['nutrients']['ME'] for n in names],
            [-self.ingredients[n]['nutrients']['Ca'] for n in names],
            [-self.ingredients[n]['nutrients']['P'] for n in names]
        ]
        b_ub = [-req_cp, -req_me, -req_ca, -req_p]
        
        A_eq, b_eq = [[1 for _ in names]], [1]
        
        # القيود المهنية المتغيرة حسب النوع
        bounds = []
        for n in names:
            if animal_type == "poultry":
                if "ذرة" in n: bounds.append((0.50, 0.70))
                elif "حجر جيري" in n: bounds.append((0.01, 0.10))
                else: bounds.append((0, 1.0))
            else: # خيل ومجترات
                if "حجر جيري" in n: bounds.append((0, 0.02))
                elif "ذرة" in n: bounds.append((0.30, 0.60))
                else: bounds.append((0, 1.0))
                
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = f"✅ تركيبة مثالية لـ {animal_type}:\n"
            for i, val in enumerate(res.x):
                if val > 0.001: output += f"- {names[i]}: {round(val*100, 2)}%\n"
            return output
        return "❌ لم يتم العثور على حل مطابق للمواصفات."
