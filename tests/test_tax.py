
import paycalc.tax as pt
from nose.tools import eq_, raises

class TestTaxBrackets:
    def setUp(self):
        self.brackets = pt.TaxBrackets(pt.TAX_BRACKETS_2018)

    def test_brackets_at_threshold(self):
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
            got = self.brackets.total_tax(income)

            print("Starting case: {}".format(i))
            eq_(got, want)
