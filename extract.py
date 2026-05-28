import requests
import logging
import time


# =====================================================
# LOGGING CONFIG (IMPORTANT FOR REPRODUCIBILITY)
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =====================================================
# API ENDPOINTS
# =====================================================
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
SUN_API_URL = "https://api.sunrise-sunset.org/json"


class Extractor:

    # =================================================
    # GET LOCATION (CITY → LAT/LON)
    # =================================================
    def get_location(self, city_name):

        for attempt in range(3):

            try:

                logging.info(f"Geocoding attempt {attempt+1} for {city_name}")

                response = requests.get(
                    GEOCODE_URL,
                    params={
                        "q": city_name,
                        "format": "json",
                        "limit": 1
                    },
                    headers={"User-Agent": "sunrise-app"}
                )

                response.raise_for_status()
                data = response.json()

                if data:
                    result = data[0]

                    logging.info("Geocoding successful")

                    return {
                        "city": city_name,
                        "latitude": float(result["lat"]),
                        "longitude": float(result["lon"])
                    }

                else:
                    logging.warning("No geocoding results found")

            except Exception as e:

                logging.warning(f"Geocoding attempt {attempt+1} failed: {e}")
                time.sleep(2)

        logging.error("Geocoding failed after 3 attempts")
        return None


    # =================================================
    # GET SUN DATA (SUNRISE / SUNSET / TWILIGHT)
    # =================================================
    def get_sun_data(self, latitude, longitude, date="today"):

        params = {
            "lat": latitude,
            "lng": longitude,
            "date": date,
            "formatted": 0
        }

        for attempt in range(3):

            try:

                logging.info(f"Sun API attempt {attempt+1}")

                response = requests.get(SUN_API_URL, params=params)
                response.raise_for_status()

                data = response.json()["results"]

                logging.info("Sun API extraction successful")

                return {
                    # REQUIRED BY YOUR OBJECTIVES
                    "sunrise": data["sunrise"],
                    "sunset": data["sunset"],
                    "day_length_seconds": float(data["day_length"]),

                    # FIRST / LAST LIGHT (OBJECTIVE MAPPING)
                    "first_light": data["civil_twilight_begin"],
                    "last_light": data["civil_twilight_end"]
                }

            except Exception as e:

                logging.warning(f"Sun API attempt {attempt+1} failed: {e}")
                time.sleep(2)

        logging.error("Sun API failed after 3 attempts")
        return None


    # =================================================
    # FULL EXTRACTION PIPELINE (USED BY MAIN / DASH)
    # =================================================
    def extract_all(self, city_name):

        try:

            location = self.get_location(city_name)

            if not location:
                logging.error("Extraction failed at location step")
                return None

            sun_data = self.get_sun_data(
                location["latitude"],
                location["longitude"]
            )

            if not sun_data:
                logging.error("Extraction failed at sun data step")
                return None

            logging.info("Full extraction pipeline successful")

            return {
                "location": location,
                "sun_data": sun_data
            }

        except Exception as e:

            logging.error(f"Unexpected extraction error: {e}")
            return None