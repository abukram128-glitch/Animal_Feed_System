import numpy as np
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, ingredients_data):
        self.ingredients = ingredients_data

    def create_formulation(self, requirements, animal_type):
        # استخراج البيانات من المكتبة المحدثة بناءً على صور الجداول
        names = [i['name'] for i in self.ingredients]
        prices = [i['price'] for i in self.ingredients]
        
        # المصفوفات الغذائية (بروتين، طاقة، كالسيوم، فسفور)
        cp_matrix = [i['nutrients']['CP'] for i in self.ingredients]
        me_matrix = [i['nutrients']['ME'] for i in self.ingredients]
        ca_matrix = [i['nutrients']['Ca'] for i in self.ingredients]
        p_matrix = [i['nutrients']['P'] for i in self.ingredients]

        # القيود (Constraints)
        A_eq = [[1] * len(names)]
        b_eq = [1] # المجموع الكلي 100% (أو 1 كجم)

        A_ub = [
            [-x for x in cp_matrix], # الحد الأدنى للبروتين
            [-x for x in me_matrix], # الحد الأدنى للطاقة
            [x for x in ca_matrix],  # الحد الأعلى للكالسيوم
            [x for x in p_matrix]    # الحد الأعلى للفسفور
        ]
        b_ub = [-requirements['cp'], -requirements['me'], requirements['ca'], requirements['p']]

        # قيود الأمان العلمية (مستخلصة من الجداول 4، 5، 6)
        bounds = []
        for name in names:
            if "حجر جيري" in name:
                # للمجترات لا يتجاوز 1.5%، للدواجن البياض يصل لـ 8%
                limit = 0.08 if "بياض" in animal_type else 0.015
                bounds.append((0, limit))
            elif "ملح" in name:
                bounds.append((0, 0.005)) # ملح الطعام لا يتجاوز 0.5%
            else:
                bounds.append((0, 1))

        # حل المعادلة (أقل تكلفة)
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        return res
