from collections import namedtuple
from operator import itemgetter
from datetime import datetime
from parse import parse
from geocoder import ip
import pendulum

LatLon = namedtuple("LatLon", "lat lon")

def guess_latlon():
  return LatLon(*ip("me").latlng)

def sortas(first: list, second: list):
  return list(map(itemgetter(0), sorted(zip(first, second), key = itemgetter(1))))

def nearest_minute(dt: datetime):
  return (dt + pendulum.duration(seconds = 30)).replace(second = 0, microsecond = 0)

def format_sunriseset(sunrise: datetime, sunset: datetime):
  return f"🌅: {nearest_minute(sunrise):%H:%M} 🌇: {nearest_minute(sunset):%H:%M}"

def lalo(s: str):
  """
  >>> swansea = lalo("51°37′N 3°57′W")
  LatLon(51.61666666666667, -3.95)
  """
  if "N" in s and "W" in s:
    a, b, c, d = parse("{:d}°{:g}′N {:d}°{:g}′W", s).fixed
    return a + b / 60, -(c + d / 60)
  elif "N" in s and "W" not in s:
    a, b, c, d = parse("{:d}°{:g}′N {:d}°{:g}′E", s).fixed
    return a + b / 60, c + d / 60
  elif "N" not in s and "W" in s:
    a, b, c, d = parse("{:d}°{:g}′S {:d}°{:g}′W", s).fixed
    return -(a + b / 60), -(c + d / 60)
  else:
    a, b, c, d = parse("{:d}°{:g}′S {:d}°{:g}′E", s).fixed
    return -(a + b / 60), c + d / 60
