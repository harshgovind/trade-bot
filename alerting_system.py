import os
from twilio.rest import Client

class AlertingSystem:
    def __init__(self):
        # Credentials should be stored in environment variables for security
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.from_number = os.environ.get('TWILIO_PHONE_NUMBER')
        self.to_number = os.environ.get('USER_PHONE_NUMBER') # Your Dublin, CA mobile
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("Warning: Twilio credentials not found. SMS alerts disabled.")

    def send_flash_alert(self, ticker, price, reason, p_bullish):
        """
        Dispatches a high-priority SMS for 'Must-Take' opportunities.
        """
        message_body = (
            f"🚨 FLASH ALERT: {ticker}\n"
            f"Price: ${price}\n"
            f"P(Bullish): {p_bullish:.2%}\n"
            f"Reason: {reason}\n"
            f"Action: Check 2027 LEAPS chain."
        )

        if self.client:
            try:
                message = self.client.messages.create(
                    body=message_body,
                    from_=self.from_number,
                    to=self.to_number
                )
                print(f"SMS Alert sent for {ticker}: {message.sid}")
            except Exception as e:
                print(f"Failed to send SMS: {e}")
        else:
            print(f"Priority Alert (Console Only): {message_body}")

    def send_daily_summary(self, top_5_list):
        """
        Sends a lower-priority summary of the top 5 ranking assets.
        """
        summary = "Daily Top 5 Opportunities:\n"
        for i, item in enumerate(top_5_list, 1):
            summary += f"{i}. {item['ticker']} - Score: {item['final_score']:.2f}\n"
        
        # Typically sent via email or Slack/Discord webhook
        print(f"Dispatching Daily Summary...\n{summary}")

# Usage Example
if __name__ == "__main__":
    alert_sys = AlertingSystem()
    # Mocking a hit on your NVDA floor
    alert_sys.send_flash_alert("NVDA", 15.21, "Hit Golden Entry Support", 0.88)
