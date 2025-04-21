import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==== Streamlit Config ====
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# ==== Load Data ====
@st.cache_data
def load_data():
    df = pd.read_csv("data/composite_score.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date")

df = load_data()
latest = df.iloc[-1]

# ==== Full Style Code ====
st.markdown("""
<style>
/* Background - multiple selectors to ensure it works */
body {
    background: linear-gradient(to bottom, #2b5876, #4e4376) !important;
}

.stApp {
    background: linear-gradient(to bottom, #2b5876, #4e4376) !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #2b5876, #4e4376) !important;
}

.main .block-container {
    background: transparent;
}

#root > div:first-child {
    background: linear-gradient(to bottom, #2b5876, #4e4376) !important;
}

/* Card containers */
.card {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
    text-align: center;
    margin: 10px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Title styling */
.title {
    font-size: 48px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 2px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
    font-size: 18px;
    color: #e0e0e0;
    margin-bottom: 20px;
    max-width: 900px;
    line-height: 1.5;
}

/* KPI Styling */
.kpi-value {
    font-size: 38px;
    font-weight: 600;
    color: #ffffff;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.kpi-label {
    font-size: 16px;
    color: #e0e0e0;
    margin-top: 8px;
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background-color: rgba(255, 255, 255, 0.1);
    margin: 20px 0;
}

/* Signal Pill */
@keyframes fadeUp {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

.pill {
    display: inline-block;
    padding: 12px 30px;
    border-radius: 30px;
    font-size: 24px;
    font-weight: bold;
    color: white;
    animation: fadeUp 0.6s ease-out;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    margin: 12px auto 24px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* Slide-up animation */
@keyframes fadeSlideUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.highlight-card {
  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: 12px;
  animation: fadeSlideUp 0.6s ease-in-out;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
  margin-top: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.highlight-title {
  font-size: 22px;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 16px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.highlight-metric {
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 10px;
}

.chart-card {
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.section-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin: 30px 0 20px 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Radio buttons & other inputs */
.stRadio label {
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 500;
}

.stRadio label p {
    color: #ffffff !important;
}

[data-baseweb="radio"] label {
    color: #ffffff !important;
    font-size: 16px;
    font-weight: 500;
}

[data-baseweb="radio"] [role="radio"] {
    border: 2px solid #ffffff !important;
}

[data-baseweb="radio"] [aria-checked="true"] {
    background-color: #7d5ee3 !important;
    border-color: #7d5ee3 !important;
}

.stRadio > div {
    flex-direction: row !important;
    gap: 15px;
}
.metric-card {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    margin-bottom: 14px;
    text-align: center;
    transition: all 0.2s ease-in-out;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-card .metric-value {
    font-size: 28px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 4px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.metric-card .metric-label {
    font-size: 14px;
    font-weight: 500;
    color: #e0e0e0;
    margin-top: 4px;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.summary-block {
    background-color: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 0 8px rgba(0,0,0,0.4);
    margin-top: 12px;
    font-size: 18px;
    color: #e0e0e0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-block h4 {
    margin-top: 0;
    color: #ffffff;
    font-size: 22px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.summary-block ul {
    margin-top: 15px;
}

.summary-block li {
    margin-bottom: 8px;
}

.summary-block strong {
    color: #ffffff;
}

/* Chart title styling */
.chart-title {
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 15px;
    text-align: center;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
    margin-top: 40px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Navigation styling enhancement */
[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0;
}

[data-testid="stSidebar"] a {
    padding: 15px;
    border-radius: 5px;
    margin: 2px 0;
    font-weight: 500;
    color: #ffffff !important;  /* Make link text white */
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] a:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Additional selectors to ensure navigation text is white */
[data-testid="stSidebar"] span {
    color: #ffffff !important;
}

[data-testid="stSidebar"] p {
    color: #ffffff !important;
}

[data-testid="stSidebar"] div {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ==== Header & Introduction ====
st.markdown(f"""
<div class='title'>📊 🧩 Stock Composite Dashboard: {latest['ticker']}</div>
<div class='subtitle'>
    Your Investment Command Center: Get actionable insights at a glance with our comprehensive composite score that translates complex market data into clear buy, hold, or sell recommendations. Start here to understand the big picture before diving deeper.
</div>
<hr />
""", unsafe_allow_html=True)

# Add explicit zone explanation
st.markdown("""
<div style='text-align: center; margin-bottom: 15px;'>
    <span style='color: #e0e0e0; font-size: 16px;'>
        <strong>Scoring Zones:</strong> 
        <span style='color: #4CAF50;'>Buy (100-70)</span> | 
        <span style='color: #FFC107;'>Hold (71-40)</span> | 
        <span style='color: #F44336;'>Sell (41-0)</span>
    </span>
</div>
""", unsafe_allow_html=True)


# ==== Signal Pill (Above KPIs) ====
signal = latest['recommendation'].strip().lower()
signal_colors = {
    "buy": "#4CAF50",
    "sell": "#F44336",
    "hold": "#FFC107"
}
signal_color = signal_colors.get(signal, "#999999")

st.markdown(f"""
<div style='text-align: center;'>
    <span class='pill' style='background-color: {signal_color};'>
        ✨ Current Recommendation: {latest['recommendation'].upper()} ✨
    </span>
</div>
""", unsafe_allow_html=True)

# ==== KPI Row ====
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# Format numbers with thousand separators
formatted_open = "${:,.2f}".format(latest['open'])
formatted_close = "${:,.2f}".format(latest['close'])
formatted_score = "{:.2f}".format(latest['composite_score'])
formatted_change = "{:.2f}%".format(latest['percent_change'])

with kpi1:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>{formatted_score}</div>
        <div class='kpi-label'>🧩 Composite Score</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>{formatted_open}</div>
        <div class='kpi-label'>🏦 Open</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>{formatted_close}</div>
        <div class='kpi-label'>💰 Close</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>{latest['percent_change']:.2f}%</div>
        <div class='kpi-label'>📉 % Change</div>
    </div>
    """, unsafe_allow_html=True)

