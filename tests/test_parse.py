
from datetime import date
from decimal import *
import paycalc.parse as pp
from nose.tools import eq_, raises

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
        gotMonth, gotYear = pp.parse_month_year(val)

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
        pp.parse_month_year(s)

    for c in cases:
        make_it_fail(c)

def test_parse_percent():
    cases = [
        ("1%", Decimal('0.01')),
        ("1.5%", Decimal('0.015')),
        ("25%", Decimal('0.25')),
        ("25.478%", Decimal('0.25478')),
        ("100%", Decimal('1')),
        ("140%", Decimal('1.4'))
    ]

    for (i, (val, want)) in enumerate(cases):
        print("starting case {}".format(i))
        got = pp.parse_percent(val)

        eq_(got, want)

def test_parse_percent_fails():
    cases = [
        "-1%",
        "40",
        "bat"
    ]

    @raises(ValueError)
    def make_it_fail(s):
        pp.parse_percent(s)

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
        got = pp.payperiod_string(*args)

        eq_(got, want)
