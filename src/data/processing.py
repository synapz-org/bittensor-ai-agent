import pandas as pd
from typing import List, Dict
import sqlite3
import json


class DataProcessor:
    def __init__(self, db_path: str = "data/metrics.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database with required schema."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subnet_metrics (
                timestamp INTEGER,
                subnet_id INTEGER,
                emissions REAL,
                pow_threshold REAL,
                PRIMARY KEY (timestamp, subnet_id)
            )
        """
        )
        conn.close()

    def process_subnet_data(self, raw_data: Dict) -> pd.DataFrame:
        """Process raw subnet data into a structured format."""
        df = pd.DataFrame(raw_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    def save_metrics(self, df: pd.DataFrame):
        """Save processed metrics to database."""
        conn = sqlite3.connect(self.db_path)
        df.to_sql("subnet_metrics", conn, if_exists="append", index=False)
        conn.close()
