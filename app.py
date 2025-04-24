
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os


st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide")
st.title("Sentiment Analysis Dashboard")


nltk.download('vader_lexicon')


class TickerNewsScraper:
    def __init__(self, tickers):
        self.tickers = tickers
        self.base_url = "https://finviz.com/quote.ashx?t="
        self.news_data = {}

    def _format_ticker(self, ticker):
        return ticker.replace('.', '-').upper()

    def fetch_news(self):
        for ticker in self.tickers:
            formatted = self._format_ticker(ticker)
            url = self.base_url + formatted
            req = Request(url, headers={'User-Agent': 'my-app'})
            try:
                response = urlopen(req)
                html = BeautifulSoup(response, 'html.parser')
                self.news_data[ticker] = html.find(id='news-table')
            except Exception as e:
                st.warning(f"❌ Failed to fetch data for {ticker}: {e}")

    def parse_news(self):
        parsed_data = []
        for ticker, news in self.news_data.items():
            if news is None:
                continue
            for row in news.findAll('tr'):
                title = row.a.text.strip()
                date_info = row.td.text.strip().split()
                if len(date_info) == 1:
                    time = date_info[0]
                    date = pd.to_datetime('today').date()
                else:
                    date = pd.to_datetime(date_info[0], errors='coerce').date()
                    time = date_info[1]
                parsed_data.append([ticker, str(date), time, title])
        return parsed_data


class SentimentAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self):
        self.df['Date'] = pd.to_datetime(self.df['Date'], errors='coerce')
        self.df['Sentiment'] = self.df['Title'].apply(
            lambda x: self.analyzer.polarity_scores(x)['compound']
        )
        self.df['Sentiment_Label'] = self.df['Sentiment'].apply(
            lambda x: 'positive' if x > 0.05 else ('negative' if x < -0.05 else 'neutral')
        )
        return self.df



tickers_input = st.sidebar.text_input("Add tickers (space-separated)", "")
tickers = [t.strip().upper() for t in tickers_input.split() if t.strip()]
scraped_df = pd.DataFrame()


if st.sidebar.button("Fetch News & Analyze"):
    if not tickers:
        st.sidebar.warning("Please enter at least one ticker.")
    else:
        # Show a loading spinner while processing
        with st.spinner("Fetching news and analyzing sentiment..."):
            scraper = TickerNewsScraper(tickers)
            scraper.fetch_news()
            parsed_news = scraper.parse_news()

            if parsed_news:
                scraped_df = pd.DataFrame(parsed_news, columns=['Ticker', 'Date', 'Time', 'Title'])
                analyzer = SentimentAnalyzer(scraped_df)
                analyzed_df = analyzer.analyze()

                # Save or merge to history
                output_file = "headlines_history.csv"
                if os.path.exists(output_file):
                    history_df = pd.read_csv(output_file)
                    combined = pd.concat([history_df, analyzed_df], ignore_index=True)
                    combined.drop_duplicates(subset=['Ticker', 'Title'], inplace=True)
                    combined.to_csv(output_file, index=False)
                    st.success("Updated Database")
                else:
                    analyzed_df.to_csv(output_file, index=False)
                    st.success("Created Database")

            else:
                st.warning("No news found for the given tickers.")


if os.path.exists("headlines_history.csv"):
    df = pd.read_csv("headlines_history.csv")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
else:
    df = pd.DataFrame(columns=['Ticker', 'Date', 'Time', 'Title', 'Sentiment', 'Sentiment_Label'])


if not df.empty:
    tickers_list = sorted(df['Ticker'].dropna().unique())
    selected_tickers = st.sidebar.multiselect("Select Tickers for Dashboard", options=tickers_list)
    filtered_df = df[df['Ticker'].isin(selected_tickers)] if selected_tickers else df.copy()

    st.write(f"### 📄 Showing {len(filtered_df)} headlines")
    st.dataframe(filtered_df)

    if not filtered_df.empty:
        st.subheader("📈 Sentiment Trends Over Time")
        daily_sentiment = filtered_df.groupby(['Date', 'Ticker'])['Sentiment'].mean().reset_index()
        fig_line = px.line(daily_sentiment, x='Date', y='Sentiment', color='Ticker',
                           title='Daily Sentiment Over Time', markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("📋 Sentiment Distribution by Company")
        sentiment_count = filtered_df.groupby(['Ticker', 'Sentiment_Label']).size().reset_index(name='Count')
        cols_per_row = 2
        tickers_unique = sorted(filtered_df['Ticker'].unique())
        max_count = sentiment_count['Count'].max()

        for i in range(0, len(tickers_unique), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(min(cols_per_row, len(tickers_unique) - i)):
                ticker = tickers_unique[i + j]
                with cols[j]:
                    data = sentiment_count[sentiment_count['Ticker'] == ticker]
                    fig, ax = plt.subplots(figsize=(6, 4))
                    sns.barplot(data=data, x='Sentiment_Label', y='Count',
                                palette='pastel', ax=ax)
                    ax.set_title(f"{ticker} Sentiment")
                    ax.set_xlabel("Sentiment")
                    ax.set_ylabel("Count")
                    ax.set_ylim(0, max_count + 5)
                    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
                    st.pyplot(fig)
                    plt.close(fig)
    else:
        st.warning("Please select at least one ticker to display visualizations.")

    
    if st.sidebar.button("💾 Export Filtered Data"):
        filtered_df.to_csv("filtered_sentiment_data.csv", index=False)
        st.sidebar.success("Filtered data saved as 'filtered_sentiment_data.csv'")
else:
    st.info("No sentiment data available. Please fetch news first.")
