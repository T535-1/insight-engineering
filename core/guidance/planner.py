# core/guidance/planner.py
from __future__ import annotations
from typing import List, Dict
from dataclasses import dataclass
from .rules import Recommendation

@dataclass
class PlanItem:
    facet: str
    action: str
    minutes: int

def build_daily_plan(recs: List[Recommendation], minutes_per_day: int = 30) -> List[PlanItem]:
    """
    يبني خطة يومية موزعة على التوصيات حسب الأولوية، بحد زمني إجمالي.
    """
    if not recs:
        return []
    # توزيع بسيط: أكثر أولوية يأخذ دقائق أكثر
    total_priority = sum(r.priority for r in recs) or 1.0
    items: List[PlanItem] = []
    for r in recs:
        share = max(1, int((r.priority / total_priority) * minutes_per_day))
        tip = r.tips[0] if r.tips else "Practice 10 minutes mindfully."
        items.append(PlanItem(facet=r.facet, action=tip, minutes=share))
    # ضبط المجموع إلى السقف
    total = sum(i.minutes for i in items)
    if total > minutes_per_day:
        # قلّص آخر عنصر
        items[-1].minutes = max(1, items[-1].minutes - (total - minutes_per_day))
    return items

def build_weekly_plan(recs: List[Recommendation]) -> Dict[str, List[PlanItem]]:
    """
    يبني خطة أسبوعية بسيطة: يوزّع كل توصية على يومين مختلفين لمرونة التنفيذ.
    """
    if not recs:
        return {}
    weekdays = ["Sat","Sun","Mon","Tue","Wed","Thu","Fri"]
    week: Dict[str, List[PlanItem]] = {d: [] for d in weekdays}
    # ثبّت 20 دقيقة لكل توصية يومين بالأسبوع
    minutes = 20
    day_idx = 0
    for r in recs:
        for _ in range(2):
            day = weekdays[day_idx % len(weekdays)]
            tip = r.tips[_ % len(r.tips)] if r.tips else "Practice 15 minutes mindfully."
            week[day].append(PlanItem(facet=r.facet, action=tip, minutes=minutes))
            day_idx += 1
    return week
