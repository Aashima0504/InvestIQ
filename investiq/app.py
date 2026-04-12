import streamlit as st
import pandas as pd

from data.fetcher import fetch_stock_data, fetch_fundamentals
from analysis.indicators import add_all_indicators
from analysis.fundamentals import analyze_fundamentals
from analysis.risk_scorer import calculate_risk_score
from ai.recommender import train_ml_model, get_ml_prediction, generate_explanation
from ui.charts import create_price_volume_chart, create_rsi_macd_chart

st.set_page_config(page_title="InvestIQ", layout="wide")

# Adding Custom CSS for Glassmorphism & sleek dark theme
st.markdown("""
<style>
/* Animated Background Gradient */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.main {
    background: linear-gradient(-45deg, #0f172a, #1e1b4b, #000000, #170d2b);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #e2e8f0;
}
/* Titles */
h1 {
    font-family: 'Outfit', 'Inter', sans-serif !important;
    background: linear-gradient(to right, #00f2fe, #4facfe, #00f2fe);
    background-size: 200% auto;
    color: #fff;
    background-clip: text;
    text-fill-color: transparent;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    font-weight: 900 !important;
    font-size: 4rem !important;
    text-align: center;
    padding-bottom: 20px;
}
@keyframes shine {
    to { background-position: 200% center; }
}
/* Subtitle/Text */
p, h2, h3, h4, h5, h6, span {
    font-family: 'Inter', sans-serif !important;
}
/* Metric container */
[data-testid="metric-container"] {
    background: rgba(17, 25, 40, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.125);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: all 0.3s ease-in-out;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    border-color: rgba(0, 242, 254, 0.5);
    box-shadow: 0 10px 30px -1px rgba(0, 242, 254, 0.2);
}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] > div {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #fff !important;
}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] > div {
    font-size: 1rem !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
}
/* Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(2, 6, 23, 0.8) !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}
/* Input fields */
.stTextInput input, .stSelectbox > div[data-baseweb="select"] > div {
    background-color: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: white !important;
}
.stTextInput input:focus, .stSelectbox > div[data-baseweb="select"] > div:focus {
    border-color: #00f2fe !important;
    box-shadow: 0 0 10px rgba(0, 242, 254, 0.3) !important;
}
/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
    color: white !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4) !important;
    transition: all 0.3s ease !important;
    width: 100%;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(79, 172, 254, 0.6) !important;
    filter: brightness(1.1);
}
/* Info Alert */
div.stAlert {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
    border-left: 5px solid #00f2fe !important;
    border-radius: 12px !important;
    color: #e0f2fe !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    padding-bottom: 1rem;
    color: #94a3b8;
    font-size: 1.1rem;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    color: #00f2fe !important;
    border-bottom: 2px solid #00f2fe !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-top: -30px;'>InvestIQ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #94a3b8; font-weight: 500; margin-bottom: 2rem;'>Intelligent Stock Screener & AI Learning Platform</p>", unsafe_allow_html=True)

# Sidebar Input
st.sidebar.markdown("### 🔍 Stock Selection")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()
period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

if st.sidebar.button("Analyze Stock"):
    with st.spinner(f"Engaging analysis engine for {ticker}..."):
        try:
            # 1. Fetch Data
            raw_data = fetch_stock_data(ticker, period)
            fundamentals = fetch_fundamentals(ticker)
            
            # 2. Add Indicators
            data = add_all_indicators(raw_data)
            
            # 3. Analyze Fundamentals & Risk
            fund_analysis = analyze_fundamentals(fundamentals)
            risk_info = calculate_risk_score(data, fundamentals)
            
            # 4. AI & Recommendation (ML Model)
            st.toast("Training ML insights on historical data...")
            model, confidence = train_ml_model(data)
            latest_data = data.iloc[-1]
            ml_pred, ml_conf = get_ml_prediction(model, latest_data)
            
            # Use max confidence available or default to ML conf
            final_conf = max(confidence, ml_conf)
            
            # 5. Generate Explanation
            explanation = generate_explanation(latest_data, fund_analysis, risk_info, ml_pred, final_conf)
            
            # ==============================
            # UI RENDER - REDESIGNED DASHBOARD
            # ==============================
            st.markdown("---")
            st.markdown(f"<div style='text-align: center; margin-bottom: 1.5rem;'><h2 style='font-size: 2.2rem; font-weight: 800; color: #fff;'>{fundamentals.get('Sector', 'Stock')} <span style='color: #475569; font-size: 1.8rem; font-weight: 400;'>| {fundamentals.get('Industry', '')}</span></h2></div>", unsafe_allow_html=True)
            
            # Top row for metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Current Price", f"${latest_data['Close']:.2f}", f"{latest_data['Close'] - data.iloc[-2]['Close']:.2f}")
            
            # Format Market Cap if available
            mcap = fundamentals.get("Market Cap", "N/A")
            if isinstance(mcap, (int, float)):
                if mcap >= 1e12:
                    mcap = f"${mcap/1e12:.2f}T"
                elif mcap >= 1e9:
                    mcap = f"${mcap/1e9:.2f}B"
                elif mcap >= 1e6:
                    mcap = f"${mcap/1e6:.2f}M"
                    
            m2.metric("Market Cap", mcap)
            m3.metric("P/E", fundamentals.get("P/E Ratio", "N/A"))
            m4.metric("Risk", f"{risk_info.get('total_score', 'N/A')}/100")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Create Tabs for better layout
            tab1, tab2, tab3 = st.tabs(["Technical Analysis", " Insights", " Advanced Indicators"])
            
            with tab1:
                st.plotly_chart(create_price_volume_chart(data, ticker), use_container_width=True)
            
            with tab2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(explanation)
                
            with tab3:
                st.plotly_chart(create_rsi_macd_chart(data), use_container_width=True)

        except Exception as e:
            st.error(f"Error fetching data: {e}. It might be delisted or invalid ticker.")
else:
    st.markdown("""
    ---
    ### Welcome to InvestIQ
    To get started, simply type a stock ticker (e.g. `AAPL`, `TSLA`, `MSFT`) in the sidebar on the left and select the timeframe. 
    Our engine will crunch the numbers and explain the "why" behind the insights in a simple and transparent way.
    """)
