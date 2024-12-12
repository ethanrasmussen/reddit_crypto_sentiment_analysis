# CS 410 Reddit Post Sentiment Analysis for Crypto-market Trend Prediction

## View a Demo Here:
[Click here to access a publicly hosted Streamlit app](https://cs410-reddit-crypto-sentiment-analysis.streamlit.app/)
[Click here to view a video demo on Mediaspace](https://mediaspace.illinois.edu/media/t/1_jfhq1l9e)

## Installation & Run:
To install, clone the repository and do the following from the root:
 - Create a file ".env" with the following values: REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET
 - Obtain & assign these values by creating a Reddit app (see reddit.com for more details, or use the demo above)
 - Install all dependencies via 'python -m pip install -r requirements.txt'
 - Run the Streamlit app via 'python -m streamlit run src/streamlit_frontend.py'

## Introduction:
Our project seeks to analyze the sentiment of Reddit users discussing various cryptocurrencies, with the goal of understanding their views on the cryptos' values. We hypothesized that users would have positive feelings toward cryptos with positive price growth, and would likely have negative feelings towards those with declining prices.

## Project Breakdown:
 - Reddit parsing functionality via PRAW
 - Sentiment analysis functionality for parsed text via NLTK
 - Functionality to grab current crypto pricing info/trends via yfinance
 - Graph, displays, and frontend UI via Streamlit

## Methods & Files:
We have three main files in our project:

**crypto_metrics.py:**
This file fetchs cryptocurrency pricing data from Yahoo Finance for graphing purposes. 

**reddit_grab.py:**
This file interfaces with the Reddit API using the PRAW package to grab relevant posts for sentiment analysis. It also includes functionality via NLTK to analyze the user sentiment, using the package's SentimentIntensityAnalyzer object.

**streamlit_frontend.py:**
This file defines our front-end via basic Streamlit code, and leverages the features from crypto_metrics.py and reddit_grab.py to fetch relevant data. Then, we display this information to the user in our front-end. The user can see whether the user sentiment & price trend match (which would be our hypothesis).

## Evaluation:
While we hypothesized that user sentiment & price trends would line up, this wasn't necessarily true across all cryptocurrencies. Many larger cryptocurrencies, such as Bitcoin & Ethereum, having user sentiments that match their price trends. However, some smaller cryptocurrencies have positive sentiment but negative trends. This could be due to users forecasting a positive uptick.
