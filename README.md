# Sunrise

Run `python3 sunrise.py` or `$ ./sunrise.py` and it'll say when the sunrise and sunset are today!

See `python3 sunrise.py -h` for options, which includes configuring the location and date.
If a location is not provided, it guesses using your IP, so an unmasked internet connection is required then.

`sunrise.py` dependencies:
- [Python 3.9](https://www.python.org)
- `pip install pendulum geocoder`
  - [Pendulum](https://pendulum.eustace.io)
  - [Geocoder 3](https://github.com/AlexBlandin/geocoder3)

If you wish to verify the accuracy for yourself, we use [Skyfield](https://rhodesmill.org/skyfield/) as a reference.
The algorithm was chosen as a balance of accuracy and performance, with margin of error acceptable under variable atmospheric refraction.
It can be installed with `pip install skyfield`. This occurs within the `testing/` directory, controlled with `test-rig.py`.
[Skyfield](https://rhodesmill.org/skyfield/) is optional, as the normal script `sunrise.py` does not need it.

We offer a [`poetry install`](https://python-poetry.org/) too, which covers all optional dependencies.

```bash
usage: sunrise.py [-h] [--where WHERE] [--when WHEN] [--boring]

optional arguments:
  -h, --help     show this help message and exit
  --where WHERE  Where we want to see the sunrise/sunset, i.e. London: --where "51°30′26″N 0°7′39″W"
  --when WHEN    Which day do we wish to know the sunrise/sunset on: --when "1999-12-31"
  --boring       A boring prinout, so "08:11 16:04" instead of "🌅: 08:11 🌇: 16:04"
```
