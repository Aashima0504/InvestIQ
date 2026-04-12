def analyze_fundamentals(fundamentals: dict) -> dict:
    """
    Analyze fundamental metrics and yield basic interpretations for beginner investors.
    """
    analysis = {}
    
    pe = fundamentals.get("P/E Ratio")
    if pe is not None:
        if pe < 15:
            analysis["P/E"] = "Low (Potentially undervalued or facing growth challenges)"
        elif pe < 25:
            analysis["P/E"] = "Moderate (Fairly valued compared to market average)"
        else:
            analysis["P/E"] = "High (Potentially overvalued or high growth expectations)"
    else:
        analysis["P/E"] = "N/A"
        
    eps = fundamentals.get("EPS")
    if eps is not None:
        if eps > 0:
            analysis["EPS"] = "Positive (Company is profitable)"
        else:
            analysis["EPS"] = "Negative (Company is losing money)"
    else:
         analysis["EPS"] = "N/A"
         
    return analysis
