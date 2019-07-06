
from decimal import Decimal, Context, ROUND_HALF_UP, localcontext
from datetime import date, datetime, timedelta

PAY_DATE_FMTS = [
    '%B %Y',
    '%b %Y'
]

# We will use this context when performing calculations
decimal_context = Context(
    prec=28,
    rounding=ROUND_HALF_UP
)

def round_to_dollar(dec):
    '''
    Rounds `dec` to the nearest whole dollar. Rounding up when cents > 50,
    otherwise down.

    :param dec: A decimal.Decimal value to round.
    :returns: A decimal.Decimal
    '''

    with localcontext(decimal_context):
        return round(dec, 0)

def parse_month_year(dstr):
    '''
    Parse a "Month Year" string, e.g. "Jan 2019" into a tuple of 2 integers.

    Is cases insensitive and support month short or long names, e.g. Jan and January.

    Note:

    :param dstr: A string in "month year" format, e.g. "March 2020"
    :returns: A (month, year) tuple where both values are integers
    :raises ValueError: If the passed in string was not valid
    '''
    for fmt in PAY_DATE_FMTS:
        try:
            d = datetime.strptime(dstr, fmt)

            return (d.month, d.year)
        except ValueError:
            continue

    raise ValueError("\"{}\" is not valid".format(dstr))

def payperiod_string(m, y):
    '''
    Given a month and year, returns the pay period as a string date range

    :param m: The month as an integer, i.e. 1-12
    :param y: The full year as an integer, e.g. 2019
    :returns: A string that describes the entire month, "01 Mar 2019 - 31 Mar 2019"
    '''
    startdate = date(y, m, 1)
    nextmonth = startdate + timedelta(days=32)
    enddate = date(nextmonth.year, nextmonth.month, 1) - timedelta(days=1)

    return "{:%d %b %Y} - {:%d %b %Y}".format(startdate, enddate)

def calc_gross_income(annual_income):
    '''
    Calculate the gross income for the month.

    :param annual_income: Their annual income
    :returns: The months gross income rounded to the dollar
    '''
    return round_to_dollar(annual_income / Decimal(12))

def calc_super_contrib(income, rate):
    '''
    Calculate the dollar super contribution amount based on `rate`

    :param income: The income for the period
    :param rate: The superannuation contribution rate
    :returns: The dollar amount of superannuation to be contributed
    '''

    return round_to_dollar(income * rate)
