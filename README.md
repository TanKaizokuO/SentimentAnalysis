# 📈 Stock Sentiment Analysis Dashboard

This project is an interactive **Streamlit** dashboard for real-time sentiment analysis of stock-related news headlines.  
It fetches news from **Finviz**, performs **sentiment analysis** using **VADER**, and visualizes trends to help you understand market sentiment towards different tickers over time.

---

## 🚀 Features

- **Ticker Input:** Fetch news headlines by entering one or more stock tickers (space-separated).
- **Sentiment Analysis:** Automatically labels headlines as Positive, Neutral, or Negative using NLTK's VADER analyzer.
- **Database:** Saves and updates a `headlines_history.csv` file to maintain headline history.
- **Interactive Dashboard:**
  - View recent news headlines.
  - Visualize daily average sentiment trends over time.
  - See sentiment distribution (positive, neutral, negative) for each company.
- **Data Export:** Download filtered datasets easily.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python 3
- **Scraping:** BeautifulSoup, urllib
- **Sentiment Analysis:** NLTK VADER
- **Visualization:** Plotly, Seaborn, Matplotlib
- **Storage:** CSV Files

---

## 📥 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/stock-sentiment-dashboard.git
   cd stock-sentiment-dashboard
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   (If you don't have `requirements.txt`, here are the main libraries to install manually:)
   ```bash
   pip install streamlit pandas matplotlib seaborn plotly beautifulsoup4 nltk
   ```

3. **Download NLTK Data:**
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

4. **Run the App:**
   ```bash
   streamlit run app.py
   ```

---

## 🖥️ Usage

- Enter stock tickers in the sidebar (space-separated), e.g., `AAPL TSLA MSFT`.
- Click **Fetch News & Analyze** to scrape headlines and perform sentiment analysis.
- Select specific tickers to filter the dashboard visualizations.
- Click **Export Filtered Data** to save the current filtered view.

---

## 📂 Project Structure

```
📁 stock-sentiment-dashboard
 ┣ 📄 app.py
 ┣ 📄 headlines_history.csv  # (Auto-created after first news fetch)
 ┗ 📄 README.md
```

---

## ⚡ Future Enhancements

- Add keyword/topic filtering (e.g., only headlines mentioning "earnings" or "mergers").
- Include more news sources beyond Finviz.
- Deploy on Streamlit Cloud or AWS EC2.
- Implement historical sentiment analysis with backtesting.

---

## 🙌 Acknowledgements

- News data sourced from [Finviz.com](https://finviz.com/).
- Sentiment analysis powered by [NLTK VADER](https://github.com/cjhutto/vaderSentiment).

