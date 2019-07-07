
import sys
from io import StringIO
from nose.tools import eq_, raises

import paycalc.tax as pt
import paycalc.cmd.csv as pcsv

class TestCSVCmd:
    '''
    Uses the same test data to test both do_paycalc and process_csv

    Just helps pinpoint any issues
    '''

    def setUp(self):
        TEST_CSV = """
David,Rudd,60050,9%,March 2018
Ryan,Chen,120000,10%,Feb 2020
""".strip()

        self.brackets = pt.TaxBrackets(pt.TAX_BRACKETS_2018)
        self.csv_in = StringIO(TEST_CSV)
        self.csv_out = StringIO()

        self.rawWant = """
David Rudd,01 Mar 2018 - 31 Mar 2018,5004,922,4082,450\r
Ryan Chen,01 Feb 2020 - 29 Feb 2020,10000,2669,7331,1000\r
"""[1:]

    def check_out(self, want):
        self.csv_out.seek(0)
        got = self.csv_out.read()
        eq_(got, want)

    def test_process_csv_noskip(self):
        pcsv.process_csv(self.brackets, self.csv_in, self.csv_out, False)

        self.check_out(self.rawWant)

    def test_process_csv_skip(self):
        pcsv.process_csv(self.brackets, self.csv_in, self.csv_out, True)

        self.check_out(self.rawWant.partition('\r\n')[2])

    def with_patched(self, argv, f):
        try:
            # patch out stdin/stdout/argv
            orig_stdout = sys.stdout
            orig_stdin = sys.stdin
            orig_argv = sys.argv
            sys.stdout = self.csv_out
            sys.stdin = self.csv_in
            sys.argv = argv

            f()

        finally:
            sys.stdout = orig_stdout
            sys.stdin = orig_stdin
            sys.argv = orig_argv

    def test_main_noskip(self):
        # do some monkey patching
        def doWork():
            pcsv.do_paycalc()

            self.check_out(self.rawWant)

        self.with_patched(sys.argv, doWork)

    def test_main_skipfirst(self):
        # do some monkey patching
        def doWork():
            pcsv.do_paycalc()

            self.check_out(self.rawWant.partition('\r\n')[2])

        # monkey argv
        argv = [sys.argv[0], "--skipfirst"]
        self.with_patched(argv, doWork)
