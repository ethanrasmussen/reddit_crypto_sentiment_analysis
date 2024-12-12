import streamlit as st
from reddit_grab import *
from crypto_metrics import getHistoricalData


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
    '''Returns a sentiment label based on following cutoff values:
         +inf, 0.15 == Very Positive
          0.15, 0.1 == Positive
          0.1, 0.05 == Slightly Positive
        0.05, -0.05 == Neutral  (with 0.0 == Completely Neutral)
        -0.05, -0.1 == Slightly Negative
        -0.1, -0.15 == Negative
        -0.15, -inf == Very Negative'''
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
    # Fetch 50 most recent CryptoMarkets posts
    session = RedditSession()
    posts = session.get_posts_from_subreddit("CryptoMarkets", limit=50, sort_type="new")
    contents = session.get_sorted_contents(posts, sort_by="content")
    # For each ticker, compute aggregate sentiment score
    return_sentiments = {}
    for ticker, val in contents.items():
        if val: # Continues if there are posts for that crypto
            avg_sentiment = 0
            sentiments = session.get_agg_sentiments(val)
            # For each post, average its sentiment score
            for post in sentiments:
                # Compute avg. sentiment based on positive & negative values
                avg_sentiment += post['pos']
                avg_sentiment -= post['neg']
            return_sentiments[ticker] = avg_sentiment / len(sentiments)
    return return_sentiments

def compare_price_and_sentiment(price_change:float, sentiment_val:float):
    # Check whether price & sentiment trends match or not, and return appropriate HTML to be injected via st.markdown
    if price_change > 0 and sentiment_val > 0:
        return '<span style="color:green">*Sentiment & Trend Match*</span>'
    elif price_change < 0 and sentiment_val < 0:
        return '<span style="color:green">*Sentiment & Trend Match*</span>'
    elif price_change == 0 and sentiment_val == 0:
        return '<span style="color:green">*Sentiment & Trend Match*</span>'
    else:
        return '''<span style="color:red">*Sentiment & Trend DON'T Match*</span>'''



## STREAMLIT UI FUNCTION: ##
def results_ui():
    with st.spinner("Loading up-to-date crypto data..."):
        # Fetch price data & Reddit sentiment data, with error message if something goes wrong (like Reddit or Yahoo Finance is down)
        try:
            prices = getHistoricalData()
        except:
            st.warning("An error occurred while fetching price data. Please reload the page to try again.")
            return
        try:
            sentiments = get_sentiments()
        except:
            st.warning("An error occurred while fetching Reddit data. Please reload the page to try again.")
            return
        # Display a st.container for all cryptos for which we successfully fetch price & sentiment data
        for ticker, val in sentiments.items():
            if not prices[ticker].empty:
                with st.container(border=True):
                    # Text elements within container
                    price_difference = prices[ticker].tail(1).iloc[0,3] - prices[ticker].head(1).iloc[0,3]
                    st.markdown(f"#### [{ticker}] {tickers[ticker]}: {compare_price_and_sentiment(price_difference, val)}", unsafe_allow_html=True)
                    st.write(f"Reddit User Sentiment: {assign_sentiment_label(val)} ({round(val,2)})")
                    st.write(f"Price Trend, YTD: {'Upward' if price_difference > 0 else 'Downward' if price_difference < 0 else 'No Movement'} (${round(price_difference,2)} change)")
                    # Provide chart on left, dataframe on right, with small spacer
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



## FULL STREAMLIT APP: ##
st.set_page_config(layout="wide")
st.title("Cryptocurrency Price Trends vs. User Sentiment on Reddit:")
results_ui()
