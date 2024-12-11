import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from reddit_grab import RedditSession
from crypto_metrics import getCurrentMetrics, getHistoricalData, tickers

def load_reddit_data(subreddit, sort_type, limit):
    reddit = RedditSession()
    posts = reddit.get_posts_from_subreddit(subreddit, sort_type, limit)
    sentiment_analysis = reddit.analyze_posts_sentiment(posts)
    return sentiment_analysis

def load_crypto_data():
    current_metrics = getCurrentMetrics(tickers)
    historical_data = getHistoricalData(tickers)
    return current_metrics, historical_data

def plot_sentiment(sentiment_data):
    sentiments = [post['title_sentiment']['compound'] for post in sentiment_data]
    plt.figure(figsize=(10, 5))
    plt.hist(sentiments, bins=20, color='skyblue', edgecolor='black')
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    st.pyplot(plt)

def plot_crypto_data(historical_data, ticker):
    if ticker not in historical_data:
        st.error(f"No historical data available for {ticker}")
        return

    data = historical_data[ticker]
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig.update_layout(title=f"{ticker} Historical Prices", xaxis_title='Date', yaxis_title='Close Price (USD)')
    st.plotly_chart(fig)

def display_ui():
    st.title("Crypto-Market Trend Prediction")

    st.sidebar.header("Reddit Data Settings")
    subreddit = st.sidebar.text_input("Subreddit", value="cryptocurrency")
    sort_type = st.sidebar.selectbox("Sort by", ["hot", "top", "rising", "new"])
    limit = st.sidebar.slider("Number of posts", min_value=1, max_value=50, value=10)

    st.sidebar.header("Crypto Data Settings")
    selected_ticker = st.sidebar.selectbox("Select Ticker", tickers)

    if st.sidebar.button("Load Data"):
        with st.spinner("Loading Reddit data..."):
            reddit_data = load_reddit_data(subreddit, sort_type, limit)
            st.success("Reddit data loaded!")

        with st.spinner("Loading Crypto data..."):
            current_metrics, historical_data = load_crypto_data()
            st.success("Crypto data loaded!")

        st.subheader("Reddit Sentiment Analysis")
        st.write(reddit_data)
        plot_sentiment(reddit_data)

        st.subheader("Crypto Historical Data")
        plot_crypto_data(historical_data, selected_ticker)

if __name__ == "__main__":
    display_ui()