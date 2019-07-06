'''
Stores tax bracket information and helper funcs
'''

from decimal import Decimal
from paycalc.calcs import round_to_dollar

# our raw tax-bracket data in (threshold, cumulative, rate) tuples
TAX_BRACKETS_2018 = [
    (18200, 0, 0.19),
    (37000, 3572, 0.325),
    (87000, 19822, 0.37),
    (180000, 54232, 0.45)
]

class TaxBrackets:
    '''
    Holds information for a set of tax brackets.

    The threshold is the lower bound at which this rate applies.

    Cumulative is the cumulative tax of prior brakets.
    '''

    class Bracket:
        '''
        Helper class to give names and correct types to tax bracket information
        '''
        def __init__(self, threshold, cumulative, rate):
            self.threshold = Decimal(threshold)
            self.cumulative = Decimal(cumulative)
            self.rate = Decimal(rate)

    def __init__(self, brackets):
        '''
        Each successive bracket must have a higher threshold. The tax free threshold
        will be inferred by the first bracket.

        :param brackets: A sequence of (threshold, rate) 2-tuples. Where `threshold` is
            the amount earned before `rate` takes effect.
        '''

        # capture in case of single-use sequence
        brackets = list(brackets)

        # check that the thresholds are in order
        if brackets != sorted(brackets, key=lambda x: x[0]):
            raise ValueError("Bracket thresholds must be in increasing order")

        self.brackets = [TaxBrackets.Bracket(t, c, r) for (t, c, r) in brackets]

    def get_bracket(self, income):
        '''
        Finds the appropriate tax bracket for a given annual income.

        :param income: The annual income of the person
        :returns: A TaxBrackets.Bracket or None if their income is below the
                  tax-free threshold
        '''

        # look for the highest bracket that is relevant
        for b in reversed(self.brackets):
            if income >= b.threshold:
                return b

        # income is below the tax-free threshold
        return None

    def total_tax(self, income):
        '''
        Calculate the total tax to be paid if `income` is earned over the year.

        :param income: The persons annual income
        :returns: The total annual tax, in whole dollars
        '''

        # find the appropriate bracket
        bracket = self.get_bracket(income)
        if bracket is None:
            return Decimal(0)

        remainder = income - bracket.threshold

        return round_to_dollar(bracket.cumulative + remainder * bracket.rate)
