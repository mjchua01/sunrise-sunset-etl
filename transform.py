from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class Transformer:

    def transform(self, data):

        location = data["location"]
        sun = data["sun_data"]

        local_tz = self._get_timezone(
            location["latitude"],
            location["longitude"]
        )

        now_local = datetime.now(timezone.utc).astimezone(local_tz)

        sunrise = self._parse(sun["sunrise"]).astimezone(local_tz)
        sunset = self._parse(sun["sunset"]).astimezone(local_tz)
        first_light = self._parse(sun["first_light"]).astimezone(local_tz)

        # -------------------------
        # DURATION
        # -------------------------
        daylight_seconds = (sunset - sunrise).total_seconds()
        hours = int(daylight_seconds // 3600)
        minutes = int((daylight_seconds % 3600) // 60)
        daylight_duration = f"{hours}h {minutes}m"

        # -------------------------
        # NEXT EVENT
        # -------------------------
        events = [
            ("first_light", first_light),
            ("sunrise", sunrise),
            ("sunset", sunset)
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

        return {
            "city": location["city"],
            "sunrise": sunrise.strftime("%Y-%m-%d %I:%M %p"),
            "sunset": sunset.strftime("%Y-%m-%d %I:%M %p"),
            "daylight_duration": daylight_duration,
            "next_event": next_event,
            "time_remaining": time_remaining
        }

    def _parse(self, t):
        return datetime.fromisoformat(t.replace("Z", "+00:00"))

    def _get_timezone(self, lat, lon):
        try:
            from timezonefinder import TimezoneFinder
            tf = TimezoneFinder()
            tz = tf.timezone_at(lat=lat, lng=lon)
            return ZoneInfo(tz)
        except:
            return timezone.utc