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
import click
import subprocess

from os import walk
from glob import glob
from os.path import join, abspath, dirname, split

from emperor import __version__


def console(cmd):
    """Small subprocess helper function

    Originally based on this SO answer:
    http://stackoverflow.com/a/33542403/379593
    """
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    o, e = process.communicate()

    return '' if o is None else o, '' if e is None else e, process.returncode


@click.command()
@click.option('--suppress_unit_tests', help="suppress execution of Emperor's "
              "unit tests", default=False, is_flag=True, show_default=True)
@click.option('--suppress_javascript_unit_tests', help="suppress Emperor's "
              "JavaScript unit tests.", default=False, is_flag=True,
              show_default=True)
@click.option('--unittest_glob', help='wildcard pattern to match the unit '
              'tests to execute.', default=None, is_flag=True,
              show_default=True)
@click.version_option(__version__)
def test(suppress_unit_tests, suppress_javascript_unit_tests, unittest_glob):
    """Run Emperor's test suite.

    Run the Python unit tests or the JavaScript unit tests (requires
    phantomjs to be installed).
    """

    # make a sanity check
    if suppress_unit_tests and suppress_javascript_unit_tests:
        raise click.UsageError("All tests have been suppresed. Nothing to "
                               "run.")

    test_dir = abspath(dirname(__file__))

    unittest_good_pattern = re.compile(b'OK\s*$')
    application_not_found_pattern = re.compile(b'ApplicationNotFoundError')
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
            print("Testing %s:\n" % unittest_name)
            command = '%s %s -v' % (python_name, unittest_name)
            stdout, stderr, return_value = console(command)
            print(stderr.decode("utf-8"))
            if not unittest_good_pattern.search(stderr):
                if application_not_found_pattern.search(stderr):
                    missing_application_tests.append(unittest_name)
                else:
                    bad_tests.append(unittest_name)

    if not suppress_javascript_unit_tests:
        runner = join(test_dir, 'javascript_tests', 'runner.js')
        index = join(test_dir, 'javascript_tests', 'index.html')

        o, e, r = console('phantomjs %s %s' % (runner, index))

        if o:
            print(o.decode('utf-8'))
        if e:
            print(e.decode('utf-8'))

        # if all the tests passed
        javascript_tests_passed = True if r == 0 else False
    else:
        javascript_tests_passed = True

    print("==============\nResult summary\n==============")

    if not suppress_unit_tests:
        print("\nUnit test result summary\n------------------------\n")
        if bad_tests:
            print("\nThe following unit tests failed.\n%s"
                  % '\n'.join(bad_tests))

        if missing_application_tests:
            print("\nThe following unit tests failed, in part or whole due "
                  "to missing external applications.\nDepending on the "
                  "Emperor features you plan to use, this may not be "
                  "critical.\n%s" % '\n'.join(missing_application_tests))

        if not(missing_application_tests or bad_tests):
            print("\nAll unit tests passed.\n")

    if not suppress_javascript_unit_tests:
        print('\nJavaScript unit tests result summary\n'
              '------------------------------------\n')
        if javascript_tests_passed:
            print('All JavaScript unit tests passed.\n')
        else:
            print('JavaScript unit tests failed, check the summary above.')

    # In case there were no failures of any type, exit with a return code of 0
    return_code = 1
    if (len(bad_tests) == 0 and len(missing_application_tests) == 0 and
       javascript_tests_passed):
        return_code = 0

    exit(return_code)

if __name__ == "__main__":
    test()
