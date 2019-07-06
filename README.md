
# Install

With the repo checked out, just run:

```bash
python setup.py install
```

Or to install in "developer mode", where the installed command references the
checked out code, just run:

```bash
python setup.py develop
```

# Example usage

Once installed, the command is *paycalc-csv*. Use the **--help** option to
display help.

paycalc-csv reads from STDIN and writes to STDOUT. If your source data is in
*"people.csv"* and you want the results to *"slips.csv"*, just run

```bash
paycalc-csv < people.csv > slips.csv
```

If you source CSV has headers, add --skipfirst to the argument list to have
paycalc-csv ignore the first line.

**Note:** The expected CSV dialect is excel format, which uses quoted strings,
comma separators and \r\n for line endings. Both \r and \n on their own are
accepted too.

# Tests

Tests are just run using nose. In the repo root, just run

```bash
nosetests
```

# Assumptions

 #. Will be run with an en_US or en_AU locale. Month names are expected in the
    correct format for the current locale.

 #. That all intermediary calculation can be performed at high (28 digit)
    precision but named values, e.g. gross income, tax, etc should be rounded
    before their use in further calculations.
