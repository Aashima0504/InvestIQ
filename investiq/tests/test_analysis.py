import pandas as pd
import numpy as np
from analysis.indicators import calculate_sma, calculate_rsi

def test_calculate_sma():
    data = pd.DataFrame({'Close': [10]*20 + [20]*20})
    sma = calculate_sma(data, 20)
    assert not pd.isna(sma.iloc[19])
    assert sma.iloc[19] == 10.0
    assert sma.iloc[39] == 20.0

def test_calculate_rsi():
    # Uptrend should have high RSI
    data_up = pd.DataFrame({'Close': np.arange(10, 50)})
    rsi_up = calculate_rsi(data_up, 14)
    assert rsi_up.iloc[-1] > 80

    # Downtrend should have low RSI
    data_down = pd.DataFrame({'Close': np.arange(50, 10, -1)})
    rsi_down = calculate_rsi(data_down, 14)
    assert rsi_down.iloc[-1] < 20
