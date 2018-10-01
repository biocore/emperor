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

import sys
import click
import subprocess

from os.path import join, abspath, dirname
from unittest import TestLoader, TextTestRunner

from emperor import __version__


def console(cmd, stdout=None, stderr=None):
    """Small subprocess helper function

    Originally based on this SO answer:
    http://stackoverflow.com/a/33542403/379593
    """
    if stdout is None:
        stdout = subprocess.PIPE
    if stderr is None:
        stderr = subprocess.PIPE

    process = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
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
    bad_tests = []

    # Run through all of Emperor's unit tests, and keep track of any files
    # which fail unit tests, note that these are the unit tests only
    if not suppress_unit_tests:
        res = TextTestRunner().run(TestLoader().discover(start_dir=test_dir))

    if not suppress_javascript_unit_tests:
        click.echo("JavaScript Test Suite")
        runner = join(test_dir, 'javascript_tests', 'runner.js')
        index = join(test_dir, 'javascript_tests', 'index.html')

        # phantomjs has some problems where the program will not terminate if
        # an error occurs during the execution of the test suite. That's why
        # all output is sent to standard output and standard error.
        _, _, r = console('phantomjs %s %s' % (runner, index), sys.stdout,
                          sys.stderr)

        # if all the tests passed
        javascript_tests_passed = True if r == 0 else False
    else:
        javascript_tests_passed = True

    click.echo("==============\nResult summary\n==============")

    if not suppress_unit_tests:
        click.echo("\nUnit test result summary\n------------------------\n")
        if not res.wasSuccessful():
            bad_tests = [i[0].id() for i in res.failures + res.errors]
            click.echo("\nThe following unit tests failed:\n%s"
                       % '\n'.join(bad_tests))
        else:
            click.echo("\nAll unit tests passed.\n")

    if not suppress_javascript_unit_tests:
        click.echo('\nJavaScript unit tests result summary\n'
                   '------------------------------------\n')
        if javascript_tests_passed:
            click.echo('All JavaScript unit tests passed.\n')
        else:
            click.echo('JavaScript unit tests failed, check the summary '
                       'above.')

    # In case there were no failures of any type, exit with a return code of 0
    return_code = 1
    if (len(bad_tests) == 0 and javascript_tests_passed):
        return_code = 0

    exit(return_code)


if __name__ == "__main__":
    test()
