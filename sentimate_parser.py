import openai
import os

# Initialize OpenAI Client
client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")

def get_sentiment_vector(ticker, news_text):
    """
    Uses LLM to analyze news impact and return a normalized score.
    Logic: Focuses on semiconductor demand and structural catalysts.
    """
    
    system_prompt = f"""
    You are a Senior Equity Analyst specializing in Semiconductors and Big Tech.
    Analyze the provided text for {ticker} and provide a sentiment score.
    
    RULES:
    1. Score must be a float between -1.0 (Very Bearish) and 1.0 (Very Bullish).
    2. Focus on structural demand, AI infrastructure growth, and supply chain resilience.
    3. Ignore short-term retail 'noise' unless it affects institutional liquidity.
    4. Provide the output in strictly valid JSON format: {{"score": float, "impact_days": int}}.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo for cost-efficiency
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this for {ticker}: {news_text}"}
            ],
            response_format={ "type": "json_object" }
        )
        
        result = response.choices[0].message.content
        data = json.loads(result)
        
        # This score feeds the w3 weight in probability_model.py
        return data.get("score", 0.0)
        
    except Exception as e:
        print(f"Sentiment Analysis Error: {e}")
        return 0.0 # Neutral fallback
