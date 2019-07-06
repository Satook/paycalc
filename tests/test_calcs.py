
from decimal import *
import paycalc.calcs as pc
from nose.tools import eq_

def test_round_to_dollar():
    cases = [
        (Decimal(1.0), Decimal(1.0)),
        (Decimal(1.50), Decimal(2.0)),
        (Decimal(1.51), Decimal(2.0)),
        (Decimal(1.49), Decimal(1.0)),
        (Decimal(1.01), Decimal(1.0)),
    ]

    for (i, (val, want)) in enumerate(cases):
        got = pc.round_to_dollar(val)

        eq_(got, want)
