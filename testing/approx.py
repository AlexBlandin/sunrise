#!/usr/bin/env python3

from math import sin, cos, tan, asin, acos, atan, floor
from math import degrees, radians
from datetime import datetime
from typing import Union

import pendulum

from helpers import format_sunriseset, guess_latlon

def approx(lat: Union[float, tuple[float, float], None] = None, lon: Union[float, None] = None, when: Union[datetime, None] = None):
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
    latitude, longitude: location for sunrise/sunset (can be given as a tuple), guesses if None
    when: date for sunrise/sunset (requires day, month, year), guesses if None
  Constants:
    zenith: upper limb of the Sun is tangent to the horizon (90 degrees 50')
  """
  # may also use some from http://answers.google.com/answers/threadview/id/782886.html
  
  if lat is None and lon is None:
    lat, lon = guess_latlon()
  elif isinstance(lat, tuple):
    lat, lon = lat
  if when is None:
    when = pendulum.today()
  else:
    when = pendulum.instance(when).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
  
  def _sunrise(rising = True):
    zenith = radians(90 + 50 / 60)
    
    # 1. first calculate the day of the year
    n = when.day_of_year # pendulum is rather marvellous
    
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
    return (when + pendulum.duration(hours = hours + when.offset_hours + 1, minutes = mins, seconds = secs))
  
  return format_sunriseset(_sunrise(), _sunrise(False))

if __name__ == "__main__":
  print(approx()) # use sun(dms_to_latlon("51°30′26″N 0°7′39″W")) for the sunrise in London today
