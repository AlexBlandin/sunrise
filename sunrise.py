#!/usr/bin/env python3

from skyfield import api
from pathlib import Path

load = api.Loader(Path(__file__).parent.absolute(), verbose=False)
ts = load.timescale()
eph = load("de421.bsp")
from skyfield import almanac
from geocoder import ip

from datetime import timedelta
def nearest_minute(dt):
  return (dt + timedelta(seconds=30)).replace(second=0, microsecond=0)
def today(ts):
  return ts.now().utc_datetime().replace(hour=0, minute=0, second=0, microsecond=0)
def tomorrow(ts):
  return (today(ts) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

def sun():
  lat, lon = ip("me").latlng
  here = api.wgs84.latlon(lat, lon)

  tdy, tmw = today(ts), tomorrow(ts)
  t0 = ts.utc(tdy.year, tdy.month, tdy.day)
  t1 = ts.utc(tmw.year, tmw.month, tmw.day)
  t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, here))
  sunrise = [None,None]
  for time, riseQ in zip(t,y):
    if riseQ:
      sunrise[0] = f"{nearest_minute(time.utc_datetime()):%H:%M}"
    else:
      sunrise[1] = f"{nearest_minute(time.utc_datetime()):%H:%M}"
  return sunrise

def format_sunrise(sunrise):
  return f"🌅: {sunrise[0]} 🌇: {sunrise[1]}"

if __name__ == "__main__":
  print(format_sunrise(sun()))
