from math import sin, cos, tan, asin, acos, atan, floor, pi
from math import degrees, radians
from parse import parse
from datetime import datetime

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

def lalo(s: str):
  if "N" in s and "W" in s:
    a,b,c,d = parse("{:d}°{:g}′N {:d}°{:g}′W", s).fixed
    return a + b/60, c + d/60
  elif "N" in s and "W" not in s:
    a,b,c,d = parse("{:d}°{:g}′N {:d}°{:g}′E", s).fixed
    return a + b/60, -(c + d/60)
  elif "N" not in s and "W" in s:
    a,b,c,d = parse("{:d}°{:g}′S {:d}°{:g}′W", s).fixed
    return -(a + b/60), c + d/60
  else:
    a,b,c,d = parse("{:d}°{:g}′S {:d}°{:g}′E", s).fixed
    return -(a + b/60), -(c + d/60)

def sunrisesunset(latitude, longitude, when: datetime = None):
  def __calc(latitude, longitude, rising, when: datetime = None):
    zenith = radians(90 + 50/60)
    latitude = radians(latitude)

    """1. first calculate the day of the year
      N1 = floor(275 * month / 9)
      N2 = floor((month + 9) / 12)
      N3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3))
      N = N1 - (N2 * N3) + day - 30
    """
    if when is None:
      day = int(datetime.now().strftime("%j"))
    else:
      day = int(when.strftime("%j"))

    """2. convert the longitude to hour value and calculate an approximate time
      lngHour = longitude / 15
      
      if rising time is desired:
        t = N + ((6 - lngHour) / 24)
      if setting time is desired:
        t = N + ((18 - lngHour) / 24)
    """
    lngHour = longitude / 15 #... could do much better than this since UTC data is available
    if rising:
      t = day + (6 - lngHour)/24
    else:
      t = day + (18 - lngHour)/24
    
    """3. calculate the Sun's mean anomaly
      M = (0.9856 * t) - 3.289
    """
    M = 0.9856*t - 3.289

    """4. calculate the Sun's true longitude
      L = M + (1.916 * sin(M)) + (0.020 * sin(2 * M)) + 282.634
      NOTE: L potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
    """
    L = M + 1.916*sin(radians(M)) + 0.020*sin(radians(2*M)) + 282.634
    L %= 360 # works in python :)

    """5a. calculate the Sun's right ascension
      RA = atan(0.91764 * tan(L))
      NOTE: RA potentially needs to be adjusted into the range [0,360) by adding/subtracting 360
    """
    RA = degrees(atan(0.91764*tan(radians(L))))
    RA %= 360

    """5b. right ascension value needs to be in the same quadrant as L
      Lquadrant  = (floor( L/90)) * 90
      RAquadrant = (floor(RA/90)) * 90
      RA = RA + (Lquadrant - RAquadrant)
    """
    Lquadrant = 90*floor(L / 90)
    RAquadrant = 90*floor(RA / 90)
    RA += Lquadrant - RAquadrant

    """5c. right ascension value needs to be converted into hours
      RA = RA / 15
    """
    RA /= 15

    """6. calculate the Sun's declination
      sinDec = 0.39782 * sin(L)
      cosDec = cos(asin(sinDec))
    """
    sinDec = 0.39782*sin(radians(L))
    cosDec = cos(asin(sinDec))

    """7a. calculate the Sun's local hour angle
      cosH = (cos(zenith) - (sinDec * sin(latitude))) / (cosDec * cos(latitude))
      
      if (cosH >  1)
        the sun never rises on this location (on the specified date)
      if (cosH < -1)
        the sun never sets on this location (on the specified date)
    """
    cosH = (cos(zenith) - (sinDec*sin(latitude))) / (cosDec*cos(latitude))
    if cosH > 1 or cosH < -1:
      return f"never {'rises' if rising else 'sets'}"
    
    """7b. finish calculating H and convert into hours
      if rising time is desired:
        H = 360 - acos(cosH)
      if setting time is desired:
        H = acos(cosH)
      
      H = H / 15
    """
    if rising:
      H = 360 - degrees(acos(cosH))
    else:
      H = degrees(acos(cosH))
    H = H / 15

    """8. calculate local mean time of rising/setting
      T = H + RA - (0.06571 * t) - 6.622
    """
    T = H + RA - 0.06571*t - 6.622

    """9. adjust back to UTC
      UT = T - lngHour
      NOTE: UT potentially needs to be adjusted into the range [0,24) by adding/subtracting 24
    """
    UT = T - lngHour
    UT %= 24

    """10. convert UT value to local time zone of latitude/longitude
      localT = UT + localOffset
    """
    offset = longitude // 15 # estimate utc correction # ooooor just do it properly...
    localT = UT + offset
    seconds = int(localT * 3600)

    sec, minutes, hours = seconds % 60, seconds % 3600 // 60, seconds % 86400 // 3600
    
    return f"{'🌅' if rising else '🌇'}: {hours:02}:{minutes:02}:{sec:02}"
  return __calc(latitude, longitude, True, when), __calc(latitude, longitude, False, when)

if __name__ == "__main__":
  jersey = "49°11.4′N 2°6.6′W"
  swansea = "51°37′N 3°57′W"
  print(*sunrisesunset(*lalo(jersey)), "in Jersey")

  # for 2021-01-19, in Jersey, it gave:
  # 🌅: 07:54:30 🌇: 16:44:30 (weather.com)
  # 🌅: 07:38:11 🌇: 16:25:58 (temp.py)
  # 🌅: 07:38:15 🌇: 16:26:58 in Jersey (sunrise-full.py)
  # wolfram claims to take account of atmospheric refraction, so it's the apparent time? gweather is very close so similar
  # now not taking account may have an effect "on order of minutes" and there's the possibility the NOAA calculations are off
  # TODO: FIX THIS MESS (both in terms of code but also just the problem itself)
