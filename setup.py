#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='paycalc',
    version='1.0',
    description='CLI and libs for pay calculations',
    author='Andrew Stewart',
    author_email='andrewstewis@gmail.com',
    url='http://github.com/Satook/paycalc',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            "paycalc-csv = paycalc.cmd.csv:do_paycalc"
        ]
    }
)
