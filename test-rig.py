from algo1 import algo1
from algo2 import algo2
from correct import correct
from helpers import guess_latlon, lalo

swansea = lalo("51°37′N 3°57′W")
latlon = guess_latlon()
print(*swansea)
print(*latlon)
print("Correct", correct(*latlon))
print("Algo 01", algo1(*latlon))
print("Algo 02", algo2(*latlon))

# Algo1 is basically as accurate as Correct, it just may be a minute off a little under half the time.
