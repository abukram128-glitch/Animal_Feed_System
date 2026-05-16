# filename: engine.py
import numpy as np
from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self, ingredients_data):
        self.ingredients = ingredients_data

    def create_formulation(self, requirements, animal_type):
        names = [i['name'] for i in self.ingredients]
        prices = [i['price'] for i in self.ingredients]
        
        cp_matrix  = [i['nutrients']['CP'] for i in self.ingredients]
        me_matrix  = [i['nutrients']['ME'] for i in self.ingredients]
        ca_matrix  = [i['nutrients']['Ca'] for i in self.ingredients]
        p_matrix   = [i['nutrients']['P'] for i in self.ingredients]
        lys_matrix = [i['nutrients']['Lys'] for i in self.ingredients]
        met_matrix = [i['nutrients']['Met'] for i in self.ingredients]

        A_eq = [[1] * len(names)]
        b_eq = [100.0] 

        A_ub = [
            [-x for x in cp_matrix],
            [-x for x in me_matrix],
            [-x for x in ca_matrix],
            [x for x in ca_matrix],
            [-x for x in p_matrix],
            [x for x in p_matrix],
            [-x for x in lys_matrix],
            [-x for x in met_matrix]
        ]
        
        b_ub = [
            -requirements['cp_min'],
            -requirements['me_min'],
            -requirements['ca_min'],
            requirements['ca_max'],
            -requirements['p_min'],
            requirements['p_max'],
            -requirements['lys_min'],
            -requirements['met_min']
        ]

        bounds = []
        for name in names:
            if "حجر جيري" in name:
                max_limit = 9.0 if "بياض" in animal_type else 1.2
                bounds.append((0, max_limit))
            elif "مسحوق سمك" in name:
                bounds.append((0, 5.0))   
            elif "عباد الشمس" in name:
                bounds.append((0, 15.0))  
            elif "نخالة" in name or "برسيم" in name:
                max_fiber_ing = 5.0 if "دواجن" in animal_type else 40.0
                bounds.append((0, max_fiber_ing))
            else:
                bounds.append((0, 100.0))

        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if res.success:
            formulation = {names[i]: round(res.x[i], 2) for i in range(len(names)) if res.x[i] > 0.01}
            actual_nutrients = {
                "CP": round(sum(res.x[i] * cp_matrix[i] for i in range(len(names))) / 100, 2),
                "ME": round(sum(res.x[i] * me_matrix[i] for i in range(len(names))), 0),
                "Ca": round(sum(res.x[i] * ca_matrix[i] for i in range(len(names))) / 100, 3),
                "P":  round(sum(res.x[i] * p_matrix[i] for i in range(len(names))) / 100, 3),
                "Lys": round(sum(res.x[i] * lys_matrix[i] for i in range(len(names))) / 100, 3),
                "Met": round(sum(res.x[i] * met_matrix[i] for i in range(len(names))) / 100, 3)
            }
            return {
                "Status": "Success",
                "Cost_per_100kg": round(res.fun, 2),
                "Formulation_Percentage": formulation,
                "Actual_Nutritional_Profile": actual_nutrients
            }
        else:
            return {"Status": "Failed", "Message": f"Infeasible solution: {res.message}"}
