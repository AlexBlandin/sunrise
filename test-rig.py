from datetime import datetime
from algo1 import algo1
from algo2 import algo2
from sunrise import sun
from helpers import day_after

swansea = 51.62, 3.95
when = datetime.now()
print("Almanac", sun(*swansea, when))
print("Algo 01", algo1(*swansea, when))
print("Algo 02", algo2(*swansea, when))

# Algo1 is basically as accurate as Almanac, it just may be a minute off a little under half the time.
