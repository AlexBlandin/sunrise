#!/usr/bin/env python3
"""
correct sunrise.

Copyright 2021 Alex Blandin
"""

from datetime import datetime

import whenever
from skyfield import almanac  # pyright: ignore[reportMissingTypeStubs]
from skyfield.api import Loader, wgs84  # pyright: ignore[reportMissingTypeStubs]

from .helpers import DATA_DIR, LatLon, current_day, current_position, format_sunrise_sunset

load = Loader(DATA_DIR.absolute(), verbose=False)
ts = load.timescale()
eph = load("de440s-100y.bsp") if (DATA_DIR / "de440s-100y.bsp").is_file() else load("de440s.bsp")


def correct(
  where: str | LatLon | tuple[float, float] | None = None,
  when: whenever.SystemDateTime | datetime | (str | None) = None,
  *,
  simple: bool = False,
) -> str:
  """
  When will the sun rise (and set) today?

  Inputs:
    where: location for sunrise/sunset (given as lat/lon tuple), guesses if None
    when: date for sunrise/sunset (YYYY-MM-DD if str), uses current system datetime if None
  """
  # may also use some from http://answers.google.com/answers/threadview/id/782886.html
  latlon = current_position(where)
  lat, lon = latlon.tuple()
  here = wgs84.latlon(lat, lon)

  tdy = current_day(when)
  tmw = tdy.add(days=1)

  t0 = ts.utc(tdy.year, tdy.month, tdy.day)
  t1 = ts.utc(tmw.year, tmw.month, tmw.day)

  sun = eph["Sun"]
  observer = eph["Earth"] + here
  (sunrise, *t), (sun_rose, *y) = almanac.find_risings(observer, sun, t0, t1)
  (sunset, *t), (sun_sets, *y) = almanac.find_settings(observer, sun, t0, t1)
  sunrise, sunset = (
    whenever.Instant.parse_rfc3339(sunrise.utc_iso()).to_system_tz(),
    whenever.Instant.parse_rfc3339(sunset.utc_iso()).to_system_tz(),
  )
  return format_sunrise_sunset(sunrise, sunset, pretty=not simple, sun_rose=sun_rose, sun_sets=sun_sets)


if __name__ == "__main__":
  print(correct())  # noqa: T201
