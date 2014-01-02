#!/usr/bin/env python
#unit tests for format.py
from __future__ import division

__author__ = "Rob Knight"
__copyright__ = "Copyright 2011, The QIIME Project" #consider project name
__credits__ = ["Rob Knight", "Daniel McDonald", "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from unittest import main, TestCase
from emperor.qiime_backports.format import format_mapping_file

class TopLevelTests(TestCase):
    """Tests of top-level module functions."""
    
    def setUp(self):
      pass

    def test_format_mapping_file(self):
        """ format_mapping file should match expected result"""
        headers = ['SampleID','col1','col0','Description']
        samples =\
         [['bsample','v1_3','v0_3','d1'],['asample','aval','another','d2']]
        comments = ['this goes after headers','this too']
        self.assertEqual(format_mapping_file(headers,samples,comments),
         example_mapping_file)
        # need file or stringIO for roundtrip test
        # roundtrip = parse_mapping_file(format_mapping_file(headers,samples,comments))
        # self.assertEqual(roundtrip, [headers,samples,comments])

example_mapping_file = """#SampleID\tcol1\tcol0\tDescription
#this goes after headers
#this too
bsample\tv1_3\tv0_3\td1
asample\taval\tanother\td2"""


#run unit tests if run from command-line
if __name__ == '__main__':
    main()
