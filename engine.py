from scipy.optimize import linprog

class SmartFeedEngine:
    def __init__(self):
        # قاعدة البيانات الشاملة (المكتبة)
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
        
        # مصفوفة القيود الكيميائية
        A_ub = [
            [-self.ingredients[n]['nutrients']['CP'] for n in names],
            [-self.ingredients[n]['nutrients']['ME'] for n in names],
            [-self.ingredients[n]['nutrients']['Ca'] for n in names],
            [-self.ingredients[n]['nutrients']['P'] for n in names]
        ]
        b_ub = [-req_cp, -req_me, -req_ca, -req_p]
        A_eq, b_eq = [[1 for _ in names]], [1]
        
        # --- القيود الفنية المهنية (تعديل حسب الفصيلة) ---
        bounds = []
        for n in names:
            if animal_type == "poultry":
                if "نخالة" in n or "برسيم" in n: bounds.append((0, 0.02)) # الدواجن لا تهضم الألياف
                elif "حجر جيري" in n: bounds.append((0.01, 0.10))
                else: bounds.append((0, 1))
            elif animal_type == "horse":
                if "برسيم" in n: bounds.append((0.20, 0.50)) # الخيل تحتاج برسيم جاف عالي الجودة
                elif "شعير" in n: bounds.append((0.10, 0.30))
                elif "نخالة" in n: bounds.append((0.05, 0.15))
                else: bounds.append((0, 1))
            else: # المجترات (أبقار وأغنام)
                if "نخالة" in n: bounds.append((0.15, 0.40))
                elif "برسيم" in n: bounds.append((0.10, 0.30))
                elif "شعير" in n: bounds.append((0.10, 0.40))
                elif "حجر جيري" in n: bounds.append((0.005, 0.02))
                else: bounds.append((0, 1))
                
        # حل المشكلة برمجياً
        res = linprog(prices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if res.success:
            output = f"✅ التركيبة المعتمدة (م. عبدالقادر):\n"
            for i, val in enumerate(res.x):
                if val > 0.001: 
                    output += f"- {names[i]}: {round(val*100, 2)}%\n"
            return output
        return "❌ الخوارزمية لم تجد حلًا؛ يرجى مراجعة توازن المواد المتاحة."
