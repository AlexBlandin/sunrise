#!/usr/bin/env python3
"""
correct sunrise.

Copyright 2021 Alex Blandin
"""

from datetime import datetime

import pendulum
from skyfield import almanac  # pyright: ignore[reportMissingTypeStubs]
from skyfield.api import Loader, wgs84  # pyright: ignore[reportMissingTypeStubs]

from .helpers import DATA_DIR, LatLon, format_sunriseset, sortas

load = Loader(DATA_DIR.absolute(), verbose=False)
ts = load.timescale()
eph = load(DATA_DIR / "de440s-100y.bsp") if (DATA_DIR / "de440s-100y.bsp").is_file() else load(DATA_DIR / "de440s.bsp")


def correct(lat: float | (tuple[float, float] | None) = None, lon: float | None = None, when: datetime | None = None):  # noqa: ANN201
  """When does the sun rise and set?"""
  if lat is None and lon is None:
    lat, lon = LatLon.guess().tuple()
  elif isinstance(lat, tuple):
    lat, lon = lat
  here = wgs84.latlon(lat, lon)

  if when is None:
    tdy, tmw = pendulum.today(), pendulum.tomorrow()
  else:
    tdy = pendulum.instance(when)
    tmw = (when + pendulum.duration(days=1, hours=tdy.offset_hours or 0)).replace(hour=0)

  t0 = ts.utc(tdy.year, tdy.month, tdy.day)
  t1 = ts.utc(tmw.year, tmw.month, tmw.day)
  t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, here))

  # for now we assume there's both (so not above artic circle etc)
  sunrise, sunset = (t.astimezone(pendulum.local_timezone()) for t in reversed(sortas(t, y)))
  return format_sunriseset(sunrise, sunset)


if __name__ == "__main__":
  print(correct())  # noqa: T201
