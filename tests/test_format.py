# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from emperor.format import format_emperor_autograph
from unittest import TestCase, main


class TopLevelTests(TestCase):

    def test_format_emperor_autograph(self):
        """Test signatures are created correctly for each of language"""

        autograph = format_emperor_autograph('mapping_file.txt',
                                             'pcoa_unweighted_unifrac.txt')

        # check for comment open and comment close
        self.assertTrue('<!--' in autograph)
        self.assertTrue('-->' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
                                             'pcoa_unweighted_unifrac.txt',
                                             'Python')
        # check for comment open and comment close
        self.assertTrue('"""' in autograph)
        self.assertTrue('"""' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
                                             'pcoa_unweighted_unifrac.txt',
                                             'C')
        # check for comment open and comment close
        self.assertTrue('/*' in autograph)
        self.assertTrue('*/' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
                                             'pcoa_unweighted_unifrac.txt',
                                             'Bash')
        # check for comment open and comment close
        self.assertTrue('<<COMMENT' in autograph)
        self.assertTrue('COMMENT' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        # haskell and cobol are ... not supported
        self.assertRaises(AssertionError, format_emperor_autograph,
                          'mapping_file.txt', 'pcoa.txt', 'Haskell')
        self.assertRaises(AssertionError, format_emperor_autograph,
                          'mapping_file.txt', 'pcoa.txt', 'Cobol')


if __name__ == "__main__":
    main()
