# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main

import pandas as pd

from emperor.core import Emperor
from emperor.pandas import scatterplot

# account for what's allowed in python 2 vs PY3K
try:
    from . import _test_core_strings as tcs
except:
    import _test_core_strings as tcs

# from http://stackoverflow.com/a/22605281/379593
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO


class TopLevelTests(TestCase):
    def setUp(self):
        self.df = pd.read_csv(StringIO(tcs.MAP_PANDAS), sep='\t',
                              index_col='#SampleID')

    def test_scatterplot(self):
        emp = scatterplot(self.df)

        self.assertTrue(isinstance(emp, Emperor))

if __name__ == "__main__":
    main()
