#!/usr/bin/env python
"""Run all tests.
"""
#Originally based on the all_tests.py script from the QIIME project
#(http://github.com/qiime/qiime) project at svn revision 3290, now taken from
#the E-vident (http://github.com/qiime/evident) project master branch at git SHA
#dde2a06f2d990db8b09da65764cd27fc047db788
import re

from os import walk
from sys import exit
from glob import glob
from os.path import join, abspath, dirname, split
from qiime.util import (parse_command_line_parameters, qiime_system_call,
    make_option)

__author__ = "Rob Knight"
__copyright__ = "Copyright 2013, Emperor" #consider project name
__credits__ = ["Rob Knight","Greg Caporaso", "Jai Ram Rideout",
    "Yoshiki Vazquez-Baeza"] #remember to add yourself if you make changes
__license__ = "GPL"
__version__ = "0.0-dev"
__maintainer__ = "Yoshiki Vazquez-Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("","","")]
script_info['output_description']= ""
script_info['required_options'] = []
script_info['optional_options'] = [
    make_option('--suppress_unit_tests', action='store_true', help='suppress '
    'unit tests [default: %default]', default=False),
    make_option('--unittest_glob', help='wildcard pattern to match tests to run'
    ' [default: %default]', default=None),
]
script_info['version'] = __version__
script_info['help_on_no_arguments'] = False

def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    if (opts.suppress_unit_tests):
        option_parser.error("Tests, suppresed. Nothing to run.")

    test_dir = abspath(dirname(__file__))

    unittest_good_pattern = re.compile('OK\s*$')
    application_not_found_pattern = re.compile('ApplicationNotFoundError')
    python_name = 'python'
    bad_tests = []
    missing_application_tests = []

    # Run through all of Emperor's unit tests, and keep track of any files which
    # fail unit tests.
    if not opts.suppress_unit_tests:
        unittest_names = []
        if not opts.unittest_glob:
            for root, dirs, files in walk(test_dir):
                for name in files:
                    if name.startswith('test_') and name.endswith('.py'):
                        unittest_names.append(join(root,name))
        else:
            for fp in glob(opts.unittest_glob):
                fn = split(fp)[1]
                if fn.startswith('test_') and fn.endswith('.py'):
                    unittest_names.append(abspath(fp))

        unittest_names.sort()

        for unittest_name in unittest_names:
            print "Testing %s:\n" % unittest_name
            command = '%s %s -v' % (python_name, unittest_name)
            stdout, stderr, return_value = qiime_system_call(command)
            print stderr
            if not unittest_good_pattern.search(stderr):
                if application_not_found_pattern.search(stderr):
                    missing_application_tests.append(unittest_name)
                else:
                    bad_tests.append(unittest_name)

    print "==============\nResult summary\n=============="

    if not opts.suppress_unit_tests:
        print "\nUnit test result summary\n------------------------\n"
        if bad_tests:
            print "\nFailed the following unit tests.\n%s" %'\n'.join(bad_tests)
    
        if missing_application_tests:
            print "\nFailed the following unit tests, in part or whole due "+\
                "to missing external applications.\nDepending on the Emperor "+\
                "features you plan to use, this may not be critical.\n%s"\
                % '\n'.join(missing_application_tests)
        
        if not (missing_application_tests or bad_tests):
            print "\nAll unit tests passed.\n\n"

    # In case there were no failures of any type, exit with a return code of 0
    return_code = 1
    if (len(bad_tests) == 0 and len(missing_application_tests) == 0):
        return_code = 0

    return return_code


if __name__ == "__main__":
    exit(main())
