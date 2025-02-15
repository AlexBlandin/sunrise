#!/usr/bin/env python3
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
- [`pip install -r requirements.txt`](https://www.python.org/)
  - [regenerate with `uv pip compile pyproject.toml -o requirements.txt`](https://github.com/astral-sh/uv)
  - We use [Pendulum](https://pendulum.eustace.io)
  - We use [Geocoder 3](https://github.com/AlexBlandin/geocoder3)
"""

from argparse import ArgumentParser

import pendulum

from sunrise.approx import approx as calculate  # pyright: ignore[reportImplicitRelativeImport]

# from sunrise.correct import correct as calculate

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

  args = parser.parse_args()

  now = pendulum.now()
  sunrise_sunset = calculate(args.where, args.when, args.simple)  # pyright: ignore[reportAny]
  print(f"{sunrise_sunset} | {now.format('dddd [the] Do [of] MMMM [|] YYYY-MM-DD [| UNIX: ~]X[s]')}")  # noqa: T201
