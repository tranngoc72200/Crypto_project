import datetime as dt
import json
import time
import numpy as np
import pandas as pd
import requests
import streamlit as st
from streamlit_plotly_events import plotly_events
from multiprocessing import Process
from get_data import get_data

from plot_graph import plot_graph, plot_percent

st.set_page_config(page_title="Crypto Dashboard")

st.markdown(
    """# **Crypto Dashboard**
A simple cryptocurrency price app pulling price data from the [Binance API](https://www.binance.com/en/support/faq/360002502072)
"""
)

import os
from binance.client import Client
from time import sleep
import json
import pandas as pd

def round_value(input_value):
        if input_value.values > 1:
            a = float(round(input_value, 2))
        else:
            a = float(round(input_value, 8))
        return a

crpytoList = ('BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'SHIBUSDT', 'DOTUSDT')
    
col1, col2, col3 = st.columns(3)

placeholder = st.empty()
column_1 = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
column_2 = ['XRPUSDT', 'ADAUSDT', 'DOGEUSDT']
column_3 = ['SHIBUSDT', 'DOTUSDT']
coin = st.sidebar.selectbox("Cryptocurrencies", crpytoList)

for seconds in range(1000):
    df = pd.read_json("https://api.binance.com/api/v3/ticker/24hr")
    
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            for i in column_1:
                col_df = df[df.symbol == i]
                col_price = round_value(col_df.weightedAvgPrice)
                col_percent = f"{float(col_df.priceChangePercent)}%"
                st.metric(i, col_price, col_percent)
        with col2:
            for i in column_2:
                col_df = df[df.symbol == i]
                col_price = round_value(col_df.weightedAvgPrice)
                col_percent = f"{float(col_df.priceChangePercent)}%"
                st.metric(i, col_price, col_percent)
        with col3:
            for i in column_3:
                col_df = df[df.symbol == i]
                col_price = round_value(col_df.weightedAvgPrice)
                col_percent = f"{float(col_df.priceChangePercent)}%"
                st.metric(i, col_price, col_percent)
        st.header("")

        # @st.cache
        def convert_df(df):
            return df.to_csv().encode("utf-8")

        download_csv = df[["symbol", "openPrice", "highPrice", "lowPrice", "volume", "priceChangePercent"]]
        download_csv.columns = ["Cryptocurrency", "Open", "High", "Low", "Volume" , "Change(%)"]
        #csv = convert_df(download_csv)
        #st.dataframe(download_csv)
        #st.download_button(
                #label="Download market's data as CSV",
                #data=csv,
                #file_name="Market_data.csv",
                #mime="text/csv",
            #)
        
        data_symbol = download_csv[download_csv.Cryptocurrency == coin]
        chart_data = get_data(coin)
        st.header(coin)
        st.dataframe(chart_data)
        csv = convert_df(chart_data)
        st.download_button(
                label=f"Download {coin} data as CSV",
                data=csv,
                file_name=f"{coin}_data.csv",
                mime="text/csv",
            )

        fig= plot_graph(chart_data)
        st.plotly_chart(fig)
        
        percent = plot_percent(chart_data, data_symbol)
        st.plotly_chart(percent)

        time.sleep(3)
    
