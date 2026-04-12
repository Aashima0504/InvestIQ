import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_price_volume_chart(df: pd.DataFrame, ticker: str):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'{ticker} Price Action & Moving Averages', 'Volume Analysis'), 
                        row_width=[0.25, 0.75])

    # Candlestick
    fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#00ffcc', decreasing_line_color='#ff3366',
                name='Price'), row=1, col=1)

    # Moving Averages
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='#00f2fe', width=2), name='SMA 20'), row=1, col=1)
    if 'EMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], line=dict(color='#f093fb', width=2, dash='dot'), name='EMA 20'), row=1, col=1)

    # Volume
    colors = ['#00ffcc' if df['Close'].iloc[i] > df['Open'].iloc[i] else '#ff3366' for i in range(len(df))]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color=colors, opacity=0.8), row=2, col=1)

    fig.update_layout(height=650, showlegend=True,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      xaxis_rangeslider_visible=False,
                      template="plotly_dark",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family="Inter, sans-serif", size=13, color="#e2e8f0"),
                      margin=dict(t=40, b=20, l=20, r=20))
                      
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    return fig

def create_rsi_macd_chart(df: pd.DataFrame):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.08, subplot_titles=('Relative Strength Index (RSI)', 'MACD Oscillator'), 
                        row_width=[0.5, 0.5])
                        
    # RSI
    if 'RSI_14' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI_14'], line=dict(color='#a18cd1', width=2), name='RSI 14'), row=1, col=1)
        # Add Overbought/Oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="#ff3366", row=1, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#00ffcc", row=1, col=1)
        # Add band background
        fig.add_hrect(y0=30, y1=70, fillcolor="rgba(161, 140, 209, 0.05)", line_width=0, row=1, col=1)
        
    # MACD
    if 'MACD' in df.columns and 'MACD_Signal' in df.columns and 'MACD_Hist' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], line=dict(color='#00f2fe', width=2), name='MACD'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], line=dict(color='#fbc2eb', width=2), name='Signal'), row=2, col=1)
        
        colors = ['#00ffcc' if val >= 0 else '#ff3366' for val in df['MACD_Hist']]
        fig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], marker_color=colors, opacity=0.8, name='Histogram'), row=2, col=1)

    fig.update_layout(height=500, showlegend=True,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                      template="plotly_dark",
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(family="Inter, sans-serif", size=13, color="#e2e8f0"),
                      margin=dict(t=40, b=20, l=20, r=20))
                      
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    return fig
