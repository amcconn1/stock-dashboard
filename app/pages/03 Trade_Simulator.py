
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# === Page Configuration ===
st.set_page_config(page_title="Trade Simulator | Stock Dashboard", layout="wide")

# === Load Data ===
@st.cache_data
def load_data():
    df = pd.read_csv("https://drive.google.com/uc?id=1-2rHajs3BynUMsR9ljXVBZ0P4AvwKbZE", parse_dates=["date"])
    return df.sort_values("date")

data = load_data()

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

/* Strategy Card */
.strategy-card {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.strategy-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.strategy-title {
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 10px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.strategy-description {
    color: #e0e0e0;
    font-size: 15px;
    margin-bottom: 15px;
    line-height: 1.5;
}

/* Strategy selection options */
.strategy-option {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    cursor: pointer;
    border: 2px solid transparent;
    transition: all 0.2s ease;
}

.strategy-option:hover {
    background-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}

.strategy-option.selected {
    border-color: #7d5ee3;
    background-color: rgba(125, 94, 227, 0.2);
}

.strategy-option-title {
    font-size: 18px;
    font-weight: 600;
    color: white;
    margin-bottom: 5px;
}

.strategy-option-desc {
    font-size: 14px;
    color: #e0e0e0;
}

/* Results Summary */
.results-summary {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.results-title {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 15px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* KPI Metrics */
.metric-container {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(5px);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    margin-bottom: 15px;
    transition: all 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.metric-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
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

/* Trade Log Table */
.trade-table {
    width: 100%;
    max-width: 1000px;
    margin: 20px auto;
    border-collapse: collapse;
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
    border-radius: 8px;
    overflow-x: auto;
    animation: fadeIn 0.6s ease-out;
    text-align: center;
}

.trade-table th {
    background-color: rgba(0, 0, 0, 0.2);
    padding: 12px 15px;
    text-align: center;
    font-weight: 600;
    color: #ffffff;
    font-size: 16px;
}

.trade-table td {
    padding: 10px 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    color: #e0e0e0;
    font-size: 15px;
    text-align: center;
}

.trade-table tr:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transition: background-color 0.2s ease;
}

/* Signal styling */
.signal-buy {
    color: #4CAF50;
    font-weight: bold;
}

.signal-sell {
    color: #F44336;
    font-weight: bold;
}

.signal-hold {
    color: #FFC107;
    font-weight: bold;
}

/* P/L Gain & Loss Color */
.pnl-profit {
    color: #4CAF50;
    font-weight: bold;
}

.pnl-loss {
    color: #F44336;
    font-weight: bold;
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

/* Section title */
.section-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin: 30px 0 20px 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Date range indicator */
.date-range {
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

/* Strategy Stats */
.strategy-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 15px 0;
    justify-content: center;
}

.stat-badge {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 15px;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.2s ease;
}

.stat-badge:hover {
    transform: translateY(-2px);
    background-color: rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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

.chart-container2 {
    background-color: rgba(0, 0, 0, 0);
    backdrop-filter: blur(5px);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0);
    margin-bottom: 20px;
    border: 1px solid rgba(0, 0, 0, 0);
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

/* Slide-up animation */
@keyframes fadeSlideUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
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

/* Settings container */
.settings-container {
    background-color: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 25px;
}

.settings-header {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 15px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    text-align: center;
}

/* Strategy selector */
.strategy-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 15px 0;
    justify-content: center;
}

/* Capital selector */
.capital-selector {
    display: flex;
    justify-content: center;
    margin: 15px 0;
    gap: 10px;
}

.capital-option {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 10px 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 2px solid transparent;
}

.capital-option:hover {
    background-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}

.capital-option.selected {
    border-color: #7d5ee3;
    background-color: rgba(125, 94, 227, 0.2);
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

/* Date selector container */
.date-selector-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
    margin: 15px 0;
}

/* Radio button styling */
[data-testid="stRadio"] > div {
    display: flex;
    justify-content: center;
    gap: 20px;
}

[data-testid="stRadio"] label {
    color: white !important;
}

.run-button {
    display: block;
    background-color: rgba(125, 94, 227, 0.8);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 25px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    margin: 20px auto 10px auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.run-button:hover {
    background-color: rgba(125, 94, 227, 1);
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

/* No data message */
.no-data-message {
    background-color: rgba(255, 165, 0, 0.2);
    border-left: 4px solid #FFA500;
    padding: 15px;
    border-radius: 0 8px 8px 0;
    margin: 15px 0;
    color: #ffffff;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# === Title and Introduction ===
st.markdown("<div class='title'>📊 💲 Trade Simulator</div>", unsafe_allow_html=True)
st.markdown("""
<div class='subtitle'>
    Risk-Free Strategy Testing: Experiment with different trading approaches using real historical data to see how they would have performed. Build confidence in your investment decisions by understanding how various strategies behave across different market conditions without risking real capital.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-panel" style="border-left: 4px solid #7d5ee3;">
    <strong>How This Works:</strong> The simulator executes trades based on signal thresholds from your selected strategy. 
    It checks for signals every 7 days to avoid overtrading and uses realistic price data. 
    This simulation helps novice investors understand strategy performance without risking real capital.
    <p style="margin-top: 15px;color: orange; font-size: 16px; text-align: center">
        <strong> Remember that past performance is not indicative of future results. This simulator is for educational purposes only.</strong>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)


# === Strategy Settings - Now on Main Page ===
st.markdown("<div class='section-title'>Simulation Settings</div>", unsafe_allow_html=True)

strategies = {
    "Composite Score Strategy": {
        "desc": "This balanced approach uses a combination of fundamental, technical, and news sentiment factors to generate trading signals. This strategy performs best in markets with clear trends and stable fundamentals. Watch for divergences between component scores which may signal upcoming trend changes.",
        "thresholds": "Buy when composite score > 70, sell when < 40. Hold otherwise.",
        "column": "composite_score",
        "icon": "🧩"
    },
    "Technical Score Strategy": {
        "desc": "Focuses exclusively on price patterns, volume, and momentum indicators, ideal for trend-following traders. Technical strategies typically generate more frequent signals and higher turnover. This performs well in trending markets but may generate false signals during sideways periods.",
        "thresholds": "Buy when technical score > 70, sell when < 40. Hold otherwise.",
        "column": "technical_score",
        "icon": "📈"
    },
    "Fundamental Score Strategy": {
        "desc": "Based on company financial health metrics and valuations, suitable for long-term value investors. Fundamental apporaches work best with a timeframe ov over a year and a lower trading frequency often improves results with fundamental strategies. Pay attention to large score changes, which may indicate significant financial events.",
        "thresholds": "Buy when fundamental score > 70, sell when < 40. Hold otherwise.",
        "column": "fundamental_score",
        "icon": "📊"
    },
    "News Sentiment Score Strategy": {
        "desc": "Determines signals based purely on market perception and news coverage sentiment analysis. News sentiment strategies oftent identify short-term price movements before technical indicators. Be cautious of overreaction to news that may quickly reverse the market. Try combining this strategy with social media sentiment or another score for improved confirmation.",
        "thresholds": "Buy when news sentiment score > 0.7, sell when < 0.3. Hold otherwise.",
        "column": "news_sentiment_score",
        "icon": "📰"
    }
}

with st.container(): 
    # Strategy selection
    st.markdown("<p style='color: #ffffff; font-size: 16px; font-weight: 500; margin-bottom: 10px;'>1. Select a Strategy:</p>", unsafe_allow_html=True)
    
    st.markdown("""<style>.stRadio label {color: #ffffff !important;font-weight: 500;}.stRadio label p {color: #ffffff !important;}</style>
    """, unsafe_allow_html=True)

    strategy = st.radio(
        "Choose a Strategy",
        list(strategies.keys()),
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown(f"""
    <div class='strategy-card'>
        <div class='strategy-title'>{strategies[strategy]["icon"]} {strategy}</div>
        <div class='strategy-description'>{strategies[strategy]["desc"]}</div>
        <div style='padding: 8px 12px; color: #ffffff; background-color: rgba(0,0,0,0.2); border-radius: 8px; margin-top: 10px;'>
            <strong>Signal Rules:</strong> {strategies[strategy]["thresholds"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<p style='color: #ffffff; font-size: 16px; font-weight: 500; margin-bottom: 10px;'>2. Set Starting Capital:</p>", unsafe_allow_html=True)
        capital = st.radio("Dollar Amount:", [100, 1000, 10000], index=1, horizontal=True)
        
    with col2:
        st.markdown("<p style='color: #ffffff; font-size: 16px; font-weight: 500; margin-bottom: 10px;'>3. Choose Simulation Period:</p>", unsafe_allow_html=True)
        
        min_date = data["date"].min().date()
        max_date = data["date"].max().date()
        default_start = (max_date - timedelta(days=180))  
        default_start = max(default_start, min_date)  
        
        date_col1, date_col2 = st.columns(2)
        
        with date_col1:
            start_date = st.date_input(
                "Start Date:", 
                value=default_start, 
                min_value=min_date, 
                max_value=max_date
            )
            
        with date_col2:
            end_date = st.date_input(
                "End Date:", 
                value=max_date, 
                min_value=start_date, 
                max_value=max_date
            )
    
    st.markdown(f"""
    <div style='text-align: center''>
        <div class='date-range'>
            📅 Simulation Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}
            ({(end_date - start_date).days} days)
        </div>
    </div>
    """, unsafe_allow_html=True)

filtered_data = data[(data["date"] >= pd.to_datetime(start_date)) & 
                    (data["date"] <= pd.to_datetime(end_date))].copy()

if filtered_data.empty:
    st.markdown("""
    <div class="no-data-message">
        <strong>No data available for the selected date range.</strong> Please adjust your simulation period.
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# === Explicit score column mapping ===
score_column = strategies[strategy]["column"]
signal_col = "signal"

# === Set thresholds ===
buy_thresh, sell_thresh = (70, 40) if "sentiment" not in score_column else (0.7, 0.3)
filtered_data[signal_col] = filtered_data[score_column].apply(
    lambda x: "Buy" if x > buy_thresh else ("Sell" if x < sell_thresh else "Hold")
)

# === Simulate trades (once per 7 days) ===
cash = capital
shares = 0
trade_log = []
portfolio_values = []
last_trade_date = None

for i, row in filtered_data.iterrows():
    price = row["close"]
    date = row["date"]
    signal = row[signal_col]
    portfolio_value = cash + shares * price

    portfolio_values.append({
        "date": date,
        "value": portfolio_value,
        "signal": signal,
        "shares": shares,
        "cash": cash
    })

    if last_trade_date and (date - last_trade_date).days < 7:
        continue

    if signal == "Buy" and cash >= price:
        buy_shares = int(cash // price)  
        if buy_shares > 0:
            shares += buy_shares
            spend = buy_shares * price
            cash -= spend
            trade_log.append({
                "Date": date,
                "Action": "Buy",
                "Price": price,
                "Shares": buy_shares,
                "Total": spend
            })
            last_trade_date = date
    elif signal == "Sell" and shares > 0:
        sell_shares = shares  
        proceeds = sell_shares * price
        shares = 0
        cash += proceeds
        trade_log.append({
            "Date": date,
            "Action": "Sell",
            "Price": price,
            "Shares": sell_shares,
            "Total": proceeds
        })
        last_trade_date = date

# === Calculate final equity and performance metrics ===
final_equity = cash + shares * filtered_data.iloc[-1]["close"]
total_return = ((final_equity - capital) / capital) * 100
annualized_return = total_return / (len(filtered_data) / 252) if len(filtered_data) > 0 else 0

portfolio_df = pd.DataFrame(portfolio_values)

if not portfolio_df.empty:
    portfolio_df['running_max'] = portfolio_df['value'].cummax()
    portfolio_df['drawdown'] = (portfolio_df['value'] - portfolio_df['running_max']) / portfolio_df['running_max'] * 100
    max_drawdown = portfolio_df['drawdown'].min()
else:
    max_drawdown = 0

st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)

# === Display Performance Summary ===
st.markdown("<div class='section-title'>Performance Summary</div>", unsafe_allow_html=True)

num_trades = len(trade_log)
num_buys = sum(1 for trade in trade_log if trade['Action'] == 'Buy')
num_sells = sum(1 for trade in trade_log if trade['Action'] == 'Sell')
final_pnl = running_pnl if 'running_pnl' in locals() else 0  # Get final P/L if available
pnl_color = "#4CAF50" if final_pnl >= 0 else "#F44336"
pnl_icon = "📈" if final_pnl >= 0 else "📉"

st.markdown(f"""
<div class="summary-block">
    <h4>📈 Overview</h4>
        The <strong>{strategy}</strong> generated a 
        <strong style="color: {'#4CAF50' if total_return >= 0 else '#F44336'};">{total_return:.2f}%</strong> 
        total return over the {(end_date - start_date).days}-day simulation period. Starting with 
        <strong>${capital:,}</strong>, your final portfolio value would be 
        <strong>${final_equity:,.2f}</strong>.
    </p>
    <p>
        During this period, the maximum drawdown (largest portfolio value decline) was 
        <strong style="color: #F44336;">{max_drawdown:.2f}%</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>${final_equity:,.2f}</div>
        <div class='kpi-label'>Final Portfolio Value</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    return_color = "#4CAF50" if total_return >= 0 else "#F44336"
    return_icon = "📈" if total_return >= 0 else "📉"
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value' style='color:{return_color};'>{return_icon} {total_return:.2f}%</div>
        <div class='kpi-label'>Total Return</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value'>🔄 {num_trades}</div>
        <div class='kpi-label'>Total Trades</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='card'>
        <div class='kpi-value' style='color:{pnl_color};'>{pnl_icon} ${abs(final_pnl):.2f}</div>
        <div class='kpi-label'>{'Net Profit' if final_pnl >= 0 else 'Net Loss'}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class='strategy-stats'>
    <span class='stat-badge' style="border-left: 3px solid #4CAF50;">🛒 Buy Signals: {num_buys}</span>
    <span class='stat-badge' style="border-left: 3px solid #F44336;">💰 Sell Signals: {num_sells}</span>
    <span class='stat-badge' style="border-left: 3px solid #FFC107;">⚠️ Max Drawdown: {max_drawdown:.2f}%</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)


# === Portfolio Value Chart ===
st.markdown("<div class='section-title'>Portfolio Performance</div>", unsafe_allow_html=True)

if not portfolio_df.empty:
    initial_price = filtered_data.iloc[0]["close"]
    final_price = filtered_data.iloc[-1]["close"]
    shares_buy_hold = capital / initial_price
    
    portfolio_df['buy_hold_value'] = filtered_data['close'] * shares_buy_hold
    
    strategy_final = portfolio_df['value'].iloc[-1]
    buyhold_final = portfolio_df['buy_hold_value'].iloc[-1]
    outperformance = ((strategy_final - buyhold_final) / buyhold_final) * 100
    
    st.markdown("""
    <div class="info-panel" style="border-left: 4px solid #7d5ee3;">
        The purple line shows your portfolio value following the selected strategy. 
        The blue dashed line represents a simple "buy & hold" approach for comparison.
        Green triangles indicate buy signals, red triangles show sell signals.
    </div>
    """, unsafe_allow_html=True)
    
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=portfolio_df["date"],
        y=portfolio_df["value"],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#7d5ee3', width=3),  # Updated to purple to match theme
        hovertemplate='Date: %{x}<br>Value: $%{y:.2f}<br>Signal: %{text}<extra></extra>',
        text=portfolio_df["signal"]
    ))
    
    fig.add_trace(go.Scatter(
        x=portfolio_df["date"],
        y=portfolio_df["buy_hold_value"],
        mode='lines',
        name='Buy & Hold',
        line=dict(color='#2196F3', width=2, dash='dash'),
        hovertemplate='Date: %{x}<br>Value: $%{y:.2f}<extra></extra>'
    ))
    
    buy_points = []
    for trade in trade_log:
        if trade['Action'] == 'Buy':
            matching_portfolio = portfolio_df[portfolio_df['date'] == trade['Date']]
            if not matching_portfolio.empty:
                buy_points.append({
                    'date': trade['Date'],
                    'value': matching_portfolio.iloc[0]['value']
                })
    
    if buy_points:
        buy_df = pd.DataFrame(buy_points)
        fig.add_trace(go.Scatter(
            x=buy_df["date"],
            y=buy_df["value"],
            mode='markers',
            name='Buy Signal',
            marker=dict(color='#4CAF50', size=12, symbol='triangle-up', line=dict(color='white', width=1)),
            hovertemplate='Buy at: $%{y:.2f}<extra></extra>'
        ))
    
    sell_points = []
    for trade in trade_log:
        if trade['Action'] == 'Sell':
            matching_portfolio = portfolio_df[portfolio_df['date'] == trade['Date']]
            if not matching_portfolio.empty:
                sell_points.append({
                    'date': trade['Date'],
                    'value': matching_portfolio.iloc[0]['value']
                })
    
    if sell_points:
        sell_df = pd.DataFrame(sell_points)
        fig.add_trace(go.Scatter(
            x=sell_df["date"],
            y=sell_df["value"],
            mode='markers',
            name='Sell Signal',
            marker=dict(color='#F44336', size=12, symbol='triangle-down', line=dict(color='white', width=1)),
            hovertemplate='Sell at: $%{y:.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,font=dict(color='white')),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(255, 255, 255, 0.07)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#ffffff'),
            title_font=dict(color='#ffffff')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            tickfont=dict(color='#ffffff'),
            title_font=dict(color='#ffffff')
        ),
        font=dict(color='white'),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
        
else:
    st.info("No portfolio data available to display the chart.")

st.markdown("<hr style='margin-top: 15px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.2);' />", unsafe_allow_html=True)

# === Transaction Log ===
st.markdown("<div class='section-title'>Transaction History</div>", unsafe_allow_html=True)

st.markdown("""
<div class="info-panel" style="border-left: 4px solid #7d5ee3;">
    This table shows all executed trades during the simulation period. The Running P/L column indicates
    the cumulative profit or loss after each transaction, helping you track performance over time.
</div>
""", unsafe_allow_html=True)

if trade_log:
    trades_df = pd.DataFrame(trade_log)

    if "P/L" not in trades_df.columns:
        trades_df["P/L"] = None
        running_pnl = 0

        for i in range(len(trades_df)):
            if trades_df.iloc[i]["Action"] == "Buy":
                running_pnl -= trades_df.iloc[i]["Total"]
            else:  
                running_pnl += trades_df.iloc[i]["Total"]
            trades_df.at[i, "P/L"] = running_pnl
    
    trades_html = """
    <div class='chart-container2' style='padding: 0;'>
        <div style='max-height: 400px; overflow-y: auto;'>
            <table class='trade-table'>
    """
    
    trades_html += "<thead><tr>"
    trades_html += "<th>Date</th>"
    trades_html += "<th>Action</th>"
    trades_html += "<th>Price</th>"
    trades_html += "<th>Shares</th>"
    trades_html += "<th>Total</th>"
    trades_html += "<th>Running P/L</th>"
    trades_html += "</tr></thead>"
    
    trades_html += "<tbody>"
    for _, row in trades_df.iterrows():
        trades_html += "<tr>"
        
        date_str = row["Date"].strftime('%Y-%m-%d') if isinstance(row["Date"], pd.Timestamp) else row["Date"]
        trades_html += f"<td>{date_str}</td>"
        
        action_class = "signal-buy" if row["Action"] == "Buy" else "signal-sell"
        trades_html += f"<td class='{action_class}'>{row['Action']}</td>"
        
        trades_html += f"<td>${row['Price']:.2f}</td>"
        
        trades_html += f"<td>{int(row['Shares'])}</td>"
        
        trades_html += f"<td>${row['Total']:.2f}</td>"
        
        pnl_class = "pnl-profit" if row["P/L"] >= 0 else "pnl-loss"
        trades_html += f"<td class='{pnl_class}'>${row['P/L']:.2f}</td>"
        
        trades_html += "</tr>"
    trades_html += "</tbody></table></div></div>"
    
    st.markdown(trades_html, unsafe_allow_html=True)
    
else:
    st.markdown("""
    <div class="summary-block" style="text-align: center; padding: 30px;">
        <img src="https://img.icons8.com/fluency/96/000000/empty-box.png" style="opacity:0.6; width:60px; margin-bottom:10px;">
        <p style="color: #e0e0e0; font-size: 18px; margin-bottom: 10px;">No trades were executed during this period</p>
        <p style="color: #c0c0c0; font-size: 14px;">Try adjusting your strategy parameters or time period</p>
    </div>
    """, unsafe_allow_html=True)


# === Raw Data View ===
with st.expander("View Raw Simulation Data"):
    simulation_data = filtered_data[["date", "close", score_column, signal_col]].rename(
        columns={score_column: "Score", signal_col: "Signal"}
    )
    simulation_data["date"] = simulation_data["date"].dt.strftime('%Y-%m-%d')
    simulation_data["close"] = simulation_data["close"].map('${:,.2f}'.format)
    simulation_data["Score"] = simulation_data["Score"].map('{:.2f}'.format)
    
    st.dataframe(simulation_data, use_container_width=True)


# === Footer ===
st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {data["date"].max().strftime('%B %d, %Y')} | © 2025 DATA 606 Capstone - Group Two</p>
</div>
""", unsafe_allow_html=True)