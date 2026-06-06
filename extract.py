import requests
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
SUN_API_URL = "https://api.sunrise-sunset.org/json"


class Extractor:

    def get_location(self, city_name):

        for attempt in range(3):
            try:
                logging.info(f"Geocoding attempt {attempt+1} for {city_name}")

                response = requests.get(
                    GEOCODE_URL,
                    params={"q": city_name, "format": "json", "limit": 1},
                    headers={"User-Agent": "sunrise-app"}
                )

                response.raise_for_status()
                data = response.json()

                if data:
                    result = data[0]
                    return {
                        "city": city_name,
                        "latitude": float(result["lat"]),
                        "longitude": float(result["lon"])
                    }

            except Exception as e:
                logging.warning(e)
                time.sleep(2)

        return None

    def get_sun_data(self, latitude, longitude, date="today"):

        for attempt in range(3):
            try:
                response = requests.get(
                    SUN_API_URL,
                    params={
                        "lat": latitude,
                        "lng": longitude,
                        "date": date,
                        "formatted": 0
                    }
                )

                response.raise_for_status()
                data = response.json()["results"]

                return {
                    "sunrise": data["sunrise"],
                    "sunset": data["sunset"],
                    "first_light": data["civil_twilight_begin"],
                    "last_light": data["civil_twilight_end"]
                }

            except Exception:
                time.sleep(2)

        return None

    def extract_all(self, city_name):

        location = self.get_location(city_name)
        if not location:
            return None

        sun_data = self.get_sun_data(
            location["latitude"],
            location["longitude"]
        )

        if not sun_data:
            return None

        return {
            "location": location,
            "sun_data": sun_data
        }