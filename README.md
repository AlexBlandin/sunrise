# Sunrise

Run `python3 sunrise.py` or `$ ./sunrise.py` and it'll say when the sunrise and sunset are today!
It guesses your location using your IP, so an unmasked internet connection is required.
Alternatively, you can fill in the call to sun() at the bottom of the script.
You may find the `dms_to_latlon` function handy, as you can pass co-ordinates from Wikipedia in.

`sunrise.py` dependencies:
- [Python 3.9](https://www.python.org)
- [Pendulum](https://pendulum.eustace.io)
  - `pip install pendulum`
- [Geocoder](https://github.com/DenisCarriere/geocoder)
  - `pip install geocoder`

If you wish to verify the accuracy for yourself, we use [Skyfield](https://rhodesmill.org/skyfield/) as a reference.
It can be installed with `pip install skyfield`. This occurs within the `testing/` directory, controlled with `test-rig.py`.
[Skyfield](https://rhodesmill.org/skyfield/) is optional, as the normal script `sunrise.py` does not need it.

We offer a [`poetry install`](https://python-poetry.org/) too, which covers all optional dependencies.
