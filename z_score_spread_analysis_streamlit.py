
import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Set the title of the Streamlit app
st.title("Z-Score Spread Analysis")

# Function to perform the analysis and plot
def analyze_spread(ticker1, ticker2, start_date, end_date):
    try:
        # Download historical data
        data = yf.download([ticker1, ticker2], start=start_date, end=end_date)

        # Calculate spread, Z-score, and signals
        data['Spread'] = data['Close'][ticker1] - data['Close'][ticker2]
        data['Mean'] = data['Spread'].rolling(window=30).mean()
        data['Std'] = data['Spread'].rolling(window=30).std()
        data['Z-Score'] = (data['Spread'] - data['Mean']) / data['Std']

        data['Signal'] = 0
        data['Signal'][data['Z-Score'] < -2] = 1
        data['Signal'][data['Z-Score'] > 2] = -1

        # Plotting Z-Score
        st.subheader(f'Z-Score of {ticker1} and {ticker2} Spread')
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(data.index, data['Z-Score'], label='Z-Score', color='blue')
        ax.axhline(2, color='red', linestyle='--', label='Upper Threshold (2)')
        ax.axhline(-2, color='green', linestyle='--', label='Lower Threshold (-2)')
        ax.set_title(f'Z-Score of {ticker1} and {ticker2} Spread')
        ax.set_xlabel('Date')
        ax.set_ylabel('Z-Score')
        ax.legend()
        ax.grid()
        st.pyplot(fig)

        # Plotting Price Spread with Trading Signals
        st.subheader(f'Price Spread of {ticker1} and {ticker2} with Trading Signals')
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.plot(data.index, data['Spread'], label='Price Spread', color='blue')
        ax.scatter(data.index[data['Signal'] == 1], data['Spread'][data['Signal'] == 1], marker='^', color='green', label='Buy Signal', s=100)
        ax.scatter(data.index[data['Signal'] == -1], data['Spread'][data['Signal'] == -1], marker='v', color='red', label='Sell Signal', s=100)
        ax.set_title(f'Price Spread of {ticker1} and {ticker2} with Trading Signals')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price Spread')
        ax.legend()
        ax.grid()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit Inputs
st.sidebar.header("Input Parameters")
ticker1 = st.sidebar.text_input("Ticker 1", value='AAPL')
ticker2 = st.sidebar.text_input("Ticker 2", value='MSFT')
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2021-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime('2021-12-31'))

# Button to trigger analysis
if st.sidebar.button("Analyze"):
    analyze_spread(ticker1, ticker2, start_date, end_date)
