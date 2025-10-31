#!/usr/bin/env -S uv run -qqs
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "attrs",
#   "cattrs",
#   "geocoder@https://github.com/AlexBlandin/geocoder3.git",
#   "whenever",
#   # "skyfield",
# ]
# ///
#
"""
Nobody ever asks: how is the sun, it's always where is the sun...

Copyright 2021 Alex Blandin

███████╗██╗   ██╗███╗   ██╗██████╗ ██╗███████╗███████╗   ██████╗ ██╗   ██╗
██╔════╝██║   ██║████╗  ██║██╔══██╗██║██╔════╝██╔════╝   ██╔══██╗╚██╗ ██╔╝
███████╗██║   ██║██╔██╗ ██║██████╔╝██║███████╗█████╗     ██████╔╝ ╚████╔╝
╚════██║██║   ██║██║╚██╗██║██╔══██╗██║╚════██║██╔══╝     ██╔═══╝   ╚██╔╝
███████║╚██████╔╝██║ ╚████║██║  ██║██║███████║███████╗██╗██║        ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚═╝        ╚═╝

Run `sunrise.py` and it'll say when the sunrise and sunset are today!

See `sunrise.py -h` for options, which includes configuring the location and date.
If a location is not provided, it guesses using your IP, so an unmasked internet connection is required then.

## Requirements

- None, if you use [`uv run --script sunrise.py`](https://github.com/astral-sh/uv), or other PEP 723 compliant invokers!
- [`pip install -r requirements.txt`](https://www.python.org/)
  - [regenerate with `uv pip compile pyproject.toml -o requirements.txt`](https://github.com/astral-sh/uv)
  - We use [`whenever`](https://github.com/ariebovenberg/whenever)
  - We use [Geocoder 3](https://github.com/AlexBlandin/geocoder3)
"""

from argparse import ArgumentParser

import whenever

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument(
    "--where",
    help="""Where are we? e.g. London: --where "51°30′26″N 0°7′39″W" """,  # noqa: RUF001
  )  # pyright: ignore[reportUnusedCallResult]
  parser.add_argument("--when", help="""What day is it? e.g. --when "1999-12-31" """)  # pyright: ignore[reportUnusedCallResult]
  parser.add_argument(
    "--simple", action="store_true", help="""Simpler output, "08:11 16:04" vs "🌅: 08:11 🌇: 16:04" """
  )  # pyright: ignore[reportUnusedCallResult]
  parser.add_argument(
    "--skyfield",
    action="store_true",
    help="""Use Skyfield to calculate exact answers https://rhodesmill.org/skyfield/""",
  )
  parser.add_argument(
    "--test", action="store_true", help="""Run tests for discrepencies over time, implies --skyfield"""
  )

  args = parser.parse_args()

  if args.test:
    from sunrise.test_rig import test

    test()
  else:
    if args.skyfield:
      from sunrise.correct import correct as calculate
    else:
      from sunrise.approx import approx as calculate  # pyright: ignore[reportImplicitRelativeImport]

    now = whenever.ZonedDateTime.now_in_system_tz()
    sunrise_sunset = calculate(args.where, args.when, simple=args.simple)  # pyright: ignore[reportAny]
    match now.day:
      case 1 | 21 | 31:
        day_ord = "st"
      case 2 | 22:
        day_ord = "nd"
      case 3 | 23:
        day_ord = "rd"
      case 7 | 17 | 27:
        day_ord = "th"  # or "nth", if you prefer
      case _:
        day_ord = "th"
    print(
      f"{sunrise_sunset} | {now.py_datetime().strftime('%A the %d# of %B | %Y-%m-%d | UNIX: ~$s'.replace('#', day_ord).replace('$', str(now.timestamp())))}"
    )
