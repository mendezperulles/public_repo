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


# Compute the mean of each row (each trading day) and add it to the plot
sns.distplot(price_paths_df.iloc[-1], kde=True, hist=True)

# Set the x-axis label to 'Price'
plt.xlabel('Price')

# Set the y-axis label to 'Frequency'
plt.ylabel('Frequency')

# Set the title of the plot to 'Price Distribution'
plt.title('Price Distribution of ' + ticker + ' Stock' + '| For 1,000 sims with 5 Yrs of Historical Data with 252 Trading Days/Year')

# Show the plot
plt.show()
