"""
sunrise helpers.

Copyright 2021 Alex Blandin
"""

from collections.abc import Iterable
from datetime import datetime
from operator import itemgetter, mul
from pathlib import Path

import pendulum
from attrs import astuple, frozen
from geocoder import ip  # pyright: ignore[reportMissingTypeStubs,reportUnknownVariableType]

DATA_DIR = Path(__file__).parent.parent / "data"


def sortas(first: Iterable, second: Iterable) -> list:
  """Sorts the first as if it was the second."""
  return list(map(itemgetter(0), sorted(zip(first, second, strict=True))))


@frozen
class LatLon:
  "Latitude and Longitude."

  lat: float
  lon: float

  def tuple(self: "LatLon") -> tuple[float, float]:
    "Convert to a tuple."
    return astuple(self)

  @classmethod
  def from_coord(cls: type["LatLon"], coord: str, *, assume_northeast: bool = True) -> "LatLon":
    """
    Convert co-ordinates (as you'd get off Wikipedia) to usable (decimal) latitude and longitude.
    NE is positive, SW is negative. Assumes coordinates are relative to NE/SW if not unspecified.

    >>> London = dms_to_latlon("51°30′26″N 0°7′39″W")
    LatLon(lat=51.71666666666667, lon=-0.44166666666666665)

    >>> London = dms_to_latlon("51.71666666666667°N 0.44166666666666665°W")
    LatLon(lat=51.71666666666667, lon=-0.44166666666666665)
    """  # noqa: D205, RUF002
    parts = coord.split()
    if len(parts) != 2:  # noqa: PLR2004
      raise ValueError  # need the full coordinate

    coord = coord.upper()
    if "N" in coord or "E" in coord or "S" in coord or "W" in coord:
      if "N" in parts[0] or "S" in parts[0]:
        ns, ew = parts
      else:
        ew, ns = parts
      north = 1 if "N" in coord else -1
      east = 1 if "E" in coord else -1
    else:
      ns, ew = parts
      north, east = (1, 1) if assume_northeast else (-1, -1)

    ns, ew = LatLon.dms_to_decimal(ns), LatLon.dms_to_decimal(ew)
    return LatLon(north * ns, east * ew)

  @classmethod
  def dms_to_decimal(cls: type["LatLon"], dms: str | list[int | float]) -> float:
    """
    Convert a "51°30′26″N" string or [degree, minute, second] list into a decimal value.

    Supports any precision of [degree, ...] (within float64 limits).

    >>> London = dms_to_float([51, 30, 26]), dms_to_float([0, 7, 39])
    (51.71666666666667, -0.44166666666666665)
    """  # noqa: RUF002
    if isinstance(dms, str):
      convert = float if "." in dms else int
      dms = list(map(convert, "".join(c if c.isnumeric() or c == "." else " " for c in dms).split()))
    return sum(map(mul, dms, [1] + [1 / (i * 60) for i in range(1, len(dms))]))

  @classmethod
  def guess(cls: type["LatLon"]) -> "LatLon":
    """Uses your current IP to guess your Lat/Lon."""
    return LatLon(*ip("me").latlng)  # pyright: ignore[reportArgumentType]


def current_position(
  where: LatLon | str | tuple[float, float] | None = None,
) -> LatLon:
  "Where on Earth are we?"
  match where:
    case (float(lat), float(lon)):
      return LatLon(lat, lon)
    case LatLon() as latlon:
      return latlon
    case str(where):
      return LatLon.from_coord(where)
    case _:
      return LatLon.guess()


def current_day(when: pendulum.DateTime | datetime | (str | None) = None) -> pendulum.DateTime:
  "When on Earth are we?"
  match when:
    case str(when):
      day = pendulum.parse(when)
      if not isinstance(day, pendulum.DateTime):
        msg = f"{when} is not formatted as a date according to pendulum, parsed as {type(day)}"
        raise TypeError(msg)
      day = pendulum.parse(day.to_date_string())
      assert isinstance(day, pendulum.DateTime)  # noqa: S101
    case pendulum.DateTime() as when:
      day = when
    case datetime() as when:
      day = pendulum.instance(when)
    case _:
      day = pendulum.today(pendulum.UTC)

  return day.astimezone(pendulum.UTC)


def nearest_minute(dt: pendulum.DateTime) -> pendulum.DateTime:
  """Rounds to the nearest minute."""
  return (dt.astimezone(pendulum.UTC) + pendulum.duration(seconds=30)).astimezone().replace(second=0, microsecond=0)


def format_sunriseset(sunrise: str | pendulum.DateTime, sunset: str | pendulum.DateTime, *, pretty: bool = True) -> str:
  """Formats into a combined sunrise/sunset time."""

  def _format(when: str | pendulum.DateTime) -> str:
    match when:
      case pendulum.DateTime() as when:
        return f"{nearest_minute(when):%H:%M}"
      case _:
        return when

  rise, sets = _format(sunrise), _format(sunset)
  return f"🌅 {rise} | 🌇 {sets}" if pretty else f"{rise} {sets}"


if __name__ == "__main__":
  print(LatLon.guess())  # noqa: T201
