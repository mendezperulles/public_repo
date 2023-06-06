import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd


# User enters the ticker symbol
ticker = input("Please enter the ticker symbol: ")

# Get the historical data for the past 5 years
data = yf.download(ticker, period='5y')

# We will use Adjusted Close prices for the simulation
log_returns = np.log(1 + data['Adj Close'].pct_change())

# Estimate the historical log returns and volatility
u = log_returns.mean() # Mean of the log-returns
var = log_returns.var() # Variance of the log-returns
drift = u - (0.5 * var) # Drift term
stdev = log_returns.std() # Standard deviation of the log return

days = 252 # Number of trading days in a year
trials = 1000 # Number of trials in the Monte Carlo simulation

# Create a random number generator for the Monte Carlo simulation
Z = np.random.standard_normal((days, trials))

# Calculate daily returns
daily_returns = np.exp(drift + stdev * Z)

# The price of the stock today
S0 = data['Adj Close'].iloc[-1]

# Create an empty matrix to hold the price paths
price_paths = np.zeros_like(daily_returns)
price_paths[0] = S0

# Simulate the price paths
for t in range(1, days):
    price_paths[t] = price_paths[t - 1] * daily_returns[t]

# Convert price_paths numpy array to pandas DataFrame
price_paths_df = pd.DataFrame(price_paths)

# Plot the price paths with transparency
fig = go.Figure()

# Add all price paths as traces with a specified transparency
for i in range(price_paths_df.shape[1]):
    fig.add_trace(go.Scatter(y=price_paths_df[i], mode='lines', line=dict(color='rgba(0,0,255,0.3)')))

# Compute the mean of each row (each trading day) and add it to the plot
mean_line = go.Scatter(y=price_paths_df.mean(axis=1), mode='lines', name='Mean', line=dict(color='ORANGE'))
fig.add_trace(mean_line)

fig.update_layout(xaxis_title='Trading Days', yaxis_title='Price', yaxis_tickprefix='$', title='Monte Carlo Simulation for ' + ticker)

fig.show()
