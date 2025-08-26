import numpy as np
import pandas as pd

# ================================
# 🧠 محرك محاكاة مسارات الاستنارة
# ================================
class EnlightenmentSimulator:
    def __init__(self, psi_score: float, iepi_score: float, intervention: str = None):
        """
        :param psi_score: مؤشر السلام النفسي (0 - 100)
        :param iepi_score: مؤشر البصيرة الداخلية (0 - 100)
        :param intervention: نوع التدخل العلاجي (اختياري)
        """
        self.psi = psi_score
        self.iepi = iepi_score
        self.intervention = intervention

        # تحديد مستويات الاستقرار
        self.states = ["جمود", "انتقال", "تدفق", "جاذبية"]
        self.history = []

    def simulate(self, steps=10):
        """
        تشغيل محاكاة مسارات الاستنارة عبر خطوات زمنية
        """
        psi = self.psi
        iepi = self.iepi

        for step in range(steps):
            # حساب ديناميكية التحول
            psi += np.random.uniform(-3, 3)  # تذبذب طبيعي
            iepi += np.random.uniform(-2, 2)

            # تأثير التدخل العلاجي إن وجد
            if self.intervention:
                if self.intervention == "التأمل":
                    psi += 2
                    iepi += 3
                elif self.intervention == "الامتنان":
                    psi += 1
                    iepi += 2

            # ضبط القيم ضمن النطاق 0 - 100
            psi = np.clip(psi, 0, 100)
            iepi = np.clip(iepi, 0, 100)

            # تحديد الحالة الحالية
            state = self._get_state(psi, iepi)
            self.history.append((step, psi, iepi, state))

        return pd.DataFrame(self.history, columns=["الخطوة", "مؤشر السلام النفسي", "مؤشر البصيرة الداخلية", "الحالة"])

    def _get_state(self, psi, iepi):
        """
        تحديد حالة الفرد النفسية-الروحية بناءً على المؤشرات
        """
        if psi < 40 and iepi < 40:
            return "جمود"       # مقاومة للتغيير
        elif 40 <= psi < 60 or 40 <= iepi < 60:
            return "انتقال"     # حالة انتقالية غير مستقرة
        elif psi >= 60 and iepi >= 60:
            return "تدفق"       # انسجام نفسي وروحي
        else:
            return "جاذبية"     # نقاط استقرار أو انهيار

# ================================
# 🧩 دالة مساعدة لواجهة Streamlit
# ================================
def run_enlightenment_simulation(psi, iepi, intervention=None, steps=12):
    simulator = EnlightenmentSimulator(psi, iepi, intervention)
    return simulator.simulate(steps)
