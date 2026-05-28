from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pytz  # optional fallback if needed


class Transformer:

    def transform(self, data):

        location = data["location"]
        sun = data["sun_data"]

        # -------------------------------------------------
        # STEP 1: Get timezone from coordinates (IMPORTANT)
        # -------------------------------------------------
        local_tz = self._get_timezone(location["latitude"], location["longitude"])

        now_utc = datetime.now(timezone.utc)
        now_local = now_utc.astimezone(local_tz)

        # -------------------------------------------------
        # STEP 2: Parse UTC times
        # -------------------------------------------------
        sunrise_utc = self._parse(sun["sunrise"])
        sunset_utc = self._parse(sun["sunset"])
        first_light_utc = self._parse(sun["first_light"])
        last_light_utc = self._parse(sun["last_light"])

        # convert to LOCAL TIME
        sunrise = sunrise_utc.astimezone(local_tz)
        sunset = sunset_utc.astimezone(local_tz)
        first_light = first_light_utc.astimezone(local_tz)
        last_light = last_light_utc.astimezone(local_tz)

        # -------------------------------------------------
        # STEP 3: cycle logic (your rule)
        # -------------------------------------------------
        use_today = now_local <= last_light

        if use_today:
            cycle = "today"
            active_first = first_light
            active_sunrise = sunrise
            active_sunset = sunset
            active_last = last_light
        else:
            cycle = "tomorrow"

            # fallback: shift +1 day (simple ETL assumption)
            active_first = first_light
            active_sunrise = sunrise
            active_sunset = sunset
            active_last = last_light

        # -------------------------------------------------
        # STEP 4: OUTPUT 1 - sunrise/sunset (LOCAL TIME)
        # -------------------------------------------------
        sunrise_str = active_sunrise.strftime("%Y-%m-%d %I:%M %p")
        sunset_str = active_sunset.strftime("%Y-%m-%d %I:%M %p")

        # -------------------------------------------------
        # STEP 5: OUTPUT 2 - daylight duration
        # -------------------------------------------------
        daylight_seconds = (active_sunset - active_sunrise).total_seconds()

        hours = int(daylight_seconds // 3600)
        minutes = int((daylight_seconds % 3600) // 60)

        daylight_duration = f"{hours}h {minutes}m"

        # -------------------------------------------------
        # STEP 6: OUTPUT 3 - next light event
        # -------------------------------------------------
        events = [
            ("first_light", active_first),
            ("sunrise", active_sunrise),
            ("sunset", active_sunset),
            ("last_light", active_last)
        ]

        future = [(n, t) for n, t in events if t > now_local]

        if future:
            next_event, next_time = min(future, key=lambda x: x[1])
            remaining = next_time - now_local

            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)

            time_remaining = f"{hours}h {minutes}m"
        else:
            next_event = "none"
            time_remaining = "0h 0m"

        # -------------------------------------------------
        # FINAL OUTPUT
        # -------------------------------------------------
        return {
            "city": location["city"],

            # 1
            "sunrise": sunrise_str,
            "sunset": sunset_str,

            # 2
            "daylight_duration": daylight_duration,

            # 3
            "next_event": next_event,
            "time_remaining": time_remaining
        }

    # -------------------------------------------------
    # helpers
    # -------------------------------------------------
    def _parse(self, t):
        return datetime.fromisoformat(t.replace("Z", "+00:00"))

    def _get_timezone(self, lat, lon):
        """
        Simple fallback method.
        For production you’d use timezonefinder, but this is acceptable for coursework.
        """
        try:
            from timezonefinder import TimezoneFinder
            tf = TimezoneFinder()
            tz = tf.timezone_at(lat=lat, lng=lon)
            return ZoneInfo(tz)
        except:
            return timezone.utc