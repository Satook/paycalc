
from datetime import date
from decimal import *
import paycalc.calcs as pc
from nose.tools import eq_, raises

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

def test_parse_month_year():
    # each case is a (input, wantMonth#, wantYear#) tuple
    cases = [
        # explicit case as example and to test mixed case
        ('jAn 2008', 1, 2008),
        ('jaNuaRy 2008', 1, 2008),
    ]

    def mkcase(m, y):
        input = '{:%b} {}'.format(date(y, m, 1), y)
        return (input, m, y)

    # generate cases for this year
    cases.extend([mkcase(x, 2019) for x in range(1, 13)])
    # add in 2020 to cover leap year too
    cases.extend([mkcase(x, 2020) for x in range(1, 13)])

    for (val, wantMonth, wantYear) in cases:
        gotMonth, gotYear = pc.parse_month_year(val)

        eq_(gotMonth, wantMonth)
        eq_(gotYear, wantYear)

def test_parse_month_year_fails():
    cases = [
        "jazuaray 2019",
        "january 20019",
        "movember 2019",
    ]

    @raises(ValueError)
    def make_it_fail(s):
        pc.parse_month_year(s)

    for c in cases:
        make_it_fail(c)

def test_payperiod_string():
    cases = [
        ((1, 2019), "01 Jan 2019 - 31 Jan 2019"),
        ((2, 2017), "01 Feb 2017 - 28 Feb 2017"),
        ((3, 2016), "01 Mar 2016 - 31 Mar 2016"),
        ((6, 2018), "01 Jun 2018 - 30 Jun 2018"),
        ((2, 2020), "01 Feb 2020 - 29 Feb 2020"),
        ((2, 2000), "01 Feb 2000 - 29 Feb 2000"),
    ]

    for (args, want) in cases:
        got = pc.payperiod_string(*args)

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
