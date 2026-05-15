from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self):
        # قاعدة بيانات داخلية ثابتة لتفادي أخطاء الملفات المفقودة
        self.ingredients = {
            "ذرة صفراء": {"nutrients": {"CP": 8.5, "ME": 3350, "Ca": 0.02, "P": 0.28}, "price": 400},
            "ذرة بيضاء": {"nutrients": {"CP": 9.0, "ME": 3250, "Ca": 0.03, "P": 0.30}, "price": 380},
            "شعير": {"nutrients": {"CP": 11.5, "ME": 2900, "Ca": 0.06, "P": 0.35}, "price": 420},
            "كسب صويا 44%": {"nutrients": {"CP": 44.0, "ME": 2230, "Ca": 0.29, "P": 0.65}, "price": 850},
            "نخالة قمح": {"nutrients": {"CP": 15.0, "ME": 1300, "Ca": 0.10, "P": 0.90}, "price": 320},
            "برسيم جاف": {"nutrients": {"CP": 16.0, "ME": 2000, "Ca": 1.40, "P": 0.22}, "price": 450},
            "مركزات": {"nutrients": {"CP": 40.0, "ME": 2100, "Ca": 8.0, "P": 4.0}, "price": 1200},
            "حجر جيري": {"nutrients": {"CP": 0, "ME": 0, "Ca": 38.0, "P": 0}, "price": 50}
        }

    def solve(self, req_cp, req_me, req_ca, req_p, animal_type):
        names = list(self.ingredients.keys())
        prices = [self.ingredients[n].get('price', 1) for n in names]
        
        # قيود الاحتياجات الغذائية
        A_ub = [
            [-self.ingredients[n]['nutrients']['CP'] for n in names],
            [-self.ingredients[n]['nutrients']['ME'] for n in names],
            [-self.ingredients[n]['nutrients']['Ca'] for n in names],
            [-self.ingredients[n]['nutrients']['P'] for n in names]
        ]
        b_ub = [-req_cp, -req_me, -req_ca, -req_p]
        A_eq, b_eq = [[1 for _ in names]], [1]
        
        # --- القيود الفنية الصارمة لمنع نسبة الـ 59% حجر جيري ---
        bounds = []
        for n in names:
            if "حجر جيري" in n:
                # حد أقصى 2% للأبقار و10% لدجاج البيض
                max_lim = 0.10 if animal_type == "poultry" else 0.02
                bounds.append((0.005, max_lim))
            elif "نخالة" in n or "برسيم" in n:
                # إجبار وجود ألياف للمجترات والخيل
                min_lim = 0.15 if animal_type in ["ruminant", "horse"] else 0
                bounds.append((min_lim, 0.50))
            else:
                bounds.append((0, 1))
                
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = "✅ التركيبة العلمية المقترحة:\n"
            for i, val in enumerate(res.x):
                if val > 0.001: output += f"- {names[i]}: {round(val*100, 2)}%\n"
            return output
        return "❌ فشل النظام في إيجاد تركيبة متوازنة، يرجى تعديل الأهداف."
