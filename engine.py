import json
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.ingredients = {i['name']: i for i in data['ingredients']}

    def solve(self, selected_feeds, prices, reqs, animal_type):
        # تحديد مفتاح الطاقة بناءً على نوع الحيوان
        energy_key = {'مجترات': 'ME_R', 'دواجن': 'ME_P', 'خيل': 'DE_H'}[animal_type]
        
        c = [prices[name] for name in selected_feeds]
        
        # مصفوفة القيود: بروتين، طاقة، كالسيوم، فسفور
        A_ub = [
            [-self.ingredients[name]['nutrients']['CP'] for name in selected_feeds],
            [-self.ingredients[name]['nutrients'][energy_key] for name in selected_feeds],
            [-self.ingredients[name]['nutrients']['Ca'] for name in selected_feeds],
            [-self.ingredients[name]['nutrients']['P'] for name in selected_feeds]
        ]
        b_ub = [-reqs['CP'], -reqs['Energy'], -reqs['Ca'], -reqs['P']]
        
        A_eq = [[1] * len(selected_feeds)]
        b_eq = [1]
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='highs')
        return res
