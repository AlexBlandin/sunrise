#!/usr/bin/env python3
"""
correct sunrise.

Copyright 2021 Alex Blandin
"""

from datetime import datetime

import pendulum
from skyfield import almanac  # pyright: ignore[reportMissingTypeStubs]
from skyfield.api import Loader, wgs84  # pyright: ignore[reportMissingTypeStubs]

from .helpers import DATA_DIR, LatLon, current_position, format_sunrise_sunset

load = Loader(DATA_DIR.absolute(), verbose=False)
ts = load.timescale()
eph = load("de440s-100y.bsp") if (DATA_DIR / "de440s-100y.bsp").is_file() else load("de440s.bsp")


def correct(
  where: str | LatLon | tuple[float, float] | None = None,
  when: pendulum.DateTime | datetime | (str | None) = None,
  simple: bool | None = None,
) -> str:
  """
  When will the sun rise (and set) today?

  Inputs:
    where: location for sunrise/sunset (given as lat/lon tuple), guesses if None
    when: date for sunrise/sunset (requires day, month, year), guesses if None
  """
  # may also use some from http://answers.google.com/answers/threadview/id/782886.html
  latlon = current_position(where)
  lat, lon = latlon.tuple()
  here = wgs84.latlon(lat, lon)

  if when is None:
    tdy, tmw = pendulum.today(), pendulum.tomorrow()
  else:
    tdy = pendulum.instance(when)
    tmw = (when + pendulum.duration(days=1, hours=tdy.offset_hours or 0)).replace(hour=0)

  t0 = ts.utc(tdy.year, tdy.month, tdy.day)
  t1 = ts.utc(tmw.year, tmw.month, tmw.day)

  sun = eph["Sun"]
  observer = eph["Earth"] + here
  (sunrise, *t), (sun_rose, *y) = almanac.find_risings(observer, sun, t0, t1)
  (sunset, *t), (sun_sets, *y) = almanac.find_settings(observer, sun, t0, t1)
  sunrise, sunset = pendulum.parse(sunrise.utc_iso(" ")).astimezone(), pendulum.parse(sunset.utc_iso(" ")).astimezone()
  return format_sunrise_sunset(sunrise, sunset, pretty=not simple, sun_rose=sun_rose, sun_sets=sun_sets)


if __name__ == "__main__":
  print(correct())  # noqa: T201
