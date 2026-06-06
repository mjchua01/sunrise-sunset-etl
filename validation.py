import logging


class Validator:

    def check_nulls(self, data):

        required = [
            "city",
            "sunrise",
            "sunset",
            "daylight_duration",
            "next_event",
            "time_remaining"
        ]

        for f in required:
            if f not in data or data[f] is None:
                logging.error(f"NULL FAILED: {f}")
                return False

        return True

    def check_format(self, data):

        if "h" not in data["daylight_duration"]:
            logging.error("FORMAT FAILED")
            return False

        return True

    def check_logic(self, data):

        if data["next_event"] not in ["sunrise", "sunset", "first_light", "none"]:
            logging.error("LOGIC FAILED")
            return False

        return True