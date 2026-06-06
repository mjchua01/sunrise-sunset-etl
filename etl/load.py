from sqlalchemy import create_engine, text
import pandas as pd
import logging


class Loader:

    def __init__(self):

        self.engine = create_engine(
            "postgresql+psycopg2://postgres:newpassword@localhost:5432/sunrise_db"
        )

    def load_data(self, transformed_data):

        try:
            df = pd.DataFrame([transformed_data])

            # 🔥 FIXED SQLAlchemy 2.0 SYNTAX
            with self.engine.begin() as conn:
                conn.execute(text("DELETE FROM sun_cycle"))

            df.to_sql(
                "sun_cycle",
                self.engine,
                if_exists="append",
                index=False
            )

            print("✅ Load successful")

        except Exception as e:
            logging.error(e)
            print("❌ Load failed")