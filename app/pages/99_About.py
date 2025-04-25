import streamlit as st

# === Page Configuration ===
st.set_page_config(page_title="📒 📝 About | Stock Dashboard", layout="wide")

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

/* Card styling */
.about-card {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

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

/* Make body text white */
html, body, .main, .block-container, .element-container {
    color: #ffffff !important;
}

/* Ensure markdown headers and bullets are also white */
h1, h2, h3, h4, h5, h6, p, li, ul {
    color: #ffffff !important;
}

/* Timeline styling */
.timeline {
    position: relative;
    max-width: 1200px;
    margin: 20px auto;
}

.timeline::after {
    content: '';
    position: absolute;
    width: 6px;
    background-color: rgba(255, 255, 255, 0.2);
    top: 0;
    bottom: 0;
    left: 50%;
    margin-left: -3px;
}

.timeline-container {
    padding: 10px 40px;
    position: relative;
    background-color: inherit;
    width: 50%;
}

.timeline-container::after {
    content: '';
    position: absolute;
    width: 20px;
    height: 20px;
    right: -10px;
    background-color: #7d5ee3;
    border: 4px solid rgba(255, 255, 255, 0.3);
    top: 15px;
    border-radius: 50%;
    z-index: 1;
}

.timeline-left {
    left: 0;
}

.timeline-right {
    left: 50%;
}

.timeline-left::before {
    content: " ";
    height: 0;
    position: absolute;
    top: 22px;
    width: 0;
    z-index: 1;
    right: 30px;
    border: medium solid rgba(255, 255, 255, 0.15);
    border-width: 10px 0 10px 10px;
    border-color: transparent transparent transparent rgba(255, 255, 255, 0.15);
}

.timeline-right::before {
    content: " ";
    height: 0;
    position: absolute;
    top: 22px;
    width: 0;
    z-index: 1;
    left: 30px;
    border: medium solid rgba(255, 255, 255, 0.15);
    border-width: 10px 10px 10px 0;
    border-color: transparent rgba(255, 255, 255, 0.15) transparent transparent;
}

.timeline-right::after {
    left: -10px;
}

.timeline-content {
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    position: relative;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.timeline-date {
    font-weight: bold;
    color: #7d5ee3;
    margin-bottom: 5px;
}

/* Team cards */
.team-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
    margin: 30px 0;
}

.team-card {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 20px;
    width: 300px;
    text-align: center;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.team-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.team-name {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 5px;
}

.team-role {
    color: #ffffff;
    font-weight: 600;
    margin-bottom: 10px;
}

.team-bio {
    font-size: 14px;
    line-height: 1.5;
    margin-bottom: 15px;
}

.team-contact {
    font-size: 14px;
    color: #e0e0e0;
}

/* Data sources section */
.data-sources {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 20px 0;
}

.data-source {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    flex: 1 1 300px;
    border-left: 4px solid #7d5ee3;
}

.data-source h4 {
    margin-top: 0;
    margin-bottom: 10px;
}

.data-source p {
    font-size: 14px;
    margin-bottom: 5px;
}

/* Future roadmap */
.roadmap-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 15px;
}

.roadmap-icon {
    flex: 0 0 30px;
    color: #7d5ee3;
    font-size: 20px;
    margin-right: 10px;
}

.roadmap-text {
    flex: 1;
}

.roadmap-title {
    font-weight: bold;
    margin-bottom: 5px;
}

.roadmap-desc {
    font-size: 14px;
    color: #e0e0e0;
}

</style>
""", unsafe_allow_html=True)

# === Title and Introduction ===
st.markdown("<div class='title'>ℹ️ About This Dashboard</div>", unsafe_allow_html=True)
st.markdown("""
<div class='subtitle'>
    Learn more about the Stock Dashboard for Novice Investors, its features, the team behind it, and our development journey.
</div>
""", unsafe_allow_html=True)

# === About Content ===
st.markdown("""
## Stock Dashboard for Novice Investors

This dashboard helps novice investors understand market signals through composite scores that combine technical analysis, 
fundamental data, and news sentiment. Our goal is to make investment decision-making more accessible by translating 
complex financial metrics into clear, actionable insights.

### Dashboard Features

* **Composite Score Analysis**: A weighted combination of fundamental, technical, and news sentiment metrics
* **Historical Snapshots**: View how stock metrics have changed over time
* **Score Breakdown**: Detailed analysis of individual components contributing to the overall score
* **Social Media Sentiment**: Analysis of online discussions to gauge market perception
* **Trade Simulator**: Test different trading strategies without risking real capital
* **Interactive Data Explorer**: Analyze correlations between different metrics and components
""")

# === Methodology Section ===
#with st.expander("Our Methodology", expanded=False):
st.markdown("""
### Methodology: How We Score

#### 1. **Fundamental Analysis (0–100)**
Scores are derived from:
- Revenue growth and trends
- Earnings Per Share (EPS)
- P/E ratio and valuation metrics
- Piotroski score for financial health
       
#### 2. **Technical Analysis (0–100)**
Includes:
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- ATR (Average True Range)
- SMA (Simple Moving Averages)

#### 3. **News Sentiment Analysis (0–100)**
- NLP models applied to financial articles
- Positive, neutral, and negative classifications
- Volume of relevant articles

#### 4. **Composite Score Calculation**
A weighted average of:
- Fundamental Score
- Technical Score
- News Sentiment Score

> **Note:** Social sentiment is not directly included in the composite score but is displayed separately for context.

### Signal Thresholds
- **Buy**: Composite Score > 70
- **Hold**: Score between 40–70
- **Sell**: Score < 40

### Validation & Data Sources
- **Backtesting** against historical performance
- **APIs**: Yahoo Finance, Polygon.io, Reddit (PRAW)

""")

# === Team Section ===
st.markdown("## Meet The Team")

st.markdown("""
<div class="team-container">
    <div class="team-card">
        <div class="team-name">Mehul Lad</div>
        <div class="team-role">Lead Data Analyst</div>
        <div class="team-bio">
            Led development of composite score algorithms. Specialized in financial data analysis and machine learning implementation.
        </div>
        <div class="team-contact">du72811@umbc.edu</div>
    </div>
        <div class="team-card">
        <div class="team-name">Ashley McConnell</div>
        <div class="team-role">UI/UX Lead</div>
        <div class="team-bio">
            Led the development of the dashboard interface with focus on accessibility and clarity for novice investors. Implemented data visualizations and interactive components.
        </div>
        <div class="team-contact">amcconn1@umbc.edu</div>
    </div>
    <div class="team-card">
        <div class="team-name">Bestover Makoko</div>
        <div class="team-role">Researcher</div>
        <div class="team-bio">
            Conducted literature review and research on financial analysis methods. Developed methodology for integrating fundamental, technical, and sentiment analysis.
        </div>
        <div class="team-contact">imakoko1@umbc.edu</div>
    </div>
</div>
""", unsafe_allow_html=True)

# === Data Sources Section ===
st.markdown("## Data Sources & Methodology")

st.markdown("""
<div class="data-sources">
    <div class="data-source">
        <h4>📊 Stock Price Data</h4>
        <p><strong>Source:</strong> Yahoo Finance API</p>
        <p><strong>Update Frequency:</strong> Daily (market close)</p>
        <p><strong>Includes:</strong> OHLC prices, volume, market cap</p>
    </div>
    <div class="data-source">
        <h4>📈 Financial Statements</h4>
        <p><strong>Source:</strong> Polygon.io</p>
        <p><strong>Update Frequency:</strong> Quarterly</p>
        <p><strong>Includes:</strong> Revenue, EPS, P/E ratios, growth metrics</p>
    </div>  
    <div class="data-source">
        <h4>📰 News Articles</h4>
        <p><strong>Source:</strong> Financial news APIs</p>
        <p><strong>Update Frequency:</strong> Daily</p>
        <p><strong>Analysis:</strong> Natural language processing for sentiment</p>
    </div>    
    <div class="data-source">
        <h4>💬 Social Media</h4>
        <p><strong>Source:</strong> Reddit PRAW API</p>
        <p><strong>Update Frequency:</strong> Daily</p>
        <p><strong>Includes:</strong> Posts from 5 financial subreddits</p>
    </div>
</div>
""", unsafe_allow_html=True)

# === Acknowledgments ===
st.markdown("## Acknowledgments")

st.markdown("""
We would like to thank our faculty advisor, Dr. Masoud Soroush, for his guidance throughout this project. 
We also appreciate the support from the UMBC Data Science program faculty and the feedback from our 
beta testers who helped refine the dashboard.

Special thanks to Yahoo Finance, Polygon.io, and Reddit for providing access to their APIs, 
which made this project possible.
""")

# === Project Information Section ===
st.markdown("### Project Information")

st.markdown("""
This dashboard was developed as a capstone project for DATA 606 at the University of Maryland, Baltimore County (UMBC) by Group Two.

The project's objective was to create an accessible investment tool that bridges the gap between complex financial analysis and 
practical decision-making for novice investors.

All code for this project is available on [GitHub](https://github.com/yourusername/stock-dashboard).
""")

# === Disclaimer ===
st.markdown("""
### Disclaimer

This dashboard is for educational purposes only and should not be considered financial advice. Always consult with a 
qualified financial advisor before making investment decisions. Historical performance is not indicative of future results.

The models and predictions provided are based on historical data analysis and may not account for all market factors. 
Users should conduct their own research and exercise caution when making investment decisions.
""")

# === Footer ===
latest_update = "April 21, 2025"  # Update with actual value from data

st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {latest_update} | © 2025 DATA 606 Capstone - UMBC</p>
</div>
""", unsafe_allow_html=True)