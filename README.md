# Sunrise

Run `python3 sunrise.py` or `$ ./sunrise.py` and it'll say when the sunrise and sunset are today!
It guesses your location using your IP, so an unmasked internet connection is required.
Alternatively, you can fill in the call to sun() at the bottom of the script.
You may find the dms_to_latlon function handy, as you can pass co-ordinates from Wikipedia in.

Dependencies:
- [Python 3.9](https://www.python.org)
- `pip install skyfield geocoder`
  - [Skyfield](https://rhodesmill.org/skyfield/)
  - [Geocoder](https://github.com/DenisCarriere/geocoder)
- or, [`poetry install`](https://python-poetry.org/)
