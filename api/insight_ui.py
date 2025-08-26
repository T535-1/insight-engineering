# ==========================================================
# 📌 استيراد المكتبات الأساسية
# ==========================================================
import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# 📌 إضافة المسار للوصول إلى المجلد الأساسي
# ==========================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ==========================================================
# 📌 استيراد الوحدات من المشروع
# ==========================================================
from core.dynamics.dynamic_balance_map import generate_smart_balance_map
from core.questionnaire import load_questionnaire

from core.scoring.indices import balance_index
from core.features.text_features import analyze_text
from core.features.audio_features import analyze_audio
from core.features.scoring import calculate_psi, calculate_iepi

# ==========================================================
# 📌 إعداد صفحة التطبيق (ضروري أن يكون أول استدعاء لـ Streamlit)
# ==========================================================
st.set_page_config(
    page_title="Insight Engineering Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# 🌗 اختيار الثيم (مضيء افتراضي + داكن اختياري)
# ==========================
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # الوضع الافتراضي

col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("<h1 style='text-align:center; font-weight:900;'>🧠 Insight Engineering Dashboard | لوحة هندسة البصيرة</h1>", unsafe_allow_html=True)
with col2:
    if st.button("🌙" if st.session_state.theme == "light" else "☀️", key="toggle_theme"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ==========================
# 🎨 تصميم CSS ديناميكي حسب الثيم
# ==========================
light_mode = """
    body, .stApp {
        background-color: #F7F9FC;
        color: #000;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1f2937;
    }
    .card {
        background-color: #fff;
        padding: 20px;
        margin: 10px;
        border-radius: 15px;
        box-shadow: 5px 5px 15px #d1d5db;
        text-align: center;
        color: #111;
        transition: transform 0.3s ease-in-out;
    }
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #2563EB;
    }
    .stButton>button {
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 45px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1E40AF;
        box-shadow: 0 0 10px #2563EB;
    }
"""

dark_mode = """
    body, .stApp {
        background-color: #0E1117;
        color: #fff;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #fff;
    }
    .card {
        background-color: #1E1E2F;
        padding: 20px;
        margin: 10px;
        border-radius: 15px;
        box-shadow: 5px 5px 15px #00000070;
        text-align: center;
        color: white;
        transition: transform 0.3s ease-in-out;
    }
    .card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #4A90E2;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 45px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        box-shadow: 0 0 10px #4A90E2;
    }
"""

st.markdown(f"<style>{light_mode if st.session_state.theme == 'light' else dark_mode}</style>", unsafe_allow_html=True)
st.markdown("---")

# ==================================================
# 📌 التبويبات الرئيسية (تعريف واحد فقط)
# ==================================================
tabs = st.tabs([
    "🌿 PSI & IEPI",           # التبويب الأول: المؤشرات
    "✍️ Text Analyzer",        # التبويب الثاني: تحليل النصوص
    "🎙️ Audio Analyzer",      # التبويب الثالث: تحليل الصوت
    "📊 Survey Analyzer",      # التبويب الرابع: تحليل ملفات الاستبيان
    "🧠 PSI & IEPI Survey"     # ✅ التبويب الجديد: الاستبيان العميق
])

# ==================================================
# 🟢 التبويب 1: PSI + IEPI
# ==================================================
with tabs[0]:
    st.subheader("✍️ أدخل درجاتك | Enter Your Scores")

    tab1, tab2 = st.tabs(["🌿 المؤشر النفسي-الروحي (PSI)", "🕌 مؤشر الاستنارة الإسلامي (IEPI)"])

    # ----------------- PSI -----------------
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            mind = st.slider("🧠 العقل | Mind", 0, 100, 50)
            heart = st.slider("❤️ القلب | Heart", 0, 100, 50)
        with col2:
            body = st.slider("🏋️ الجسد | Body", 0, 100, 50)
            spirit = st.slider("🕊️ الروح | Spirit", 0, 100, 50)
        with col3:
            relations = st.slider("🤝 العلاقات | Relations", 0, 100, 50)
            work = st.slider("💼 العمل | Work", 0, 100, 50)

        psi_score = calculate_psi(mind, heart, body, spirit, relations, work)

        st.markdown(f"""
            <div class="card">
                <h3>🧩 PSI Score</h3>
                <p style="font-size:26px; color:#2563EB;"><b>{psi_score} / 100</b></p>
            </div>
        """, unsafe_allow_html=True)

        # رسم عدادات تفاعلية لكل مؤشر PSI
        st.markdown("### 🧠 توزيع المؤشرات النفسية (PSI)")
        psi_fig = go.Figure()

        psi_metrics = {
            "Mind": mind, "Heart": heart, "Body": body,
            "Spirit": spirit, "Relations": relations, "Work": work
        }

        # إضافة Gauge لكل مؤشر
        for i, (label, value) in enumerate(psi_metrics.items()):
            psi_fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=value,
                title={'text': label},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2563EB"},
                    'steps': [
                        {'range': [0, 40], 'color': "#FCA5A5"},
                        {'range': [40, 70], 'color': "#FCD34D"},
                        {'range': [70, 100], 'color': "#86EFAC"}
                    ]
                },
                domain={'row': i // 3, 'column': i % 3}
            ))

        psi_fig.update_layout(
            grid={'rows': 2, 'columns': 3, 'pattern': "independent"},
            height=500,
            template="plotly_white" if st.session_state.theme == "light" else "plotly_dark"
        )

        st.plotly_chart(psi_fig, use_container_width=True)

        # مخطط PSI راداري
        categories = ["Mind", "Heart", "Body", "Spirit", "Relations", "Work"]
        values = [mind, heart, body, spirit, relations, work]
        fig_psi = go.Figure(data=go.Scatterpolar(
            r=values, theta=categories,
            fill="toself",
            line=dict(color="#2563EB" if st.session_state.theme == "light" else "#4A90E2", width=3)
        ))
        fig_psi.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                              showlegend=False,
                              template="plotly_white" if st.session_state.theme == "light" else "plotly_dark")
        st.plotly_chart(fig_psi, use_container_width=True)

    # ----------------- IEPI -----------------
    with tab2:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            iman = st.slider("🕋 الإيمان | Faith", 0, 100, 70)
            niyyah = st.slider("🤲 النية | Intention", 0, 100, 70)
        with col2:
            ibadah = st.slider("🕌 العبادة | Worship", 0, 100, 70)
            dhikr = st.slider("📿 الذكر | Remembrance", 0, 100, 70)
        with col3:
            akhlaq = st.slider("🌿 الأخلاق | Morality", 0, 100, 70)
            ilm = st.slider("📚 العلم | Knowledge", 0, 100, 70)
        with col4:
            mizan = st.slider("⚖️ التوازن | Balance", 0, 100, 70)
            ummah = st.slider("🤝 المجتمع | Community", 0, 100, 70)

        iepi_score = calculate_iepi(iman, niyyah, ibadah, dhikr, akhlaq, ilm, mizan, ummah)

        st.markdown(f"""
            <div class="card">
                <h3>🕌 IEPI Score</h3>
                <p style="font-size:26px; color:#22d3ee;"><b>{iepi_score} / 100</b></p>
            </div>
        """, unsafe_allow_html=True)

    # ============================
    # 🔄 مخطط مدمج تفاعلي ديناميكي
    # ============================
    st.subheader("📊 مقارنة PSI و IEPI")
    combined_fig = go.Figure()
    combined_fig.add_trace(go.Scatterpolar(
        r=values, theta=categories,
        fill='toself', name='PSI',
        line=dict(color="#2563EB", width=3)
    ))
    combined_fig.add_trace(go.Scatterpolar(
        r=[iman, niyyah, ibadah, dhikr, akhlaq, ilm, mizan, ummah],
        theta=["Faith", "Intention", "Worship", "Remembrance", "Morality", "Knowledge", "Balance", "Community"],
        fill='toself', name='IEPI',
        line=dict(color="#22d3ee", width=3)
    ))
    combined_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        template="plotly_white" if st.session_state.theme == "light" else "plotly_dark"
    )
    st.plotly_chart(combined_fig, use_container_width=True)
