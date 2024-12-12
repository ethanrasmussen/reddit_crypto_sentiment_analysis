import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from reddit_grab import RedditSession
from crypto_metrics import getHistoricalData, getCurrentMetrics

# Initialize Reddit session
reddit = RedditSession()

# Function to fetch Reddit sentiment data for a given cryptocurrency
def get_sentiment_data(ticker: str, limit=10):
    posts = reddit.get_sorted_contents(reddit.get_posts_from_subreddit('cryptocurrency', sort_type="top", limit=limit), sort_by="content")
    sentiment_data = reddit.analyze_posts_sentiment(posts.get(ticker, []))
    sentiment_df = pd.DataFrame(sentiment_data)
    return sentiment_df

# Function to fetch historical data for cryptocurrency from `crypto_metrics.py`
def get_crypto_data(ticker: str):
    historical_data = getHistoricalData([ticker])
    historical_df = historical_data.get(ticker)
    return historical_df

# Plot the data for the selected cryptocurrency
def plot_crypto_data(ticker):
    crypto_data = get_crypto_data(ticker)
    if crypto_data is not None:
        st.subheader(f"{ticker} Price Trend")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(crypto_data.index, crypto_data['Close'], label=f'{ticker} Price')
        ax.set_title(f'{ticker} Price Trend')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No data available for this cryptocurrency.")

# Display Reddit sentiment analysis for the selected cryptocurrency
def display_reddit_sentiment(ticker):
    sentiment_df = get_sentiment_data(ticker)
    if not sentiment_df.empty:
        st.subheader(f"Reddit Sentiment for {ticker}")
        st.write(sentiment_df)
    else:
        st.write(f"No sentiment data available for {ticker}.")

def main():
    # Sidebar for selecting cryptocurrency
    st.sidebar.title("Crypto Sentiment and Price Analysis")
    selected_ticker = st.sidebar.selectbox("Select a Cryptocurrency", ["BTC", "ETH", "USDT", "SOL", "BNB", "XRP", "DOGE", "USDC", "ADA", "TRX"])
    
    # Displaying the price trend chart
    plot_crypto_data(selected_ticker)
    
    # Displaying the Reddit sentiment table
    display_reddit_sentiment(selected_ticker)

if __name__ == "__main__":
    main()
