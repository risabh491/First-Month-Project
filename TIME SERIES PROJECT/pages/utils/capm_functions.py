from cv2 import dft
import numpy as np
import plotly.express as px

# function to plot interactive plotly chart
def interactive_plot(df):
    fig = px.line()    
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y =df[i], name = i)
    fig.update_layout(width = 450, margin = dict(l=20,r =20, t = 50, b = 20), legend =  dict(orientation = 'h', yanchor = 'bottom',
            y = 1.02, xanchor = 'right', x = 1, )) 
    return fig 

#  function to normalize the prices based on the initial price
def normalize(df_2):
    df = df_2.copy()
    for i in df.columns[1:]:
        df[i] = df[i]/df[i][0]
    return df

# function to calculate daily returns
def daily_return(df):
    df_daily_return = df.copy()
    for col in df.columns[1:]:
        df_daily_return[col] = df[col].pct_change() * 100  # percent change
    df_daily_return.iloc[0, 1:] = 0  # set first row to 0 for all returns
    return df_daily_return

# function to calculate beta
def calculate_beta(df, stock):
    # Drop any rows with missing values in the required columns
    clean_df = df[['sp500', stock]].dropna()

    # Ensure both columns are float type
    x = clean_df['sp500'].astype(float)
    y = clean_df[stock].astype(float)

    # Now fit the regression line
    b, a = np.polyfit(x, y, 1)
    return b, a