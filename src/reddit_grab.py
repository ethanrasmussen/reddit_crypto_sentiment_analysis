from praw import Reddit
from dotenv import load_dotenv
import os


# Load from .env
load_dotenv()
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')




class RedditSession:

    def __init__(self, id:str = REDDIT_CLIENT_ID, secret:str = REDDIT_CLIENT_SECRET, agent:str = "Reddit scraper for sentiment analysis project for UIUC MCS CS410") -> None:
        self.session = Reddit(
            client_id = id,
            client_secret = secret,
            user_agent = agent
        )
        self.client_id = id
        self.client_secret = secret
        self.user_agent = agent

    def get_posts_from_subreddit(self, subreddit:str, sort_type:str = "top", limit:int = 10):
        sub = self.session.subreddit(subreddit)
        if sort_type == "hot":
            sub = [post for post in sub.hot(limit=limit)]
        elif sort_type == "top":
            sub = [post for post in sub.top(limit=limit)]
        elif sort_type == "rising":
            sub = [post for post in sub.rising(limit=limit)]
        elif sort_type == "new":
            sub = [post for post in sub.new(limit=limit)]
        else:
            raise Exception("Error: Invalid sort type for subreddit")
        return sub
    
    def get_post_titles(self, posts:list):
        return [post.title for post in posts]
    
    def get_post_urls(self, posts:list):
        return [post.permalink for post in posts]
    
    def get_post_contents(self, posts:list):
        return [post.selftext for post in posts]

    def get_sorted_contents(self, posts:list, sort_by:str="title"):
        # Helper function
        def sort_helper(ticker:tuple, posts:list=posts, sort_by:str=sort_by):
            post_items = self.get_post_titles(posts) if sort_by=="title" else self.get_post_contents(posts)
            sorted = [(post if ticker[0] in post else (
                        post if ticker[0].lower() in post else (
                            post if ticker[1] in post else (
                                post if ticker[1].lower() in post else None
                            )
                        )
                    )) for post in post_items]
            return [x for x in sorted if x is not None]
        # Assert correct input
        if sort_by not in ["title", "content"]:
            assert Exception("Error: Invalid sort type for function")
        # Top 10 cryptocurrencies by market cap
        tickers = [
            ("Bitcoin", "BTC"),
            ("Ethereum ", "ETH"),
            ("Tether", "USDT"),
            ("Solana", "SOL"),
            ("Binance", "BNB"), # Technically, "binance coin"
            ("Ripple", "XRP"),
            ("Dogecoin", "DOGE"),
            ("USD Coin", "USDC"), # Including the coin here to ensure not confused with $USD
            ("Cardano", "ADA"),
            ("TRON", "TRX")
        ]
        return {ticker[1]: list(set(sort_helper(ticker))) for ticker in tickers}