# ============================
# 🕸️ خريطة التوازن الديناميكية
# ============================
st.subheader("🌿 خريطة التوازن الشاملة")
radar_fig = go.Figure()

# دمج جميع المؤشرات في خريطة واحدة
radar_fig.add_trace(go.Scatterpolar(
    r=[mind, heart, body, spirit, relations, work],
    theta=["Mind", "Heart", "Body", "Spirit", "Relations", "Work"],
    fill="toself",
    name="PSI"
))

radar_fig.add_trace(go.Scatterpolar(
    r=[iman, niyyah, ibadah, dhikr, akhlaq, ilm, mizan, ummah],
    theta=["Faith", "Intention", "Worship", "Remembrance", "Morality", "Knowledge", "Balance", "Community"],
    fill="toself",
    name="IEPI"
))

radar_fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    template="plotly_white" if st.session_state.theme == "light" else "plotly_dark"
)

st.plotly_chart(radar_fig, use_container_width=True)
# ============================
# 🧩 التوصيات الشخصية
# ============================
st.subheader("🔍 توصيات ذكية لتحسين مؤشراتك")

def generate_recommendation(value):
    if value >= 70:
        return "✅ ممتاز: حافظ على ممارساتك الحالية."
    elif 40 <= value < 70:
        return "⚠️ متوسط: حاول تحسين العادات اليومية."
    else:
        return "🚨 ضعيف: تحتاج إلى تدخل وخطة تدريبية."

