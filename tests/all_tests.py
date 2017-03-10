#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
"""Run all tests.

Originally based on the all_tests.py script from the QIIME project
(http://github.com/qiime/qiime) project at svn revision 3290, now taken from
the E-vident (http://github.com/qiime/evident) project master branch at git SHA
dde2a06f2d990db8b09da65764cd27fc047db788
"""

import re

from os import walk, getcwd, chdir
from sys import exit
from glob import glob
from os.path import join, abspath, dirname, split, exists

from emperor.util import get_emperor_project_dir
from emperor import __version__

from qcli.util import qcli_system_call
from qcli.test import run_script_usage_tests
from qcli.option_parsing import parse_command_line_parameters, make_option

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = [("", "", "")]
script_info['output_description'] = ""
script_info['required_options'] = []
script_info['optional_options'] = [
    make_option('--suppress_unit_tests', action='store_true', help='suppress '
                " execution of Emperor's unit tests [default: %default]",
                default=False),
    make_option('--suppress_script_usage_tests', action='store_true',
                help="suppress Emperor's script usage tests [default: "
                "%default]", default=False),
    make_option('--suppress_javascript_unit_tests', action='store_true',
                help='suppress Emperor\'s JavaScript unit tests [default: '
                '%default]', default=False),
    make_option('--unittest_glob', help='wildcard pattern to match the unit '
                'tests to execute [default: %default]', default=None),
    make_option('--script_usage_tests', help='comma-separated list of the '
                'script usage tests to execute [default: run all]',
                default=None),
    make_option('-p', '--temp_filepath', type='existing_path', help='temporary'
                ' directory where the script usage tests will be executed',
                default='/tmp/'),
    make_option('--emperor_scripts_dir', help='filepath where the scripts are'
                ' stored', type='existing_path', default=None)
]
script_info['version'] = __version__
script_info['help_on_no_arguments'] = False


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)

    unittest_glob = opts.unittest_glob
    temp_filepath = opts.temp_filepath
    script_usage_tests = opts.script_usage_tests
    suppress_unit_tests = opts.suppress_unit_tests
    suppress_script_usage_tests = opts.suppress_script_usage_tests
    suppress_javascript_unit_tests = opts.suppress_javascript_unit_tests

    # since the test data is in the tests folder just add scripts_test_data
    emperor_test_data_dir = join(abspath(dirname(__file__)),
                                 'scripts_test_data/')

    # offer the option for the user to pass the scripts dir from the command
    # line since there is no other way to get the scripts dir. If not provided
    # the base structure of the repository will be assumed. Note that for both
    # cases we are using absolute paths, to avoid unwanted failures.
    if opts.emperor_scripts_dir is None:
        emperor_scripts_dir = abspath(join(get_emperor_project_dir(),
                                           'scripts/'))

        # let's try to guess cases for qiime-deploy type of installs
        if get_emperor_project_dir().endswith('/lib'):
            emperor_scripts_dir = abspath(join(get_emperor_project_dir()[:-3],
                                               'scripts/'))

    else:
        emperor_scripts_dir = abspath(opts.emperor_scripts_dir)

    # make a sanity check
    if (suppress_unit_tests and suppress_script_usage_tests and
            suppress_javascript_unit_tests):
        option_parser.error("All tests have been suppresed. Nothing to run.")

    test_dir = abspath(dirname(__file__))

    unittest_good_pattern = re.compile('OK\s*$')
    application_not_found_pattern = re.compile('ApplicationNotFoundError')
    python_name = 'python'
    bad_tests = []
    missing_application_tests = []

    # Run through all of Emperor's unit tests, and keep track of any files
    # which fail unit tests, note that these are the unit tests only
    if not suppress_unit_tests:
        unittest_names = []
        if not unittest_glob:
            for root, dirs, files in walk(test_dir):
                for name in files:
                    if name.startswith('test_') and name.endswith('.py'):
                        unittest_names.append(join(root, name))
        else:
            for fp in glob(unittest_glob):
                fn = split(fp)[1]
                if fn.startswith('test_') and fn.endswith('.py'):
                    unittest_names.append(abspath(fp))

        unittest_names.sort()

        for unittest_name in unittest_names:
            print "Testing %s:\n" % unittest_name
            command = '%s %s -v' % (python_name, unittest_name)
            stdout, stderr, return_value = qcli_system_call(command)
            print stderr
            if not unittest_good_pattern.search(stderr):
                if application_not_found_pattern.search(stderr):
                    missing_application_tests.append(unittest_name)
                else:
                    bad_tests.append(unittest_name)

    script_usage_failures = 0

    # choose to run some of the script usage tests or all the available ones
    if (not suppress_script_usage_tests and exists(emperor_test_data_dir) and
            exists(emperor_scripts_dir)):
        if script_usage_tests is not None:
            script_tests = script_usage_tests.split(',')
        else:
            script_tests = None

        initial_working_directory = getcwd()

        # Run the script usage testing functionality; note that depending on
        # the module where this was imported, the name of the arguments will
        # change that's the reason why I added the name of the arguments in
        # here
        script_usage_result_summary, script_usage_failures = \
            run_script_usage_tests(emperor_test_data_dir,  # test_data_dir
                                   emperor_scripts_dir,    # scripts_dir
                                   temp_filepath,          # working_dir
                                   True,                   # verbose
                                   script_tests,           # tests
                                   None,                   # failure_log_fp
                                   False)                  # force_overwrite

        # running script usage tests breaks the current working directory
        chdir(initial_working_directory)

    if not suppress_javascript_unit_tests:
        runner = join(test_dir, 'javascript_tests', 'runner.js')
        index = join(test_dir, 'javascript_tests', 'index.html')

        o, e, r = qcli_system_call('phantomjs %s %s' % (runner, index))

        if o:
            print o
        if e:
            print e

        # if all the tests passed
        javascript_tests_passed = True if r == 0 else False
    else:
        javascript_tests_passed = True

    print "==============\nResult summary\n=============="

    if not suppress_unit_tests:
        print "\nUnit test result summary\n------------------------\n"
        if bad_tests:
            print("\nFailed the following unit tests.\n%s"
                  % '\n'.join(bad_tests))

        if missing_application_tests:
            print("\nFailed the following unit tests, in part or whole due "
                  "to missing external applications.\nDepending on the "
                  "Emperor features you plan to use, this may not be "
                  "critical.\n%s" % '\n'.join(missing_application_tests))

        if not(missing_application_tests or bad_tests):
            print "\nAll unit tests passed.\n"

    if not suppress_script_usage_tests:
        if exists(emperor_test_data_dir) and exists(emperor_scripts_dir):
            print("\nScript usage test result summary"
                  "\n--------------------------------\n")
            print script_usage_result_summary
        else:
            print("\nCould not run script usage tests.\nThe Emperor scripts "
                  "directory could not be automatically located, try "
                  "supplying it manually using the --emperor_scripts_dir "
                  "option.")

    if not suppress_javascript_unit_tests:
        print('\nJavaScript unit tests result summary\n'
              '------------------------------------\n')
        if javascript_tests_passed:
            print 'All JavaScript unit tests passed.\n'
        else:
            print 'JavaScript unit tests failed, check the summary above.'

    # In case there were no failures of any type, exit with a return code of 0
    return_code = 1
    if (len(bad_tests) == 0 and len(missing_application_tests) == 0 and
            script_usage_failures == 0 and javascript_tests_passed):
        return_code = 0

    return return_code


if __name__ == "__main__":
    exit(main())
