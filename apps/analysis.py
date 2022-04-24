import streamlit as st
import numpy as np
import yfinance as yf
from typing import Callable
import pandas as pd
import datetime
import cufflinks as cf
import matplotlib.pyplot as plt

def calc_rsi(over: pd.Series, fn_roll: Callable) -> pd.Series:
    length = 14
    delta = over.diff()
    delta = delta[1:] 
    up, down = delta.clip(lower=0), delta.clip(upper=0).abs()
    roll_up, roll_down = fn_roll(up), fn_roll(down)
    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    rsi[:] = np.select([roll_down == 0, roll_up == 0, True], [100, 0, rsi])
    rsi.name = 'rsi'
    valid_rsi = rsi[length - 1:]
    assert ((0 <= valid_rsi) & (valid_rsi <= 100)).all()
    return rsi

def BB(df):
    period=20
    #SMA
    df['SMA']=df['Close'].rolling(window=period).mean()
    #SD
    df["SD"]=df['Close'].rolling(window=period).std()
    #Upper BB
    df['Upper']=df['SMA']+(df['SD']*2)
    #Lower BB
    df['Lower']=df['SMA']-(df['SD']*2)
    column_list=['Close','SMA','Upper','Lower']
    
def EMA(df):
    EMA12 =df.Close.ewm(span=12, adjust=False).mean()
    EMA26 = df.Close.ewm(span=26, adjust=False).mean()


def app():
    st.header("**Technical Analysis of Stocks**")
    ticker_list=pd.read_csv("ticker_list.txt")
    st.sidebar.header("Select Parameters")
    tickerSymbol = st.sidebar.selectbox('Company Symbol', ticker_list)
    start_date = st.sidebar.date_input("Start date", datetime.date(2018, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))
    if st.sidebar.button("Display Technical Analysis"):
        tickerData = yf.Ticker(tickerSymbol)
        df = tickerData.history(start=start_date, end=end_date)
        st.header("Relative Strength Index (RSI)")
        st.info("The relative strength index (RSI) is a momentum indicator used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. Traditional interpretation and usage of the RSI are that values of 70 or above indicate that a security is becoming overbought or overvalued and may be primed for a trend reversal or corrective pullback in price. An RSI reading of 30 or below indicates an oversold or undervalued condition.")
        st.text("")
        rf=cf.QuantFig(df,title='Relative Strength Index (RSI)',legend='top')
        rf.add_rsi(periods=20, rsi_upper=70, rsi_lower=30, showbands=True, legend="top")
        fig = rf.iplot(asFigure=True)
        st.plotly_chart(fig)
        st.text("")
        st.text("")
        st.header("Bollinger Bands")
        st.info("Bollinger Bands are envelopes plotted at a standard deviation level above and below a simple moving average of the price. Because the distance of the bands is based on standard deviation, they adjust to volatility swings in the underlying price. Bollinger bands help determine whether prices are high or low on a relative basis. They are used in pairs, both upper and lower bands and in conjunction with a moving average.When the bands tighten during a period of low volatility, it raises the likelihood of a sharp price move in either direction. This may begin a trending move. Watch out for a false move in opposite direction which reverses before the proper trend begins.\nWhen the bands separate by an unusual large amount, volatility increases and any existing trend may be ending. A strong trend continuation can be expected when the price moves out of the bands. However, if prices move immediately back inside the band, then the suggested strength is negated.")
        st.text("")
        bf=cf.QuantFig(df,title='Bollinger Bands',legend='top')
        bf.add_bollinger_bands(periods=20, boll_std=2, fill=True)
        fig = bf.iplot(asFigure=True)
        st.plotly_chart(fig)
        st.text("")
        st.text("")
        st.header("Exponential Moving Average (EMA)")
        st.info("An exponential moving average (EMA) is a type of moving average (MA) that places a greater weight and significance on the most recent data points. The exponential moving average is also referred to as the exponentially weighted moving average. The EMA is a moving average that places a greater weight and significance on the most recent data points. Like all moving averages, this technical indicator is used to produce buy and sell signals based on crossovers and divergences from the historical average. Investors tend to interpret a rising EMA as a support to price action and a falling EMA as a resistance. With that interpretation, investors look to buy when the price is near the rising EMA and sell when the price is near the falling EMA.")
        st.text("")
        ef=cf.QuantFig(df,title='Exponential Moving Average (EMA)',legend='top')
        ef.add_ema(periods=12, color='Red')
        ef.add_ema(periods=26, color='Green')
        fig = ef.iplot(asFigure=True)
        st.plotly_chart(fig)
        st.text("")
        st.text("")
        st.header("Moving Average Convergence Divergence (MACD)")
        st.info("Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. The MACD is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA. The result of that calculation is the MACD line. A nine-day EMA of the MACD called the signal line, is then plotted on top of the MACD line, which can function as a trigger for buy and sell signals. Traders may buy the security when the MACD crosses above its signal line and sell—or short—the security when the MACD crosses below the signal line.")
        st.text("")
        mf=cf.QuantFig(df,title='Moving Average Convergence Divergence (MACD)',legend='top')
        mf.add_ema(periods=12, color='Brown')
        mf.add_ema(periods=26, color='Green')
        mf.add_macd(fast_period=12, slow_period=26, signal_period=9)
        fig = mf.iplot(asFigure=True)
        st.plotly_chart(fig)