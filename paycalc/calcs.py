
from decimal import *

# We will use this context when performing calculations
decimal_context = Context(
    prec=28,
    rounding=ROUND_HALF_UP
)

def round_to_dollar(dec):
    '''
    Rounds `dec` to the nearest whole dollar. Rounding up when cents > 50,
    otherwise down.
    '''

    with localcontext(decimal_context):
        return round(dec, 0)
