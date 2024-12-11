# CS 410 Reddit Post Sentiment Analysis for Crypto-market Trend Prediction

To run:
 - 'python -m streamlit run src/app.py'

Necessary setup items:
 - 'pip install -r requirements.txt'
 - Create .env file with variables: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET

Notes on what we'll need to complete:
 - Functionality to grab & parse posts/subreddits via Reddit API (likely via PRAW package)
 - Functionality to perform sentiment analysis on our parsed text input (maybe via NLTK package or something like that?)
 - Functionality to grab current crypto pricing info/trends (probably via Yahoo Finance / yfinance package & snag time-series data for graphing)
 - Functionality to graph/display our data (this should be pretty easy via one of the big Python dataviz libraries, unless we want to go crazy with mouseover features or something)
 - Frontend UI via Streamlit (should be pretty easy to implement once we've got some backend stuff built out)
