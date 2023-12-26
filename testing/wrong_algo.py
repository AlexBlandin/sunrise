#!/usr/bin/env python3

from math import degrees as deg, radians as rad
from math import sin, cos, tan, asin, acos
from datetime import datetime

from helpers import format_sunriseset, guess_latlon


def algo2(lat: float | None = None, lon: float | None = None, when: datetime | None = None):  # noqa: PLR0914
  """
  Calculate sunrise and sunset based on equations from NOAA
  http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html
  """
  if lat is None and lon is None:
    lat, lon = guess_latlon()
  if when is None:
    when = datetime.utcnow()

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

  Jday = day + 2415018.5 + time - timezone / 24  # Julian day
  Jcent = (Jday - 2451545) / 36525  # Julian century

  Manom = 357.52911 + Jcent * (35999.05029 - 0.0001537 * Jcent)
  Mlong = 280.46646 + Jcent * (36000.76983 + Jcent * 0.0003032) % 360
  Eccent = 0.016708634 - Jcent * (0.000042037 + 0.0001537 * Jcent)
  Mobliq = 23 + (26 + (21.448 - Jcent * (46.815 + Jcent * (0.00059 - Jcent * 0.001813))) / 60) / 60
  obliq = Mobliq + 0.00256 * cos(rad(125.04 - 1934.136 * Jcent))
  vary = tan(rad(obliq / 2)) * tan(rad(obliq / 2))
  Seqcent = (
    sin(rad(Manom)) * (1.914602 - Jcent * (0.004817 + 0.000014 * Jcent)) + sin(rad(2 * Manom)) * (0.019993 - 0.000101 * Jcent) + sin(rad(3 * Manom)) * 0.000289
  )
  Struelong = Mlong + Seqcent
  Sapplong = Struelong - 0.00569 - 0.00478 * sin(rad(125.04 - 1934.136 * Jcent))
  declination = deg(asin(sin(rad(obliq)) * sin(rad(Sapplong))))

  eqtime = 4 * deg(
    vary * sin(2 * rad(Mlong))
    - 2 * Eccent * sin(rad(Manom))
    + 4 * Eccent * vary * sin(rad(Manom)) * cos(2 * rad(Mlong))
    - 0.5 * vary * vary * sin(4 * rad(Mlong))
    - 1.25 * Eccent * Eccent * sin(2 * rad(Manom))
  )

  hourangle = deg(acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(declination))) - tan(rad(latitude)) * tan(rad(declination))))  # type: ignore

  solarnoon_t = (720 - 4 * longitude - eqtime + timezone * 60) / 1440  # type: ignore
  sunrise_t = solarnoon_t - hourangle * 4 / 1440
  sunset_t = solarnoon_t + hourangle * 4 / 1440

  def as_datetime(dd):
    """
    dd is a decimal day between 0.0 and 1.0, e.g. noon = 0.5
    """
    hours = 24.0 * dd
    h = int(hours)
    minutes = (hours - h) * 60
    m = int(minutes)
    seconds = (minutes - m) * 60
    s = int(seconds)
    return datetime(year=when.year, month=when.month, day=when.day, hour=h, minute=m, second=s)

  sunrise, sunset = as_datetime(sunrise_t), as_datetime(sunset_t)
  return format_sunriseset(sunrise, sunset)


if __name__ == "__main__":
  print(algo2())
