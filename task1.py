import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import dash
from dash import dcc, html, Input, Output

# ==================================================
# 🚀 PRE-LOAD DATA & CLUSTERING ONCE (NOT EVERY VISIT)
# ==================================================
# This runs ONLY when building, not when users visit
if not os.environ.get("VERCEL"):
    pass  # normal run locally
df = pd.read_csv("superstore_cleaned.csv", usecols=["Customer ID","Order ID","Sales","Profit","Quantity","Discount"])
df = df.dropna(subset=["Customer ID","Sales","Profit","Discount"])

# Customer metrics
customer_metrics = df.groupby("Customer ID", as_index=False).agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_orders=("Order ID","nunique"),
    avg_discount=("Discount","mean")
)

# Outliers
for col in ["total_sales","total_profit"]:
    q1,q3 = customer_metrics[col].quantile([0.01,0.99])
    iqr = q3-q1
    customer_metrics = customer_metrics[(customer_metrics[col]>=q1-1.5*iqr) & (customer_metrics[col]<=q3+1.5*iqr)]

# Clustering
features = ["total_sales","total_profit","total_orders","avg_discount"]
X_scaled = StandardScaler().fit_transform(customer_metrics[features])
customer_metrics["Cluster"] = pd.Series(KMeans(4,random_state=42,n_init=10).fit_predict(X_scaled)).astype("category")

# Add readable labels
cluster_names = {
    "0": "Low-Value / Low Discount",
    "1": "🏆 High-Value Top Customers",
    "2": "Mid-Tier / Steady Buyers",
    "3": "Discount-Driven / Low Margin"
}
customer_metrics["Cluster Label"] = customer_metrics["Cluster"].astype(str).map(cluster_names)

# ==================================================
# 🎨 DASH THEME & APP START
# ==================================================
theme = {
    "bg_main": "#121217",
    "bg_card": "#1A1A22",
    "text": "#E8E8F0",
    "text_light": "#9CA3AF",
    "grid": "#2A2A35",
    "colors": ["#8B5CF6", "#3B82F6", "#10B981", "#F59E0B"]
}

app = dash.Dash(__name__)
app.title = "Customer Segmentation Dashboard | Power BI Style"
server = app.server  # ✅ KEEP THIS — CORRECT PLACE

# --- REST OF YOUR CODE (layout, callbacks) STAYS EXACTLY THE SAME ---
import os
os.environ["PYTHONUNBUFFERED"] = "1"
# ==================================================
# INTERACTIVE POWER BI / TABLEAU STYLE DASHBOARD
# Click any cluster → ALL charts update automatically
# ==================================================
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import dash
from dash import dcc, html, Input, Output

# ==================================================
# 🎨 DARK THEME (MATCHES YOUR DESIGN)
# ==================================================
theme = {
    "bg_main": "#121217",
    "bg_card": "#1A1A22",
    "text": "#E8E8F0",
    "text_light": "#9CA3AF",
    "grid": "#2A2A35",
    "colors": ["#8B5CF6", "#3B82F6", "#10B981", "#F59E0B"] # Purple, Blue, Green, Orange
}

# ==================================================
# DATA & CLUSTERING (SAME LOGIC AS BEFORE)
# ==================================================
df = pd.read_csv("superstore_cleaned.csv", usecols=["Customer ID","Order ID","Sales","Profit","Quantity","Discount"])
df = df.dropna(subset=["Customer ID","Sales","Profit","Discount"])

# Customer metrics
customer_metrics = df.groupby("Customer ID", as_index=False).agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    total_orders=("Order ID","nunique"),
    avg_discount=("Discount","mean")
)

# Outliers
for col in ["total_sales","total_profit"]:
    q1,q3 = customer_metrics[col].quantile([0.01,0.99])
    iqr = q3-q1
    customer_metrics = customer_metrics[(customer_metrics[col]>=q1-1.5*iqr) & (customer_metrics[col]<=q3+1.5*iqr)]

