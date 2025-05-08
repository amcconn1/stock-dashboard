![NOVICE STOCK PLATFORM (1)](https://github.com/user-attachments/assets/6d42afba-d043-42d4-9819-2fa8c2e71a42)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue.svg)

Welcome to the **Novice Stock Platform**, a Streamlit-based dashboard that helps novice investors analyze market sentiment, technical indicators, and fundamental metrics. It brings together data from news, Reddit, technical analysis, and financial fundamentals — wrapped in an intuitive UI.

## 🗂 Table of Contents

1. [Live App](#-live-app)
2. [Problem Statement & Project Overview](#-problem-statement--project-overview)
3. [Features](#-features)
4. [Data Sources](#-data-sources)
5. [Methodology & Code Access](#-methodology--code-access)
6. [Technologies](#-technologies)
7. [Future Enhancements (Next Steps)](#-future-enhancements-next-steps)
8. [Author](#-author)
9. [License](#-license)

## 🚀 Live App
👉 [Launch the App](https://novicestockdashboard.streamlit.app/)

## 📌 Problem Statement & Project Overview
Since novice investors are constantly bombarded with fragmented financial information and analytical tools, making clear and informed investment decisions challenging. This robust information overload creating confusion and difficulty in formulating effective long-term stock investment strategies. As such, this project proposes an innovative approach by integrating long-term technical analysis, fundamental analysis, and news sentiment with short-term social media sentiment data.

The **Novice Stock Platform** bridges this gap by integrating diverse data sources into an intuitive, easy-to-understand dashboard. By consolidating these signals into a **composite investment score** and providing interactive visualizations, the platform empowers users to make better-informed trading decisions without requiring deep financial expertise.

## 📝 Features
- **Home - Stock Overview**: Introduction to top discussed stocks and composite score for highest discussed.
- **Historical Snapshot**: Composite score over time with trade signals.
- **Score Breakdown**: Visual deep dive into the fundamental, technical, news, and social sentiment scores.
- **Market Simulator**: Test trading strategies based on your selected signals and capital allocation.
- **Social Media Sentiment**: Reddit trends and sentiment analysis.
- **Data Explorer**: View and export the underlying data.
- **Glossary**: Definitions and explanations of key metrics.
- **About**: Learn about the project and methodology.

## 🗂 Data Sources
- Financial fundamentals - 5 years of data (alphavantage api)
- Technical indicators - 5 years of data (alphavantage api)
- News sentiment - 5 years of data (polygon.io)
- Reddit sentiment- 30 days of data (reddit praw api)

## 🔍 Methodology & Code Access
The core logic and data processing behind the dashboard were developed and tested in a series of **Colab Notebooks** located in the [`notebooks/`](./notebooks) directory.
These notebooks cover:
- Data scraping (Reddit, news, fundamentals, technical indicators)
- Signal scoring methodologies
- Composite score calculation
- Model testing 
For those seeking to review or extend the data pipeline, the notebooks provide a comprehensive, step-by-step walkthrough of the methodology.
The final app code is organized within the [`app/`](./app) directory, using **Streamlit** to create a user-friendly web interface.

## 🖥 Technologies
- Python (pandas, numpy, plotly, streamlit, asyncpraw)
- Google Colab for data preparation
- Streamlit Cloud for deployment
- Git & GitHub for version control

## 🔮 Future Enhancements (Next Steps)
- Automate data refresh using GitHub Actions or Google Cloud.
- Extend multi-ticker support (top 5-10 tickers).
- Integrate AI-driven natural language queries.
- Build alert system for trading signals.

## 👩‍💻 Author
Mehul Lad, Ashley McConnell, & Bestover Makoko | UMBC - DATA 606 Capstone

## 📜 License
MIT License
