#! /usr/bin/env python

# PonyGE2
# Copyright (c) 2017 Michael Fenton, James McDermott,
#                    David Fagan, Stefan Forstenlechner,
#                    and Erik Hemberg
# Hereby licensed under the GNU GPL v3.
""" Python GE implementation """

from algorithm.parameters import params
from utilities.algorithm.general import check_python_version
from utilities.stats.save_plots import draw_and_save_turtle_plot
from utilities.stats import trackers

check_python_version()

from stats.stats import get_stats
from algorithm.parameters import params, set_params
import sys


def mane():
    """ Run program """

    # Run evolution
    individuals = params['SEARCH_LOOP']()

    # Print final review
    get_stats(individuals, end=True)


if __name__ == "__main__":
    set_params(sys.argv[1:])  # exclude the ponyge.py arg itself
    mane()
