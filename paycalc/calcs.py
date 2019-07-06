
from decimal import Decimal, Context, ROUND_HALF_UP, localcontext

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

def calculate_pay_slip(tax_bracket, annual_income, super_rate):
    '''
    Calculates the info for a monthly payslip.

    :param tax_bracket: A TaxBrackets object for calculating tax.
    :param annual_income: The persons gross annual income.
    :param super_rate: The employer super contribution rate.
    :returns: A (gross income, tax, net income, super contrib) tuple where all
              values are Decimals
    '''

    monthly_gross = calc_gross_income(annual_income)
    monthly_tax = round_to_dollar(tax_bracket.total_tax(annual_income) / Decimal(12))
    net_income = monthly_gross - monthly_tax
    monthly_super = calc_super_contrib(monthly_gross, super_rate)

    return (monthly_gross, monthly_tax, net_income, monthly_super)
