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
        earnings_data = pd.DataFrame(earnings_history)
        st.write(earnings_data)
        if 'epsEstimate' in earnings_data.columns and 'epsActual' in earnings_data.columns:
                        df = earnings_data.reset_index().melt(id_vars=['index'], value_vars=['epsEstimate', 'epsActual'], var_name='variable', value_name='value')
                        df['index'] = df['index'].dt.strftime('%Y-%m-%d')
                        actual_data = df[df['variable'] == 'epsActual']
                        estimate_data = df[df['variable'] == 'epsEstimate']
                        bar = go.Bar(
                            x=actual_data['index'],  
                            y=actual_data['value'],
                            name='Actual',
                            marker=dict(color='#FFCE54'),
                        )
                        estimate = go.Scatter(
                            x=estimate_data['index'],
                            y=estimate_data['value'],
                            mode='markers+lines',
                            name='Estimate',
                            marker=dict(color='red', size=10), 
                            line=dict(width=3) 
                        )
                        fig = go.Figure(data=[bar, estimate])
                        fig.update_layout(
                            title='Earnings Estimate vs Actual',
                            title_y=1,  
                            title_x=0, 
                            margin=dict(t=30, b=40, l=40, r=30),
                            xaxis_title='Date',
                            yaxis_title='Earnings',
                            xaxis=dict(type='category',tickangle=30,showgrid=True),
                            yaxis=dict(showgrid=True),
                            barmode='group',
                            height=400,
                            width=600,
                        )
                        st.plotly_chart(fig)
        else:
                        st.write("no data")
        ''
        try:
            st.write(eps_trend)
            eps_data = eps_trend.loc[["0y", "+1y"], ["current", "7daysAgo", "30daysAgo", "60daysAgo", "90daysAgo"]]
            eps_data = eps_data.T.reset_index()
            eps_data.columns = ['TimePeriod', 'CurrentYear', 'NextYear']
            label_map = {
                                    'current': 'Current',
                                    '7daysAgo': '7 Days Ago',
                                    '30daysAgo': '30 Days Ago',
                                    '60daysAgo': '60 Days Ago',
                                    '90daysAgo': '90 Days Ago'
                        }
            eps_data['TimePeriod'] = eps_data['TimePeriod'].map(label_map)
            eps_melted = pd.melt(eps_data, id_vars=['TimePeriod'], value_vars=['CurrentYear', 'NextYear'],
                                                    var_name='Year', value_name='EPS')
            current_year_data = eps_melted[eps_melted['Year'] == 'CurrentYear']
            next_year_data = eps_melted[eps_melted['Year'] == 'NextYear']
            color_map = {'CurrentYear': '#9678DC', 'NextYear': '#D772AD'}
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                                    x=current_year_data['TimePeriod'],
                                    y=current_year_data['EPS'],
                                    mode='lines+markers',
                                    name='Current Year',
                                    line=dict(color=color_map['CurrentYear']),
                                    marker=dict(color=color_map['CurrentYear'])
                            ))
            fig.add_trace(go.Scatter(
                                    x=next_year_data['TimePeriod'],
                                    y=next_year_data['EPS'],
                                    mode='lines+markers',
                                    name='Next Year',
                                    line=dict(color=color_map['NextYear']),
                                    marker=dict(color=color_map['NextYear'])
                            ))
            fig.update_layout(
                                    title='EPS Trend',
                                    title_y=1,  
                                    title_x=0, 
                                    margin=dict(t=30, b=40, l=40, r=30),
                                    xaxis=dict(
                                        title='Time Period',
                                        categoryorder='array',
                                        showgrid=True,  
                                        categoryarray=['90 Days Ago', '60 Days Ago', '30 Days Ago', '7 Days Ago', 'Current'],
                                    ),
                                    yaxis=dict(
                                        title='EPS',
                                        showgrid=True
                                    ),
                                    height=400,
                                    legend=dict(title_text=None),
                            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e: st.write(e)
        ''
        st.write(growth_estimates)
        ''
        st.write(earnings_estimate)
        ''
        st.write(revenue_estimate)
        ''

    except Exception as e:
        st.write(e)
