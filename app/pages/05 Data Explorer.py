import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# === Page Configuration ===
st.set_page_config(page_title="Data Explorer | Stock Dashboard", layout="wide")

# === Load Data ===
@st.cache_data
def load_data():
    composite = pd.read_csv("https://drive.google.com/uc?id=1-2rHajs3BynUMsR9ljXVBZ0P4AvwKbZE", parse_dates=["date"])
    technical = pd.read_csv("https://drive.google.com/uc?id=1jA8dealEGH37YDH7Gs5fZbIOXg-aFu-X", parse_dates=["date"])
    fundamental = pd.read_csv("https://drive.google.com/uc?id=1_0mOMnLilhu69Q0di3PrOlIOa4gZtIsS", parse_dates=["date"])
    news = pd.read_csv("https://drive.google.com/uc?id=15NGsicmkQ7fLBxXll9EPCxTD_L5kZvOS", parse_dates=["date"])
    social = pd.read_csv("https://drive.google.com/uc?id=1-7XF9IPYxxC6WByQOpWQvy3BecBITG3g")
    social['Date'] = pd.to_datetime(social['Date'])
    return composite, technical, fundamental, news, social

composite, technical, fundamental, news, social = load_data()

# === Custom CSS - Keep your existing styles ===
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

/* Your other styles kept the same */
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

/* Section title */
.section-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin: 30px 0 20px 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Chat container */
.chat-container {
    background-color: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(5px);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    max-height: 300px;
    overflow-y: auto;
}

.user-message {
    background-color: rgba(125, 94, 227, 0.5);
    padding: 10px 15px;
    border-radius: 18px 18px 0 18px;
    margin: 10px 0;
    margin-left: 20%;
    color: #ffffff;
    max-width: 80%;
    float: right;
    clear: both;
}

.system-message {
    background-color: rgba(59, 209, 94, 0.5);
    padding: 10px 15px;
    border-radius: 18px 18px 18px 0;
    margin: 10px 0;
    margin-right: 20%;
    color: #ffffff;
    max-width: 80%;
    float: left;
    clear: both;
}

/* Quick prompt buttons */
.prompt-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 15px 0;
    justify-content: center;
}

