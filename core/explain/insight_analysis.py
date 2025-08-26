import numpy as np

# 🧠 تحليل نصوص نفسي وروحي بسيط (مكان الذكاء الاصطناعي لاحقاً)
def analyze_psychospiritual_state(user_text: str):
    # تقسيم النص لكلمات
    words = user_text.lower().split()

    # مؤشرات نفسية أساسية
    categories_psi = ["Mind", "Heart", "Body", "Spirit", "Relations", "Work"]
    categories_iepi = ["Faith", "Intention", "Worship", "Remembrance", "Morality", "Knowledge", "Balance", "Community"]

    # تحليل بدائي (placeholder) - لاحقاً سنستبدله بنموذج ذكاء اصطناعي
    psi_scores = np.random.randint(40, 90, size=len(categories_psi))  # قيم تقريبية مؤقتة
    iepi_scores = np.random.randint(50, 95, size=len(categories_iepi))  # قيم تقريبية مؤقتة

    return categories_psi, psi_scores, categories_iepi, iepi_scores
