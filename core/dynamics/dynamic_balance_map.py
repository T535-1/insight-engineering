import plotly.graph_objects as go
import networkx as nx
import numpy as np

def generate_smart_balance_map(scores: dict):
    """
    إنشاء خريطة توازن ديناميكية ذكية متكاملة مع الاستبيان PSI & IEPI.
    :param scores: قاموس يحتوي على القيم النهائية لكل مؤشر.
    :return: كائن رسم Plotly تفاعلي جاهز للعرض.
    """

    # ================================
    # 1. بناء شبكة المؤشرات
    # ================================
    G = nx.Graph()

    for indicator, value in scores.items():
        G.add_node(indicator, value=value)

    relations = [
        ("الإيمان", "النية"),
        ("النية", "الأخلاق"),
        ("الذكر", "العبادة"),
        ("العلم", "المجتمع"),
        ("التوازن", "الإيمان"),
        ("التوازن", "الذكر"),
        ("التوازن", "الأخلاق"),
        ("المجتمع", "الأخلاق")
    ]
    G.add_edges_from(relations)

    pos = nx.spring_layout(G, seed=42)

    # ================================
    # 2. إعداد البيانات للرسم
    # ================================
    node_x, node_y, node_size, node_color, node_text, recommendations = [], [], [], [], [], []

    for node, attr in G.nodes(data=True):
        x, y = pos[node]
        value = attr["value"]

        node_x.append(x)
        node_y.append(y)
        node_size.append(max(10, value * 15))  # حجم العقدة حسب القيمة
        node_color.append(value)

        # النص المعروض عند تمرير الماوس
        node_text.append(f"{node}: {value:.2f}")

        # توصيات علاجية لكل مؤشر
        if value >= 7:
            rec = "⚡ مؤشر قوي: استمر في الممارسات الحالية."
        elif 4 <= value < 7:
            rec = "🔄 متوسط: يمكن تحسينه بالتركيز والمثابرة."
        else:
            rec = "🚨 ضعيف: يوصى بالتأمل والتدريب العميق."
        recommendations.append(rec)

    # ================================
    # 3. رسم الحواف (العلاقات)
    # ================================
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines"
    )

    # ================================
    # 4. رسم العقد
    # ================================
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="RdYlGn",  # 🔵 ألوان من الأحمر (ضعيف) إلى الأخضر (قوي)
            color=node_color,
            size=node_size,
            colorbar=dict(
                thickness=15,
                title="مستوى المؤشر",
                xanchor="left",
                titleside="right"
            )
        )
    )

    # ================================
    # 5. إضافة التوصيات الجانبية
    # ================================
    annotations = []
    for i, node in enumerate(G.nodes()):
        annotations.append(dict(
            x=1.15,
            y=1 - (i * 0.08),
            xref="paper",
            yref="paper",
            text=f"{node}: {recommendations[i]}",
            showarrow=False,
            font=dict(size=12, color="black")
        ))

    # ================================
    # 6. الشكل النهائي
    # ================================
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="🌿 خريطة التوازن الديناميكية الذكية",
                        title_x=0.5,
                        showlegend=False,
                        hovermode="closest",
                        margin=dict(b=0, l=0, r=250, t=50),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        annotations=annotations
                    ))

    return fig
