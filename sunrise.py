#!/usr/bin/env python3

from skyfield import api

ts = api.load.timescale()
eph = api.load("de421.bsp")
from skyfield import almanac
from geocoder import ip

from datetime import timedelta
def nearest_minute(dt):
  return (dt + timedelta(seconds=30)).replace(second=0, microsecond=0)
def today(ts):
  return ts.now().utc_datetime().replace(hour=0, minute=0, second=0, microsecond=0)
def tomorrow(ts):
  return (today(ts) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

def sun(RISE=True):
  lat, lon = ip("me").latlng
  here = api.wgs84.latlon(lat, lon)

  tdy, tmw = today(ts), tomorrow(ts)
  t0 = ts.utc(tdy.year, tdy.month, tdy.day)
  t1 = ts.utc(tmw.year, tmw.month, tmw.day)
  t, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(eph, here))
  for time, riseQ in zip(t,y):
    if riseQ and not RISE:
      continue
    elif not riseQ and RISE:
      continue
    print(f"{nearest_minute(time.utc_datetime()):%H:%M}")

def sunrise():
  sun()

def sunset():
  sun(False)

if __name__ == "__main__":
  sunrise()
