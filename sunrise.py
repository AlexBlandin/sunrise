#!/usr/bin/env python3

from skyfield.timelib import Timescale, Time
from datetime import timedelta, datetime
from skyfield import api
from pathlib import Path

load = api.Loader(Path(__file__).parent.absolute(), verbose = False)
ts = load.timescale()
eph = load("de440s-100y.bsp") if (Path(__file__).parent / "de440s-100y.bsp").is_file() else load("de440s.bsp")

from skyfield import almanac
from geocoder import ip
from helpers import format_sunriseset, sortas, day_after

def today(ts: Timescale):
  return ts.now().utc_datetime().replace(hour = 0, minute = 0, second = 0, microsecond = 0)

def tomorrow(ts: Timescale):
  return day_after(today(ts))

def sun(lat: float = None, lon: float = None, when: datetime = None):
  if lat is None and lon is None:
    lat, lon = ip("me").latlng
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
  print(sun())
