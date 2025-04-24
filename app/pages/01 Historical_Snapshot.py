import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# === Page Configuration ===
st.set_page_config(page_title="Historical Snapshot | Stock Dashboard", layout="wide")

# === Load Data ===
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("https://drive.google.com/uc?id=1-2rHajs3BynUMsR9ljXVBZ0P4AvwKbZE")
        df["date"] = pd.to_datetime(df["date"])
        return df.sort_values("date")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

df = load_data()

# === Custom CSS - Using the same styling as Home page ===
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

/* KPI Styling - Matched to Home page */
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
    padding: 6px 15px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: bold;
    color: white;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    margin: 0 auto;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* Slide-up animation */
@keyframes fadeSlideUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.section-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin: 30px 0 20px 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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

/* Summary styling */
.summary-block {
    background-color: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 0 8px rgba(0,0,0,0.4);
    margin-top: 18px;
    font-size: 16px;
    color: #e0e0e0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    animation: fadeIn 0.6s ease-out;
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

.summary-block p {
    margin-bottom: 10px;
    line-height: 1.5;
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

/* Date display */
.date-display {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 16px;
    color: #ffffff;
    display: inline-block;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    animation: fadeIn 0.5s ease-out;
}

/* Observations panel */
.observations {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    border-radius: 10px;
    padding: 15px 20px;
    margin: 15px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    animation: fadeIn 0.7s ease-out;
}

.observation-item {
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
    animation: fadeSlideUp 0.5s ease-out;
    animation-delay: calc(var(--delay) * 150ms);
    opacity: 0;
    animation-fill-mode: forwards;
}

.observation-icon {
    flex: 0 0 24px;
    margin-right: 10px;
    color: #4CAF50;
    font-size: 20px;  /* Increased icon size */
}

.observation-text {
    flex: 1;
    color: #e0e0e0;
    line-height: 1.5;
    font-size: 18px;  /* Increased font size */
}

/* Historical table */
.historical-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
    border-radius: 8px;
    overflow: hidden;
    animation: fadeIn 0.6s ease-out;
    text-align: center;
}

.historical-table th {
    background-color: rgba(0, 0, 0, 0.2);
    padding: 12px 15px;
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    font-size: 16px;
}

.historical-table td {
    padding: 10px 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    color: #e0e0e0;
    font-size: 16px;
    text-align: center;
}

.historical-table tr:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transition: background-color 0.2s ease;
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

/* Better date input styling */
[data-testid="stDateInput"] {
    background-color: rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 20px;
}

[data-testid="stDateInput"] > div {
    color: black !important;
}

[data-testid="stDateInput"] > div > div > div {
    color: black !important;
    background-color: rgba(255, 255, 255, 0.15) !important;
}

[data-testid="stDateInput"] input {
    color: black !important;
    background-color: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    font-size: 16px !important;
}

[data-testid="stDateInput"] label {
    color: white !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

[data-testid="stDateInput"]::before {
    background-color: transparent !important;
}

/* Download button styling */
[data-testid="baseButton-secondary"] {
    background-color: rgba(33, 150, 243, 0.7) !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

[data-testid="baseButton-secondary"]:hover {
    background-color: rgba(33, 150, 243, 0.9) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
}

.narrow-card {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
    text-align: center;
    margin: 10px auto;
    max-width: 220px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.narrow-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-container {
    padding: 15px 0;
    margin-bottom: 20px;
}

.date-container {
    background-color: rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 20px;
}

.section-title {
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Ensure consistent padding in summary block */
.summary-block {
    padding: 20px !important;
    margin-bottom: 20px !important;
}

</style>
""", unsafe_allow_html=True)

# === Title and Introduction ===
st.markdown(f"""
<div class='title'>📊 ⏳ Historical Analysis</div>
<div class='subtitle'>
    Time Travel Through Market Data: Examine how indicators have changed over time, compare performance across different periods, and identify patterns that may inform future investment decisions. Essential for understanding how markets have responded to past conditions.
</div>
<hr />
""", unsafe_allow_html=True)

# === Handle Empty DataFrame Error ===
if df.empty:
    st.error("No data available. Please check the data source and try again.")
    st.stop()

# === Select Date ===
try:
    selected_date = st.date_input(
        "Select a historical date:", 
        value=df["date"].max().date(), 
        min_value=df["date"].min().date(), 
        max_value=df["date"].max().date()
    )
    # Convert to pandas datetime for comparisons
    selected_datetime = pd.to_datetime(selected_date)
    
    # Get the closest date if exact date doesn't exist
    if selected_datetime not in df["date"].values:
        closest_date = df["date"].iloc[abs(df["date"] - selected_datetime).argmin()]
        st.info(f"Data for {selected_date} not available. Showing closest available date: {closest_date.strftime('%B %d, %Y')}")
        selected_datetime = closest_date
    
    selected_row = df[df["date"] == selected_datetime].iloc[0]
except Exception as e:
    st.error(f"Error selecting date: {e}")
    st.stop()

# === Display selected date ===
st.markdown(f"""
<div class='date-display'>
    📅 Viewing data for: <strong>{selected_datetime.strftime('%B %d, %Y')}</strong> | 
    Ticker: <strong>{selected_row['ticker']}</strong>
</div>
""", unsafe_allow_html=True)

# === Year-over-Year Comparison ===
try:
    # Safer calculation for previous year date
    previous_year_date = selected_datetime - pd.DateOffset(years=1)
    prev_year_row = df[df["date"] == previous_year_date]

    if not prev_year_row.empty:
        prev_row = prev_year_row.iloc[0]
        yoy_score_diff = selected_row["composite_score"] - prev_row["composite_score"]
        yoy_signal_change = f"{prev_row['recommendation']} → {selected_row['recommendation']}"
        yoy_price_diff = selected_row["close"] - prev_row["close"]
        yoy_price_pct = (yoy_price_diff / prev_row["close"]) * 100
    else:
        yoy_score_diff, yoy_signal_change, yoy_price_diff, yoy_price_pct = None, None, None, None
        prev_row = None
except Exception as e:
    st.warning(f"Could not calculate year-over-year comparison: {e}")
    yoy_score_diff, yoy_signal_change, yoy_price_diff, yoy_price_pct = None, None, None, None
    prev_row = None

# === Signal styling ===
signal_color_map = {
    "buy": "#4CAF50",
    "sell": "#F44336",
    "hold": "#FFC107"
}
signal = selected_row["recommendation"].lower()
signal_color = signal_color_map.get(signal, "#999999")

# === Smart Summary Block ===
if yoy_score_diff is not None:
    score_trend = "increased" if yoy_score_diff > 0 else "decreased"
    price_trend = "rose" if yoy_price_diff > 0 else "fell"
    
    formatted_price_diff = "${:,.2f}".format(abs(yoy_price_diff))
    
    st.markdown(f"""
    <div class="summary-block" style="margin-top: 0; border-top: none;">
        <h4>💡 Snapshot Summary</h4>
        <p>On <strong>{selected_datetime.strftime('%B %d, %Y')}</strong>, the model generated a composite score of 
        <strong>{selected_row['composite_score']:.2f}</strong>, resulting in a
        <span class='pill' style='background-color:{signal_color};'>{signal.upper()}</span> recommendation.</p>
        <p>Compared to the same day in the previous year, the composite score <strong>{score_trend}</strong> by 
        <strong>{abs(yoy_score_diff):.2f}</strong> points.
        The closing price <strong>{price_trend}</strong> by <strong>{formatted_price_diff}</strong> 
        (<strong>{abs(yoy_price_pct):.2f}%</strong>), and the investment signal changed from 
        <strong>{yoy_signal_change}</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

# Close the div in a separate markdown call
st.markdown("</div>", unsafe_allow_html=True)

# === Main KPI Row ===
st.markdown("<div class='section-title'>Key Performance Indicators</div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Format values with thousand separators consistently
formatted_open = "${:,.2f}".format(selected_row['open'])
formatted_close = "${:,.2f}".format(selected_row['close'])
formatted_score = "{:.2f}".format(selected_row['composite_score'])
percent_change = selected_row['percent_change']
change_icon = "📈" if percent_change >= 0 else "📉"
change_color = "#4CAF50" if percent_change >= 0 else "#F44336"

with col1:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>{formatted_score}</div>
        <div class='kpi-label'>🧩 Composite Score</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>{formatted_open}</div>
        <div class='kpi-label'>🏦 Open Price</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>{formatted_close}</div>
        <div class='kpi-label'>💰 Close Price</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value' style='color:{change_color};'>{percent_change:.2f}%</div>
        <div class='kpi-label'>{change_icon} Daily Change</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 40px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)

# === Component Scores ===
st.markdown("<div class='section-title'>Component Scores</div>", unsafe_allow_html=True)

sub1, space1, sub2, space2, sub3 = st.columns([3, 0.5, 3, 0.5, 3])

with sub1:
    st.markdown(f"""
    <div class='narrow-card'>
        <div class='kpi-value'>{selected_row['fundamental_score']:.2f}</div>
        <div class='kpi-label'>📊 Fundamental Score</div>
    </div>
    """, unsafe_allow_html=True)

with sub2:
    st.markdown(f"""
    <div class='narrow-card'>
        <div class='kpi-value'>{selected_row['technical_score']:.2f}</div>
        <div class='kpi-label'>📈 Technical Score</div>
    </div>
    """, unsafe_allow_html=True)

with sub3:
    st.markdown(f"""
    <div class='narrow-card'>
        <div class='kpi-value'>{selected_row['news_sentiment_score']:.2f}</div>
        <div class='kpi-label'>📰 News Sentiment</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 40px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)

# === 90-Day Historical Performance Chart ===
st.markdown("<div class='section-title'>90-Day Historical Performance</div>", unsafe_allow_html=True)

try:
    historical_data = df.sort_values("date").tail(90).copy()
    
    if len(historical_data) > 1:
        fig = px.line(
            historical_data,
            x="date",
            y="composite_score",
            markers=True,
            line_shape="spline"
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title="Date",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color='#ffffff'),
                title_font=dict(color='#ffffff')
            ),
            yaxis=dict(
                title="Composite Score",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color='#ffffff'),
                title_font=dict(color='#ffffff')
            ),
            margin=dict(l=10, r=10, t=30, b=10),
            hovermode="x unified",
            font=dict(color="white")
        )
        
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
        
        fig.update_traces(
            line=dict(color='#7d5ee3', width=4),
            marker=dict(color='#ffffff', size=8, line=dict(color='#7d5ee3', width=2))
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient historical data to display chart.")
except Exception as e:
    st.error(f"Error creating chart: {e}")

    
st.markdown("<hr style='margin-top: 40px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)


# === Smart Insights Section ===
st.markdown("<div class='section-title'>Key Observations</div>", unsafe_allow_html=True)

observations_html = """
<div class='observations'>
"""

try:
    # 1. Top Driver
    components = {
        "Fundamental Score": selected_row.get("fundamental_score", 0),
        "Technical Score": selected_row.get("technical_score", 0),
        "News Sentiment": selected_row.get("news_sentiment_score", 0)
    }
    driver = max(components.items(), key=lambda x: abs(x[1]))[0]

    st.markdown(f"""
    <div class='observation-item' style='--delay: 1'>
        <div class='observation-icon'>📊</div>
        <div class='observation-text'>
            The strongest score driver on this day was <strong>{driver}</strong> with a value of <strong>{max(components.values()):.2f}</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Sentiment vs Fundamental Conflict
    if abs(components["News Sentiment"] - components["Fundamental Score"]) > 20:
        st.markdown(f"""
        <div class='observation-item' style='--delay: 2'>
            <div class='observation-icon'>⚠️</div>
            <div class='observation-text'>
                <strong>Conflicting Signals:</strong> News sentiment ({components["News Sentiment"]:.2f}) and 
                fundamentals ({components["Fundamental Score"]:.2f}) are significantly out of sync, suggesting potential market inefficiency.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3. Extreme Movement Alert (YoY)
    if prev_row is not None:
        delay_counter = 3
        for label, curr in components.items():
            key = label.lower().replace(" ", "_")
            prev_val = prev_row.get(key)
            if prev_val is not None and abs(curr - prev_val) > 15:
                delta = curr - prev_val
                movement = "increased" if delta > 0 else "decreased"
                st.markdown(f"""
                <div class='observation-item' style='--delay: {delay_counter}'>
                    <div class='observation-icon'>📈</div>
                    <div class='observation-text'>
                        <strong>{label} {movement} by {delta:+.2f} points year-over-year</strong>, indicating significant 
                        change in this component.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                delay_counter += 1

    # 4. Price-Score Alignment
    score_above_50 = selected_row["composite_score"] > 50
    price_increased = selected_row["percent_change"] > 0

    if (score_above_50 and price_increased) or (not score_above_50 and not price_increased):
        st.markdown(f"""
        <div class='observation-item' style='--delay: 5'>
            <div class='observation-icon'>✅</div>
            <div class='observation-text'>
                <strong>Score-Price Alignment:</strong> The composite score and price change are moving in the same direction,
                suggesting model accuracy.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='observation-item' style='--delay: 5'>
            <div class='observation-icon'>⚠️</div>
            <div class='observation-text'>
                <strong>Score-Price Misalignment:</strong> The composite score and price change are moving in opposite directions,
                suggesting potential market lag or model recalibration needed.
            </div>
        </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not generate all observations: {e}")


st.markdown("<hr style='margin-top: 40px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)


# === Historical Snapshot Table: Same Day in Prior Years ===
st.markdown("<div class='section-title'>Same-Day Performance in Prior Years</div>", unsafe_allow_html=True)

try:
    same_day_matches = df[
        (df["date"].dt.month == selected_datetime.month) & 
        (df["date"].dt.day == selected_datetime.day) &
        (df["date"].dt.year < selected_datetime.year)  
    ]
    same_day_matches = same_day_matches.sort_values("date", ascending=False)

    if not same_day_matches.empty:
        def render_row(row):
            year = row["date"].year
            score = f"{row['composite_score']:.2f}"
            close = f"${row['close']:,.2f}"  
            rec = row["recommendation"].capitalize()
            color = signal_color_map.get(rec.lower(), "#999999")
            
            pill = f"<span class='pill' style='background-color:{color};'>{rec}</span>"
            
            return f"<tr><td>{year}</td><td>{score}</td><td>{pill}</td><td>{close}</td></tr>"

        table_rows = "\n".join([render_row(row) for _, row in same_day_matches.iterrows()])

        st.markdown(f"""
        <table class='historical-table'>
            <thead>
                <tr>
                    <th>Year</th>
                    <th>Composite Score</th>
                    <th>Recommendation</th>
                    <th>Close Price</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        """, unsafe_allow_html=True)
    else:
        st.info("No prior data available for this exact day in previous years.")
except Exception as e:
    st.warning(f"Could not generate historical table: {e}")

# === Data Export Option ===
st.markdown("<div class='section-title'>Export Data</div>", unsafe_allow_html=True)
st.markdown("""
    <div style='color: white;'>
        <strong>Download the historical data for further analysis</strong> </p>
        </div>
    """, unsafe_allow_html=True)

try:
    end_date = selected_datetime
    start_date = end_date - pd.Timedelta(days=90)
    export_data = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    
    for col in export_data.select_dtypes(include=['float', 'int']).columns:
        if 'price' in col.lower() or 'open' in col.lower() or 'close' in col.lower() or 'high' in col.lower() or 'low' in col.lower():
            export_data[col] = export_data[col].map('${:,.2f}'.format)
    
    csv = export_data.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"historical_data_{selected_datetime.strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
        key="download-csv"
    )
except Exception as e:
    st.error(f"Error preparing data for export: {e}")

# === Footer ===
st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {df["date"].max().strftime('%B %d, %Y')} | © 2025 DATA 606 Capstone - UMBC</p>
</div>
""", unsafe_allow_html=True)