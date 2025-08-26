import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import tempfile
import os
from pathlib import Path
from core.dynamics.dynamic_balance_map import generate_smart_balance_map

st.subheader("🌿 خريطة التوازن الديناميكية الذكية")
if st.button("🔍 عرض الخريطة"):
    st.info("⏳ جارٍ إنشاء الخريطة...")
    fig = generate_smart_balance_map(user_scores)
    st.plotly_chart(fig, use_container_width=True)

# --------- CORE MODULES ---------
from core.config import load_config
from core.questionnaire import load_questionnaire, default_scores
from core.scoring.indices import balance_index
from core.dynamics.ode_models import simple_emotion_model
from core.dynamics.simulators import euler_integrate, vector_field
from core.graph.builder import graph_from_config
from core.graph.laplacian import laplacian_smoothing
from core.graph.metrics import degree_centrality
from core.explain.attribution import explain_summary
from core.guidance.rules import merge_rules, recommend_for_scores
from core.guidance.planner import build_daily_plan, build_weekly_plan
from core.storage.db import init_db
from core.storage.repository import (
    save_session,
    save_recommendations,
    save_plan,
    list_sessions,
    get_recommendations,
    get_plan,
)
from core.features.text_features import analyze_text
from core.features.audio_features import analyze_audio
from core.features.signal_features import analyze_wearable_signals

# --------- إعداد واجهة التطبيق ---------
st.set_page_config(
    page_title="هندسة البصيرة – Insight Engineering",
    layout="wide",
    initial_sidebar_state="expanded"
)

cfg = load_config()
q = load_questionnaire()
facets = q["facets"]
defaults = default_scores(facets, q["default_score"])

# ==========================================================
# العنوان الرئيسي
# ==========================================================
st.title(f"{cfg.title_ar} – {cfg.title_en}")
st.caption("لوحة هندسة البصيرة – التقييم، التحليل، التفسير، والتوصيات.")

# ==========================================================
# تبويبات رئيسية لواجهة الاستخدام
# ==========================================================
tabs = st.tabs([
    "📊 تقييم الاتزان النفسي-الروحي",
    "📈 تصور ديناميكيات المشاعر",
    "🕸️ شبكة العلاقات والمركزية",
    "💡 التفسير والتوصيات",
    "💾 الجلسات المحفوظة",
    "📝 تحليل النصوص والملاحظات",
    "🎙️ تحليل الصوت",
    "⌚ إشارات الأجهزة القابلة للارتداء"
])

# ==========================================================
# 1. تبويب التقييم والرادار
# ==========================================================
with tabs[0]:
    st.subheader("أدخل درجاتك")
    cols = st.columns(3)
    values = {}
    for i, f in enumerate(facets):
        with cols[i % 3]:
            values[f] = st.slider(f, 0, 100, int(defaults[f]))

    idx, s_norm = balance_index(values)
    st.metric("Spiritual-Psychological Balance Index", f"{idx}/100")

    # رسم الرادار
    angles = np.linspace(0, 2*np.pi, len(facets), endpoint=False)
    scores = np.array([s_norm[f] for f in facets], dtype=float)
    scores_closed = np.concatenate((scores, [scores[0]]))
    angles_closed = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(5,5))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles_closed, scores_closed, color="blue")
    ax.fill(angles_closed, scores_closed, alpha=0.2, color="cyan")
    ax.set_thetagrids(angles * 180/np.pi, facets)
    ax.set_rlabel_position(0)
    st.pyplot(fig)

# ==========================================================
# 2. تبويب ديناميكيات المشاعر
# ==========================================================
with tabs[1]:
    st.subheader("Emotion-State Dynamics (Phase Portrait)")

    f = simple_emotion_model()
    X, Y, dX, dY = vector_field(f, x_range=(-2,2), y_range=(-2,2), density=20)

    fig3, ax3 = plt.subplots(figsize=(5,5))
    ax3.streamplot(X, Y, dX, dY, density=1.0, color="purple", linewidth=1)
    ax3.set_xlabel("Calm ↔ Tension (x)")
    ax3.set_ylabel("Clarity ↔ Confusion (y)")
    ax3.set_title("Emotion-State Dynamics")

    traj = euler_integrate(f, x0=(1.2, 0.2), t_span=(0, 20), steps=300)
    ax3.plot(traj[:,0], traj[:,1], "r-", lw=2, label="Trajectory")
    ax3.legend()
    st.pyplot(fig3)

# ==========================================================
# 3. تبويب شبكة العلاقات
# ==========================================================
with tabs[2]:
    st.subheader("Insight Graph")

    G = graph_from_config()
    smoothed = laplacian_smoothing(G, s_norm, p=2.0, alpha=0.3, iterations=10)

    fig2, ax2 = plt.subplots(figsize=(5,5))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(
        G, pos,
        node_size=[smoothed[n]*5 for n in G.nodes()],
        node_color="skyblue", ax=ax2
    )
    nx.draw_networkx_edges(G, pos, width=[G[u][v].get("weight",1.0) for u,v in G.edges()], ax=ax2)
    nx.draw_networkx_labels(G, pos, ax=ax2)
    st.pyplot(fig2)

