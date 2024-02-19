#!/usr/bin/env python3
"""
approx sunrise.

Copyright 2022 Alex Blandin
"""

from datetime import datetime
from math import acos, asin, atan, cos, degrees, floor, radians, sin, tan

import pendulum
from helpers import format_sunriseset, guess_latlon


def approx(
  lat: float | tuple[float, float] | None = None, lon: float | None = None, when: datetime | None = None
) -> str:
  """
  Algorithm for approximating this.

  Source:
    Almanac for Computers, 1990
    published by Nautical Almanac Office
    United States Naval Observatory
    Washington, DC 20392
  Archived:
    https://www.edwilliams.org/sunrise_sunset_algorithm.htm
    https://web.archive.org/web/20210115202147/https://edwilliams.org/sunrise_sunset_algorithm.htm.

  Inputs:
    latitude, longitude: location for sunrise/sunset (can be given as a tuple), guesses if None
    when: date for sunrise/sunset (requires day, month, year), guesses if None
  Constants:
    zenith: upper limb of the Sun is tangent to the horizon (90 degrees 50')
  """
  # may also use some from http://answers.google.com/answers/threadview/id/782886.html

  if lat is None or lon is None:
    lat, lon = guess_latlon()
  elif isinstance(lat, tuple):
    lat, lon = lat
  when = (
    pendulum.today() if when is None else pendulum.instance(when).replace(hour=0, minute=0, second=0, microsecond=0)
  )

  def _sunrise(*, rising: bool = True, lat: float = lat, lon: float = lon) -> str | datetime:
    zenith = radians(90 + 50 / 60)

    # 1. first calculate the day of the year
    day_of_year = when.day_of_year  # pendulum is rather marvellous

    # 2. convert the longitude to hour value and calculate an approximate time
    approximate_hour = lon / 15
    local_mean_time = (
      day_of_year + (6 - approximate_hour) / 24 if rising else day_of_year + (18 - approximate_hour) / 24
    )

    # 3. calculate the Sun's mean anomaly
    mean_anomaly = 0.9856 * local_mean_time - 3.289

    # 4. calculate the Sun's true longitude
    longitude = mean_anomaly + 1.916 * sin(radians(mean_anomaly)) + 0.020 * sin(radians(2 * mean_anomaly)) + 282.634
    longitude %= 360

    # 5a. calculate the Sun's right ascension
    right_ascension = degrees(atan(0.91764 * tan(radians(longitude))))
    right_ascension %= 360

    # 5b. right ascension value needs to be in the same quadrant as L
    longitude_quadrant = 90 * floor(longitude / 90)
    right_ascension_quadrant = 90 * floor(right_ascension / 90)
    right_ascension += longitude_quadrant - right_ascension_quadrant

    # 5c. right ascension value needs to be converted into hours
    right_ascension /= 15

    # 6. calculate the Sun's declination
    sin_declination = 0.39782 * sin(radians(longitude))
    cos_declination = cos(asin(sin_declination))

    # 7a. calculate the Sun's local hour angle
    sun_local_hour = (cos(zenith) - (sin_declination * sin(radians(lat)))) / (cos_declination * cos(radians(lat)))
    if sun_local_hour > 1 or sun_local_hour < -1:
      return f"never {'rises' if rising else 'sets'}"

    # 7b. finish calculating H and convert into hours
    hour = 360 - degrees(acos(sun_local_hour)) if rising else degrees(acos(sun_local_hour))
    hour = hour / 15

    # 8. calculate local mean time of rising/setting
    local_mean_time = hour + right_ascension - 0.06571 * local_mean_time - 6.622

    # 9. adjust back to UTC
    utc_time = local_mean_time - approximate_hour
    utc_time %= 24

    # 10. convert UT value to local time zone of latitude/longitude
    timezone = lon // 15
    local_time = utc_time + timezone

    # 11. convert to human-readable time
    seconds = int(local_time * 3600)
    secs, mins, hours = seconds % 60, seconds % 3600 // 60, seconds % 86400 // 3600
    return when + pendulum.duration(hours=hours + when.offset_hours + 1, minutes=mins, seconds=secs)  # type: ignore  # noqa: PGH003

  return format_sunriseset(_sunrise(), _sunrise(rising=False))  # type: ignore  # noqa: PGH003


if __name__ == "__main__":
  print(approx())  # use sun(dms_to_latlon("51°30′26″N 0°7′39″W")) for the sunrise in London today  # noqa: RUF003
