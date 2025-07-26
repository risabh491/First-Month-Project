import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta

def get_data(ticker):
    df = yf.download(ticker, start='2024-01-01')
    return df[['Close']].dropna()

def prepare_data(data, window_size=30):
    X, y = [], []
    for i in range(window_size, len(data)):
        X.append(data[i-window_size:i])
        y.append(data[i])
    return np.array(X), np.array(y)

def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

def forecast_next_days(model, last_window, steps=30):
    predictions = []
    current_window = last_window.copy()
    for _ in range(steps):
        pred = model.predict(current_window.reshape(1, -1))[0]
        predictions.append(pred)
        current_window = np.append(current_window[1:], pred)
    return np.array(predictions)

def get_forecast(ticker, forecast_days=30, window_size=30):
    data = get_data(ticker)
    close_prices = data['Close'].values

    # Normalize data
    scaler = StandardScaler()
    scaled_prices = scaler.fit_transform(close_prices.reshape(-1, 1)).flatten()

    # Prepare training data
    X, y = prepare_data(scaled_prices, window_size)
    model = train_model(X, y)

    # Forecast
    forecast_scaled = forecast_next_days(model, scaled_prices[-window_size:], steps=forecast_days)
    forecast = scaler.inverse_transform(forecast_scaled.reshape(-1, 1)).flatten()

    # Create date index
    start_date = datetime.now()
    forecast_dates = [start_date + timedelta(days=i) for i in range(forecast_days)]
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Close': forecast})

    # Format date for Streamlit/CSV
    forecast_df['Date'] = forecast_df['Date'].dt.strftime('%Y-%m-%d 00:00:00')

    # Calculate RMSE on training data
    predictions_train = model.predict(X)
    rmse = round(np.sqrt(mean_squared_error(y, predictions_train)), 2)

    return forecast_df, rmse

def evaluate_model(ticker):
    data = get_data(ticker)
    close_prices = data['Close'].values

    scaler = StandardScaler()
    scaled_prices = scaler.fit_transform(close_prices.reshape(-1, 1)).flatten()

    X, y = prepare_data(scaled_prices)
    model = train_model(X, y)

    predictions = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    return round(rmse, 2)

if __name__ == "__main__":
    ticker = 'AMZN'
    forecast_df, rmse = get_forecast(ticker)
    print(f"Model RMSE: {rmse}")
    print(forecast_df)

