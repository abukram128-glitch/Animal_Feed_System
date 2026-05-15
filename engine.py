import json
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, db_path):
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.ingredients = {i['name']: i for i in data['ingredients']}
        except:
            # قاعدة بيانات احتياطية في حال فقدان الملف
            self.ingredients = {
                "ذرة صفراء": {"nutrients": {"CP": 8.5, "ME": 3350, "Ca": 0.02, "P": 0.28}, "price": 400},
                "كسب صويا 44%": {"nutrients": {"CP": 44.0, "ME": 2230, "Ca": 0.29, "P": 0.65}, "price": 800},
                "مركزات": {"nutrients": {"CP": 40.0, "ME": 2100, "Ca": 8.0, "P": 4.0}, "price": 1200},
                "حجر جيري": {"nutrients": {"CP": 0, "ME": 0, "Ca": 38.0, "P": 0}, "price": 50}
            }

    def solve(self, req_cp, req_me, req_ca, req_p, animal_type):
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
        
        # القيود الفنية المهنية
        bounds = []
        for n in names:
            if animal_type == "poultry":
                if "حجر جيري" in n: bounds.append((0.01, 0.12))
                elif "ذرة" in n: bounds.append((0.50, 0.75))
                else: bounds.append((0, 1))
            else:
                if "حجر جيري" in n: bounds.append((0, 0.02))
                elif "ذرة" in n: bounds.append((0.30, 0.65))
                else: bounds.append((0, 1))
                
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = f"✅ التركيبة المثالية المعتمدة لـ {animal_type}:\n"
            for i, val in enumerate(res.x):
                if val > 0.001:
                    output += f"- {names[i]}: {round(val*100, 2)}%\n"
            return output
        return "❌ لا يوجد حل كيميائي مطابق، يرجى مراجعة المكونات."
