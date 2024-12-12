def match_tickers(tickers1, tickers2):
  """Matches tickers from two lists based on their ticker symbols.

  Args:
    tickers1: A list of ticker symbols.
    tickers2: A list of tuples, where each tuple contains a full name and a ticker symbol.

  Returns:
    A dictionary mapping ticker symbols to their full names.
  """

  ticker_map = {}
  for full_name, ticker in tickers2:
    if ticker in tickers1:
      ticker_map[ticker] = full_name

  return ticker_map

# Example usage:
tickers1 = ["BTC", "ETH", "USDT", "SOL", "BNB", "XRP", "DOGE", "USDC", "ADA", "TRX"]
tickers2 = [("Bitcoin", "BTC"), ("Ethereum ", "ETH"), ("Tether", "USDT"), ("Solana", "SOL"), ("Binance", "BNB"), ("Ripple", "XRP"), ("Dogecoin", "DOGE"), ("USD Coin", "USDC"), ("Cardano", "ADA"), ("TRON", "TRX")]

matched_tickers = match_tickers(tickers1, tickers2)
print(matched_tickers)