import streamlit as st
from reddit_grab import *
from crypto_metrics import getHistoricalData
import pandas
import numpy


## FUNCTION DEFINITIONS: ##

tickers = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "USDT": "Tether",
    "SOL": "Solana",
    "BNB": "Binance Coin",
    "XRP": "Ripple",
    "DOGE": "Dogecoin",
    "USDC": "USD Coin",
    "ADA": "Cardano",
    "TRX": "TRON"
}

def assign_sentiment_label(val:float):
    if val == 0.0:
        return "Completely Neutral"
    elif val < 0.05 and val > -0.05:
        return "Neutral"
    elif val < 0.1 and val >= 0.05:
        return "Slightly Positive"
    elif val < -0.05 and val > -0.1:
        return "Slightly Negative"
    elif val < 0.15 and val >= 0.1:
        return "Positive"
    elif val >= 0.15:
        return "Very Positive"
    elif val <= -0.1 and val > -0.15:
        return "Negative"
    elif val <= -0.15:
        return "Very Negative"
    else:
        return "n/a"

def get_sentiments():
    session = RedditSession()
    posts = session.get_posts_from_subreddit("CryptoMarkets", limit=50, sort_type="new")
    contents = session.get_sorted_contents(posts, sort_by="content")
    return_sentiments = {}
    all_pos = []
    all_neg = []
    for ticker, val in contents.items():
        if val:
            avg_sentiment = 0
            avg_sentiment_focused = 0
            sentiments = session.get_agg_sentiments(val)
            for post in sentiments:
                # Compute avg. sentiment based on highest sentiment value
                primary_sentiment = max(post, key=post.get)
                if primary_sentiment == "pos":
                    avg_sentiment += 1
                elif primary_sentiment == "neg":
                    avg_sentiment -=1
                # Compute avg. sentiment based on positive & negative values
                avg_sentiment_focused += post['pos']
                avg_sentiment_focused -= post['neg']
                all_pos.append(post['pos'])
                all_neg.append(post['neg'])
            print(round(avg_sentiment_focused / len(sentiments), 2))
            print(f"POS: {sum(all_pos)/len(all_pos)} ({max(all_pos)})")
            print(f"NEG: {sum(all_neg)/len(all_neg)} ({max(all_neg)})")
            return_sentiments[ticker] = avg_sentiment_focused / len(sentiments)
    return return_sentiments

def get_price_data():
    data = getHistoricalData()
    return data

def compare_price_and_sentiment(price_change:float, sentiment_val:float):
    if price_change > 0 and sentiment_val > 0:
        return '<span style="color:green">*Sentiment & Trend Match*</span>'
    elif price_change < 0 and sentiment_val < 0:
        return '<span style="color:green">*Sentiment & Trend Match*</span>'
    elif price_change == 0 and sentiment_val == 0:
        return '<span style="color:green">*Sentiment & Trend Match*</span>'
    else:
        return '''<span style="color:red">*Sentiment & Trend DON'T Match*</span>'''



## STREAMLIT APP: ##
st.set_page_config(layout="wide")
st.title("Cryptocurrency Price Trends vs. User Sentiment on Reddit:")

with st.spinner("Loading up-to-date crypto data..."):
    prices = get_price_data()
    sentiments = get_sentiments()
    for ticker, val in sentiments.items():
        if not prices[ticker].empty:
            with st.container(border=True):
                price_difference = prices[ticker].tail(1).iloc[0,3] - prices[ticker].head(1).iloc[0,3]
                st.markdown(f"#### [{ticker}] {tickers[ticker]}: {compare_price_and_sentiment(price_difference, val)}", unsafe_allow_html=True)
                st.write(f"Reddit User Sentiment: {assign_sentiment_label(val)} ({round(val,2)})")
                st.write(f"Price Trend: {'Upward' if price_difference > 0 else 'Downward' if price_difference < 0 else 'No Movement'} (${round(price_difference,2)} change)")
                chart_col, _, data_col = st.columns([0.47, 0.06, 0.47])
                with chart_col:
                    st.line_chart(
                        data=prices[ticker],
                        y="Close",
                        x_label="Date/Time",
                        y_label="Close Price"
                    )
                with data_col:
                    st.dataframe(data=prices[ticker])
