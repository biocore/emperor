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
import numpy as np

from emperor.core import Emperor
from emperor._pandas import scatterplot

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

        x = np.array([[0.27272727, 0.65384615, 1., 0.24657534],
                      [0.03896104, 0.46153846, 0.58666667, 0.57534247],
                      [0.68831169, 1., 0.06666667, 0.95890411],
                      [0.61038961, 0.92307692, 0.96, 0.17808219],
                      [0.16883117, 0.71794872, 0.01333333, 0.68493151],
                      [0.16883117, 0.06410256, 0.52, 0.76712329],
                      [1., 0.82051282, 0.34666667, 0.23287671],
                      [0.81818182, 0.88461538, 0.98666667, 0.2739726],
                      [0.25974026, 0.20512821, 0.52, 0.43835616],
                      [0.24675325, 0.21794872, 0.81333333, 0.60273973],
                      [0.61038961, 0.53846154, 0.49333333, 0.34246575],
                      [0.64935065, 0.74358974, 0.36, 1.],
                      [0.14285714, 0.41025641, 0.54666667, 0.49315068],
                      [0.11688312, 0.32051282, 0.56, 0.43835616]])
        ind = pd.Index(['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9',
                        's10', 's11', 's12', 's13', 's14'], dtype='object',
                       name='#SampleID')
        cols = pd.Index(['num_1', 'num_4', 'num_3', 'num_2'], dtype='object')
        self.samples = pd.DataFrame(data=x, index=ind, columns=cols)

    def test_scatterplot(self):
        emp = scatterplot(self.df)

        self.assertTrue(isinstance(emp, Emperor))
        self.assertEqual(emp.dimensions, 4)
        self.assertEqual(emp.base_url, 'https://cdn.rawgit.com/biocore/'
                         'emperor/new-api/emperor/support_files')

        pd.util.testing.assert_frame_equal(self.df, emp.mf)

        pd.util.testing.assert_frame_equal(emp.ordination.samples,
                                           self.samples)

    def test_scatterplot_reordered(self):
        emp = scatterplot(self.df, x='num_3', y='num_2', z='num_1')

        self.assertTrue(isinstance(emp, Emperor))
        self.assertEqual(emp.dimensions, 4)
        self.assertEqual(emp.base_url, 'https://cdn.rawgit.com/biocore/'
                         'emperor/new-api/emperor/support_files')

        pd.util.testing.assert_frame_equal(self.df, emp.mf)

        reordered = self.samples[['num_3', 'num_2', 'num_1', 'num_4']].copy()

        pd.util.testing.assert_frame_equal(emp.ordination.samples,
                                           reordered)

    def test_bad_column_names(self):
        np.testing.assert_raises(ValueError, scatterplot, self.df, x=':L')
        np.testing.assert_raises(ValueError, scatterplot, self.df, x='num_1',
                                 y='column', z='McColumnFace')

    def test_bad_data(self):
        no_numeric = self.df.select_dtypes(include=['object']).copy()

        np.testing.assert_raises(ValueError, scatterplot, no_numeric)

    def test_bad_non_numeric_columns(self):
        np.testing.assert_raises(ValueError, scatterplot, self.df, x='cat_a')

    def test_no_dataframe(self):
        np.testing.assert_raises(ValueError, scatterplot, None)
        np.testing.assert_raises(ValueError, scatterplot, 1)
        np.testing.assert_raises(ValueError, scatterplot, 'DataMcDataface')


if __name__ == "__main__":
    main()
