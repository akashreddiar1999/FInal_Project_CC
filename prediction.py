import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go


def app():
    def load_data():
        components = pd.read_html('https://en.wikipedia.org/wiki/List_of_S'
                                  '%26P_500_companies')[0]
        return components.drop('SEC filings', axis=1).set_index('Symbol')

    components = load_data()

    def label(symbol):
        a = components.loc[symbol]
        return symbol + ' - ' + a.Security

    st.subheader('Select asset')

    asset = st.selectbox('Click below to select a new asset',
                         components.index.sort_values(), index=3,
                         format_func=label)

    # tickerData = yf.Ticker(asset)

    START = "2005-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    #st.title('Stock Forecast App')

    #stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
    #selected_stock = st.selectbox('Select dataset for prediction', stocks)

    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365

    @st.cache
    def load_data(asset):
        data = yf.download(asset, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text('Loading data...')
    data = load_data(asset)
    data_load_state.text('Loading data... done!')

    #st.subheader('Raw data')
    #st.write(data.tail())

    # Plot raw data
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    # Predict forecast with Prophet.
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)
    #
    #st.write("Forecast components")
    #fig2 = m.plot_components(forecast)
    #st.write(fig2)
