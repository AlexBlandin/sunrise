"""
sunrise test rig.

Copyright 2021 Alex Blandin
"""

import whenever

from .approx import approx
from .correct import correct
from .helpers import LatLon


def test():
  latlon = LatLon.guess().tuple()
  print("correct", correct(latlon))  # noqa: T201
  print("approx", approx(latlon))  # noqa: T201

  # approx is basically correct, and WAY faster, if you're okay with being just a tad off at times

  delta = {"years": 10}
  print(f"discrepencies over the next {delta}")
  today = whenever.SystemDateTime.now()
  guesses = [
    (
      correct(latlon, today.add(days=day), simple=True).split(),
      approx(latlon, today.add(days=day), simple=True).split(),
      day,
    )
    for day in range(today.date().days_until(today.add(**delta).date()) + 1)
  ]

  def off_by_more_than_a_tad(t0, t1):  # noqa: ANN001, ANN201, D103
    t0d, t1d = int(t0[-2:]), int(t1[-2:])
    return t0 != t1 and abs(t0d - t1d) > 2 and {t0d, t1d} != {0, 59} and {t0d, t1d} != {1, 59} and {t0d, t1d} != {0, 58}  # noqa: PLR2004

  for (r0, s0), (r1, s1), day in guesses:
    if off_by_more_than_a_tad(r0, r1):
      print(day, r0, r1)  # noqa: T201
    if off_by_more_than_a_tad(s0, s1):
      print(day, s0, s1)  # noqa: T201
