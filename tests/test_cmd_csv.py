
from io import StringIO
from nose.tools import eq_, raises

import paycalc.tax as pt
import paycalc.cmd.csv as pcsv

def test_process_csv():
    brackets = pt.TaxBrackets(pt.TAX_BRACKETS_2018)

    csv_in = StringIO("""
David,Rudd,60050,9%,March 2018
Ryan,Chen,120000,10%,Feb 2020
""".strip())
    csv_out = StringIO()

    want = """
David Rudd,01 Mar 2018 - 31 Mar 2018,5004,922,4082,450\r
Ryan Chen,01 Feb 2020 - 29 Feb 2020,10000,2669,7331,1000\r
"""[1:]

    pcsv.process_csv(brackets, csv_in, csv_out, False)
    csv_out.seek(0)
    got = csv_out.read()

    eq_(got, want)
