import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

def app():
    ticker_list=pd.read_csv("ticker_list.txt")
    st.sidebar.header("Select Parameters")
    tickerSymbol = st.sidebar.selectbox('Company Symbol', ticker_list)
    ticker=yf.Ticker(tickerSymbol)
    start_date = st.sidebar.date_input("Start date", datetime.date(2018, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))
    options=st.multiselect("Choose Information to Display", ticker.info.keys())
    if st.button("Display"):
        st.text("")
        st.text("")
        ticker=yf.Ticker(tickerSymbol)
        df=ticker.history(start=start_date, end=end_date)
        string_name = ticker.info['longName']
        st.header('**%s**' % string_name)
        string_logo = '<img src=%s>' % ticker.info['logo_url']
        st.markdown(string_logo, unsafe_allow_html=True)
        st.text("")
        string_summary = ticker.info['longBusinessSummary']
        st.info(string_summary)
        st.header("Stock Price Data - "+ticker.info['longName'])
        st.dataframe(df)
        st.header("Line Chart of Closing Stock Price")
        st.line_chart(df['Close'])        
        for opt in options:
            st.header(opt)
            st.info(ticker.info[opt])
            
        
        
        
        