import logging
from datetime import datetime


class Validator:

    # -------------------------------------------------
    # 1. NULL VALUE CHECK
    # -------------------------------------------------
    def check_nulls(self, data):

        required_fields = [
            "city",
            "sunrise",
            "sunset",
            "daylight_duration",
            "next_event",
            "time_remaining"
        ]

        for field in required_fields:
            if field not in data or data[field] is None:
                logging.error(f"NULL CHECK FAILED: {field}")
                return False

        return True


    # -------------------------------------------------
    # 2. API RESPONSE VALIDATION
    # (Ensures ETL didn't break upstream)
    # -------------------------------------------------
    def check_api_response(self, raw_data):

        if not raw_data:
            logging.error("API CHECK FAILED: raw_data is None")
            return False

        if "location" not in raw_data or "sun_data" not in raw_data:
            logging.error("API CHECK FAILED: missing keys in raw_data")
            return False

        return True


    # -------------------------------------------------
    # 3. SCHEMA / TYPE VALIDATION
    # -------------------------------------------------
    def check_schema(self, data):

        expected_types = {
            "city": str,
            "sunrise": str,
            "sunset": str,
            "daylight_duration": str,
            "next_event": str,
            "time_remaining": str
        }

        for key, expected_type in expected_types.items():

            if key not in data:
                logging.error(f"SCHEMA CHECK FAILED: missing {key}")
                return False

            if not isinstance(data[key], expected_type):
                logging.error(f"SCHEMA CHECK FAILED: {key} not {expected_type}")
                return False

        return True


    # -------------------------------------------------
    # 4. RANGE VALIDATION (DAYLIGHT SANITY CHECK)
    # -------------------------------------------------
    def check_range(self, data):

        try:
            # format: "14h 36m"
            hours = int(data["daylight_duration"].split("h")[0])

            if hours < 0 or hours > 24:
                logging.error("RANGE CHECK FAILED: invalid daylight hours")
                return False

            return True

        except Exception as e:
            logging.error(f"RANGE CHECK ERROR: {e}")
            return False


    # -------------------------------------------------
    # 5. LOGICAL VALIDATION (SUNRISE < SUNSET)
    # -------------------------------------------------
    def check_sun_logic(self, data):

        try:
            sunrise = datetime.strptime(data["sunrise"], "%Y-%m-%d %I:%M %p")
            sunset = datetime.strptime(data["sunset"], "%Y-%m-%d %I:%M %p")

            if sunrise >= sunset:
                logging.error("LOGIC CHECK FAILED: sunrise >= sunset")
                return False

            return True

        except Exception as e:
            logging.error(f"LOGIC CHECK ERROR: {e}")
            return False