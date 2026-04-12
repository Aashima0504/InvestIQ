import pandas as pd
import numpy as np

def calculate_risk_score(data: pd.DataFrame, fundamentals: dict) -> dict:
    """
    Calculate a simple risk score from 1 (Low) to 10 (High).
    Based on Volatility (Standard Deviation of returns) and P/E ratio.
    """
    if len(data) < 20:
        return {"score": 5, "level": "Unknown", "reasoning": ["Not enough data"]}
        
    returns = data['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252) * 100 # Annualized volatility in %
    
    score = 5 # base score
    reasons = []
    
    if volatility > 40:
        score += 3
        reasons.append("High price volatility (>40% annualized)")
    elif volatility < 20:
        score -= 2
        reasons.append("Low price volatility (<20% annualized)")
        
    pe = fundamentals.get("P/E Ratio")
    if pe is not None:
        if pe > 30:
            score += 2
            reasons.append("High P/E ratio indicates premium valuation risk")
        elif pe < 15 and pe > 0:
            score -= 1
            reasons.append("Low P/E ratio offers some value protection")
        elif pe < 0:
            score += 3
            reasons.append("Negative Earnings (Unprofitable) adds to risk")
            
    # Clamp score
    score = max(1, min(10, score))
    
    if score >= 8:
        level = "High"
    elif score >= 5:
        level = "Moderate"
    else:
        level = "Low"
        
    return {
        "score": round(score),
        "level": level,
        "volatility_pct": round(volatility, 2),
        "reasons": reasons
    }
