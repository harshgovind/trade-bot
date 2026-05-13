import asyncio
from probability_model import calculate_bullish_probability

class RankingPipeline:
    def __init__(self, universe_list):
        self.universe = universe_list # List of S&P 500 tickers
        self.min_volume = 2000000     # 2M share liquidity gate
        self.min_mcap = 2000000000    # $2B market cap floor

    async def get_market_metrics(self, ticker):
        """
        Placeholder for fetching current liquidity and volatility (ATR/Beta).
        Ensures the stock meets the Step 3 'Liquidity Gate'.
        """
        # In implementation, this calls your DB or Polygon REST API
        return {"volume": 5000000, "mcap": 150000000000, "expected_move_pct": 5.2}

    async def score_ticker(self, ticker, horizon_days):
        """
        Calculates the risk-adjusted score: P(Bullish) * Expected Move.
        """
        metrics = await self.get_market_metrics(ticker)
        
        # Universe Filtering
        if metrics['volume'] < self.min_volume or metrics['mcap'] < self.min_mcap:
            return None

        # Calculate Probability using our ML Routing Algorithm
        p_bullish = calculate_bullish_probability(ticker, horizon_days)
        
        # Risk-Adjusted Ranking Formula
        final_score = p_bullish * metrics['expected_move_pct']
        
        return {
            "ticker": ticker,
            "p_bullish": p_bullish,
            "final_score": final_score,
            "expected_move": metrics['expected_move_pct']
        }

    async def get_top_5(self, horizon_days):
        """
        Runs concurrent scoring across the universe and returns the top 5.
        """
        tasks = [self.score_ticker(ticker, horizon_days) for ticker in self.universe]
        results = await asyncio.gather(*tasks)
        
        # Filter out None values and sort by final_score descending
        valid_results = [r for r in results if r is not None]
        sorted_results = sorted(valid_results, key=lambda x: x['final_score'], reverse=True)
        
        return sorted_results[:5]

# Usage Example
if __name__ == "__main__":
    sp500_sample = ["NVDA", "AMZN", "CSCO", "AAPL", "MSFT", "GOOGL"]
    pipeline = RankingPipeline(sp500_sample)
    
    # User selects a 30-day horizon on the slider
    top_5 = asyncio.run(pipeline.get_top_5(30))
    print(f"Top 5 Opportunities: {top_5}")
