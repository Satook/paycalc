
import argparse
import csv
import sys
from paycalc import parse

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

    process_csv(sys.stdin, sys.stdout, args.skipfirst)

ROW_PRINTERS = [
    lambda fn: fn,
    lambda ln: ln,
]

def process_csv(filein, fileout, skip_first_row):

    writer = csv.writer(fileout)

    for in_row in parse.parse_csv(sys.stdin):
        out_row = process_slip(in_row)

        writer.writerow(out_row)
