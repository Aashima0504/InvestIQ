import pandas as pd

def calculate_sma(data: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculate Simple Moving Average."""
    return data['Close'].rolling(window=window).mean()

def calculate_ema(data: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculate Exponential Moving Average."""
    return data['Close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculate Relative Strength Index."""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """Calculate MACD and Signal Line."""
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    
    return pd.DataFrame({
        'MACD': macd,
        'MACD_Signal': signal_line,
        'MACD_Hist': macd - signal_line
    })

def add_all_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Add all technical indicators to the dataframe."""
    df = data.copy()
    if len(df) < 26:
        return df # Not enough data
        
    df['SMA_20'] = calculate_sma(df, 20)
    df['SMA_50'] = calculate_sma(df, 50)
    df['EMA_20'] = calculate_ema(df, 20)
    df['RSI_14'] = calculate_rsi(df, 14)
    
    macd_df = calculate_macd(df)
    df = pd.concat([df, macd_df], axis=1)
    
    return df