cols = st.columns(3)
for i, (label, value) in enumerate(psi_metrics.items()):
    with cols[i % 3]:
        st.markdown(f"**{label}:** {generate_recommendation(value)}")

# ============================
# 🧩 التوصيات الشخصية
# ============================
st.subheader("🔍 توصيات ذكية لتحسين مؤشراتك")

def generate_recommendation(value):
    if value >= 70:
        return "✅ ممتاز: حافظ على ممارساتك الحالية."
    elif 40 <= value < 70:
        return "⚠️ متوسط: حاول تحسين العادات اليومية."
    else:
        return "🚨 ضعيف: تحتاج إلى تدخل وخطة تدريبية."

cols = st.columns(3)
for i, (label, value) in enumerate(psi_metrics.items()):
    with cols[i % 3]:
        st.markdown(f"**{label}:** {generate_recommendation(value)}")

# ==================================================
# 🟠 التبويب 2: Text Analyzer مع رسم PSI & IEPI
# ==================================================
with tabs[1]:
    st.subheader("✍️ تحليل النصوص | Text Analyzer")
    user_text = st.text_area("📜 أدخل النص هنا | Enter Text Here", height=180)

    if st.button("🔍 تحليل النص"):
        if user_text.strip():
            # تحليل النصوص عبر الدالة الموجودة في core
            results = analyze_text(user_text)

            # استخراج القيم الأساسية من النتيجة
            sentiment_score = results.get("sentiment_score", 0)
            sentiment_label = results.get("sentiment_label", "neutral")
            keywords = results.get("keywords", [])
            length = results.get("length", 0)

            # عرض نتيجة التحليل بشكل منسق
            st.success("✅ تم التحليل بنجاح!")
            st.json(results)

            # -------------------------------
            # ⚡ حساب PSI و IEPI من التحليل
            # -------------------------------
            # نفترض أن المشاعر تؤثر بنسبة مباشرة على PSI و IEPI
            # حيث يتم تحويل sentiment_score من (-1 → 1) إلى (0 → 100)
            psi_from_text = max(0, min(100, (sentiment_score + 1) * 50))
            iepi_from_text = max(0, min(100, (sentiment_score + 1) * 50))

            # -------------------------------
            # 🎨 إنشاء المخطط البياني
            # -------------------------------
            fig = go.Figure()

            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=psi_from_text,
                title={'text': "🌿 مؤشر PSI"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2563EB"},
                    'steps': [
                        {'range': [0, 40], 'color': "#FCA5A5"},
                        {'range': [40, 70], 'color': "#FCD34D"},
                        {'range': [70, 100], 'color': "#86EFAC"}
                    ]
                },
                domain={'x': [0, 0.48], 'y': [0, 1]}
            ))

            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=iepi_from_text,
                title={'text': "🕌 مؤشر IEPI"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#22D3EE"},
                    'steps': [
                        {'range': [0, 40], 'color': "#FCA5A5"},
                        {'range': [40, 70], 'color': "#FCD34D"},
                        {'range': [70, 100], 'color': "#86EFAC"}
                    ]
                },
                domain={'x': [0.52, 1], 'y': [0, 1]}
            ))

            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor="white" if st.session_state.theme == "light" else "#0E1117",
                font=dict(color="black" if st.session_state.theme == "light" else "white")
            )

            st.markdown("### 📊 تأثير النص على مؤشرات PSI & IEPI")
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("⚠️ الرجاء إدخال نص للتحليل.")

