from datetime import datetime
from algo1 import algo1
from algo2 import algo2
from sunrise import sun
from helpers import tf

swansea = 51.62, 3.95
when = datetime.now()
tf(sun, *swansea, when)
tf(algo1, *swansea, when)
tf(algo2, *swansea, when)

# for 2022-05-29, in Swansea, we get:
# Sun 🌅: 03:35 🌇: 19:49
# Algo1 🌅: 03:35 🌇: 19:49
# Algo2 🌅: 03:36 🌇: 19:47