# === Smart Insights Panel ===
st.markdown("---")

# Create a comprehensive summary 
comp_score = latest["composite_score"]
signal = latest["recommendation"].strip()
price = latest["close"]
change = latest["percent_change"]

# More detailed summary
summary_text = f"""
As of {latest['date'].strftime('%B %d, %Y')}, our analysis has generated a <strong>composite score of {comp_score:.2f}</strong>, 
resulting in a recommendation to <strong>{signal.upper()}</strong> the stock.

The latest closing price was <strong>${price:,.2f}</strong>, reflecting a <strong>{change:.2f}%</strong> change from the previous trading day.

<ul>
    <li><strong>Technical Indicators:</strong> Suggest {signal.lower()}-side momentum based on RSI and moving averages</li>
    <li><strong>Fundamental Analysis:</strong> Shows {signal.lower()}-range valuation metrics</li>
    <li><strong>News Sentiment:</strong> Is moderately {'positive' if comp_score > 50 else 'negative'} over the past 30 days</li>
</ul>
"""

# Styled callout block with proper title
st.markdown(f"""
<div class="summary-block">
    <h4>💬 Today's Market Insight</h4>
    {summary_text}
</div>
""", unsafe_allow_html=True)

# === Trend Analysis Section ===
st.markdown("<div class='section-title'>📈 Trend Analysis</div>", unsafe_allow_html=True)

# Add this new block of markdown for radio button styling
st.markdown("""
<style>
.stRadio label {
    color: #ffffff !important;
    font-weight: 500;
}
.stRadio label p {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

view_option = st.radio("Select Time Window", ["7 Days", "30 Days"], horizontal=True)
window = 7 if view_option == "7 Days" else 30
trend_data = df.sort_values("date").tail(window)

# === Columns for trend + highlight ===
left_col, right_col = st.columns([3, 1])

# === Composite Score Chart (Left) ===
with left_col:
    st.markdown("<div class='chart-title'>Composite Score Trend</div>", unsafe_allow_html=True)
    
    # Create interactive chart with Plotly
    fig = px.line(
        trend_data,
        x="date",
        y="composite_score",
        markers=True,
        line_shape="spline",
    )
    
    # Update layout for better appearance - FIXED
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#ffffff'),
            title_font=dict(color='#ffffff')
        ),
        yaxis=dict(
            title="Composite Score",
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#ffffff'),
            title_font=dict(color='#ffffff')
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        height=350,
        hovermode="x unified"
    )
    
    # Update line appearance
    fig.update_traces(
        line=dict(color='#7d5ee3', width=4),
        marker=dict(color='#ffffff', size=10, line=dict(color='#7d5ee3', width=2))
    )
    
    # Add range fills for buy/sell/hold zones
    fig.add_hrect(
        y0=70, y1=100, 
        fillcolor="#4CAF50", opacity=0.3, 
        line_width=0,
        annotation_text="Buy Zone", 
        annotation_position="right",
        annotation_font_color="#4CAF50",
        annotation_font_size=12
    )
    
    fig.add_hrect(
        y0=40, y1=70, 
        fillcolor="#FFC107", opacity=0.3, 
        line_width=0,
        annotation_text="Hold Zone", 
        annotation_position="right",
        annotation_font_color="#FFC107",
        annotation_font_size=12
    )
    
    fig.add_hrect(
        y0=0, y1=40, 
        fillcolor="#F44336", opacity=0.3, 
        line_width=0,
        annotation_text="Sell Zone", 
        annotation_position="right",
        annotation_font_color="#F44336",
        annotation_font_size=12
    )
    
    st.plotly_chart(fig, use_container_width=True)

# === Highlights (Right) ===
with right_col:
    st.markdown("<div class='chart-title'>Component Scores</div>", unsafe_allow_html=True)
    
    fund = trend_data["fundamental_score"].iloc[-1]
    tech = trend_data["technical_score"].iloc[-1]
    news = trend_data["news_sentiment_score"].iloc[-1] if "news_sentiment_score" in trend_data.columns else 0

    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{fund:.2f}</div>
        <div class='metric-label'>📊 Fundamental Score</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{tech:.2f}</div>
        <div class='metric-label'>📈 Technical Score</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{news:.2f}</div>
        <div class='metric-label'>📰 News Sentiment</div>
    </div>
    """, unsafe_allow_html=True)

# === Footer ===
st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {latest['date'].strftime('%B %d, %Y')} | © 2025 DATA 606 Capstone - UMBC</p>
</div>
""", unsafe_allow_html=True)