import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import random
import datetime as dt
import pandas_datareader.data as web
import mplfinance as mpf
from finquant.portfolio import build_portfolio
import yfinance as yf
from datetime import timedelta
import plotly.express as px

st.set_page_config(layout='wide')


def app():
    uploaded_file = st.file_uploader("Choose a file: ", type="csv")
    if uploaded_file is not None:


        df = pd.read_csv(uploaded_file)

        kpi1, kpi2, kpi3 = st.beta_columns(3)

        Portfolio_Total_Amount = sum(df['Allocation'] * df['Average_Price'])
        Portfolio_Total_Amount = round(Portfolio_Total_Amount, 2)

        stock_tickers = df['Name'].values
        sizes = df['Allocation'] * df['Average_Price']

        fig1 = px.pie(df, values=sizes, names=stock_tickers, width=550, height=550, color_discrete_sequence=px.colors.sequential.RdBu)
        fig1.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))


        with kpi1:
            st.markdown("**Amount Invested(in USD)**")
            st.markdown(f"<h1 style='text-align: center; color: red;'>{Portfolio_Total_Amount}</h1>",
                        unsafe_allow_html=True)

        with kpi2:
            st.markdown("**Maximum Gainer**")
            st.markdown("**GOOG**")

            df_pct = pd.DataFrame(columns=['Date'])
            for i in df['Name']:
                df_1 = yf.Ticker(i).history(start=dt.datetime.now() - timedelta(days=8),
                                            end=dt.datetime.now() - timedelta(days=1), interval="1d")
                df_1 = df_1.reset_index().loc[[0, 4], ['Date', 'Close']].rename({'Close': str(i)}, axis='columns')
                df_pct = pd.merge(df_pct, df_1, how='outer', on='Date')
            df_pct = df_pct.set_index('Date').pct_change() * 100
            df_pct = df_pct.reset_index()
            df_pct.drop(index=df.index[0], axis=1, inplace=True)
            df_pct['Max'] = df_pct.max(axis=1)
            max_gainer = round(df_pct['Max'].loc[1], 2)

            st.markdown(f"<h1 style='text-align: center; color: red;'>{max_gainer}</h1>", unsafe_allow_html=True)

        with kpi3:
            st.markdown("**Maximum Loser**")
            st.markdown("**HON**")
            df_pct['Min'] = df_pct.min(axis=1)
            min_loser = round(df_pct['Min'].loc[1], 2)

            st.markdown(f"<h1 style='text-align: center; color: red;'>{min_loser}</h1>", unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

        st.markdown("## Portfolio Allocation")

        df_1 = df[['Name', 'Allocation']]
        pf_allocation = df_1
        # pf_allocation

        names = df_1["Name"].values.tolist()
        # names

        start_date = dt.datetime(2015, 1, 1)
        end_date = dt.datetime.now()

        pf = build_portfolio(names=names, pf_allocation=pf_allocation, start_date=start_date, end_date=end_date,
                             data_api='yfinance')

        pf_1 = round(pf.expected_return, 1) * 100
        pf_2 = round(pf.volatility, 1) * 100
        pf_3 = round(pf.sharpe, 1)

        chart1, chart2 = st.beta_columns(2)

        with chart1:
            st.plotly_chart(fig1)

        with chart2:
            pf_fig = pf.comp_cumulative_returns().plot().axhline(y=0, color="black", lw=3)
            #st.write(pf_fig)

        st.markdown("## Overview")

        kpi01, kpi02, kpi03, kpi04 = st.beta_columns(4)

        with kpi01:
            st.markdown("**Expected Return (in %)**")
            st.markdown(f"<h1 style='text-align: center; color: yellow;'>{pf_1}</h1>", unsafe_allow_html=True)

        with kpi02:
            st.markdown("**Volatility/Risk (in %)**")
            st.markdown(f"<h1 style='text-align: center; color: yellow;'>{pf_2}</h1>", unsafe_allow_html=True)

        with kpi03:
            st.markdown("**Sharpe Ratio**")
            st.markdown(f"<h1 style='text-align: center; color: yellow;'>{pf_3}</h1>", unsafe_allow_html=True)

        with kpi04:
            st.markdown("**Risk Free Rate (in %)**")
            number1 = 5
            st.markdown(f"<h1 style='text-align: center; color: yellow;'>{number1}</h1>", unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)

