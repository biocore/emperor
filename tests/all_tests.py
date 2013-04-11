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
from qiime.test import run_script_usage_tests
from emperor.util import get_emperor_project_dir
from os.path import join, abspath, dirname, split, exists
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
    ' execution of Emperor\'s unit tests [default: %default]', default=False),
    make_option('--suppress_script_usage_tests', action='store_true', help=
    'suppress Emperor\'s script usage tests [default: %default]',default=False),
    make_option('--unittest_glob', help='wildcard pattern to match the unit '
    'tests to execute [default: %default]', default=None),
    make_option('--scripts_to_test', help='comma-separated list of the script '
    'tests to execute [default: run all]', default=None),
    make_option('-p', '--temp_filepath', type='existing_path', help='temporary '
    'directory where the script usage tests will be executed', default='/tmp/'),
    make_option('--emperor_test_data_dir', help='filepath where the test data'
    'is stored', type='existing_path', default=None),
    make_option('--emperor_scripts_dir', help='filepath where the scripts are'
    ' stored', type='existing_path', default=None)
]
script_info['version'] = __version__
script_info['help_on_no_arguments'] = False


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    unittest_glob = opts.unittest_glob
    temp_filepath = opts.temp_filepath
    scripts_to_test = opts.scripts_to_test
    suppress_unit_tests = opts.suppress_unit_tests
    suppress_script_usage_tests = opts.suppress_script_usage_tests


    # offer the option for the user to pass the test and the scripts dir
    # from the command line since the test data is not deployed with setup.py
    # if not provided, the base structure of the repository will be assumed
    if opts.emperor_test_data_dir == None:
        emperor_test_data_dir = join(get_emperor_project_dir(), 'tests/'
            'scripts_test_data/')
    else:
        emperor_test_data_dir = opts.emperor_test_data_dir
    if opts.emperor_scripts_dir == None:
        emperor_scripts_dir = join(get_emperor_project_dir(), 'scripts/')
    else:
        emperor_scripts_dir = opts.emperor_scripts_dir

    # make a sanity check
    if (suppress_unit_tests and suppress_script_usage_tests):
        option_parser.error("All tests have been suppresed. Nothing to run.")

    test_dir = abspath(dirname(__file__))

    unittest_good_pattern = re.compile('OK\s*$')
    application_not_found_pattern = re.compile('ApplicationNotFoundError')
    python_name = 'python'
    bad_tests = []
    missing_application_tests = []

    # Run through all of Emperor's unit tests, and keep track of any files which
    # fail unit tests, note that these are the unit tests only
    if not suppress_unit_tests:
        unittest_names = []
        if not unittest_glob:
            for root, dirs, files in walk(test_dir):
                for name in files:
                    if name.startswith('test_') and name.endswith('.py'):
                        unittest_names.append(join(root,name))
        else:
            for fp in glob(unittest_glob):
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

    script_usage_failures = 0

    # choose to run some of the script usage tests or all the available ones
    if not suppress_script_usage_tests and exists(emperor_test_data_dir) and\
        exists(emperor_scripts_dir):
        if scripts_to_test != None:
            script_tests = scripts_to_test.split(',')
        else:
            script_tests = None
        # Run the script usage testing functionality
        script_usage_result_summary, script_usage_failures = \
            run_script_usage_tests(qiime_test_data_dir=emperor_test_data_dir,
            qiime_scripts_dir=emperor_scripts_dir,
            working_dir=temp_filepath, verbose=True,
            tests=script_tests, failure_log_fp=None, force_overwrite=False)

    print "==============\nResult summary\n=============="

    if not suppress_unit_tests:
        print "\nUnit test result summary\n------------------------\n"
        if bad_tests:
            print "\nFailed the following unit tests.\n%s" %'\n'.join(bad_tests)
    
        if missing_application_tests:
            print "\nFailed the following unit tests, in part or whole due "+\
                "to missing external applications.\nDepending on the Emperor "+\
                "features you plan to use, this may not be critical.\n%s"\
                % '\n'.join(missing_application_tests)
        
        if not(missing_application_tests or bad_tests):
            print "\nAll unit tests passed.\n\n"

    if not suppress_script_usage_tests:
        if exists(emperor_test_data_dir) and exists(emperor_scripts_dir):
            print "\nScript usage test result summary\n------------------------------------\n"
            print script_usage_result_summary
        else:
            print ("\nCould not run script usage tests.\nThe Emperor test data"
                " directory and the Emperor scripts directory could not be "
                " automatically located, try supplying them manually with the"
                " --emperor_test_data_dir and with --emperor_scripts_dir "
                "options.")

    # In case there were no failures of any type, exit with a return code of 0
    return_code = 1
    if (len(bad_tests) == 0 and len(missing_application_tests) == 0 and
        script_usage_failures == 0):
        return_code = 0

    return return_code


if __name__ == "__main__":
    exit(main())
