import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate synthetic target labels for training the ML model.
    1 = Buy, -1 = Sell (No Hold)
    Based on future 10-day returns.
    """
    data = df.copy()
    data['Future_Return'] = data['Close'].shift(-10) / data['Close'] - 1
    
    # Binary classification: Buy if return > 0, else Sell (No Hold)
    data['Target'] = np.where(data['Future_Return'] > 0, 1, -1)
    return data.dropna()

def train_ml_model(data: pd.DataFrame):
    """
    Train a simple Random Forest model on technical indicators.
    """
    df = generate_signals(data)
    features = ['SMA_20', 'EMA_20', 'RSI_14', 'MACD', 'MACD_Signal', 'MACD_Hist']
    
    # Ensure features exist
    for f in features:
        if f not in df.columns:
            return None, 0.0
            
    X = df[features]
    y = df['Target']
    
    if len(X) < 50:
        return None, 0.0
        
    # Added class_weight='balanced_subsample' to prevent bias towards the majority class (Hold)
    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=5, class_weight='balanced_subsample')
    model.fit(X, y)
    
    # Calculate a rough confidence based on training score
    confidence = model.score(X, y) * 100
    return model, confidence

def get_ml_prediction(model, latest_data: pd.Series) -> tuple:
    if model is None:
        return "Sell", 50.0
        
    features = ['SMA_20', 'EMA_20', 'RSI_14', 'MACD', 'MACD_Signal', 'MACD_Hist']
    X_pred = pd.DataFrame([latest_data[features]])
    
    pred = model.predict(X_pred)[0]
    proba = model.predict_proba(X_pred)[0]
    confidence = float(max(proba)) * 100
    
    mapping = {1: "Buy", -1: "Sell"}
    return mapping.get(pred, "Sell"), confidence

def generate_explanation(latest_data: pd.Series, fundamentals_analysis: dict, risk_info: dict, ml_prediction: str, ml_confidence: float) -> str:
    """
    Rule-based educational explanation for beginner investors.
    """
    explanation = f"### Overall Recommendation: **{ml_prediction.upper()}** (Confidence: {ml_confidence:.1f}%)\n\n"
    explanation += "Here is a breakdown of why this recommendation was made based on today's metrics:\n\n"
    
    explanation += "#### 1. Technical Indicators (Price Trends)\n"
    # RSI
    rsi = latest_data.get('RSI_14', 50)
    if pd.isna(rsi):
        rsi = 50
    if rsi >= 70:
        explanation += f"- **RSI ({rsi:.1f}):**  Overbought. The stock has been bought heavily and may be due for a price drop (pullback).\n"
    elif rsi <= 30:
        explanation += f"- **RSI ({rsi:.1f}):**  Oversold. The stock has been sold heavily and might be undervalued right now.\n"
    else:
        explanation += f"- **RSI ({rsi:.1f}):**  Neutral. The stock is neither overbought nor oversold.\n"
        
    # MACD
    macd = latest_data.get('MACD_Hist', 0)
    if pd.isna(macd):
        macd = 0
    if macd > 0:
        explanation += f"- **MACD:**  Bullish momentum. The short-term trend is stronger than the long-term trend.\n"
    else:
        explanation += f"- **MACD:**  Bearish momentum. The short-term trend is weakening.\n"
        
    # Moving Averages
    close = latest_data.get('Close', 0)
    sma_20 = latest_data.get('SMA_20', 0)
    if not pd.isna(close) and not pd.isna(sma_20):
        if close > sma_20:
            explanation += f"- **Price vs SMA:**  Stock price (${close:.2f}) is above its 20-day average (${sma_20:.2f}), indicating an uptrend.\n"
        else:
            explanation += f"- **Price vs SMA:**  Stock price (${close:.2f}) is below its 20-day average (${sma_20:.2f}), indicating a downtrend.\n"
        
    explanation += "\n#### 2. Fundamental Analysis (Company Health)\n"
    for metric, interpretation in fundamentals_analysis.items():
        if metric == "P/E":
            explanation += f"- **P/E Ratio:** {interpretation}. *Learning Note: P/E compares the stock price to the company's earnings. A high P/E means it's expensive relative to profits.*\n"
        elif metric == "EPS":
             explanation += f"- **Earnings Per Share (EPS):** {interpretation}. *Learning Note: Positive EPS means the company is profitable.*\n"
             
    explanation += "\n#### 3. Risk Profile\n"
    explanation += f"- **Risk Level:** {risk_info.get('level', 'Unknown')} (Score: {risk_info.get('score', 5)}/10)\n"
    for reason in risk_info.get('reasons', []):
        explanation += f"  - {reason}\n"
    explanation += f"  - *Annualized Volatility:* {risk_info.get('volatility_pct', 0)}%\n"
    
    explanation += "\n---\n*Disclaimer: This is for educational purposes only and does not constitute financial advice.*"
    return explanation
