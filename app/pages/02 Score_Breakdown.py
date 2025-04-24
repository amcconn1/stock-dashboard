import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# === Page Configuration ===
st.set_page_config(page_title="Score Breakdown | Stock Dashboard", layout="wide")

# === Load Data ===
@st.cache_data
def load_data():
    fund = pd.read_csv("https://drive.google.com/uc?id=1_0mOMnLilhu69Q0di3PrOlIOa4gZtIsS", parse_dates=["date"])
    tech = pd.read_csv("https://drive.google.com/uc?id=1jA8dealEGH37YDH7Gs5fZbIOXg-aFu-X", parse_dates=["date"])
    news = pd.read_csv("https://drive.google.com/uc?id=15NGsicmkQ7fLBxXll9EPCxTD_L5kZvOS", parse_dates=["date"])
    return fund, tech, news

fund, tech, news = load_data()

# === Custom CSS ===
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

/* Page Title */
.title {
    font-size: 48px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 10px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
    font-size: 18px;
    color: #e0e0e0;
    margin-bottom: 20px;
    max-width: 800px;
}

/* Card styling */
.card {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Score display */
.score-value {
    font-size: 36px;
    font-weight: 600;
    color: #ffffff;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.score-label {
    font-size: 16px;
    color: #e0e0e0;
    margin-top: 5px;
}

/* Component header */
.component-header {
    font-size: 28px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 15px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Section title */
.section-title {
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin: 30px 0 15px 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    text-align: center;
}

/* Divider */
hr {
    border: none;
    height: 2px;
    background-color: rgba(255, 255, 255, 0.1);
    margin: 20px 0;
}

/* Info panel */
.info-panel {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #4CAF50;
    margin-bottom: 20px;
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
}

/* Chart container */
.chart-container {
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Expander styling */
.streamlit-expander {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 8px !important;
}

/* Metric tiles */
.metric-tile {
    background-color: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(5px);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    margin-bottom: 15px;
    text-align: center;
    border: 1px solid rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.metric-tile:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.metric-tile-value {
    font-size: 28px;
    font-weight: 600;
    color: #ffffff;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.metric-tile-label {
    font-size: 14px;
    color: #e0e0e0;
    margin-top: 5px;
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

[data-testid="stDateInput"] {
    background-color: rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 20px;
}

[data-testid="stDateInput"] label {
    color: white !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

.narrow-card {
    max-width: 300px;
    margin: auto;
}

.streamlit-expanderHeader {
    color: white !important;
}

/* Fix expander header text color */
[data-testid="stExpander"] > summary {
    color: white !important;
}


</style>
""", unsafe_allow_html=True)

# === Title and Introduction ===
st.markdown("<div class='title'>📊 📝 Score Breakdown</div>", unsafe_allow_html=True)
st.markdown("""
<div class='subtitle'>
    Under the Hood: Dissect the composite score into its fundamental, technical, and sentiment components to understand exactly what's driving the current recommendation. Perfect for investors wanting to learn which factors have the greatest impact on a stock's performance.
</div>
""", unsafe_allow_html=True)

# === Date Selector ===
with st.container():
    selected_date = st.date_input(
        "Select a historical date:", 
        value=fund["date"].max()
    )

selected_datetime = pd.to_datetime(selected_date)

# === Date Display ===
st.markdown(f"""
<div class='date-display'>
    <i class="fa fa-calendar"></i>📅Viewing metrics for: <strong>{selected_date.strftime('%B %d, %Y')}</strong>
</div>
""", unsafe_allow_html=True)

# === Create Radar Chart for Selected Date ===
st.markdown("<div class='section-title'> Composite Analysis</div>", unsafe_allow_html=True)

st.markdown("""
<div style='color: #e0e0e0; font-size: 16px; text-align: center; margin-top: -10px; margin-bottom: 20px;'>
    <em>Note: Values in the radar chart are normalized (0–100 scale) to highlight relative strengths across components.</em>
</div>
""", unsafe_allow_html=True)

radar_values = {
    "Fundamental": fund[fund["date"] == selected_datetime]["fundamental score"].values,
    "Technical": tech[tech["date"] == selected_datetime]["technical_score"].values,
    "News Sentiment": news[news["date"] == selected_datetime]["news_sentiment_score"].values
}

# Check if we have data for all components
if all(len(v) > 0 for v in radar_values.values()):
    # Extract values for the radar chart
    categories = list(radar_values.keys())
    values = [v[0] for v in radar_values.values()]
    
    # Normalize values for better radar visualization (0-100 scale)
    max_value = max(values)
    normalized_values = [min(v / max_value * 100, 100) for v in values]
    
    # Create radar chart with Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(225, 165, 0, 0.5)',
        line=dict(color='#7d5ee3', width=2),
        name='Score Components'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor='rgba(255, 255, 255, 0.2)'
            ),
            angularaxis=dict(
                showticklabels=True,
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='#ffffff')
            ),
            bgcolor='rgba(0, 0, 0, 0)'
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255, 255, 255, 0.05)',
        margin=dict(l=80, r=80, t=20, b=20),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display value summary below the chart
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-tile'>
            <div class='metric-tile-value'>{values[0]:.2f}</div>
            <div class='metric-tile-label'>📊 Fundamental Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-tile'>
            <div class='metric-tile-value'>{values[1]:.2f}</div>
            <div class='metric-tile-label'>📈 Technical Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-tile'>
            <div class='metric-tile-value'>{values[2]:.2f}</div>
            <div class='metric-tile-label'>📰 News Sentiment Score</div>
        </div>
        """, unsafe_allow_html=True)
    
else:
    st.info("Not all scores are available for the selected date. Please choose another date.")


def render_component_metrics(title, df, score_col, drivers, color, icon):
    latest = df[df["date"] == selected_datetime]
    
    if latest.empty:
        st.warning(f"No data for {title} on {selected_date}")
        return
    
    latest = latest.iloc[0]
    
    
    st.markdown("<hr style='margin-top: 30px; margin-bottom: 30px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)


    st.markdown(f"<div class='component-header'>{icon} {title}</div>", unsafe_allow_html=True)
    
    # Score card
    st.markdown(f"""
    <div class='card narrow-card' style='text-align: center; margin-bottom: 25px;'>
        <div class='score-value'>{latest[score_col]:.2f}</div>
        <div class='score-label'>Score Value</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key driver metrics (styled manually instead of expander)
    st.markdown("""
    <div style='color: white; font-size: 14px; font-weight: bold; margin-bottom: 10px;'>
        View Key Driver Metrics
    </div>
    """, unsafe_allow_html=True)

    driver_data = {drv: latest[drv] for drv in drivers if drv in latest}

    if driver_data:
        cols = st.columns(len(driver_data))
        for i, (metric, value) in enumerate(driver_data.items()):
            with cols[i]:
                formatted_value = f"{value:,.2f}" if "ratio" not in metric.lower() and metric != "rsi" else f"{value:.2f}"
                st.markdown(f"""
                <div class='metric-tile'>
                    <div class='metric-tile-value'>{formatted_value}</div>
                    <div class='metric-tile-label'>{metric.replace('_', ' ').title()}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No driver metrics available for this component.")
    
    # 30-day trend chart
    if not df.empty:
        trend_data = df[df["date"] <= selected_datetime].sort_values("date").tail(30)
        if not trend_data.empty:
            fig = px.line(
                trend_data, 
                x="date", 
                y=score_col,
                labels={"date": "Date", score_col: "Score"}
            )
            fig.update_layout(
                paper_bgcolor='rgba(0, 0, 0, 0)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='#ffffff'),
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    showline=False,
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    showline=False,
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                hovermode='x unified'
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

            fig.update_traces(
                line=dict(shape='spline',color=color, width=4),
                mode='lines+markers',
                marker=dict(size=7, line=dict(width=2, color='white'))
            )
            st.plotly_chart(fig, use_container_width=True)

# === Render Component Sections ===
#st.markdown("<div class='section-title'>Score Components</div>", unsafe_allow_html=True)

# Fundamental Analysis
render_component_metrics(
    "Fundamental Score", 
    fund, 
    "fundamental score", 
    ["revenue score", "Profit Margin Score", "EPS Surprise Score", "Piotroski_Score_Scaled"], 
    "#2196F3",
    "📊"
)

# Technical Analysis
render_component_metrics(
    "Technical Score", 
    tech, 
    "technical_score", 
    ["rsi_score", "macd_score", "atr_score", "sma_score"], 
    "#F44336",
    "📈"
)

# News Sentiment Analysis
render_component_metrics(
    "News Sentiment", 
    news, 
    "news_sentiment_score", 
    ["article_count", "positive_sentiment_news", "neutral_sentiment_news", "negative_sentiment_news"], 
    "#FFC107",
    "📰"
)

st.markdown("<hr style='margin-top: 40px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)



st.markdown("""
<div style='color: white;'>

### 📚 Understanding Score Components

#### Component Scores Explained

**Fundamental Score**  
Based on company financial health and valuations. Higher scores indicate stronger financial position, revenue growth, and reasonable valuation.

**Technical Score**  
Derived from price patterns, RSI, and moving averages.

**News Sentiment Score**  
Measures market perception through news coverage and sentiment analysis. Tracks article count and the ratio of positive to negative coverage.

#### Key Metrics Definitions

- **RSI Score (Relative Strength Index)**: Momentum indicator measuring recent price changes (0–100). Above 70 = potentially overbought, below 30 = potentially oversold.
- **MACD (Moving Average Convergence Divergence) Indicator**: Technical indicator to help investors identify entry points for buying or selling. The MACD line is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA.It's interpreted based on its movement and relationship with other indicators.
- **Profit Margin Score (PMS)**: A financial ratio that measures the percentage of profit earned by a company in relation to its revenue. Higher = better profitability.
- **Piotroski Score**: A system for assessing a company's financial strength, using a numerical score between 0 and 9. A higher score (8 or 9) generally indicates a stronger financial position, while a lower score (1 or 2) suggests potential weaknesses.

</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 30px; margin-bottom: 30px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)


# === Correlation Analysis ===

label_map = {
    "fundamental score": "Fundamental Score",
    "technical_score": "Technical Score",
    "news_sentiment_score": "News Sentiment Score",
    "percent_change": "Price Change" 
}

# Add this after the component sections
st.markdown("<div class='section-title'>Score Correlation Analysis</div>", unsafe_allow_html=True)

st.markdown("""
<div style='color: #e0e0e0; font-size: 14px; text-align: center; margin-top: -10px; margin-bottom: 20px;'>
    <em>This heatmap shows how different score components correlate with each other and with price changes.</em>
</div>
""", unsafe_allow_html=True)

try:
    # Merge all datasets on date
    correlation_df = pd.merge(fund, tech, on=['date', 'ticker'], how='inner')
    correlation_df = pd.merge(correlation_df, news, on=['date', 'ticker'], how='inner')
    
    # Select relevant columns for correlation
    corr_columns = [
        'fundamental score', 
        'technical_score', 
        'news_sentiment_score'
    ]

    # Add price change if available
    if 'percent_change' in correlation_df.columns:
        corr_columns.append('percent_change')
    
    # Ensure all columns exist
    valid_columns = [col for col in corr_columns if col in correlation_df.columns]
    
    if len(valid_columns) >= 2:  # Need at least 2 columns for correlation
        # Calculate correlation
        corr_matrix = correlation_df[valid_columns].corr()
        
            # Apply label map to correlation matrix
        corr_matrix_renamed = corr_matrix.rename(index=label_map, columns=label_map)
          

        # Create correlation heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix_renamed.values,
            x=corr_matrix_renamed.columns,
            y=corr_matrix_renamed.index,
            colorscale=[
                [0.0, "rgb(165,0,38)"],
                [0.1, "rgb(215,48,39)"],
                [0.2, "rgb(244,109,67)"],
                [0.3, "rgb(253,174,97)"],
                [0.4, "rgb(254,224,144)"],
                [0.5, "rgb(255,255,191)"],
                [0.6, "rgb(224,243,248)"],
                [0.7, "rgb(171,217,233)"],
                [0.8, "rgb(116,173,209)"],
                [0.9, "rgb(69,117,180)"],
                [1.0, "rgb(49,54,149)"]
            ],
            text=corr_matrix.round(2).values,
            hoverinfo="text",
        ))
        
        # Add annotations
        for i in range(len(corr_matrix_renamed.index)):
            for j in range(len(corr_matrix_renamed.columns)):
                fig.add_annotation(
                    x=j,
                    y=i,
                    text=f"{corr_matrix_renamed.values[i, j]:.2f}",
                    showarrow=False,
                    font=dict(
                        color="white" if abs(corr_matrix_renamed.values[i, j]) < 0.5 else "black",
                        size=12
                    )
                )
        
        # Update layout
        fig.update_layout(
            #title="Correlation Between Score Components",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add correlation insights
        st.markdown("""
        <div style="border-left: 4px solid #7d5ee3; font-size: 12px; padding: 15px; color: white; background-color: rgba(255,255,255,0.05); border-radius: 8px; margin-top: 20px;">
            <strong>Correlation Insights:</strong> 
            <ul style='color: white;'>
                <li>Values close to 1 indicate strong positive correlation (when one score increases, the other tends to as well)</li>
                <li>Values close to -1 indicate strong negative correlation (when one score increases, the other tends to decrease)</li>
                <li>Values close to 0 indicate little to no relationship between the scores</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Insufficient data columns available for correlation analysis.")
except Exception as e:
    st.error(f"Error creating correlation analysis: {e}")



# === Footer ===
st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {fund["date"].max().strftime('%B %d, %Y')} | © 2025 DATA 606 Capstone - UMBC</p>
</div>
""", unsafe_allow_html=True)