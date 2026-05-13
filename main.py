import asyncio
import os
from src.ingestion.ingestion_engine import polygon_handler
from src.logic.flash_engine import FlashOpportunityEngine
from src.logic.ranking_pipeline import RankingPipeline
from src.storage.persistence import DataPersistence
from src.notifications.alerting_system import AlertingSystem

# Initialize Global Components
db = DataPersistence()
alert_sys = AlertingSystem()
flash_engine = FlashOpportunityEngine()

# Core Watchlist for your 2027 LEAPS and specialized positions
WATCHLIST = ["NVDA", "AMZN", "CSCO"]

async def main_execution_loop():
    """
    Orchestrates the lifecycle of a market event from tick to alert.
    """
    print("🚀 Initializing trade-bot Ecosystem...")
    
    # 1. Initialize Database Schema
    db.init_db()
    
    # 2. Setup Ranking Pipeline for the S&P 500
    # In a production env, this would be the full S&P 500 list
    pipeline = RankingPipeline(WATCHLIST)

    print("✅ System Ready. Listening for market events...")

    # 3. Define the Callback for real-time trade processing
    def on_trade_captured(trade_event):
        ticker = trade_event.get('sym')
        price = trade_event.get('p')
        
        # Check for Flash Opportunities (e.g., hitting your 15.21 floor)
        # We wrap this in a task to ensure ingestion isn't blocked
        asyncio.create_task(process_potential_opportunity(ticker, price))

    # 4. Start the Ingestion Engine
    # We pass the callback to ingestion_engine to handle incoming ticks
    await polygon_handler(on_trade_captured)

async def process_potential_opportunity(ticker, price):
    """
    Analyzes a specific tick for Flash or Ranking significance.
    """
    # Mocking volatility for the Sigma-drop calculation (Step 4)
    mock_volatility = 2.5 
    
    # Check for Flash Signal
    snapshot = {ticker: {'price': price, 'volatility': mock_volatility}}
    signals = await flash_engine.scan_sp500(snapshot)
    
    for signal in signals:
        # 1. Dispatch Priority 1 SMS via Twilio
        alert_sys.send_flash_alert(
            ticker=signal['ticker'],
            price=signal['price'],
            reason=signal['reason'],
            p_bullish=0.85  # Placeholder for real-time prob calculation
        )
        
        # 2. Persist the event to TimescaleDB for backtesting audit
        db.log_prediction(
            ticker=signal['ticker'],
            horizon=7, # Defaulting to short-term for Flash
            probability=0.85,
            price=price,
            is_flash=True
        )

if __name__ == "__main__":
    try:
        asyncio.run(main_execution_loop())
    except KeyboardInterrupt:
        print("\nShutting down trade-bot gracefully...")