# ==========================================================
# 4. تبويب التفسير والتوصيات
# ==========================================================
with tabs[3]:
    st.subheader("Explainability & Guidance")

    ex = explain_summary(s_norm, baseline=70.0, weights=None, top_k=3)
    st.write("**Summary:**", ex["summary"])
    with st.expander("Show contributions (%)"):
        st.json({k: round(v,2) for k,v in ex["contributions_pct"].items()})

    G2 = graph_from_config()
    cent = degree_centrality(G2)
    recs = recommend_for_scores(s_norm, k=3, rules=merge_rules(), centrality=cent)

    st.markdown("### Recommendations")
    for r in recs:
        st.markdown(f"- **{r.facet}** (priority {r.priority})")
        for t in r.tips:
            st.markdown(f"  - {t}")

    day_plan = build_daily_plan(recs, minutes_per_day=30)
    st.markdown("### Daily Plan")
    for it in day_plan:
        st.markdown(f"- **{it.facet}** — {it.minutes} min: {it.action}")

    week_plan = build_weekly_plan(recs)
    with st.expander("Weekly Plan"):
        for day, items in week_plan.items():
            st.markdown(f"**{day}**")
            if not items:
                st.write("· Rest / Review")
            for it in items:
                st.markdown(f"  - {it.facet}: {it.minutes} min — {it.action}")

# ==========================================================
# 5. تبويب الجلسات المحفوظة
# ==========================================================
with tabs[4]:
    st.subheader("📂 Saved Sessions")
    init_db()

    if st.button("💾 Save Session"):
        sid = save_session("demo_user", idx, s_norm)
        save_recommendations(
            sid,
            [{"facet": r.facet, "priority": r.priority, "tips": r.tips} for r in recs],
        )
        save_plan(sid, "daily", [it.__dict__ for it in day_plan])
        save_plan(sid, "weekly", {day: [it.__dict__ for it in items] for day, items in week_plan.items()})
        st.success(f"Session {sid} saved!")

    with st.expander("📂 Show Saved Sessions"):
        sessions = list_sessions(limit=5)
        for s in sessions:
            st.write(f"**ID {s['id']}** | {s['created_at']} | Score: {s['balance_index']}")
            st.json(s["scores"])
            recs_saved = get_recommendations(s["id"])
            if recs_saved:
                st.markdown("*Recommendations:*")
                for r in recs_saved:
                    st.write(f"- {r['facet']} ({r['priority']}): {', '.join(r['tips'])}")

# ==========================================================
# 6. تبويب تحليل النصوص
# ==========================================================
with tabs[5]:
    st.subheader("Analyze Your Notes")
    user_text = st.text_area("اكتب ملاحظاتك أو شعورك الحالي هنا:")

    if st.button("🔍 Analyze Text"):
        analysis = analyze_text(user_text)
        st.json(analysis)
        if analysis["sentiment_score"] > 0:
            st.success("مزاجك يميل إلى الإيجابية 🌿")
        elif analysis["sentiment_score"] < 0:
            st.warning("هناك بعض المشاعر السلبية 😔")
        else:
            st.info("مزاجك متوازن حاليًا ⚖️")

# ==========================================================
# 7. تبويب تحليل الصوت
# ==========================================================
with tabs[6]:
    st.subheader("🎙️ Analyze Your Voice")
    uploaded_audio = st.file_uploader("ارفع تسجيلًا صوتيًا", type=["wav", "mp3"])

    if uploaded_audio is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_audio.read())
            tmp_path = tmp.name

        analysis = analyze_audio(tmp_path)
        st.json(analysis)

        if "error" not in analysis:
            stress = analysis["stress_index"]
            if stress < 30:
                st.success("مؤشر التوتر منخفض 🌿")
            elif stress < 70:
                st.warning("مؤشر التوتر متوسط 😌")
            else:
                st.error("مؤشر التوتر مرتفع 🧘‍♂️")

        os.unlink(tmp_path)

# ==========================================================
# 8. تبويب إشارات الأجهزة القابلة للارتداء
# ==========================================================
with tabs[7]:
    st.subheader("⌚ Analyze Wearable Device Signals")

    with st.expander("أدخل بيانات الجهاز القابل للارتداء يدويًا:"):
        col1, col2 = st.columns(2)
        hr = col1.number_input("معدل ضربات القلب (BPM)", min_value=30, max_value=180, value=72)
        hrv = col2.number_input("تباين معدل ضربات القلب HRV (ms)", min_value=0, max_value=200, value=55)

        col3, col4 = st.columns(2)
        sleep_score = col3.number_input("جودة النوم (0-100)", min_value=0, max_value=100, value=80)
        activity_score = col4.number_input("النشاط البدني (0-100)", min_value=0, max_value=100, value=65)

        stress_score = st.slider("مؤشر التوتر من الجهاز (0-100)", min_value=0, max_value=100, value=30)

    if st.button("🔍 Analyze Wearable Data"):
        signals_data = {
            "hr": hr,
            "hrv": hrv,
            "sleep_score": sleep_score,
            "activity_score": activity_score,
            "stress_score": stress_score
        }
        analysis = analyze_wearable_signals(signals_data)
        st.json(analysis)

        if analysis["overall_health_index"] is not None:
            st.metric("🧠 Overall Health Index", f"{analysis['overall_health_index']}/100")
