#!/usr/bin/env python

# ASuMa, Mar 2018
# Read parse data in MST-parser format, from reference and test files
# and evaluate the accuracy of the test parses.
# See main() documentation below for usage details

import platform
import getopt, sys
import os
# import matplotlib.pyplot as plt
# import numpy as np

try:
    # from link_grammar.lgparse import *
    from link_grammar.cliutils import *
    from link_grammar.evaluate import *

except ImportError:
    # from lgparse import *
    from cliutils import *
    from evaluate import *

class EvalError(Exception):
    pass


def version():
    """
        Prints Python version used
    """
    print("Code writen for Python3.6.4. Using: %s"%platform.python_version())



def main(argv):
    """
        Evaluates parses compared to given gold standard (GS).
        For each parse, loops through all links in GS and checks if those
        2 word-instances are also connected in parse to evaluate.

        Parses must be in format:
        Sentence to evaluate
        # word1 # word2
        # word2 # word3
        ...

        Another sentence to evaluate
        # word1 # word2
        ...

        Usage: ./parse_evaluator.py -t <testfile> -r <reffile> [-v] [-i]

        testfile        file with parses to evaluate
        goldfile        file with reference (gold standard) parses
        -v              verbose
        -i              ignore LEFT-WALL and end-of-sentence dot, if any

    """

    version()

    test_file = ''
    ref_file = ''
    verbose = False
    ignore_WALL = False

    try:
        opts, args = getopt.getopt(argv, "ht:r:vi", ["test=", "reference=", "verbose", "ignore"])

    except getopt.GetoptError:
        print(main.__doc__)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(main.__doc__)
            sys.exit(0)
        elif opt in ("-t", "--test"):
            test_file = handle_path_string(arg)
        elif opt in ("-r", "--reference"):
            ref_file = handle_path_string(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-i", "--ignore"):
            ignore_WALL = True

    # Check if the arguments are properly specified.
    if test_file is None or ref_file is None or len(test_file) == 0 or len(ref_file) == 0:
        print(main.__doc__)
        exit(3)

    # If reference file does not exist then there is nothing to compare.
    if not os.path.isfile(ref_file):
        print("Error: File '" + ref_file + "' does not exist.")
        exit(4)

    try:
        compare_ull_files(test_file, ref_file, verbose, ignore_WALL)

    except EvalError as err:
        print(str(err))
        exit(4)


if __name__ == '__main__':
    main(sys.argv[1:])
