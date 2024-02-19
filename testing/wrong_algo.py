#!/usr/bin/env python3
"""
sunrise wrong algo.

Copyright 2022 Alex Blandin
"""

from datetime import UTC, datetime
from math import acos, asin, cos, sin, tan
from math import degrees as deg
from math import radians as rad

from helpers import format_sunriseset, guess_latlon


def algo2(lat: float | None = None, lon: float | None = None, when: datetime | None = None) -> str:
  """
  Calculate sunrise and sunset based on equations from NOAA.

  http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html.
  """
  if lat is None or lon is None:
    lat, lon = guess_latlon()
  if when is None:
    when = datetime.now(UTC)

  # datetime days are numbered in the Gregorian calendar
  # while the calculations from NOAA are distibuted as
  # OpenOffice spreadsheets with days numbered from
  # 1/1/1900. The difference are those numbers taken for
  # 18/12/2010
  day = when.toordinal() - (734124 - 40529)  # daynumber 1=1/1/1900
  t = when.time()
  time = (t.hour + t.minute / 60.0 + t.second / 3600.0) / 24.0  # percentage past midnight, i.e. noon is 0.5

  timezone = 0  # in hours, east is positive
  offset = when.utcoffset()
  if offset is not None:
    timezone = offset.seconds / 3600.0 + (offset.days * 24)

  longitude = lon  # in decimal degrees, east is positive
  latitude = lat  # in decimal degrees, north is positive

  julian_day = day + 2415018.5 + time - timezone / 24  # Julian day
  julian_century = (julian_day - 2451545) / 36525  # Julian century

  m_anom = 357.52911 + julian_century * (35999.05029 - 0.0001537 * julian_century)
  m_long = 280.46646 + julian_century * (36000.76983 + julian_century * 0.0003032) % 360
  eccent = 0.016708634 - julian_century * (0.000042037 + 0.0001537 * julian_century)
  m_obliq = (
    23 + (26 + (21.448 - julian_century * (46.815 + julian_century * (0.00059 - julian_century * 0.001813))) / 60) / 60
  )
  obliq = m_obliq + 0.00256 * cos(rad(125.04 - 1934.136 * julian_century))
  vary = tan(rad(obliq / 2)) * tan(rad(obliq / 2))
  seqcent = (
    sin(rad(m_anom)) * (1.914602 - julian_century * (0.004817 + 0.000014 * julian_century))
    + sin(rad(2 * m_anom)) * (0.019993 - 0.000101 * julian_century)
    + sin(rad(3 * m_anom)) * 0.000289
  )
  sun_truelong = m_long + seqcent
  sun_applong = sun_truelong - 0.00569 - 0.00478 * sin(rad(125.04 - 1934.136 * julian_century))
  declination = deg(asin(sin(rad(obliq)) * sin(rad(sun_applong))))

  eqtime = 4 * deg(
    vary * sin(2 * rad(m_long))
    - 2 * eccent * sin(rad(m_anom))
    + 4 * eccent * vary * sin(rad(m_anom)) * cos(2 * rad(m_long))
    - 0.5 * vary * vary * sin(4 * rad(m_long))
    - 1.25 * eccent * eccent * sin(2 * rad(m_anom)),
  )

  hourangle = deg(
    acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(declination))) - tan(rad(latitude)) * tan(rad(declination)))
  )

  solarnoon_t = (720 - 4 * longitude - eqtime + timezone * 60) / 1440
  sunrise_t = solarnoon_t - hourangle * 4 / 1440
  sunset_t = solarnoon_t + hourangle * 4 / 1440

  def as_datetime(dd):  # noqa: ANN001, ANN202
    """Dd is a decimal day between 0.0 and 1.0, e.g. noon = 0.5."""
    hours = 24.0 * dd
    h = int(hours)
    minutes = (hours - h) * 60
    m = int(minutes)
    seconds = (minutes - m) * 60
    s = int(seconds)
    return datetime(year=when.year, month=when.month, day=when.day, hour=h, minute=m, second=s, tzinfo=UTC)

  sunrise, sunset = as_datetime(sunrise_t), as_datetime(sunset_t)
  return format_sunriseset(sunrise, sunset)


if __name__ == "__main__":
  print(algo2())
