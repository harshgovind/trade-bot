import asyncio
import json
import websockets

# Configuration for high-performance ingestion
POLYGON_API_KEY = "YOUR_POLYGON_API_KEY"
WSS_URL = "wss://socket.polygon.io/stocks" 

# Watchlist includes core stocks and 2027 Call Options
WATCHLIST = ["T.NVDA", "T.AMZN", "T.CSCO", "O:NVDA270115C00150000"] 

async def polygon_handler():
    async with websockets.connect(WSS_URL) as ws:
        # Step 1: Authentication
        auth_msg = {"action": "auth", "params": POLYGON_API_KEY}
        await ws.send(json.dumps(auth_msg))
        
        # Step 2: Subscribe to Trades (T) for the watchlist
        subscribe_msg = {"action": "subscribe", "params": ",".join(WATCHLIST)}
        await ws.send(json.dumps(subscribe_msg))

        print(f"Ingestion Engine Started: Monitoring {len(WATCHLIST)} assets...")

        while True:
            try:
                response = await ws.recv()
                data = json.loads(response)
                
                for event in data:
                    # Logic for the 'Flash Opportunity' Tab
                    if event.get('ev') == 'T':
                        process_trade(event)
                        
            except websockets.ConnectionClosed:
                print("Connection lost. Reconnecting...")
                break

def process_trade(trade):
    # This feeds into the P(Bullish | T) formula
    ticker = trade.get('sym')
    price = trade.get('p')
    print(f"Tick Captured: {ticker} @ {price}")

if __name__ == "__main__":
    asyncio.run(polygon_handler())
