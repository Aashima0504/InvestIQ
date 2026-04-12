# InvestIQ - Future Improvements & Scaling Ideas

## Backend
- **Caching:** Implement Redis or Streamlit's `@st.cache_data` on fetching to reduce API calls to yfinance and speed up load times.
- **Database:** Store historical analysis and user portfolios in a PostgreSQL or MongoDB database instead of processing on the fly.
- **Advanced ML:** Move from a simple Random Forest over 10-day labels to an LSTM or Transformer model forecasting continuous price movements.

## Frontend
- **Portfolio Tracker:** Allow users to add a list of tickers and see the aggregated risk score and ML recommendations.
- **News Sentiment:** Integrate with a news API (e.g., NewsAPI) using FinBERT to analyze the sentiment of recent headlines for the ticker.
