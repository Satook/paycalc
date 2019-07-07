
from nose.tools import eq_, raises

import paycalc.tax as pt

def test_brackets_at_threshold():
    brackets = pt.TaxBrackets(pt.TAX_BRACKETS_2018)

    cases = [
        (100, 0),
        (18200, 0),
        (18300, 19),
        (37000, 3572),
        (37200, 3572 + (32.5*2)),
        (87000, 19822),
        (87100, 19822 + 37),
        (180000, 54232),
        (180100, 54232 + 45),
        (240000, 54232 + 27000),
    ]

    for (i, (income, want)) in enumerate(cases):
        got = brackets.total_tax(income)

        print("Starting case: {}".format(i))
        eq_(got, want)

@raises(ValueError)
def test_brackets_fails():
    # we'll hand them in out-of-order and check that they're rejected
    pt.TaxBrackets([
        (25000, 25),
        (18000, 19),
        (99000, 30),
    ])
