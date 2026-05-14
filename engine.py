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
        
        # مصفوفة المعايير الستة + شرط مجموع النسب 100%
        A_eq = [
            [self.ingredients[n]['nutrients']['CP'] / 1000 for n in names],
            [self.ingredients[n]['nutrients']['ME'] for n in names],
            [self.ingredients[n]['nutrients']['Ca'] / 1000 for n in names],
            [self.ingredients[n]['nutrients']['P'] / 1000 for n in names],
            [self.ingredients[n]['nutrients']['Lys'] / 100 for n in names],
            [self.ingredients[n]['nutrients']['Met'] / 100 for n in names],
            [1 for _ in names]
        ]
        
        b_eq = [req_cp/100, req_me, req_ca/100, req_p/100, req_lys/100, req_met/100, 1]
        bounds = [(0, 1) for _ in names]
        
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            result_text = "التركيبة المقترحة:\n"
            for i, val in enumerate(res.x):
                if val > 0.001:
                    result_text += f"- {names[i]}: {round(val*100, 2)}%\n"
            return result_text
        else:
            return "⚠️ لم يتم العثور على حل دقيق. حاول تعديل النسب قليلاً."
