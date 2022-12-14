# Sunrise

Run `python3 sunrise.py` or `$ ./sunrise.py` and it'll say when the sunrise and sunset are today!
See `python3 sunrise.py -h` for options, which include setting the relevat location, date, and timezone.
If a location is not provided, it guesses using your IP, so an unmasked internet connection is required then.
Alternatively, you can fill in the call to `sun()` at the bottom of the script and have it baked it.
You may find the `dms_to_latlon` function handy, as you can pass co-ordinates from Wikipedia in.

`sunrise.py` dependencies:
- [Python 3.9](https://www.python.org)
- `pip install pendulum geocoder`
  - [Pendulum](https://pendulum.eustace.io)
  - [Geocoder](https://github.com/DenisCarriere/geocoder)

If you wish to verify the accuracy for yourself, we use [Skyfield](https://rhodesmill.org/skyfield/) as a reference.
The algorithm was chosen as a balance of accuracy and performance, with margin of error acceptable under variable atmospheric refraction.
It can be installed with `pip install skyfield`. This occurs within the `testing/` directory, controlled with `test-rig.py`.
[Skyfield](https://rhodesmill.org/skyfield/) is optional, as the normal script `sunrise.py` does not need it.

We offer a [`poetry install`](https://python-poetry.org/) too, which covers all optional dependencies.

```cmd
usage: sunrise.py [-h] [--where WHERE] [--when WHEN] [--tz TZ]

optional arguments:
  -h, --help     show this help message and exit
  --where WHERE  Where we want to see the sunrise/sunset, in DMS form, i.e. London is: --where "51°30′26″N 0°7′39″W"
  --when WHEN    Which day do we wish to know the sunrise/sunset on: --when "1999-12-31"
  --tz TZ        Which timezone to use, defaults to local (or UTC if unknown): --tz "Europe/London"
```
