import json
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.ingredients = {i['name']: i for i in data['ingredients']}

    def solve(self, req_cp, req_me, req_ca, req_p, req_lys, req_met):
        names = list(self.ingredients.keys())
        prices = [self.ingredients[n].get('price', 1) for n in names]
        
        # القيود الغذائية
        A_ub = [
            [-self.ingredients[n]['nutrients']['CP'] for n in names],
            [-self.ingredients[n]['nutrients']['ME'] for n in names],
            [-self.ingredients[n]['nutrients']['Ca'] for n in names],
            [-self.ingredients[n]['nutrients']['P'] for n in names],
            [-self.ingredients[n]['nutrients']['Lys'] for n in names],
            [-self.ingredients[n]['nutrients']['Met'] for n in names]
        ]
        b_ub = [-req_cp, -req_me, -req_ca, -req_p, -req_lys, -req_met]
        
        # قيد المجموع 100%
        A_eq = [[1 for _ in names]]
        b_eq = [1]
        
        # حدود استهلاك المواد (مثلاً المركز لا يزيد عن 10%)
        bounds = []
        for n in names:
            if "مركز" in n: bounds.append((0, 0.10)) # حد أقصى للمركز 10%
            else: bounds.append((0, 1))
            
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = "✅ التركيبة المقترحة (النسب المئوية):\n"
            for i, val in enumerate(res.x):
                if val > 0.001:
                    output += f"- {names[i]}: {round(val*100, 2)}%\n"
            return output
        return "❌ لم يتم العثور على تركيبة اقتصادية تحقق هذه الشروط."