# Clustering
features = ["total_sales","total_profit","total_orders","avg_discount"]
X_scaled = StandardScaler().fit_transform(customer_metrics[features])
customer_metrics["Cluster"] = pd.Series(KMeans(4,random_state=42,n_init=10).fit_predict(X_scaled)).astype("category")

# Add readable labels
cluster_names = {
    "0": "Low-Value / Low Discount",
    "1": "🏆 High-Value Top Customers",
    "2": "Mid-Tier / Steady Buyers",
    "3": "Discount-Driven / Low Margin"
}
customer_metrics["Cluster Label"] = customer_metrics["Cluster"].astype(str).map(cluster_names)

# ==================================================
# 🚀 BUILD INTERACTIVE DASHBOARD
# ==================================================
app = dash.Dash(__name__)
app.title = "Customer Segmentation Dashboard | Power BI Style"
server = app.server
app.layout = html.Div(style={"backgroundColor":theme["bg_main"], "color":theme["text"], "padding":"20px", "fontFamily":"Segoe UI, sans-serif"}, children=[
    html.H1("📊 Customer Segmentation Dashboard | Superstore K-Means Analysis", style={"textAlign":"center", "marginBottom":"30px", "fontWeight":"bold"}),

    # --- ROW 1: ELBOW + SILHOUETTE ---
    html.Div(style={"display":"flex", "gap":"20px", "marginBottom":"20px"}, children=[
        html.Div(style={"width":"48%", "backgroundColor":theme["bg_card"], "padding":"15px", "borderRadius":"10px"}, children=[
            html.H3("Elbow Method", style={"textAlign":"center"}),
            dcc.Graph(id="elbow_plot")
        ]),
        html.Div(style={"width":"48%", "backgroundColor":theme["bg_card"], "padding":"15px", "borderRadius":"10px"}, children=[
            html.H3("Silhouette Score", style={"textAlign":"center"}),
            dcc.Graph(id="sil_plot")
        ])
    ]),

    # --- ROW 2: MAIN SCATTER PLOT (CLICKABLE!) ---
    html.Div(style={"backgroundColor":theme["bg_card"], "padding":"15px", "borderRadius":"10px", "marginBottom":"20px"}, children=[
        html.H3("Customer Segments: Total Sales vs Total Profit", style={"textAlign":"center"}),
        html.P("💡 Click a cluster in the legend or points → All charts will filter automatically", style={"textAlign":"center", "color":theme["text_light"]}),
        dcc.Graph(id="scatter_plot")
    ]),

    # --- ROW 3: BAR CHART + PROFILE TABLE ---
    html.Div(style={"display":"flex", "gap":"20px"}, children=[
        html.Div(style={"width":"35%", "backgroundColor":theme["bg_card"], "padding":"15px", "borderRadius":"10px"}, children=[
            html.H3("Customers per Cluster", style={"textAlign":"center"}),
            dcc.Graph(id="bar_plot")
        ]),
        html.Div(style={"width":"60%", "backgroundColor":theme["bg_card"], "padding":"15px", "borderRadius":"10px"}, children=[
            html.H3("Cluster Profile & Metrics", style={"textAlign":"center"}),
            dcc.Graph(id="profile_table")
        ])
    ])
])

