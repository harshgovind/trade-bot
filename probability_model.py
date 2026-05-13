def calculate_bullish_probability(ticker, time_horizon_days):
    """
    Implements the core formula: 
    P(Bullish | T) = w1(T)*Tech(x) + w2(T)*Fund(x) + w3(T)*Sent(x)
    """
    
    # 1. Fetch normalized feature vectors (0.0 to 1.0)
    tech_score = get_technical_vector(ticker)   # RSI, MACD, Volume
    fund_score = get_fundamental_vector(ticker) # EPS, P/E, Debt
    sent_score = get_sentiment_vector(ticker)   # LLM Sentiment Analysis
    
    # 2. Dynamic Weight Routing Logic
    if time_horizon_days <= 7:
        # Short-term: Prioritize Technicals and Sentiment
        w_tech, w_fund, w_sent = 0.70, 0.05, 0.25
    elif time_horizon_days >= 360:
        # Long-term: Prioritize Fundamentals
        w_tech, w_fund, w_sent = 0.10, 0.70, 0.20
    else:
        # Mid-term: Balanced weights (Linear Interpolation)
        w_tech = 0.70 - (0.60 * (time_horizon_days / 365))
        w_fund = 0.05 + (0.65 * (time_horizon_days / 365))
        w_sent = 1.0 - (w_tech + w_fund)
        
    # 3. Final Probability Calculation
    p_bullish = (w_tech * tech_score) + (w_fund * fund_score) + (w_sent * sent_score)
    
    return round(p_bullish, 4)
