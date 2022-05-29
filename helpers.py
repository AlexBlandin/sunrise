from datetime import datetime, timedelta
from operator import itemgetter
from parse import parse
from time import time

def sortas(first: list, second: list):
  return list(map(itemgetter(0), sorted(zip(first, second), key = itemgetter(1))))

def nearest_minute(dt: datetime):
  return (dt + timedelta(seconds = 30)).replace(second = 0, microsecond = 0)

def day_after(dt: datetime):
  return (dt + timedelta(days = 1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)

def format_sunriseset(sunrise: datetime, sunset: datetime):
  return f"🌅: {nearest_minute(sunrise):%H:%M} 🌇: {nearest_minute(sunset):%H:%M}"

def lalo(s: str):
  if "N" in s and "W" in s:
    a, b, c, d = parse("{:d}°{:g}′N {:d}°{:g}′W", s).fixed
    return a + b / 60, c + d / 60
  elif "N" in s and "W" not in s:
    a, b, c, d = parse("{:d}°{:g}′N {:d}°{:g}′E", s).fixed
    return a + b / 60, -(c + d / 60)
  elif "N" not in s and "W" in s:
    a, b, c, d = parse("{:d}°{:g}′S {:d}°{:g}′W", s).fixed
    return -(a + b / 60), c + d / 60
  else:
    a, b, c, d = parse("{:d}°{:g}′S {:d}°{:g}′E", s).fixed
    return -(a + b / 60), -(c + d / 60)

def human_time(t: float, seconds = True):
  "because nobody makes it humanly readable"
  return f"{int(t//60)}m {human_time((int(t)%60)+(t-int(t)), True)}" if t > 60 else \
         f"{t:.3f}s" if t > 0.1 and seconds else                                    \
         f"{t*1000:.3f}ms" if t > 0.0001 else                                       \
         f"{t*1000000:.3f}us"

def tf(func, *args, pretty = True, **kwargs):
  "time func func, as in, time the function func"
  start = time()
  r = func(*args, **kwargs)
  end = time()
  if pretty:
    print(
      f"{func.__qualname__}({', '.join(list(map(str,args)) + [f'{k}={v}' for k,v in kwargs.items()])}) = {r}, took {human_time(end-start)}"
    )
  else:
    print(human_time(end - start))
  return r
