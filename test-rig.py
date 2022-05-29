from datetime import datetime
from algo1 import algo1
from algo2 import algo2
from sunrise import sun

swansea = 51.62, 3.95
when = datetime.now()
print("Almanac", sun(*swansea, when))
print("Algo 01", algo1(*swansea, when))
print("Algo 02", algo2(*swansea, when))

# for 2022-05-29, in Swansea, we get:
# Almanac 🌅: 03:35 🌇: 19:49
# Algo 01 🌅: 03:35 🌇: 19:49
# Algo 02 🌅: 03:36 🌇: 19:47
