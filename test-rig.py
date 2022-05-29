from algo1 import sun
from correct import correct
from helpers import guess_latlon
import pendulum

latlon = guess_latlon()
print("correct", correct(*latlon))
print("algo 01", sun(*latlon))

# algo1 is basically correct, just WAY faster, if you're okay with being a tad off at times

guesses = [
  (correct(*latlon, day).removeprefix("🌅: ").split(" 🌇: "), sun(*latlon, day).removeprefix("🌅: ").split(" 🌇: "), day)
  for day in (pendulum.today() + pendulum.duration(years = 10) - pendulum.today())
]

def not_off_by_a_tad(t0, t1):
  t0d, t1d = int(t0[-2:]), int(t1[-2:])
  return t0 != t1 and abs(t0d - t1d) > 2 and {t0d, t1d} != {0, 59} and {t0d, t1d} != {1, 59} and {t0d, t1d} != {0, 58}

for (r0, s0), (r1, s1), day in guesses:
  if not_off_by_a_tad(r0, r1):
    print(day, r0, r1)
  if not_off_by_a_tad(s0, s1):
    print(day, s0, s1)
