
from decimal import *

# we want to round up if we're over 50 cents
ROUND_MODE = ROUND_05UP

def round_to_dollar(dec):
    return round(dec)
