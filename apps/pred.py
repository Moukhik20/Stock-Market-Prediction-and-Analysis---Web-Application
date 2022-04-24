import streamlit as st
import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import plotly.express as px
import cufflinks as cf
import datetime
import yfinance as yf
from IPython.display import display, HTML
from get_all_tickers import get_tickers as gt
plt.style.use('fivethirtyeight')
import warnings
warnings.filterwarnings("ignore")


    


def app():
    ticker_list=pd.read_csv("ticker_list.txt")
    st.sidebar.header("Select Parameters")
    tickerSymbol = st.sidebar.selectbox('Company Symbol', ticker_list)
    start_date = st.sidebar.date_input("Start date", datetime.date(2018, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))
    st.text("")
    st.text("")
    if st.sidebar.button('Confirm Parameters'):
        tickerData=yf.Ticker(tickerSymbol)
        df=web.DataReader(tickerSymbol, data_source='yahoo', start=start_date, end=end_date)
        st.header("Stock Price Data - "+tickerData.info['longName'])
        st.dataframe(df)
        st.header("Line Chart of Closing Stock Price")
        st.line_chart(df['Close'])
        st.text("")
        st.text("")
        st.header("Predicted Stock Price")
        data=df.filter(['Close'])
        dataset=data.values
        #Train-test split (80-20)
        training_data_len=math.ceil(len(dataset)*.8)
        training_data_len
        
        #Normalizing the data using Min-Max Scalar
        scaler=MinMaxScaler(feature_range=(0,1))
        scaled_data=scaler.fit_transform(dataset)
        
        train_data=scaled_data[0:training_data_len, :]
        x_train=[]
        y_train=[]
        for i in range (60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])
        
        # Creating x_train and y_train arrays
        x_train, y_train =np.array(x_train), np.array(y_train)
        x_train =np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        
        ### CREATING LSTM MODEL ###
        model=Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, batch_size=1, epochs=1)
        
        test_data=scaled_data[training_data_len - 60: , :]
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i-60:i, 0])
        x_test=np.array(x_test)
        x_test=np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        
        ## Prediction
        predictions=model.predict(x_test)
        predictions=scaler.inverse_transform(predictions)
        
        ## Plot
        train=data[:training_data_len]
        valid=data[training_data_len:]
        valid['Predictions']=predictions
        st.line_chart(valid)
        st.text("")
        st.subheader("Comparison between Actual Close and Predicted Close price")
        st.dataframe(valid)
        # Prediction for next day
        st.text("")
        st.text("")
        new_df=df.filter(["Close"])
        last_60_days=new_df[-60:].values
        last_60_days_scaled=scaler.transform(last_60_days)
        X_test=[]
        X_test.append(last_60_days_scaled)
        X_test=np.array(X_test)
        X_test=np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        pred_price=model.predict(X_test)
        pred_price=scaler.inverse_transform(pred_price)
        st.header("Predicted Price for Next Day")
        st.write(pred_price[0])
        
        
        
       


       
        
   
    