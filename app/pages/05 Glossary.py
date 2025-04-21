import streamlit as st

# === Page Configuration ===
st.set_page_config(page_title="📊 📒 Glossary | Stock Dashboard", layout="wide")

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

/* Footer */
.footer {
    text-align: center;
    padding: 20px 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
    margin-top: 40px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Make body text white */
html, body, .main, .block-container, .element-container {
    color: #ffffff !important;
}

/* Ensure markdown headers and bullets are also white */
h1, h2, h3, h4, h5, h6, p, li, ul {
    color: #ffffff !important;
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

# === Title and Introduction ===
st.markdown("<div class='title'>📊 📖 Glossary & Reference</div>", unsafe_allow_html=True)
st.markdown("""
<div class='subtitle'>
    This page provides definitions for key terms, score scales, and thresholds to help you navigate and understand the dashboard more effectively.
</div>
""", unsafe_allow_html=True)

# === Glossary Content in Alphabetical Order ===
st.markdown("""
## A
---

### Annualized Return
The return on investment expressed as a yearly rate. Used to compare investments over different time periods.

## B
---

### Buy Signal
Generated when a score exceeds the upper threshold (typically 70). Suggests favorable conditions for purchasing a stock.

### Buy Zone
Score range of 70-100, indicating favorable investment conditions based on the selected metrics.

## C
---

### Composite Score
A weighted average combining fundamental, technical, and news sentiment scores to provide an overall investment signal.

### Correlation
Measures the relationship between two variables. Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation).

## D
---

### Drawdown
The percentage decline from a peak to a trough in an investment's value. Used to assess risk and potential losses.

## E
---

### EPS (Earnings Per Share)
A company's profit divided by the number of outstanding shares. Higher values generally indicate better profitability.

## F
---

### Fundamental Analysis
An evaluation method focusing on a company's financial health through metrics like revenue, earnings, and growth rates.

### Fundamental Score
Component of the composite score based on financial statements and economic indicators (0-100 scale).

## H
---

### Hold Signal
Generated when a score falls between upper and lower thresholds (typically 40-70). Suggests maintaining current positions.

### Hold Zone
Score range of 40-70, indicating neutral conditions based on the selected metrics.

## M
---

### MA (Moving Average)
The average closing price over a specified time period. MA 20 refers to the 20-day moving average.

### Maximum Drawdown
The largest percentage drop from peak to trough during a specific time period.

## N
---

### News Sentiment Score
Component of the composite score based on news and media coverage sentiment analysis (0-100 scale).

## P
---

### P/E Ratio (Price-to-Earnings)
The ratio of a company's share price to its earnings per share. Indicates market expectations for growth.

### Portfolio Value
The total worth of an investment portfolio at a given point in time.

## R
---

### RSI (Relative Strength Index)
A momentum oscillator that measures the speed and change of price movements on a scale from 0 to 100.
- Above 70: Potentially overbought condition
- Below 30: Potentially oversold condition

## S
---

### Sell Signal
Generated when a score falls below the lower threshold (typically 40). Suggests unfavorable conditions for holding a stock.

### Sell Zone
Score range of 0-40, indicating unfavorable investment conditions based on the selected metrics.

### Social Sentiment
Analysis of conversations from social media platforms to gauge market perception.

## T
---

### Technical Analysis
An evaluation method focusing on statistical trends gathered from market activity, such as price movement and volume.

### Technical Score
Component of the composite score based on price patterns, momentum indicators, and trading volumes (0-100 scale).

### Trade Simulation
A method of testing trading strategies using historical data without risking real capital.

## W
---

### Win Rate
The percentage of profitable trades in a strategy, calculated by dividing the number of winning trades by the total number of trades.
""")

# === Footer ===
latest_update = "April 15, 2025"  # Replace with actual value from data

st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {latest_update} | © 2025 DATA 606 Capstone - UMBC</p>
</div>
""", unsafe_allow_html=True)