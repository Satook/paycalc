
import argparse
import csv
import sys
import paycalc.tax as pt
from paycalc import parse
from paycalc.calcs import calculate_pay_slip

def do_paycalc():
    '''
    An entry point that takes in a CSV data and prints the resulting pay
    slip data to stdout.
    '''
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
Calculate pay slip information by reading in CSV data.

Quoted CSV data is read in on STDIN and the calculation results are
printed to STDOUT.

Each line of the CSV must contain:
    first name, last name, annual salary, super rate (%), payment month

Annual salary must be a number without commas or punctuation, e.g. 60050.
Super rate should be a number from 0-100 followed by a % sign, e.g. 9%.
Payment month should be a "month year" string, e.g. "jan 2018" or "March 2020".
""")
    parser.add_argument('--skipfirst', action='store_true', help='Skip the first line, often a header')

    # we don't have any arguments, we just wanted a nice --help answer :)
    args = parser.parse_args()

    # we are only using this single set of tax brackets
    brackets = pt.TaxBrackets(pt.TAX_BRACKETS_2018)

    process_csv(brackets, sys.stdin, sys.stdout, args.skipfirst)

def process_csv(tax_brackets, filein, fileout, skip_first_row):
    '''
    Runs the parsing and processing of CSV based data.

    :param tax_brackets: The paycalc.tax.TaxBrackets object to use for calculating
                         annual tax owed.
    :param filein: A file-like object from which CSV data will be read.
    :param fileout: A file-like object into which CSV formatted payslips data
                    will be written.
    :param skip_first_row: If True, the first line of data in filein will be ignored.
    '''

    writer = csv.writer(fileout)

    for (firstname, lastname, annual_salary, super_rate, pay_month) in parse.parse_csv(filein, skip_first_row):
        slip_data = calculate_pay_slip(tax_brackets, annual_salary, super_rate)
        (monthly_gross, monthly_tax, net_income, monthly_super) = slip_data

        out_data = (
            "{} {}".format(firstname, lastname),
            parse.payperiod_string(*pay_month),
            str(monthly_gross),
            str(monthly_tax),
            str(net_income),
            str(monthly_super)
        )

        writer.writerow(out_data)
