import streamlit as st
from pages.utils.model_train import get_data, get_forecast, evaluate_model
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="📉",
    layout="wide",
)

st.title("📈 Stock Prediction")

# UI Input
col1, col2, col3 = st.columns(3)
with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')

# Get historical data
close_price = get_data(ticker)

# Forecast the next 30 days
forecast_df, rmse = get_forecast(ticker)

# Display RMSE
st.write(f"*Model RMSE Score:* {rmse}")

# Show forecast data table
st.write("##### Forecast Data (Next 30 Days)")
fig_table = plotly_table(forecast_df.round(2))
fig_table.update_layout(height=250)
st.plotly_chart(fig_table, use_container_width=True)

# Combine actual and forecasted data for line chart
combined = pd.concat([close_price, forecast_df.set_index('Date')])
st.write("##### Close Price + Forecast")
st.plotly_chart(Moving_average_forecast(combined.iloc[-180:]), use_container_width=True)
