"""
sunrise helpers.

Copyright 2022 Alex Blandin
"""

from datetime import datetime
from operator import itemgetter, mul
from typing import NamedTuple

import pendulum
from geocoder import ip


class LatLon(NamedTuple):  # noqa: D101
  lat: float
  lon: float


def guess_latlon():  # noqa: ANN201, D103
  return LatLon(*ip("me").latlng)


def sortas(first: list, second: list):  # noqa: ANN201, D103
  return list(map(itemgetter(0), sorted(zip(first, second, strict=False), key=itemgetter(1))))


def nearest_minute(dt: datetime):  # noqa: ANN201, D103
  return (dt + pendulum.duration(seconds=30)).replace(second=0, microsecond=0)


def format_sunriseset(sunrise: datetime, sunset: datetime) -> str:  # noqa: D103
  return f"🌅: {nearest_minute(sunrise):%H:%M} 🌇: {nearest_minute(sunset):%H:%M}"


def dms_to_latlon(s: str):  # noqa: ANN201
  """
  Convert degree-minute-second co-ordinates (as you'd get off Wikipedia) to decimal latitude and longitude.

  NE is positive, SW is negative.

  >>> London = dms_to_latlon("51°30′26″N 0°7′39″W")
  LatLon(51.71666666666667, -0.44166666666666665)
  >>> Roughly_London = dms_to_latlon("51°30′N 0°7′W")
  LatLon(51.5, -0.11666666666666667)
  """  # noqa: RUF002
  ns, ew = tuple(list(map(int, "".join(c if c.isnumeric() else " " for c in p).split())) for p in s.split(maxsplit=1))
  north, east = 1 if "N" in s.upper() else -1, 1 if "E" in s.upper() else -1

  def convert(dms):  # noqa: ANN001, ANN202
    return sum(map(mul, dms, [1] + [1 / (i * 60) for i in range(1, len(dms))]))

  return LatLon(north * convert(ns), east * convert(ew))


if __name__ == "__main__":
  print(guess_latlon())
