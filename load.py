from sqlalchemy import create_engine
import pandas as pd
import logging


class Loader:

    def __init__(self):

        # ----------------------------------------
        # UPDATE THESE WITH YOUR POSTGRES INFO
        # ----------------------------------------
        username = "postgres"
        password = "newpassword"
        host = "localhost"
        port = "5432"
        database = "sunrise_db"

        # SQLAlchemy connection string
        self.engine = create_engine(
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        )

    # -------------------------------------------------
    # LOAD DATA INTO POSTGRES
    # -------------------------------------------------
    def load_data(self, transformed_data):

        try:

            # Convert dictionary -> DataFrame
            df = pd.DataFrame([transformed_data])

            # Load into PostgreSQL
            df.to_sql(
                name="sun_cycle",
                con=self.engine,
                if_exists="append",
                index=False
            )

            logging.info("Data loaded successfully")

            print("\n✅ Data loaded into PostgreSQL")

        except Exception as e:

            logging.error(f"Load error: {e}")
            print(f"\n❌ Load failed: {e}")