# ==================================================
# 🔵 التبويب 3: Audio Analyzer
# ==================================================
with tabs[2]:
    st.subheader("🎙️ تحليل الصوت | Audio Analyzer")
    uploaded_audio = st.file_uploader("🎵 قم برفع ملف صوتي (WAV, MP3)", type=["wav", "mp3"])

    # عند الضغط على زر التحليل
    if uploaded_audio and st.button("🎧 تحليل الصوت"):
        st.info("⏳ جارٍ تحليل الصوت...")
        audio_results = analyze_audio(uploaded_audio)

        if audio_results:
            st.success("✅ تم تحليل الصوت بنجاح!")
            st.json(audio_results)  # عرض النتائج بشكل منظم

            # إنشاء بيانات الرسم البياني
            features = {
                "⏱️ المدة (ثانية)": audio_results["duration_sec"],
                "🔊 طاقة الصوت (RMS)": audio_results["rms_energy"],
                "🎼 المعامل الطيفي": audio_results["spectral_centroid"],
                "🎶 طبقة الصوت (Pitch)": audio_results["pitch_hz"],
                "🤫 نسبة الصمت": audio_results["silence_ratio"]
            }

            # إنشاء المخطط العمودي التفاعلي
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=list(features.keys()),
                y=list(features.values()),
                marker=dict(color="cornflowerblue"),
                text=[f"{val:.2f}" for val in features.values()],
                textposition="outside"
            ))

            # تخصيص مظهر المخطط
            fig.update_layout(
                title="🎧 مؤشرات تحليل الصوت",
                xaxis_title="المؤشر",
                yaxis_title="القيمة",
                template="plotly_white",
                height=500,
                title_x=0.5
            )

            # عرض المخطط في Streamlit
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("⚠️ تعذّر تحليل الصوت. يرجى المحاولة مرة أخرى.")