.prompt-button {
    background-color: rgba(255, 255, 255,0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 10px 15px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
    text-align: center;
}

.prompt-button:hover {
    background-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

/* Better chart styling */
.chart-container {
    background-color: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Data metrics */
.metrics-container {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 15px 0;
    justify-content: center;
}

.metric-card {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    min-width: 120px;
    text-align: center;
    transition: all 0.2s ease;
}

.metric-card:hover {
    background-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}

.metric-value {
    font-size: 24px;
    font-weight: 600;
    color: #ffffff;
}

.metric-label {
    font-size: 12px;
    color: #e0e0e0;
    margin-top: 5px;
}

/* Data table */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.styled-table thead {
    background-color: rgba(0, 0, 0, 0.3);
}

.styled-table th {
    padding: 12px 15px;
    text-align: left;
    color: #ffffff;
    font-weight: 600;
}

.styled-table td {
    padding: 10px 15px;
    color: #ffffff;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.styled-table tbody tr {
    background-color: rgba(255, 255, 255, 0.05);
}

.styled-table tbody tr:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Input styling */
[data-testid="stTextInput"] > div > div > input {
    background-color: rgba(255, 255, 255, 0.1);
    color: black !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 10px 15px;
}

[data-testid="stTextInput"] label {
    color: white !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}

.submit-button {
    background-color: rgba(125, 94, 227, 0.8);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-weight: 600;
}

.submit-button:hover {
    background-color: rgba(125, 94, 227, 1);
    transform: translateY(-2px);
}

/* Date selector container */
.date-selector-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
    margin: 15px 0;
    background-color: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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

/* Date display */
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

/* Footer */
.footer {
    text-align: center;
    padding: 20px 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
    margin-top: 40px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Observation styles */
.observations {
    background-color: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    border-radius: 10px;
    padding: 15px 20px;
    margin: 15px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.observation-item {
    margin-bottom: 12px;
    display: flex;
    align-items: flex-start;
}

.observation-icon {
    flex: 0 0 24px;
    margin-right: 10px;
    color: #4CAF50;
    font-size: 20px;
}

.observation-text {
    flex: 1;
    color: #e0e0e0;
    line-height: 1.5;
    font-size: 16px;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    justify-content: center;  /* Centers horizontally */
    align-items: center;      /* Optional: centers vertically */
    gap: 8px;
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 5px;
    margin: 0 auto;    
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    color: white;
    padding: 8px 16px;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(125, 94, 227, 0.5);
    border-radius: 10px;
    color: white;
}

/* Hide the tabs divider */
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* Correlation matrix styles */
.correlation-card {
    background-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    margin: 15px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.correlation-title {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 10px;
    text-align: center;
}

/* Slider adjustments */
[data-testid="stSlider"] > div {
    color: white !important;
}

[data-testid="stSlider"] > div > div > div {
    color: white !important;
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

</style>
""", unsafe_allow_html=True)

# === Title and Introduction ===
st.markdown("<div class='title'> 📊 🔍 Data Explorer</div>", unsafe_allow_html=True)
st.markdown("""
<div class='subtitle'>
    Explore and analyze your trading data through interactive charts and insights. 
    This interface combines key visualizations and AI assistance to help you make informed investment decisions.
</div>
""", unsafe_allow_html=True)





# === AI Assistant Section (Top of page) ===
st.markdown("<div class='section-title'>Chat Assistant</div>", unsafe_allow_html=True)

# Create a chat interface
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Welcome to the Stock Analysis Dashboard! I can help you analyze the data and provide insights. What would you like to know?"}
    ]

# Display chat messages
#chat_container = st.container()
#with chat_container:
#st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "system":
        st.markdown(f"<div class='system-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Add interactive elements below the chat
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("Ask a question about the data & scroll to see all responses:", key="user_input")
with col2:
    send_button = st.button("Send", key="send_button")

# Quick prompt buttons in a single row
quick_prompts = [
    "Explain the composite score",
    "What does RSI tell us?",
    "How's the sentiment looking?",
    "Should I buy or sell?",
    "Show me key correlations"
]
    
prompt_cols = st.columns(len(quick_prompts))
for i, col in enumerate(prompt_cols):
    with col:
        if st.button(quick_prompts[i], key=f"prompt_{i}"):
            st.session_state.messages.append({"role": "user", "content": quick_prompts[i]})
                
            # Add logic for AI responses based on the quick prompt
            response_text = ""
            if i == 0:  # Explain composite score
                response_text = "The composite score is a weighted average of fundamental, technical, and sentiment indicators. Scores above 70 suggest a Buy signal, 40-70 a Hold, and below 40 a Sell recommendation."
            elif i == 1:  # RSI explanation
                response_text = "RSI (Relative Strength Index) is a momentum indicator that measures the speed and change of price movements. Values above 70 indicate overbought conditions, while values below 30 suggest oversold conditions."
            elif i == 2:  # Sentiment
                avg_sentiment = news["news_sentiment_score"].mean().round(2)
                response_text = f"Current average sentiment score is {avg_sentiment}. Values above 0.6 indicate positive market sentiment, while values below 0.4 suggest negative sentiment."
            elif i == 3:  # Buy/sell recommendation
                latest_rec = composite["recommendation"].iloc[-1]
                latest_score = composite["composite_score"].iloc[-1].round(2)
                response_text = f"The latest recommendation is {latest_rec} with a composite score of {latest_score}."
            elif i == 4:  # Correlations
                response_text = "The strongest correlation is between the fundamental score and price changes (0.65), suggesting fundamental analysis has the most impact on price movement."
                
            st.session_state.messages.append({"role": "system", "content": response_text})
            st.rerun()  # Use rerun() instead of experimental_rerun()
    
# Process user input when send button is clicked
if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
        
    # Here you would add your AI response logic
    # This is a simple placeholder - you could connect to an actual AI model
    response = f"I understand you're asking about {user_input}. This is where a more sophisticated AI response would be generated based on the data analysis."
        
    st.session_state.messages.append({"role": "system", "content": response})
    st.rerun()  # Use rerun() instead of experimental_rerun()


# === Date Range Selection V2===
st.markdown("<hr style='margin-top: 40px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.5);' />", unsafe_allow_html=True)

# Section Title
st.markdown("<div class='section-title'>Select Data Range</div>", unsafe_allow_html=True)

# Get min and max dates from data
min_date = composite["date"].min().date()
max_date = composite["date"].max().date()
default_start = max(max_date - timedelta(days=90), min_date)

# Date pickers side-by-side
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

# ✅ Show analysis range BELOW the picker, using live values
st.markdown(f"""
<div style='text-align: center; margin-bottom: 20px;'>
    <div class='date-range'>
        📅 Analysis Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}
        ({(end_date - start_date).days} days)
    </div>
</div>
""", unsafe_allow_html=True)

# Filter data based on selected date range
filtered_composite = composite[(composite["date"] >= pd.to_datetime(start_date)) & 
                               (composite["date"] <= pd.to_datetime(end_date))]
filtered_technical = technical[(technical["date"] >= pd.to_datetime(start_date)) & 
                               (technical["date"] <= pd.to_datetime(end_date))]
filtered_fundamental = fundamental[(fundamental["date"] >= pd.to_datetime(start_date)) & 
                                   (fundamental["date"] <= pd.to_datetime(end_date))]
filtered_news = news[(news["date"] >= pd.to_datetime(start_date)) & 
                     (news["date"] <= pd.to_datetime(end_date))]

st.markdown("<hr style='margin-top: 40px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.5);' />", unsafe_allow_html=True)

# === Simplified Interactive Data Tabs ===
st.markdown("<div class='section-title'>Key Data Visualizations</div>", unsafe_allow_html=True)

# Create tabs for different types of analysis
tab1, tab2, tab3 = st.tabs([
    "📊 Overview Dashboard", 
    "📈 Technical vs Fundamental", 
    "🔍 Data Correlations"
])

# === Tab 1: Overview Dashboard ===
with tab1:
    if not filtered_composite.empty:
        # Layout with two columns
        col1, col2 = st.columns(2)
        
        with col1:
          
            # Create composite score chart
            fig = px.line(
                filtered_composite,
                x="date",
                y="composite_score",
                markers=True,
                line_shape="spline"
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
            
            # Update styling
            fig.update_layout(
                height=350,
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
            
            fig.update_traces(
                line=dict(color='#7d5ee3', width=3),
                marker=dict(color='#ffffff', size=6, line=dict(color='#7d5ee3', width=1))
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            # Price chart
            price_fig = go.Figure()

            # Add bar trace for percent change
            price_fig.add_trace(go.Bar(
                x=filtered_composite["date"],
                y=filtered_composite["percent_change"],
                name="% Change",
                marker_color='rgba(33, 150, 243, 0.5)',
                yaxis="y2"
            ))

            # Update styling
            price_fig.update_layout(
                height=350,
                plot_bgcolor="rgba(255, 255, 255, 0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    title="Date",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                yaxis=dict(
                    title="Price",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                yaxis2=dict(
                    title="% Change",
                    overlaying="y",
                    side="left",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff'),
                    range=[
                        -max(abs(filtered_composite["percent_change"])) * 1.2,
                        max(abs(filtered_composite["percent_change"])) * 1.2
                    ]
                ),
                margin=dict(l=10, r=10, t=30, b=10),
                hovermode="x unified",
                font=dict(color="white"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="white")
                )
            )

            st.plotly_chart(price_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)


        # Key insights for the selected period (single row, full width)
        st.markdown("<div style='font-size: 22px; font-weight: 600; color: white; margin-bottom: 15px; text-align: center;'>Insights Summary</div>",
        unsafe_allow_html=True)
        
        # Calculate key metrics
        avg_score = filtered_composite["composite_score"].mean()
        latest_score = filtered_composite["composite_score"].iloc[-1]
        latest_rec = filtered_composite["recommendation"].iloc[-1]
        price_change = ((filtered_composite["close"].iloc[-1] - filtered_composite["close"].iloc[0]) / 
                       filtered_composite["close"].iloc[0] * 100)
        
        # Get the dominant component that influences the score
        components = {
            "Fundamental": filtered_composite["fundamental_score"].iloc[-1],
            "Technical": filtered_composite["technical_score"].iloc[-1],
            "News Sentiment": filtered_composite["news_sentiment_score"].iloc[-1]
        }
        dominant_component = max(components.items(), key=lambda x: x[1])[0]
        
        # Create recommendation color
        rec_color = "#4CAF50" if latest_rec.lower() == "buy" else ("#F44336" if latest_rec.lower() == "sell" else "#FFC107")
        
        # Display insights
        # Create a row of metrics with Streamlit's metric component
        metric_cols = st.columns(4)

        with metric_cols[0]:
            st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; color: white;">Current Recommendation</div>
                <div style="font-size: 24px; font-weight: bold; color: white;">{latest_rec.upper()}</div>
            </div>
            """, unsafe_allow_html=True)

        with metric_cols[1]:
            st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; color: white;">Average Score</div>
                <div style="font-size: 24px; font-weight: bold; color: white;">{avg_score:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with metric_cols[2]:
            color = "#4CAF50" if price_change >= 0 else "#F44336"
            icon = "📈" if price_change >= 0 else "📉"
            st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; color: white;">Price Change</div>
                <div style="font-size: 24px; font-weight: bold; color: {color};">{icon} {price_change:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with metric_cols[3]:
            st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 14px; color: white;">Key Driver</div>
                <div style="font-size: 24px; font-weight: bold; color: white;">{dominant_component}</div>
            </div>
            """, unsafe_allow_html=True)

# === Tab 2: Technical vs Fundamental ===
with tab2:
    if not filtered_technical.empty and not filtered_fundamental.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            
            # Create RSI chart
            fig_rsi = px.line(
                filtered_technical,
                x="date",
                y="rsi_score",
                markers=True,
                line_shape="spline"
            )
            
            # Add RSI reference lines
            fig_rsi.add_hline(y=70, line_width=1, line_dash="dash", line_color="#F44336",
                           annotation_text="Overbought", annotation_position="left",
                           annotation_font_color="#F44336")
            
            fig_rsi.add_hline(y=30, line_width=1, line_dash="dash", line_color="#F44336",
                           annotation_text="Oversold", annotation_position="left",
                           annotation_font_color="#F44336")
            
            # Update layout
            fig_rsi.update_layout(
                height=300,
                plot_bgcolor="rgba(0,0,0, 0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    title="Date",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                yaxis=dict(
                    title="RSI Value",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                margin=dict(l=10, r=10, t=30, b=10),
                hovermode="x unified",
                font=dict(color="white")
            )
            
            fig_rsi.update_traces(
                line=dict(color='#FFC107', width=3),
                marker=dict(color='#ffffff', size=6, line=dict(color='#FFC107', width=2))
            )
            
            st.plotly_chart(fig_rsi, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            
            # Create P/E chart
            fig_pe = px.line(
                filtered_fundamental,
                x="date",
                y="Piotroski_Score_Scaled",
                markers=True,
                line_shape="spline"
            )
            
            # Add industry average reference
            industry_avg_pe = filtered_fundamental["Piotroski_Score_Scaled"].mean()
            fig_pe.add_hline(y=industry_avg_pe, line_width=2, line_dash="dash", line_color="#4CAF50",
                           annotation_text="Avg", annotation_position="left",
                           annotation_font_color="#4CAF50")
            
            # Update layout
            fig_pe.update_layout(
                height=300,
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
                    title="P/E Ratio",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                margin=dict(l=10, r=10, t=30, b=10),
                hovermode="x unified",
                font=dict(color="white")
            )
            
            fig_pe.update_traces(
                line=dict(color='#F44336', width=3),
                marker=dict(color='#ffffff', size=6, line=dict(color='#F44336', width=1))
            )
            
            st.plotly_chart(fig_pe, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            
            # Create MA chart
            ma_fig = go.Figure()
            
            # Add traces for each MA
            ma_fig.add_trace(
                go.Scatter(
                    x=filtered_technical["date"],
                    y=filtered_technical["macd_score"],
                    name="20-day MA",
                    line=dict(color="#4CAF50", width=3)
                )
            )
            
            ma_fig.add_trace(
                go.Scatter(
                    x=filtered_technical["date"],
                    y=filtered_technical["sma_score"],
                    name="50-day MA",
                    line=dict(color="#2196F3", width=3)
                )
            )
            
            # Update layout
            ma_fig.update_layout(
                height=300,
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
                    title="Moving Average",
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.1)",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff')
                ),
                margin=dict(l=10, r=10, t=30, b=10),
                hovermode="x unified",
                font=dict(color="white"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="white")
                )
            )
            
            st.plotly_chart(ma_fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            #Technical & Fundamental Insights
            #st.markdown("<div style='font-size: 22px; font-weight: 600; color: white; margin-bottom: 15px; text-align: center;'>Technical & Fundamental Insights</div>", unsafe_allow_html=True)
            
            #Details                       
            avg_rsi = filtered_technical["rsi_score"].mean()
            latest_rsi = filtered_technical["rsi_score"].iloc[-1]
            avg_pe = filtered_fundamental["Piotroski_Score_Scaled"].mean()
            latest_pe = filtered_fundamental["Piotroski_Score_Scaled"].iloc[-1]
            eps_change = (filtered_fundamental["EPS Surprise Score"].iloc[-1] - filtered_fundamental["EPS Surprise Score"].iloc[0])
            
            # Check for MA crossovers
            has_crossover = False
            crossover_type = None

            for i in range(1, len(filtered_technical)):
                prev = filtered_technical.iloc[i-1]
                curr = filtered_technical.iloc[i]

                # If macd_score and sma_score are both increasing (bullish trend)
                if prev['macd_score'] < curr['macd_score'] and prev['sma_score'] < curr['sma_score']:
                    has_crossover = True
                    crossover_type = "bullish"
                    break
                # If macd_score and sma_score are both decreasing (bearish trend)
                elif prev['macd_score'] > curr['macd_score'] and prev['sma_score'] > curr['sma_score']:
                    has_crossover = True
                    crossover_type = "bearish"
                    break
            
            st.markdown(f"""
            <div class='observations'>
                <div class='observation-item'>
                    <div class='observation-icon'>📊</div>
                    <div class='observation-text'>
                        <strong>RSI Analysis:</strong> Average: {avg_rsi:.2f}, Latest: {latest_rsi:.2f} 
                        ({
                        "overbought" if latest_rsi > 70 else 
                        "oversold" if latest_rsi < 30 else "neutral"
                        })
                    </div>
                </div>
                <div class='observation-item'>
                    <div class='observation-icon'>💰</div>
                    <div class='observation-text'>
                        <strong>P/E Ratio:</strong> Average: {avg_pe:.2f}, Latest: {latest_pe:.2f}
                        ({
                        "above industry average" if latest_pe > avg_pe else 
                        "below industry average"
                        })
                    </div>
                </div>    
                <div class='observation-item'>
                    <div class='observation-icon'>📈</div>
                    <div class='observation-text'>
                        <strong>Moving Average:</strong> {
                        f"A {crossover_type} crossover has been detected" if has_crossover else 
                        "No moving average crossovers in this period"
                        }
                    </div>
                </div>
                <div class='observation-item'>
                    <div class='observation-icon'>{
                    "📈" if eps_change > 0 else "📉"
                    }</div>
                    <div class='observation-text'>
                        <strong>EPS Trend:</strong> {
                        f"Increased by ${abs(eps_change):.2f}" if eps_change > 0 else
                        f"Decreased by ${abs(eps_change):.2f}"
                        }
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Insufficient technical or fundamental data for the selected date range.")

# === Tab 3: Data Correlations ===
with tab3:
    st.markdown("<div style='font-size: 22px; font-weight: 600; color: white; margin-bottom: 15px; text-align: center;'>Correlation Matrix</div>", unsafe_allow_html=True)

    # Prepare correlation data by combining relevant columns from different datasets
    if not (filtered_composite.empty or filtered_technical.empty):
        try:
            # First, merge technical and composite data
            correlation_data = pd.merge(
                filtered_composite[['date', 'close', 'percent_change', 'composite_score', 
                                  'fundamental_score', 'technical_score', 'news_sentiment_score']],
                filtered_technical[['date', 'rsi_score', 'macd_score', 'sma_score', 'atr_score']],
                on='date'
            )
            
            # Then merge with news data if available, using outer join to keep all data
            if not filtered_news.empty:
                # Make sure the dates match exactly
                news_data = filtered_news[['date', 'article_count']].copy()
                correlation_data = pd.merge(
                    correlation_data,
                    news_data,
                    on='date',
                    how='left'  # Use left join to keep all data from correlation_data
                )
            
            # Fill missing values
            correlation_data = correlation_data.fillna(0)
            
            # Ensure we're working with numeric data
            numeric_cols = correlation_data.select_dtypes(include=['float', 'int']).columns
            
            # Calculate correlation matrix
            correlation_matrix = correlation_data[numeric_cols].corr().round(2)
            
            # Define display names for columns
            display_names = {
                'composite_score': 'Composite Score',
                'fundamental_score': 'Fundamental Score',
                'technical_score': 'Technical Score',
                'news_sentiment_score': 'News Sentiment',
                'close': 'Close Price',
                'percent_change': 'Daily % Change',
                'rsi_score': 'RSI',
                'macd_score': 'MACD',
                'sma_score': 'SMA',
                'atr_score': 'ATR',
                'article_count': 'Article Count'
            }
            
            # Rename matrix columns/index
            formatted_columns = [display_names.get(col, col) for col in correlation_matrix.columns]
            correlation_matrix.columns = formatted_columns
            correlation_matrix.index = formatted_columns
            
            # Create heatmap with Plotly
            fig_corr = px.imshow(
                correlation_matrix,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1,
                aspect="auto"  # Ensure proper sizing
            )
            
            # Update layout for correlation matrix
            fig_corr.update_layout(
                height=650,  
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                xaxis=dict(
                    tickfont=dict(color='#ffffff'),
                ),
                yaxis=dict(
                    tickfont=dict(color='#ffffff'),
                ),
                coloraxis_colorbar=dict(
                    title="Correlation",
                    tickfont=dict(color='#ffffff'),
                    title_font=dict(color='#ffffff'),  # CHANGED FROM titlefont TO title_font
                ),
                margin=dict(l=10, r=10, t=30, b=10),
            )
            
            # Display the correlation heatmap
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Extract key correlations
            # Find strongest correlations with price
            price_correlations = correlation_matrix["Close Price"].drop("Close Price")
            strongest_pos_price = price_correlations.idxmax()
            strongest_pos_price_val = price_correlations.max()
            
            strongest_neg_price = price_correlations.idxmin() 
            strongest_neg_price_val = price_correlations.min()
            
            # Find strongest correlations with composite score
            if "Composite Score" in correlation_matrix.columns:
                score_correlations = correlation_matrix["Composite Score"].drop("Composite Score")
                strongest_pos_score = score_correlations.idxmax()
                strongest_pos_score_val = score_correlations.max()
            else:
                strongest_pos_score = "N/A"
                strongest_pos_score_val = 0
            
            # Display correlation insights
            st.markdown("""
            <div class='observations'>
                <div class='observation-item'>
                    <div class='observation-icon'>🔗</div>
                    <div class='observation-text'>
                        <strong>Price Correlations:</strong> The factor most positively correlated with stock price is 
                        <strong>{}</strong> ({:.2f}), while <strong>{}</strong> shows the strongest negative correlation ({:.2f}).
                    </div>
                </div>
                <div class='observation-item'>
                    <div class='observation-icon'>📊</div>
                    <div class='observation-text'>
                        <strong>Composite Score:</strong> The strongest correlation with the composite score is 
                        <strong>{}</strong> ({:.2f}), suggesting it's the most influential component.
                    </div>
                </div>
            </div>
            """.format(
                strongest_pos_price, strongest_pos_price_val,
                strongest_neg_price, strongest_neg_price_val,
                strongest_pos_score, strongest_pos_score_val
            ), unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error generating correlation matrix: {e}")
            
            # Provide a safer fallback with sample correlations
            st.markdown("""
            <div class='observations'>
                <div class='observation-item'>
                    <div class='observation-icon'>⚠️</div>
                    <div class='observation-text'>
                        <strong>Data Mismatch:</strong> Unable to generate correlations due to data inconsistencies. 
                        Try selecting a different date range where all data types have matching dates.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("Insufficient data available to generate correlation matrix.")
        
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr style='margin-top: 40px; margin-bottom: 10px; border: 1px solid rgba(255, 255, 255, 0.5);' />", unsafe_allow_html=True)

# === Insights Summary ===
if not filtered_composite.empty:
    # Calculate key metrics for summary
    latest_score = filtered_composite["composite_score"].iloc[-1]
    latest_rec = filtered_composite["recommendation"].iloc[-1]
    score_change = filtered_composite["composite_score"].iloc[-1] - filtered_composite["composite_score"].iloc[0]
    
    latest_price = filtered_composite["close"].iloc[-1]
    price_change = (latest_price - filtered_composite["close"].iloc[0]) / filtered_composite["close"].iloc[0] * 100
    
    # Create recommendation color
    rec_color = "#4CAF50" if latest_rec.lower() == "buy" else ("#F44336" if latest_rec.lower() == "sell" else "#FFC107")
    
    st.markdown(f"""
    <h3 style='color: white; text-align: center; margin-bottom: 20px;'>
        Summary for {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}
    </h3>
    
    <p style='color: #e0e0e0; font-size: 16px; line-height: 1.6; margin-bottom: 15px;'>
        During this {(end_date - start_date).days}-day period, the composite score 
        {"increased" if score_change > 0 else "decreased"} by <strong>{abs(score_change):.2f}</strong> points,
        ending at <strong>{latest_score:.2f}</strong> with a current 
        <span style='color: {rec_color}; font-weight: bold;'>{latest_rec.upper()}</span> recommendation.
    </p>
    
    <p style='color: #e0e0e0; font-size: 16px; line-height: 1.6; margin-bottom: 15px;'>
        The stock price {"rose" if price_change > 0 else "fell"} by <strong>{abs(price_change):.2f}%</strong>
        from ${filtered_composite["close"].iloc[0]:.2f} to ${latest_price:.2f}.
    </p>
    
    <p style='color: #e0e0e0; font-size: 16px; line-height: 1.6;'>
        Use the AI Assistant at the top of this page to ask specific questions about the data
        or explore different time periods to identify patterns and investment opportunities.
    </p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style='color: #e0e0e0; font-size: 16px; line-height: 1.6; text-align: center;'>
        No data available for the selected date range. Please adjust your date selection to see analysis results.
    </p>
    """, unsafe_allow_html=True)

# === Data Export Options ===
st.markdown("<div style='text-align: center; margin-top: 30px; margin-bottom: 30px;'>", unsafe_allow_html=True)

if not (filtered_composite.empty and filtered_technical.empty and filtered_fundamental.empty and filtered_news.empty):
    # Create row of download buttons
    dl_col1, dl_col2, dl_col3, dl_col4 = st.columns(4)
    
    with dl_col1:
        if not filtered_composite.empty:
            # Prepare data for export
            export_composite = filtered_composite.copy()
            export_composite["date"] = export_composite["date"].dt.strftime('%Y-%m-%d')
            csv = export_composite.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Composite Data",
                data=csv,
                file_name=f"composite_data_{start_date}_{end_date}.csv",
                mime="text/csv",
                key="download-composite"
            )
    
    with dl_col2:
        if not filtered_technical.empty:
            # Prepare data for export
            export_technical = filtered_technical.copy()
            export_technical["date"] = export_technical["date"].dt.strftime('%Y-%m-%d')
            csv = export_technical.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Technical Data",
                data=csv,
                file_name=f"technical_data_{start_date}_{end_date}.csv",
                mime="text/csv",
                key="download-technical"
            )
    
    with dl_col4:
        if not filtered_news.empty:
            # Prepare data for export
            export_news = filtered_news.copy()
            export_news["date"] = export_news["date"].dt.strftime('%Y-%m-%d')
            csv = export_news.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download News Sentiment Data",
                data=csv,
                file_name=f"sentiment_data_{start_date}_{end_date}.csv",
                mime="text/csv",
                key="download-news"
            )
    with dl_col3:
        if not filtered_fundamental.empty:
            # Prepare data for export
            export_fundamental = filtered_fundamental.copy()
            export_fundamental["date"] = export_fundamental["date"].dt.strftime('%Y-%m-%d')
            csv = export_fundamental.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Fundamental Data",
                data=csv,
                file_name=f"fundamental_data_{start_date}_{end_date}.csv",
                mime="text/csv",
                key="download-fundamental"
            )


st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
    <p>Stock Dashboard for Novice Investors | Data last updated: {composite["date"].max().strftime('%B %d, %Y')} | © 2025 DATA 606 Capstone - UMBC</p>
</div>
""", unsafe_allow_html=True)