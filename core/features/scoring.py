from typing import Dict, Tuple

# ------------------------------
# أدوات مساعدة
# ------------------------------
def _clamp_0_100(x: float) -> float:
    """تقييد القيمة بين 0 و 100"""
    return max(0.0, min(100.0, float(x)))

def _weighted_score(values: Dict[str, float], weights: Dict[str, float]) -> float:
    """حساب المجموع المرجح"""
    return sum(_clamp_0_100(values[k]) * weights[k] for k in weights)

def _interpret_band(score: float) -> Tuple[str, str]:
    """تفسير النتيجة وتحويلها إلى مستوى نصي"""
    if score < 50:
        return "منخفض", "⚠️ هناك فجوات كبيرة تحتاج تدخلًا عاجلًا."
    elif score < 70:
        return "متوسط", "🔹 هناك بعض التوازن لكن تحتاج تعزيز محاور محددة."
    elif score < 85:
        return "جيّد", "✅ توازن مقبول وتحسن ملحوظ — استمر ووسع الممارسات الإيجابية."
    else:
        return "ممتاز", "🌟 انسجام عالٍ بين الجوانب النفسية والروحية."

# ------------------------------
# المؤشر العام PSI
# ------------------------------
def calculate_psi(mind: float, heart: float, body: float, spirit: float,
                  relations: float, work: float) -> float:
    """حساب المؤشر النفسي الروحي العام"""
    weights = {
        "mind": 0.25, "heart": 0.20, "body": 0.15,
        "spirit": 0.20, "relations": 0.10, "work": 0.10
    }
    vals = {
        "mind": mind, "heart": heart, "body": body,
        "spirit": spirit, "relations": relations, "work": work
    }
    psi_score = _weighted_score(vals, weights)
    return round(psi_score, 2)

# ------------------------------
# مؤشر الاستنارة الإسلامي IEPI
# ------------------------------
def calculate_iepi(iman: float, niyyah: float, ibadah: float, dhikr: float,
                   akhlaq: float, ilm: float, mizan: float, ummah: float) -> float:
    """حساب مؤشر الاستنارة الإسلامي"""
    weights = {
        "iman": 0.20, "niyyah": 0.15, "ibadah": 0.15, "dhikr": 0.10,
        "akhlaq": 0.15, "ilm": 0.10, "mizan": 0.10, "ummah": 0.05
    }
    vals = {
        "iman": iman, "niyyah": niyyah, "ibadah": ibadah, "dhikr": dhikr,
        "akhlaq": akhlaq, "ilm": ilm, "mizan": mizan, "ummah": ummah
    }
    score = _weighted_score(vals, weights)
    return round(score, 2)

def iepi_profile_report(iman: float, niyyah: float, ibadah: float, dhikr: float,
                        akhlaq: float, ilm: float, mizan: float, ummah: float) -> Dict[str, object]:
    """إرجاع تقرير شامل لمؤشر الاستنارة"""
    score = calculate_iepi(iman, niyyah, ibadah, dhikr, akhlaq, ilm, mizan, ummah)
    level, summary = _interpret_band(score)

    # التوصيات للمحاور الضعيفة
    threshold = 70.0
    tips: Dict[str, str] = {}

    def add_tip(name: str, val: float, text: str):
        if _clamp_0_100(val) < threshold:
            tips[name] = text

    add_tip("الإيمان", iman, "ثبّت المعنى عبر التدبر اليومي ودعاء التوكّل.")
    add_tip("النية", niyyah, "جدّد النية قبل الأعمال وحدد هدفًا واضحًا.")
    add_tip("العبادة", ibadah, "خطط ثابتة للفرائض والسنن مع تتبع أسبوعي.")
    add_tip("الذكر/اليقظة", dhikr, "مارس جلسة ذكر وتأمل 10 دقائق يوميًا.")
    add_tip("الأخلاق", akhlaq, "ركز على خلق واحد أسبوعيًا (كالصدق/الحلم).")
    add_tip("العلم", ilm, "اقرأ يوميًا 15 دقيقة مع تطبيق معرفي بسيط.")
    add_tip("التوازن", mizan, "جدول وقتك بين نفسك وأسرتك وعملك وروحك.")
    add_tip("المجتمع", ummah, "خصص ساعة أسبوعيًا لخدمة المجتمع.")

    return {
        "score": score,
        "level": level,
        "summary": summary,
        "improvement_tips": tips
    }
