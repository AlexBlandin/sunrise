#!/usr/bin/env python3

from skyfield.timelib import Time
from datetime import datetime
from skyfield import api
from pathlib import Path

load = api.Loader(Path(__file__).parent.absolute(), verbose = False)
ts = load.timescale()
eph = load("de440s-100y.bsp") if (Path(__file__).parent / "de440s-100y.bsp").is_file() else load("de440s.bsp")

from skyfield import almanac
from helpers import format_sunriseset, sortas, day_after, guess_latlon, today, tomorrow

def correct(lat: float = None, lon: float = None, when: datetime = None):
  "When does the sun rise and set?"
  
  if lat is None and lon is None:
    lat, lon = guess_latlon()
  here = api.wgs84.latlon(lat, lon)
  
  if when is None:
    tdy, tmw = today(ts), tomorrow(ts)
  else:
    tdy = when.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    tmw = day_after(tdy)
  
  t0 = ts.utc(tdy.year, tdy.month, tdy.day)
  t1 = ts.utc(tmw.year, tmw.month, tmw.day)
  t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, here))
  
  # for now we assume there's both (so not above artic circle etc)
  sunrise, sunset = map(Time.utc_datetime, reversed(sortas(t, y)))
  return format_sunriseset(sunrise, sunset)

if __name__ == "__main__":
  print(correct())