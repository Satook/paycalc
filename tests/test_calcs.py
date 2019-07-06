
from datetime import date
from decimal import *
from nose.tools import eq_, raises

import paycalc.calcs as pc
import paycalc.tax as pt

def test_round_to_dollar():
    cases = [
        (Decimal(1.0), Decimal(1.0)),
        (Decimal(1.50), Decimal(2.0)),
        (Decimal(1.51), Decimal(2.0)),
        (Decimal(1.49), Decimal(1.0)),
        (Decimal(1.01), Decimal(1.0)),
    ]

    for (val, want) in cases:
        got = pc.round_to_dollar(val)

        eq_(got, want)

def test_calc_gross_income():
    cases = [
        (Decimal(60050), Decimal(5004)),
        (Decimal(120000), Decimal(10000)),
    ]

    for (val, want) in cases:
        got = pc.calc_gross_income(val)

        assert isinstance(got, Decimal)
        eq_(got, want)

def test_calc_super_contrib():
    cases = [
        ((5004, 0.09), 450),
        ((10000, 0.1), 1000),
    ]

    for ((inc, rate), want) in cases:
        got = pc.calc_super_contrib(inc, rate)

        eq_(got, want)

def test_calculate_pay_slip():

    # This is technically an integraton test, but it's not too naughty
    brackets = pt.TaxBrackets(pt.TAX_BRACKETS_2018)

    cases = [
        (
            (Decimal('60050'), Decimal('0.09')),
            (Decimal('5004'), Decimal('922'), Decimal('4082'), Decimal('450'))
        ),
        (
            (Decimal('120000'), Decimal('0.1')),
            (Decimal('10000'), Decimal('2669'), Decimal('7331'), Decimal('1000'))
        ),
    ]

    for (i, (val, want)) in enumerate(cases):
        print("starting case: {}".format(i))

        got = pc.calculate_pay_slip(brackets, *val)

        eq_(got, want)
