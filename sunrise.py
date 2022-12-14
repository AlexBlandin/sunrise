#!/usr/bin/env python3
"""
███████╗██╗   ██╗███╗   ██╗██████╗ ██╗███████╗███████╗   ██████╗ ██╗   ██╗
██╔════╝██║   ██║████╗  ██║██╔══██╗██║██╔════╝██╔════╝   ██╔══██╗╚██╗ ██╔╝
███████╗██║   ██║██╔██╗ ██║██████╔╝██║███████╗█████╗     ██████╔╝ ╚████╔╝ 
╚════██║██║   ██║██║╚██╗██║██╔══██╗██║╚════██║██╔══╝     ██╔═══╝   ╚██╔╝  
███████║╚██████╔╝██║ ╚████║██║  ██║██║███████║███████╗██╗██║        ██║   
╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚═╝        ╚═╝   

Run `python3 sunrise.py` or `$ ./sunrise.py` and it'll say when the sunrise and sunset are today!

See `python3 sunrise.py -h` for options, which includes configuring the location and date.
If a location is not provided, it guesses using your IP, so an unmasked internet connection is required then.

Dependencies:
- Python 3.9
- `pip install pendulum geocoder`
    - [Pendulum](https://pendulum.eustace.io)
    - [Geocoder](https://github.com/DenisCarriere/geocoder)

"""

from operator import itemgetter, mul
from datetime import datetime
from argparse import ArgumentParser
from typing import NamedTuple, Union
from math import radians, degrees, floor, atan, asin, acos, tan, sin, cos

from geocoder import ip
import pendulum

LatLon = NamedTuple("LatLon", lat = float, lon = float)

def guess_latlon():
  return LatLon(*ip("me").latlng)

def sortas(first: list, second: list):
  return list(map(itemgetter(0), sorted(zip(first, second), key = itemgetter(1))))

def nearest_minute(dt: datetime):
  return (dt + pendulum.duration(seconds = 30)).replace(second = 0, microsecond = 0)

def format_sunriseset(sunrise: datetime, sunset: datetime, pretty = True):
  return f"🌅: {nearest_minute(sunrise):%H:%M} 🌇: {nearest_minute(sunset):%H:%M}" if pretty else f"{nearest_minute(sunrise):%H:%M} {nearest_minute(sunset):%H:%M}"

def dms_to_latlon(s: str):
  """
  Convert degree-minute-second co-ordinates (as you'd get off Wikipedia) to decimal latitude and longitude.
  NE is positive, SW is negative.
  
  >>> London = dms_to_latlon("51°30′26″N 0°7′39″W")
  LatLon(51.71666666666667, -0.44166666666666665)
  >>> Roughly_London = dms_to_latlon("51°30′N 0°7′W")
  LatLon(51.5, -0.11666666666666667)
  """
  ns, ew = tuple(list(map(int, "".join(c if c.isnumeric() else " " for c in p).split())) for p in s.split(maxsplit = 1))
  north, east = 1 if "N" in s.upper() else -1, 1 if "E" in s.upper() else -1
  convert = lambda dms: sum(map(mul, dms, [1] + [1 / (i * 60) for i in range(1, len(dms))]))
  return LatLon(north * convert(ns), east * convert(ew))

def sun(where: Union[str, tuple[float, float], None] = None, when: Union[datetime, str, None] = None, boring: Union[bool, None] = None):
  """
  Source:
    Almanac for Computers, 1990
    published by Nautical Almanac Office
    United States Naval Observatory
    Washington, DC 20392
  Archived:
    https://www.edwilliams.org/sunrise_sunset_algorithm.htm
    https://web.archive.org/web/20210115202147/https://edwilliams.org/sunrise_sunset_algorithm.htm
  
  Inputs:
    where: location for sunrise/sunset (given as lat/lon tuple), guesses if None
    when: date for sunrise/sunset (requires day, month, year), guesses if None
  Constants:
    zenith: upper limb of the Sun is tangent to the horizon (90 degrees 50')
  """
  # may also use some from http://answers.google.com/answers/threadview/id/782886.html
  
  lat, lon = dms_to_latlon(where) if isinstance(where, str) else where if isinstance(where, tuple) else guess_latlon()
  
  if isinstance(when, str):
    day = pendulum.parse(when) # type: ignore
    if not isinstance(day, pendulum.DateTime): # Pylance doesn't think pendulum exports DateTime, but it does...
      raise TypeError(f"{when} is not formatted as a date according to pendulum")
  elif isinstance(when, datetime):
    day = pendulum.instance(when)
  else:
    day = pendulum.today()
  day = day.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
  
  def _sunrise(rising = True):
    zenith = radians(90 + 50 / 60)
    
    # 1. first calculate the day of the year
    n = day.day_of_year # pendulum is rather marvellous
    
    # 2. convert the longitude to hour value and calculate an approximate time
    lng_hour = lon / 15
    if rising:
      t = n + (6 - lng_hour) / 24
    else:
      t = n + (18 - lng_hour) / 24
    
    # 3. calculate the Sun's mean anomaly
    m = 0.9856 * t - 3.289
    
    # 4. calculate the Sun's true longitude
    l = m + 1.916 * sin(radians(m)) + 0.020 * sin(radians(2 * m)) + 282.634
    l %= 360
    
    # 5a. calculate the Sun's right ascension
    ra = degrees(atan(0.91764 * tan(radians(l))))
    ra %= 360
    
    # 5b. right ascension value needs to be in the same quadrant as L
    l_quad = 90 * floor(l / 90)
    ra_quad = 90 * floor(ra / 90)
    ra += l_quad - ra_quad
    
    # 5c. right ascension value needs to be converted into hours
    ra /= 15
    
    # 6. calculate the Sun's declination
    sin_dec = 0.39782 * sin(radians(l))
    cos_dec = cos(asin(sin_dec))
    
    #7a. calculate the Sun's local hour angle
    cos_local_h = (cos(zenith) - (sin_dec * sin(radians(lat)))) / (cos_dec * cos(radians(lat)))
    if cos_local_h > 1 or cos_local_h < -1:
      return f"never {'rises' if rising else 'sets'}"
    
    # 7b. finish calculating H and convert into hours
    if rising:
      h = 360 - degrees(acos(cos_local_h))
    else:
      h = degrees(acos(cos_local_h))
    h = h / 15
    
    # 8. calculate local mean time of rising/setting
    t = h + ra - 0.06571 * t - 6.622
    
    # 9. adjust back to UTC
    ut = t - lng_hour
    ut %= 24
    
    # 10. convert UT value to local time zone of latitude/longitude
    offset = lon // 15
    local_t = ut + offset
    
    # 11. convert to human-readable time
    seconds = int(local_t * 3600)
    secs, mins, hours = seconds % 60, seconds % 3600 // 60, seconds % 86400 // 3600
    
    return day + pendulum.duration(hours = hours + day.offset_hours + 1, minutes = mins, seconds = secs)
  
  return format_sunriseset(_sunrise(), _sunrise(False), not boring)

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument(
    "--where", help = """Where we want to see the sunrise/sunset, i.e. London: --where "51°30′26″N 0°7′39″W" """
  )
  parser.add_argument("--when", help = """Which day do we wish to know the sunrise/sunset on: --when "1999-12-31" """)
  parser.add_argument("--boring", action = "store_true", help = """A boring prinout, so "08:11 16:04" instead of "🌅: 08:11 🌇: 16:04" """)
  
  args = parser.parse_args()
  
  print(sun(args.where, args.when, args.boring))
