'''
Helper functions to read and print data in CSV format
'''

import csv
from decimal import Decimal
from datetime import date, datetime, timedelta

PAY_DATE_FMTS = [
    '%B %Y',
    '%b %Y'
]

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

def parse_percent(pstr):
    pass

ROW_PARSERS = [
    lambda fn: fn,
    lambda ln: ln,
    Decimal,
    parse_percent,
    parse_month_year
]

def parse_csv(filein):
    '''
    Reads in CSV rows from filein, yielding parsed rows.

    Firstname and lastname are left as-is.
    Annual salary will be a Decimal
    Super rate will be a decimal (adjusted from % to fraction)
    Payment month will be a (month, year) tuple as returned by calcs.parse_month_year

    :param filein: A file-like object for reading CSV data
    :yields: (firstname, lastname, annual salary, super rate, payment month) tuples
    :raises: ValueError if a row is not valid
    '''

    reader = csv.reader(filein)

    for (i, row) in enumerate(reader):
        pass
