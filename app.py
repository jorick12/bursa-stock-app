import streamlit as st
import yfinance as yf
import pandas as pd

# Title of the app
st.title("Bursa Malaysia Stock Tracker")

# 1. Input: Bursa Stock Code (e.g., 1155 for Maybank)
stock_code = st.text_input("Enter Bursa Stock Code (e.g., 1155):", "1155")

if stock_code:
    # Bursa stocks on Yahoo Finance need the '.KL' suffix
    ticker_symbol = f"{stock_code}.KL"
    ticker = yf.Ticker(ticker_symbol)

    try:
        # 2. Fetch Fundamental Data (PE, EPS)
        info = ticker.info
        name = info.get('longName', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')
        eps = info.get('trailingEps', 'N/A')
        current_price = info.get('currentPrice', 'N/A')

        st.subheader(f"Stock: {name}")
        
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"RM {current_price}")
        col2.metric("PE Ratio", pe_ratio)
        col3.metric("EPS", eps)

        # 3. Fetch Monthly Stock Price
        st.subheader("Monthly Historical Prices")
        history = ticker.history(period="5y", interval="1mo")
        
        if not history.empty:
            # Clean up the dataframe for display
            df_monthly = history[['Close']].copy()
            df_monthly.index = df_monthly.index.strftime('%B %Y')
            df_monthly.columns = ['Closing Price (RM)']
            
            # Show a line chart and the data table
            st.line_chart(history['Close'])
            st.write(df_monthly)
        else:
            st.warning("No historical data found for this period.")

    except Exception as e:
        st.error(f"Error: Could not find data for {ticker_symbol}. Check the code or try again.")
