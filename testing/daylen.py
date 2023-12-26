import matplotlib.pyplot as plt
import numpy as np
import pendulum
from skyfield.api import Time, load
from skyfield.api import iers2010 as geoid
from skyfield.positionlib import position_of_radec  # noqa: F401
from skyfield.searchlib import find_discrete, find_maxima, find_minima  # noqa: F401

# from skyfield.projections import build_stereographic_projection


def calendar(year):
  return {
    1: 31,
    2: 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
  }


def rotation_matrix_between(a: Time, b: Time):
  return pole.rotation_at(a) * pole.rotation_at(b).T


def rotation_between(a: Time, b: Time):
  return np.arccos((np.trace(rotation_matrix_between(a, b)) - 1) / 2)


def angles_of_matrix(rtm: np.ndarray):
  return (  # Euler axis/angle°, 3-1-3 Euler extrinsic
    f"{np.degrees(np.arccos((np.trace(rtm) - 1) / 2)):0.3f}° (θ angle)",
    f"{np.degrees(np.arctan2(rtm[2, 0], rtm[2, 1])):0.3f}° (z ex.)",
    f"{np.degrees(np.arccos(rtm[2, 2])):0.3f}° (x ex.)",
    f"{np.degrees(-np.arctan2(rtm[0, 2], rtm[1, 2])):0.3f}° (Z ex.)",
  )


np.set_printoptions(formatter={"float": lambda f: f"{f:0.6f}" if f > 0.0 else f"{f:0.5f}"})  # type: ignore
fig, ax = plt.subplots(figsize=(12, 8))
ts = load.timescale()
pole = geoid.latlon(90, 0)

# rotations_at_midnight = {
#   time: pole.rotation_at(time)
#   for time in [ts.utc(year=year, month=month, day=day) for year in range(2020, 2025) for month, days in calendar(year).items() for day in range(1, days + 1)]
# }
# print(len(rotations_at_midnight))
# print(next(iter(rotations_at_midnight.values())))
# deltas = list(starmap(rotation_between, pairwise(rotations_at_midnight.values())))
# print(len(deltas))
# print(deltas)
# so we just need to collapse that to axis of spin around the poles, and the difference there is it!
# then our differences of midnights are "how far are we", so the least difference is the "best" 24 hours!
# so we need to get the axis between the north & south poles?
today, midday, tomorrow = ts.from_datetime(pendulum.today()), ts.from_datetime(pendulum.today().replace(hour=12)), ts.from_datetime(pendulum.tomorrow())

print("rotation at pole <today> <midday> <tomorrow>")
print(pole.rotation_at(today))
print(pole.rotation_at(midday))
print(pole.rotation_at(tomorrow))
print("precession at pole <today> <midday> <tomorrow>")
print(today.precession_matrix())
print(midday.precession_matrix())
print(tomorrow.precession_matrix())
print("rotation at pole between <today>/<midday>/<tomorrow> & <today>/<tomorrow>")
rtm_tm = rotation_matrix_between(today, midday)
rtm_mt = rotation_matrix_between(midday, tomorrow)
rtm_tt = rotation_matrix_between(today, tomorrow)


print(rtm_tm, *angles_of_matrix(rtm_tm), sep=", ")
print(rtm_mt, *angles_of_matrix(rtm_mt), sep=", ")
print(rtm_tt, *angles_of_matrix(rtm_tt), sep=", ")

"""
rotation at pole <today> <midday> <tomorrow>
[[-0.01739 -0.99985 0.000073]
 [-0.99985 0.017390 0.002316]
 [0.002317 0.000033 0.999997]]
[[0.008789 0.999961 -0.00005]
 [0.999959 -0.00879 -0.00232]
 [0.002317 0.000033 0.999997]]
[[-0.00019 -1.00000 0.000033]
 [-1.00000 0.000188 0.002317]
 [0.002317 0.000033 0.999997]]
precession at pole <today> <midday> <tomorrow>
[[0.999983 -0.00536 -0.00233]
 [0.005360 0.999986 -0.00001]
 [0.002329 -0.00001 0.999997]]
[[0.999983 -0.00536 -0.00233]
 [0.005360 0.999986 -0.00001]
 [0.002329 -0.00001 0.999997]]
[[0.999983 -0.00536 -0.00233]
 [0.005360 0.999986 -0.00001]
 [0.002329 -0.00001 0.999997]]
rotation at pole between <today>/<midday>/<tomorrow> & <today>/<tomorrow>
[[-0.00015 -0.99981 0.000000]
 [-0.99981 -0.00015 0.000000]
 [-0.00000 -0.00000 0.999995]], 90.009° (θ angle), -121.691° (z ex.), 0.188° (x ex.), -65.900° (Z ex.)
[[-0.00000 -0.99996 -0.00000]
 [-0.99996 -0.00000 -0.00000]
 [0.000000 0.000000 0.999995]], 90.000° (θ angle), 45.297° (z ex.), 0.188° (x ex.), 121.561° (Z ex.)
[[0.000003 0.999846 0.000000]
 [0.999846 0.000003 0.000000]
 [0.000000 0.000000 0.999995]], 90.000° (θ angle), 45.235° (z ex.), 0.188° (x ex.), -65.962° (Z ex.)
"""