# ==================================================
# 🟣 التبويب 4: Survey Analyzer مع رسم كامل للأبعاد
# ==================================================
with tabs[3]:
    st.subheader("📊 تحليل الاستبيانات | Survey Analyzer")
    uploaded_file = st.file_uploader("📄 قم برفع ملف استبيان (CSV / Excel)", type=["csv", "xlsx"])

    if uploaded_file and st.button("📈 تحليل الاستبيان"):
        # قراءة البيانات
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        st.success("✅ تم تحميل بيانات الاستبيان بنجاح!")

        # اختيار الأعمدة الخاصة بالمؤشرات (مثال: العقل، الروح، العلاقات، الإيمان... إلخ)
        indicator_columns = df.columns[2:]  # تجاوز ID و Participant

        # ==================================================
        # 🔹 1. رسم مخطط عنكبوتي لكل مشارك
        # ==================================================
        st.markdown("### 🕸️ تحليل المؤشرات النفسية والروحية لكل مشارك")

        for idx, row in df.iterrows():
            categories = list(indicator_columns)
            values = row[indicator_columns].values.tolist()
            values += values[:1]  # إغلاق الدائرة

            fig = go.Figure()

            # إنشاء المخطط العنكبوتي
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=row["Participant"]
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=True,
                title=f"تحليل مؤشرات {row['Participant']}",
                template="plotly_white" if st.session_state.theme == "light" else "plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

        # ==================================================
        # 🔹 2. رسم مخطط عنكبوتي للمقارنة بين جميع المشاركين
        # ==================================================
        st.markdown("### 🕸️ مقارنة شاملة بين جميع المشاركين")

        fig_all = go.Figure()
        for idx, row in df.iterrows():
            values = row[indicator_columns].values.tolist()
            values += values[:1]
            fig_all.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=row["Participant"]
            ))

        fig_all.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title="📊 مقارنة المؤشرات النفسية والروحية بين جميع المشاركين",
            template="plotly_white" if st.session_state.theme == "light" else "plotly_dark"
        )

        st.plotly_chart(fig_all, use_container_width=True)
# ==================================================
# 🔶 التبويب 5: الاستبيان النفسي-الروحي PSI & IEPI
# ==================================================
with tabs[4]:
    st.subheader("🧠 استبيان المؤشرات | PSI & IEPI Survey")

    st.markdown("""
    هذا الاستبيان مخصص لقياس **المؤشر النفسي-الروحي (PSI)** و **مؤشر الاستنارة الإسلامية (IEPI)**  
    يرجى تحريك المؤشرات بناءً على شعورك وتجربتك الشخصية.
    """)

    # تعريف الأسئلة والمجالات
    survey_questions = [
        ("أشعر بسلام داخلي عند مواجهة الضغوط اليومية", "PSI"),
        ("أجد أن العبادة تعزز إدراكي لذاتي وروحي", "IEPI"),
        ("أستطيع التحكم في انفعالاتي السلبية بسهولة", "PSI"),
        ("أشعر أن علاقتي بالخالق تعزز وعيي بذاتي", "IEPI"),
        ("لدي القدرة على موازنة العقل والعاطفة في قراراتي", "PSI"),
        ("أستشعر النور الداخلي أثناء ممارسة التأمل أو الذكر", "IEPI"),
        ("أشعر بالانسجام بين أهدافي الدنيوية والروحية", "PSI"),
        ("أتعامل مع الآخرين بتسامح ورحمة نابعة من وعي روحي", "IEPI"),
        ("أستطيع الحفاظ على تركيزي الذهني لفترات طويلة", "PSI"),
        ("أجد أن العلم والمعرفة يرفعان مستوى إدراكي الروحي", "IEPI")
    ]

    # إدخال القيم
    psi_scores = []
    iepi_scores = []

    for idx, (question, category) in enumerate(survey_questions):
        score = st.slider(f"**{idx+1}. {question}**", 0, 100, 50)
        if category == "PSI":
            psi_scores.append(score)
        else:
            iepi_scores.append(score)

    # حساب المتوسطات
    avg_psi = sum(psi_scores) / len(psi_scores)
    avg_iepi = sum(iepi_scores) / len(iepi_scores)

    # عرض النتائج
    st.markdown("### 📊 نتائج الاستبيان")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("المؤشر النفسي-الروحي (PSI)", f"{avg_psi:.1f} / 100")
    with col2:
        st.metric("مؤشر الاستنارة الإسلامية (IEPI)", f"{avg_iepi:.1f} / 100")

    # رسم بياني للمؤشرات
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=avg_psi,
        title={'text': "PSI"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "blue"}}
    ))
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=avg_iepi,
        title={'text': "IEPI"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
    ))

    fig.update_layout(
        grid={'rows': 1, 'columns': 2, 'pattern': "independent"},
        height=300,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
