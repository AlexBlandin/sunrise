#!/usr/bin/env -S uv run -qqs
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "attrs",
#   "cattrs",
#   "geocoder@https://github.com/AlexBlandin/geocoder3.git",
#   "whenever",
#   # "skyfield",
# ]
# ///
#
"""
approx sunrise.

Copyright 2021 Alex Blandin
"""

from datetime import datetime
from math import acos, asin, atan, cos, degrees, floor, radians, sin, tan

import whenever

from .helpers import LatLon, current_day, current_position, format_sunrise_sunset


def approx(
  where: str | LatLon | tuple[float, float] | None = None,
  when: whenever.SystemDateTime | datetime | (str | None) = None,
  *,
  simple: bool = False,
) -> str:
  """
  When will the sun rise (and set) today?

  Source:
    Almanac for Computers, 1990
    published by Nautical Almanac Office
    United States Naval Observatory
    Washington, DC 20392
  Archived:
    https://www.edwilliams.org/sunrise_sunset_algorithm.htm
    https://web.archive.org/web/20210115202147/https://edwilliams.org/sunrise_sunset_algorithm.htm.

  Inputs:
    where: location for sunrise/sunset (given as lat/lon tuple), guesses if None
    when: date for sunrise/sunset (requires day, month, year), guesses if None
  Constants:
    zenith: upper limb of the Sun is tangent to the horizon (90 degrees 50')
  """
  # may also use some from http://answers.google.com/answers/threadview/id/782886.html
  latlon = current_position(where)
  latitude, longitude = latlon.lat, latlon.lon

  day = current_day(when)

  def _sunrise(*, rising: bool = True) -> str | whenever.SystemDateTime:
    zenith = radians(90 + 50 / 60)

    # 1. first calculate the day of the year
    day_of_year = day.date().days_since(whenever.Date(day.year, 1, 1)) + 1

    # 2. convert the longitude to hour value and calculate an approximate time
    lng_hour = longitude / 15
    t = day_of_year + ((6 - lng_hour) if rising else (18 - lng_hour)) / 24

    # 3. calculate the Sun's mean anomaly
    m = 0.9856 * t - 3.289

    # 4. calculate the Sun's true longitude
    tl = m + 1.916 * sin(radians(m)) + 0.020 * sin(radians(2 * m)) + 282.634
    tl %= 360

    # 5a. calculate the Sun's right ascension
    ra = degrees(atan(0.91764 * tan(radians(tl))))
    ra %= 360

    # 5b. right ascension value needs to be in the same quadrant as L
    l_quad = 90 * floor(tl / 90)
    ra_quad = 90 * floor(ra / 90)
    ra += l_quad - ra_quad

    # 5c. right ascension value needs to be converted into hours
    ra /= 15

    # 6. calculate the Sun's declination
    sin_dec = 0.39782 * sin(radians(tl))
    cos_dec = cos(asin(sin_dec))

    # 7a. calculate the Sun's local hour angle
    cos_local_h = (cos(zenith) - (sin_dec * sin(radians(latitude)))) / (cos_dec * cos(radians(latitude)))
    if cos_local_h > 1 or cos_local_h < -1:
      return f"never {'rises' if rising else 'sets'}"

    # 7b. finish calculating H and convert into hours
    h = degrees(acos(cos_local_h))
    if rising:
      h = 360 - h
    h = h / 15

    # 8. calculate local mean time of rising/setting
    t = h + ra - 0.06571 * t - 6.622

    # 9. adjust back to UTC
    ut = t - lng_hour
    ut %= 24

    # convert to human-readable time
    seconds = int(ut * 3600)
    secs, mins, hours = seconds % 60, seconds % 3600 // 60, seconds % 86400 // 3600

    return day.date().at(whenever.Time(hours, mins, secs)).assume_utc().to_system_tz()

  return format_sunrise_sunset(_sunrise(), _sunrise(rising=False), pretty=not simple)


if __name__ == "__main__":
  print(approx())  # use sun(dms_to_latlon("51°30′26″N 0°7′39″W")) for the sunrise in London today  # noqa: RUF003, T201
