#!/usr/bin/env python3

from math import sin, cos, tan, asin, acos, atan, floor
from math import degrees, radians
from datetime import datetime
from helpers import lalo, format_sunriseset, guess_latlon

def algo1(lat: float = None, lon: float = None, when: datetime = None):
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
    day, month, year:      date of sunrise/sunset
    latitude, longitude:   location for sunrise/sunset
    zenith:                Sun's zenith for sunrise/sunset
      offical      = 90 degrees 50'
      civil        = 96 degrees
      nautical     = 102 degrees
      astronomical = 108 degrees
    
    NOTE: longitude is positive for East and negative for West
  """
  # may also use some from http://answers.google.com/answers/threadview/id/782886.html
  
  if lat is None and lon is None:
    lat, lon = guess_latlon()
  if when is None:
    when = datetime.utcnow() # TODO: it's not respecting timezones (BST etc)
  
  def _sunrise(rising = True):
    zenith = radians(90 + 50 / 60)
    rlat = radians(lat)
    """1. first calculate the day of the year
      N1 = floor(275 * month / 9)
      N2 = floor((month + 9) / 12)
      N3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3))
      N = N1 - (N2 * N3) + day - 30
    """
    
    n = int(when.strftime("%j"))
    """2. convert the longitude to hour value and calculate an approximate time
      lng_hour = longitude / 15
      
      if rising time is desired:
        t = N + ((6 - lng_hour) / 24)
      if setting time is desired:
        t = N + ((18 - lng_hour) / 24)
    """
    lng_hour = lon / 15 # TODO: do correctly
    if rising:
      t = n + (6 - lng_hour) / 24
    else:
      t = n + (18 - lng_hour) / 24
    """3. calculate the Sun's mean anomaly
      M = (0.9856 * t) - 3.289
    """
    m = 0.9856 * t - 3.289
    """4. calculate the Sun's true longitude
      L = M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) + 282.634
      NOTE: L should now be modulo 360
    """
    l = m + 1.916 * sin(radians(m)) + 0.020 * sin(radians(2 * m)) + 282.634
    l %= 360
    """5a. calculate the Sun's right ascension
      RA = atan(0.91764 * tan(L))
      NOTE: RA should now by modulo 360
    """
    ra = degrees(atan(0.91764 * tan(radians(l))))
    ra %= 360
    """5b. right ascension value needs to be in the same quadrant as L
      l_quad = (floor( L/90)) * 90
      ra_quad = (floor(RA/90)) * 90
      RA = RA + (l_quad - ra_quad)
    """
    l_quad = 90 * floor(l / 90)
    ra_quad = 90 * floor(ra / 90)
    ra += l_quad - ra_quad
    """5c. right ascension value needs to be converted into hours
      RA = RA / 15
    """
    ra /= 15
    """6. calculate the Sun's declination
      sin_dec = 0.39782 * sin(L)
      cos_dec = cos(asin(sin_dec))
    """
    sin_dec = 0.39782 * sin(radians(l))
    cos_dec = cos(asin(sin_dec))
    """7a. calculate the Sun's local hour angle
      cos_local_h = (cos(zenith) - (sin_dec * sin(latitude))) / (cos_dec * cos(latitude))
      
      if (cos_local_h >  1)
        the sun never rises on this location (on the specified date)
      if (cos_local_h < -1)
        the sun never sets on this location (on the specified date)
    """
    cos_local_h = (cos(zenith) - (sin_dec * sin(rlat))) / (cos_dec * cos(rlat))
    if cos_local_h > 1 or cos_local_h < -1:
      return f"never {'rises' if rising else 'sets'}"
    """7b. finish calculating H and convert into hours
      if rising time is desired:
        H = 360 - acos(cos_local_h)
      if setting time is desired:
        H = acos(cos_local_h)
      
      H = H / 15
    """
    if rising:
      h = 360 - degrees(acos(cos_local_h))
    else:
      h = degrees(acos(cos_local_h))
    h = h / 15
    """8. calculate local mean time of rising/setting
      T = H + RA - (0.06571 * t) - 6.622
    """
    t = h + ra - 0.06571 * t - 6.622
    """9. adjust back to UTC
      UT = T - lng_hour
      NOTE: UT should now be modulo 24
    """
    ut = t - lng_hour
    ut %= 24
    """10. convert UT value to local time zone of latitude/longitude
      local_t = UT + localOffset
    """
    offset = lon // 15 # TODO: do correctly
    local_t = ut + offset
    """
    convert local_t to human-readable time
    """
    seconds = int(local_t * 3600)
    sec, minutes, hours = seconds % 60, seconds % 3600 // 60, seconds % 86400 // 3600
    return when.replace(hour = hours, minute = minutes, second = sec)
  
  return format_sunriseset(_sunrise(), _sunrise(False))

if __name__ == "__main__":
  swansea = "51°37′N 3°57′W"
  print(*algo1(*lalo(swansea)))
