import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# === Page Configuration ===
st.set_page_config(page_title="Social Media Sentiment | Stock Dashboard", layout="wide")

# === Load Data ===
@st.cache_data
def load_data():
    try:
        sentiment = pd.read_csv("data/social_sentiment.csv", parse_dates=["Date"])
        raw = pd.read_csv("data/social_raw.csv", parse_dates=["Date"])
        return sentiment, raw
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

sentiment, raw = load_data()

if sentiment is None or raw is None:
    st.stop()

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
    margin-top: 12px;
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

/* Date range display */
.date-range {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 16px;
    color: #ffffff;
    display: inline-block;
    margin: 0 0 20px 15px;
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
    font-size: 16px;  /* Increased font size */
}

/* Metric cards */
.metric-card {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    margin-bottom: 15px;
    text-align: center;
    transition: all 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.metric-value {
    font-size: 28px;
    font-weight: 600;
    color: #ffffff;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.metric-label {
    font-size: 14px;
    color: #e0e0e0;
    margin-top: 5px;
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

/* Reddit post styling enhanced */
.reddit-post {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    margin-bottom: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.2s ease;
    border-left: 4px solid #7d5ee3;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

.reddit-post:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-left: 4px solid #7d5ee3;
}

.post-header {
    font-size: 15px;
    margin-bottom: 6px;
    color: #e0e0e0;
}

.post-title {
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 6px;
}

.post-title a {
    color: #00ccff  !important;
    font-weight: bold
    text-decoration: none;
    transition: all 0.2s ease;
}

.post-title a:hover {
    text-decoration: underline;
    color: #9d7ee3 !important;
}

.post-text {
    font-size: 14px;
    color: #e0e0e0;
    line-height: 1.5;
}

/* Info panel */
.info-panel {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #4CAF50;
    margin-bottom: 20px;
    color: #e0e0e0;
    font-size: 14px;
    line-height: 1.5;
}

/* Sentiment Pill */
.sentiment-pill {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: bold;
    margin-right: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Narrow card for metrics */
.narrow-card {
    max-width: 300px;
    margin: auto;
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

/* Date context styling */
.date-context {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

# === Title and Introduction ===
st.markdown("<div class='title'>📊 📱 Social Media Sentiment</div>", unsafe_allow_html=True)
st.markdown("""
<div class='subtitle'>
    The Market's Digital Pulse: Tap into the collective wisdom (or panic) of online investors through our social media sentiment analysis. See what Reddit communities are saying about your stocks and how online sentiment may foreshadow market movements before they appear in traditional metrics.
</div>
""", unsafe_allow_html=True)

# === Informational Note About Social Media Data ===
st.markdown("""
<div class="info-panel">
    <strong>Note:</strong> Social media sentiment provides additional context for understanding market perception,
    but is not directly incorporated into the composite score calculation. This analysis helps identify potential 
    shifts in investor sentiment that may eventually impact traditional metrics.
</div>
""", unsafe_allow_html=True)

# === Date Selection ===
# Get the most recent date with data
max_date = sentiment["Date"].max()
if pd.notna(max_date):
    max_date = max_date.date()
else:
    st.warning("No dates available in the sentiment data.")
    st.stop()

# Create a container for date selection with better explanation
with st.container():
    #st.markdown("<p style='color: #ffffff; font-size: 16px; font-weight: 500;'>Select a snapshot date to view sentiment analysis for that specific day:</p>", unsafe_allow_html=True)
    selected_date = st.date_input(
        "Select a date to view social media sentiment analysis for that specific date:", 
        value=max_date,
        help="Selecting a date will show both metrics for this specific day and the 30-day trend ending on this date"
    )

# === Select matching row by date (avoid datetime precision issues) ===
match = sentiment[sentiment["Date"].dt.date == selected_date]
if match.empty:
    st.warning(f"No sentiment data available for {selected_date}. Please select another date.")
    st.stop()
else:
    row = match.iloc[0]

# === Calculate date range for display ===
end_date = pd.to_datetime(selected_date)
start_date = end_date - timedelta(days=30)

# === Convert data safely and handle potential issues ===
try:
    # Use safe conversion functions
    def safe_convert(value, default=0):
        if pd.isna(value):
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    # Convert values with fallbacks
    post_count = safe_convert(row.get('Post_Count', 0))
    comment_count = safe_convert(row.get('Comment_Count', 0))
    neg_sentiment = safe_convert(row.get('Negative_Sentiment_Social', 0))
    neutral_sentiment = safe_convert(row.get('Neutral_Sentiment_Social', 0))
    pos_sentiment = safe_convert(row.get('Positive_Sentiment_Social', 0))
    social_score = safe_convert(row.get('Social_Sentiment_Score', 0))
    ticker = row.get('Ticker', 'Unknown')
    
    # === Display Date Context ===
    st.markdown(f"""
    <div class="date-context">
        <div class='date-display'>
            📅 Snapshot date: <strong>{selected_date.strftime('%B %d, %Y')}</strong> | 
            Ticker: <strong>{ticker}</strong>
        </div>
        <div class='date-range'>
            📊 Showing 30-day trend: <strong>{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # === Summary Dashboard ===
    st.markdown("<div class='section-title'>Sentiment Overview</div>", unsafe_allow_html=True)
    

    sentiment_signal_colors = {
    "positive": "#4CAF50",  # Buy - green
    "neutral": "#FFC107",   # Hold - yellow/amber
    "negative": "#F44336"   # Sell - red
    }

    # Create sentiment metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='card'>
            <div class='kpi-value'>{social_score:.2f}</div>
            <div class='kpi-label'>💭 Overall Sentiment Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Format with thousand separators
        formatted_post_count = f"{int(post_count):,}"
        st.markdown(f"""
        <div class='card'>
            <div class='kpi-value'>{formatted_post_count}</div>
            <div class='kpi-label'>📱 Reddit Posts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Format with thousand separators
        formatted_comment_count = f"{int(comment_count):,}"
        st.markdown(f"""
        <div class='card'>
            <div class='kpi-value'>{formatted_comment_count}</div>
            <div class='kpi-label'>💬 CommentsComments</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Determine dominant sentiment
        sentiments = {
            "Positive": pos_sentiment,
            "Neutral": neutral_sentiment,
            "Negative": neg_sentiment
        }
        dominant = max(sentiments.items(), key=lambda x: x[1])[0]
        
        dominant_color = sentiment_signal_colors.get(dominant.lower(), "#7d5ee3")

        sentiment_emoji = {
            "Positive": "😀",
            "Neutral": "😐",
            "Negative": "😟"
        }
        sentiment_icon = sentiment_emoji.get(dominant, "💭")

        st.markdown(f"""
        <div class='card'>
            <div class='kpi-value' style='color:{dominant_color};'>{sentiment_icon} {dominant}</div>
            <div class='kpi-label'>Dominant Sentiment</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # === Social Media Sentiment Snapshot ===
    sentiments = {
    "negative": neg_sentiment,
    "neutral": neutral_sentiment,
    "positive": pos_sentiment
    }

    sentiment_labels = list(sentiments.keys())
    sentiment_values = list(sentiments.values())

    if sum(sentiment_values) == 0:
        sentiment_values = [0.1, 0.1, 0.1]

    sentiment_colors = [
        sentiment_signal_colors["negative"],
        sentiment_signal_colors["neutral"],
        sentiment_signal_colors["positive"]
    ]
       
    # Pill UI block
    st.markdown(f"""
    <div class='summary-block'>
        <h4>📊 Social Media Analysis - Snapshot</h4>
        <p>
            On <strong>{selected_date.strftime('%B %d, %Y')}</strong>, there were <strong>{formatted_post_count}</strong> Reddit posts and 
            <strong>{formatted_comment_count}</strong> comments discussing {ticker}. The overall social sentiment score was <strong>{social_score:.2f}</strong>.
        </p>
        <p>
            Sentiment breakdown: 
            <span class='sentiment-pill' style='background-color:  {sentiment_signal_colors["negative"]}; color: white;'>😠Negative: {neg_sentiment*100:.1f} %</span>
            <span class='sentiment-pill' style='background-color:  {sentiment_signal_colors["neutral"]}; color: white;'>😐Neutral: {sentiments["neutral"] * 100:.1f}%</span>
            <span class='sentiment-pill' style='background-color:  {sentiment_signal_colors["positive"]}; color: white;'>😄Positive: {sentiments["positive"] * 100:.1f}%</span>
        </p>
        <p>
            <em>This analysis provides insight into market perception that may precede changes in traditional metrics.
            A significant shift in social sentiment can indicate changing investor attitudes.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
     
    st.markdown("<hr style='margin-top: 50px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)

    # === 30-Day Sentiment Score Trend ===
    st.markdown("<div class='section-title'>30-Day Sentiment Trend</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-panel" style="border-left: 4px solid #7d5ee3;">
        <strong>Trend Analysis:</strong> 
        This chart shows how social sentiment has evolved over the past 30 days. 
        Look for consistent direction changes that may signal shifting market perception.
    </div>
    """, unsafe_allow_html=True)
    
    if 'Social_Sentiment_Score' in sentiment.columns:
        # Get last 30 days of data, ordered by date
        trend_data = sentiment[(sentiment["Date"] >= start_date) & (sentiment["Date"] <= end_date)]
        trend_data = trend_data.sort_values("Date")
        
        if not trend_data.empty:
            # Convert to numeric and handle potential errors
            trend_data["Social_Sentiment_Score"] = pd.to_numeric(
                trend_data["Social_Sentiment_Score"], 
                errors='coerce'
            )
            
            # Drop NaN values before plotting
            trend_data = trend_data.dropna(subset=["Social_Sentiment_Score"])
            
            if not trend_data.empty:
                
                fig = px.line(
                    trend_data, 
                    x="Date", 
                    y="Social_Sentiment_Score",
                    labels={"Date": "Date", "Social_Sentiment_Score": "Sentiment Score"},
                )
                
                # Add a reference line at zero
                fig.add_hline(
                    y=0, 
                    line_dash="dash", 
                    line_color="white", 
                    opacity=0.5,
                    annotation_text="Neutral",
                    annotation_position="bottom right",
                    annotation_font_color="white"
                )
                
                # Update styling
                fig.update_layout(
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    plot_bgcolor='rgba(255, 255, 255, 0.07)',
                    font=dict(color='#ffffff'),
                    xaxis=dict(
                        title="Date",
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        zeroline=False,
                        tickfont=dict(color='#ffffff'),
                        title_font=dict(color='#ffffff')
                    ),
                    yaxis=dict(
                        title="Sentiment Score",
                        showgrid=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        zeroline=False,
                        tickfont=dict(color='#ffffff'),
                        title_font=dict(color='#ffffff')
                    ),
                    hovermode='x unified',
                    margin=dict(l=10, r=10, t=30, b=10),
                    height=400
                )
                
                # Update line appearance to match theme
                fig.update_traces(
                    line=dict(shape='spline', color='#7d5ee3', width=4),
                    mode='lines+markers',
                    marker=dict(size=8, line=dict(width=2, color='white'))
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No valid data points for the sentiment trend chart.")
        else:
            st.info("Insufficient data for a 30-day trend analysis.")
    else:
        st.warning("The Social_Sentiment_Score column is missing from the data.")

    st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)

    
    # === Top Subreddits Table ===
    st.markdown("<div class='section-title'>Community Analysis</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-panel" style="border-left: 4px solid #7d5ee3;">
        <strong>Community Insight:</strong> 
        Different subreddits can have distinct sentiment biases. Tracking which communities are most active
        can provide context for sentiment shifts.
    </div>
    """, unsafe_allow_html=True)
    
    filtered_raw = raw[raw["Date"].dt.date == selected_date]
    
    if not filtered_raw.empty and "Subreddit Name" in filtered_raw.columns:
        top_subs = filtered_raw["Subreddit Name"].value_counts().head(5)
        
        
        # Create a bar chart for subreddits
        fig = px.bar(
            x=top_subs.index,
            y=top_subs.values,
            labels={"x": "Subreddit", "y": "Post Count"}
        )
        
        # Update styling
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(255, 255, 255, 0.07)',
            font=dict(color='#ffffff'),
            xaxis=dict(
                title="Subreddit",
                showgrid=False,
                categoryorder='total descending',
                tickfont=dict(color='#ffffff'),
                title_font=dict(color='#ffffff')
            ),
            yaxis=dict(
                title="Post Count",
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                tickfont=dict(color='#ffffff'),
                title_font=dict(color='#ffffff')
            ),
            margin=dict(l=10, r=10, t=30, b=10),
            height=350
        )
        
        # Update colors to match theme
        fig.update_traces(
            marker_color='#7d5ee3'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No subreddit data available for the selected date.")
    
    st.markdown("<hr style='margin-top: 20px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)


    # === Top Reddit Posts ===
    st.markdown("<div class='section-title'>Trending Discussions</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-panel" style="border-left: 4px solid #7d5ee3;">
        <strong>Discussion Analysis:</strong> 
        The most popular posts often drive sentiment and can indicate emerging concerns or excitement.
        Pay attention to recurring themes that might signal broader market sentiment shifts.
    </div>
    """, unsafe_allow_html=True)
    
    if not filtered_raw.empty:
        # Check available columns
        available_cols = filtered_raw.columns.tolist()
        required_cols = {
            "score_col": "Score" if "Score" in available_cols else None,
            "author_col": "Author" if "Author" in available_cols else None,
            "subreddit_col": "Subreddit Name" if "Subreddit Name" in available_cols else None,
            "url_col": "URL" if "URL" in available_cols else None,
            "title_col": "Title" if "Title" in available_cols else None,
            "text_col": "Text" if "Text" in available_cols else None,
        }
        
        # Check if minimum required columns exist
        if required_cols["score_col"] or (required_cols["title_col"] or required_cols["text_col"]):
            # Sort by score if available
            if required_cols["score_col"]:
                top_posts = filtered_raw.sort_values(required_cols["score_col"], ascending=False).head(5)
            else:
                top_posts = filtered_raw.head(5)
            
            # Display posts in enhanced card format
            for i, post in top_posts.iterrows():
                # Handle potential missing values with safe extraction
                author = post.get(required_cols["author_col"], 'Anonymous') if required_cols["author_col"] else 'Anonymous'
                subreddit = post.get(required_cols["subreddit_col"], 'Unknown') if required_cols["subreddit_col"] else 'Unknown'
                url = post.get(required_cols["url_col"], '#') if required_cols["url_col"] else '#'
                title = post.get(required_cols["title_col"], 'No title') if required_cols["title_col"] else 'No title'
                text = post.get(required_cols["text_col"], '') if required_cols["text_col"] else ''
                score = post.get(required_cols["score_col"], 0) if required_cols["score_col"] else 0
                
                # Format score with thousand separators
                formatted_score = f"{int(score):,}" if score else "0"
                
                # Truncate text if too long
                text_preview = str(text)[:150] + "..." if isinstance(text, str) and len(str(text)) > 150 else text
                
                st.markdown(f"""
                <div class='reddit-post'>
                    <div class='post-header'>
                        <strong>u/{author}</strong> in <em>r/{subreddit}</em> • Score: {formatted_score}
                    </div>
                    <div class='post-title'>
                        <a href='{url}' target='_blank' style='color: #7d5ee3;'>{title}</a>
                    </div>
                    <div class='post-text'>{text_preview}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Required Reddit post data is missing.")
    else:
        st.info("No Reddit posts available for the selected date.")
        
    # === Word Cloud of Comments (Enhanced)===
    st.markdown("<div class='section-title'>Key Terms Analysis</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-panel" style="border-left: 4px solid #7d5ee3;">
        <strong>Topic Analysis:</strong> 
        This word cloud highlights frequently mentioned terms in recent discussions.
        Larger words indicate more frequent mentions and can reveal emerging topics of interest.
    </div>
    """, unsafe_allow_html=True)
    
    # Filter for the last 30 days of comments
    thirty_days_ago = pd.to_datetime(selected_date) - timedelta(days=30)
    recent_comments = raw[raw["Date"] >= thirty_days_ago]
    
    if not recent_comments.empty and "Text" in recent_comments.columns:
        # Combine all comments, handling potential NaN values
        comments = recent_comments["Text"].dropna().astype(str).str.cat(sep=" ")
        
        if comments and len(comments.strip()) > 0:
            # Generate word cloud with proper error handling
            try:
                # Use matplotlib properly for wordcloud with updated styling
                plt.figure(figsize=(10, 5))
                wordcloud = WordCloud(
                    width=800, 
                    height=400, 
                    background_color='#2b5876', 
                    colormap='viridis',  # Using viridis to better match the theme
                    max_words=100,
                    contour_width=1,
                    contour_color='#7d7d7d',
                    prefer_horizontal=0.9  # Allow more vertical words
                ).generate(comments)
                
                # Create a figure for the wordcloud
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")
                fig.tight_layout(pad=0)
                
                # Update figure styling
                fig.patch.set_facecolor('#2b5876')
                
                st.pyplot(fig)
                
                st.markdown("""
                <div style='text-align: center; font-size: 14px; color: #e0e0e0; margin-top: -10px'>
                    Word cloud based on all comments from the past 30 days
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating word cloud: {e}")
                st.info("Word cloud generation failed. This may be due to insufficient text data or missing dependencies.")
        else:
            st.info("Not enough text data to generate a word cloud.")
    else:
        st.info("No comment data available for the selected time period.")

except Exception as e:
    st.error(f"Error processing data: {e}")

# === Footer ===
st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {max_date.strftime('%B %d, %Y')} | © 2025 DATA 606 Capstone - UMBC</p>
</div>
""", unsafe_allow_html=True)
    