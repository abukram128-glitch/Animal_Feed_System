import pandas as pd
from scipy.optimize import linprog
import json

class SmartFeedEngine:
    def __init__(self, db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.ingredients = {i['name']: i for i in data['ingredients']}

    def solve(self, req_cp, req_me, req_ca, req_p, req_lys, req_met):
        names = list(self.ingredients.keys())
        c = [self.ingredients[n].get('price', 1) for n in names]
        
        A_ub = []
        A_ub.append([-self.ingredients[n]['nutrients']['CP'] / (10 if self.ingredients[n]['nutrients']['CP'] > 100 else 1) for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['ME'] for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['Ca'] / (10 if self.ingredients[n]['nutrients']['Ca'] > 100 else 1) for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['P'] / (10 if self.ingredients[n]['nutrients']['P'] > 100 else 1) for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['Lys'] for n in names])
        A_ub.append([-self.ingredients[n]['nutrients']['Met'] for n in names])
        
        b_ub = [-req_cp, -req_me, -req_ca, -req_p, -req_lys, -req_met]
        A_eq = [[1 for _ in names]]
        b_eq = [1]
        bounds = [(0, 1) for _ in names]
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            result_text = "✅ تم إيجاد التركيبة المثالية:\n"
            for i, val in enumerate(res.x):
                if val > 0.001:
                    result_text += f"- {names[i]}: {round(val*100, 2)}%\n"
            return result_text
        else:
            return "⚠️ تعذر إيجاد حل. حاول إضافة مكونات إضافية مثل المركزات أو تقليل القيود."
