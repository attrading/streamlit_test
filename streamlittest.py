import streamlit as st
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import math
import numpy as np
import http.client
import json
import pandas as pd
import plotly.graph_objects as go
import datetime
import re
from dateutil.relativedelta import relativedelta
import pytz

st.set_page_config(page_title='test', layout='wide')

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    try: earnings_history = stock.earnings_history
    except: earnings_history = ""
    try: eps_trend = stock.eps_trend
    except: eps_trend = ""
    try: growth_estimates = stock.growth_estimates
    except: growth_estimates = ""
    try: earnings_estimate = stock.earnings_estimate
    except: earnings_estimate = ""
    try: revenue_estimate = stock.revenue_estimate
    except: revenue_estimate = ""

    return ticker,news,earnings_history,eps_trend,growth_estimates,earnings_estimate,revenue_estimate

main_col1, main_col2 = st.columns([3,1])
with main_col1:
    st.title("US Stock Analysis Tool")
    input_col1, input_col2, input_col3 = st.columns([1, 3, 1])
    with input_col1:
        ticker = st.text_input("Enter US Stock Ticker:", "AAPL")
    with input_col2:
        apiKey = st.text_input("Enter your RapidAPI Key (optional):", "")

if st.button("Get Data"):
    try:
        ticker,news,earnings_history,eps_trend,growth_estimates,earnings_estimate,revenue_estimate = get_stock_data(ticker)

        st.header(ticker)
        ''
        st.write(earnings_history)
        ''
        st.write(eps_trend)
        ''
        st.write(growth_estimates)
        ''
        st.write(earnings_estimate)
        ''
        st.write(revenue_estimate)
        ''

    except Exception as e:
        st.write(e)