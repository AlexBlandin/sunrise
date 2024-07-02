# Sunrise

Run `sunrise.py` and it'll say when the sunrise and sunset are today!

See `sunrise.py -h` for options, which includes configuring the location and date. If a location is not provided, it guesses using your IP, so an unmasked internet connection is required then.

## Requirements
- [`pip install -r requirements.txt`](https://www.python.org/)
  - [regenerate with `uv pip compile pyproject.toml -o requirements.txt`](https://github.com/astral-sh/uv)
  - We use [Pendulum](https://pendulum.eustace.io)
  - We use [Geocoder 3](https://github.com/AlexBlandin/geocoder3)

Our algorithm was chosen as a balance of accuracy and performance, with margin of error acceptable under variable atmospheric refraction. If you wish to verify the accuracy for yourself, `./test/test_rig.py` uses [Skyfield](https://rhodesmill.org/skyfield/) as a reference. It can be installed with `pip install skyfield` or `pip install -r requirements-skyfield.txt`. **This is optional**, as `sunrise.py` does not use it.

```bash
usage: python sunrise.py [-h] [--where WHERE] [--when WHEN] [--boring]

optional arguments:
  -h, --help     show this help message and exit
  --where WHERE  Where we want to see the sunrise/sunset, i.e. London: --where "51°30′26″N 0°7′39″W"
  --when WHEN    Which day do we wish to know the sunrise/sunset on: --when "1999-12-31"
  --simple       A simple printout, so "08:11 16:04" instead of "🌅: 08:11 🌇: 16:04"
```

## Windows Task Scheduler

In `TaskScheduler/` is a template for running `sunrise.cmd` in the background on Windows via Task Scheduler (`taskschd`). This can also be achieved with [`schtasks`](https://ss64.com/nt/schtasks.html) in `cmd.exe`, e.g. `schtasks /create /tn "Sunrise" /tr "sunrise.cmd" /sc daily /mo 1`.
