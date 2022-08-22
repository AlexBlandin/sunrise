#!/usr/bin/env python3

from datetime import datetime
from typing import Union

from skyfield import api
from pathlib import Path

load = api.Loader(Path(__file__).parent.absolute(), verbose = False)
ts = load.timescale()
eph = load("de440s-100y.bsp") if (Path(__file__).parent / "de440s-100y.bsp").is_file() else load("de440s.bsp")

from skyfield import almanac
import pendulum

from helpers import format_sunriseset, sortas, guess_latlon

def correct(lat: Union[float, tuple[float, float], None] = None, lon: Union[float, None] = None, when: Union[datetime, None] = None):
  "When does the sun rise and set?"
  
  if lat is None and lon is None:
    lat, lon = guess_latlon()
  elif isinstance(lat, tuple):
    lat, lon = lat
  here = api.wgs84.latlon(lat, lon)
  
  if when is None:
    tdy, tmw = pendulum.today(), pendulum.tomorrow()
  else:
    tdy = pendulum.instance(when)
    tmw = (when + pendulum.duration(days = 1, hours = tdy.offset_hours)).replace(hour = 0)
  
  t0 = ts.utc(tdy.year, tdy.month, tdy.day)
  t1 = ts.utc(tmw.year, tmw.month, tmw.day)
  t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, here))
  
  # for now we assume there's both (so not above artic circle etc)
  sunrise, sunset = map(lambda t: t.astimezone(pendulum.tz.local_timezone()), reversed(sortas(t, y)))
  return format_sunriseset(sunrise, sunset)

if __name__ == "__main__":
  print(correct())
