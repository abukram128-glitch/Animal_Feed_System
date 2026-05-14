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
        
        # مصفوفة القيود (تحويلها من مسواة صارمة إلى حدود دنيا)
        # نستخدم - قبل القيم لتمثيل "أكبر من أو يساوي" في مكتبة scipy
        A_ub = [
            [-self.ingredients[n]['nutrients']['CP'] / 10 for n in names], # بروتين
            [-self.ingredients[n]['nutrients']['ME'] for n in names],      # طاقة
            [-self.ingredients[n]['nutrients']['Ca'] / 10 for n in names], # كالسيوم
            [-self.ingredients[n]['nutrients']['P'] / 10 for n in names],  # فسفور
            [-self.ingredients[n]['nutrients']['Lys'] for n in names],     # ليسين
            [-self.ingredients[n]['nutrients']['Met'] for n in names]      # ميثيونين
        ]
        
        b_ub = [-req_cp, -req_me, -req_ca, -req_p, -req_lys, -req_met]
        
        # قيد واحد صارم: مجموع المكونات يجب أن يساوي 100%
        A_eq = [[1 for _ in names]]
        b_eq = [1]
        
        bounds = [(0, 1) for _ in names]
        
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            result_text = "✅ التركيبة المثالية المكتشفة:\n"
            for i, val in enumerate(res.x):
                if val > 0.001:
                    result_text += f"- {names[i]}: {round(val*100, 2)}%\n"
            return result_text
        else:
            return "❌ تعذر إيجاد حل. السبب محتمل: المكونات المختارة لا تكفي لتحقيق نسب البروتين أو الأحماض المطلوبة. حاول إضافة مركزات أو أحماض مصنعة."