# ==================================================
# 🔄 AUTO-UPDATE ALL CHARTS ON CLICK
# ==================================================
@app.callback(
    [Output("scatter_plot", "figure"),
     Output("bar_plot", "figure"),
     Output("profile_table", "figure")],
    [Input("scatter_plot", "clickData"),
     Input("scatter_plot", "selectedData")]
)
def update_dashboard(click, selected):
    # Default: show ALL clusters
    filtered = customer_metrics.copy()
    title_suffix = " | All Clusters"

    # If user clicks a cluster → filter everything
    if click:
        selected_cluster = click["points"][0]["curveNumber"]
        filtered = customer_metrics[customer_metrics["Cluster"] == str(selected_cluster)]
        title_suffix = f" | Selected: {cluster_names[str(selected_cluster)]}"

    # --- SCATTER PLOT ---
    fig_scatter = px.scatter(
        filtered, x="total_sales", y="total_profit", color="Cluster Label",
        color_discrete_sequence=theme["colors"],
        labels={"total_sales":"Total Sales ($)", "total_profit":"Total Profit ($)"},
        title=f"Customer Segments: Sales vs Profit {title_suffix}"
    )
    fig_scatter.update_layout(
        plot_bgcolor=theme["bg_card"], paper_bgcolor=theme["bg_card"],
        font_color=theme["text"], xaxis_gridcolor=theme["grid"], yaxis_gridcolor=theme["grid"],
        legend_title="Customer Cluster", clickmode="event+select"
    )

    # --- BAR CHART ---
    counts = filtered["Cluster Label"].value_counts().sort_index()
    fig_bar = px.bar(
        x=counts.index, y=counts.values, color=counts.index,
        color_discrete_sequence=theme["colors"],
        labels={"x":"Cluster", "y":"Number of Customers"},
        title=f"Customers per Cluster {title_suffix}"
    )
    fig_bar.update_layout(
        plot_bgcolor=theme["bg_card"], paper_bgcolor=theme["bg_card"],
        font_color=theme["text"], xaxis_gridcolor=theme["grid"], yaxis_gridcolor=theme["grid"], showlegend=False
    )

    # --- PROFILE TABLE ---
    profile = filtered.groupby("Cluster Label", as_index=False)[features].mean().round(2)
    fig_table = go.Figure(data=[go.Table(
        header=dict(values=["Cluster Name", "Total Sales", "Total Profit", "Total Orders", "Avg Discount"],
                    fill_color="#252530", font=dict(color=theme["text"], size=12, weight="bold")),
        cells=dict(values=[profile[c] for c in profile.columns],
                   fill_color=theme["bg_card"], font=dict(color=theme["text"], size=11))
    )])
    fig_table.update_layout(
        title=f"Average Metrics {title_suffix}",
        paper_bgcolor=theme["bg_card"], font_color=theme["text"]
    )

    return fig_scatter, fig_bar, fig_table

# --- STATIC ELBOW & SILHOUETTE PLOTS ---
@app.callback(
    [Output("elbow_plot", "figure"), Output("sil_plot", "figure")]
)
def build_validation():
    k_range = range(2,8)
    X = StandardScaler().fit_transform(customer_metrics[features])
    wcss = [KMeans(k,random_state=42,n_init=10).fit(X).inertia_ for k in k_range]
    sil = [silhouette_score(X, KMeans(k,random_state=42,n_init=10).fit_predict(X)) for k in k_range]

    fig_e = go.Figure(go.Scatter(x=list(k_range), y=wcss, mode="lines+markers", line=dict(color=theme["colors"][1],width=3), marker=dict(size=8)))
    fig_e.add_vline(x=4, line_dash="dash", line_color="#EF4444", annotation_text="Optimal K=4")
    fig_e.update_layout(title="Elbow Method", xaxis_title="Number of Clusters", yaxis_title="Within-Cluster Sum of Squares",
                        plot_bgcolor=theme["bg_card"], paper_bgcolor=theme["bg_card"], font_color=theme["text"], xaxis_gridcolor=theme["grid"])

    fig_s = go.Figure(go.Scatter(x=list(k_range), y=sil, mode="lines+markers", line=dict(color=theme["colors"][2],width=3), marker=dict(size=8)))
    fig_s.add_vline(x=4, line_dash="dash", line_color="#EF4444")
    fig_s.update_layout(title="Silhouette Score", xaxis_title="Number of Clusters", yaxis_title="Silhouette Score",
                        plot_bgcolor=theme["bg_card"], paper_bgcolor=theme["bg_card"], font_color=theme["text"], xaxis_gridcolor=theme["grid"])

    return fig_e, fig_s

# ==================================================
# ✅ FIXED: USE app.run() INSTEAD OF app.run_server()
# ==================================================
if __name__ == "__main__":
    app.run(debug=True)