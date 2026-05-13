import psycopg2
from psycopg2.extras import execute_values
import datetime

class DataPersistence:
    def __init__(self):
        # Database connection parameters
        self.conn_params = "dbname=trade_bot user=harshal host=localhost password=yourpassword"

    def init_db(self):
        """
        Initializes the schema and creates the TimescaleDB Hypertable.
        """
        with psycopg2.connect(self.conn_params) as conn:
            with conn.cursor() as cur:
                # Table to audit model predictions vs actual results
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS prediction_audit (
                        time TIMESTAMPTZ NOT NULL,
                        ticker TEXT NOT NULL,
                        horizon_days INT NOT NULL,
                        prob_bullish DOUBLE PRECISION,
                        entry_price DOUBLE PRECISION,
                        is_flash BOOLEAN
                    );
                """)
                # Convert to Hypertable for time-series optimization
                cur.execute("SELECT create_hypertable('prediction_audit', 'time', if_not_exists => TRUE);")
            conn.commit()

    def log_prediction(self, ticker, horizon, probability, price, is_flash=False):
        """
        Saves a generated prediction to the database for future backtesting.
        """
        with psycopg2.connect(self.conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO prediction_audit (time, ticker, horizon_days, prob_bullish, entry_price, is_flash)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (datetime.datetime.now(), ticker, horizon, probability, price, is_flash))
            conn.commit()

# Usage Example
if __name__ == "__main__":
    db = DataPersistence()
    db.init_db()
    # Log a mock prediction for NVDA at your target floor
    db.log_prediction("NVDA", 7, 0.88, 15.21, is_flash=True)
    print("Prediction logged to TimescaleDB.")
