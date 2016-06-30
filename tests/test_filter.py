# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from numpy import array
from emperor.filter import (filter_samples_from_coords,
                            keep_samples_from_pcoa_data)
from unittest import TestCase, main
from numpy.testing import assert_almost_equal


class TopLevelTests(TestCase):

    def setUp(self):
        self.jk_coords_header = [['1', '2', '3'], ['1', '2', '3'],
                                 ['1', '2', '3'], ['1', '2', '3']]
        self.jk_coords_data = [array([[1.2, 0.1, -1.2], [-2.5, -4.0, 4.5],
                                      [0.11, 5.33, -0.23]]),
                               array([[-1.4, 0.05, 1.3], [2.6, 4.1, -4.7],
                                      [0.14, 2.00, -1.11]]),
                               array([[-1.5, 0.05, 1.6], [2.4, 4.0, -4.8],
                                      [1.0, -0.8, 0.01]]),
                               array([[-1.5, 0.05, 1.6], [2.4, 4.0, -4.8],
                                      [2, 0, 1.11111]])]

        self.coords_header = ['PC.355', 'PC.635', 'PC.636', 'PC.354']
        self.coords_data = COORDS_DATA

    def test_filter_samples_from_coords(self):
        """Check it filters samples from coords data as requested"""
        # check the function raises an exception on an empty set
        self.assertRaises(ValueError, filter_samples_from_coords,
                          self.coords_header, self.coords_data,
                          ['foo', 'bar', 'PC.666'])

        # check it keeps the requested samples
        out_headers, out_coords = \
            filter_samples_from_coords(self.coords_header,
                                       self.coords_data,
                                       ['PC.636', 'PC.355'])
        self.assertEqual(out_headers, ['PC.355', 'PC.636'])
        assert_almost_equal(out_coords, array([[-0.2, -0.1, 0.06, -0.06],
                                               [0.1, -0.1, -0.2, 0.08]]))

        # check it removes the requested samples
        out_headers, out_coords = \
            filter_samples_from_coords(self.coords_header,
                                       self.coords_data,
                                       ['PC.636', 'PC.355'],
                                       negate=True)

        self.assertEqual(out_headers, ['PC.635', 'PC.354'])
        assert_almost_equal(out_coords, array([[-0.3, 0.04, -0.1, 0.15],
                                               [0.04, -0.01, 0.06, -0.34]]))

    def test_remove_samples_from_pcoa_data(self):
        """ """
        # check it keeps the requested samples
        out_headers, out_coords = keep_samples_from_pcoa_data(
            self.coords_header, self.coords_data, ['PC.636', 'PC.355'])
        self.assertEqual(out_headers, ['PC.355', 'PC.636'])
        assert_almost_equal(out_coords, array([[-0.2, -0.1, 0.06, -0.06],
                                               [0.1, -0.1, -0.2, 0.08]]))

        # check it keeps the requested samples when the input is jackknifed
        # data
        out_headers, out_coords = \
            keep_samples_from_pcoa_data(self.jk_coords_header,
                                        self.jk_coords_data,
                                        ['1', '3'])
        self.assertEqual(out_headers,
                         [['1', '3'],
                          ['1', '3'],
                          ['1', '3'],
                          ['1', '3']])

        assert_almost_equal(out_coords, [array([[1.2, 0.1, -1.2],
                                                [0.11, 5.33, -0.23]]),
                                         array([[-1.4, 0.05, 1.3],
                                                [0.14, 2.00, -1.11]]),
                                         array([[-1.5, 0.05, 1.6],
                                                [1.0, -0.8, 0.01]]),
                                         array([[-1.5, 0.05, 1.6],
                                                [2, 0, 1.11111]])])

        # flip the order of the samples to keep
        out_headers, out_coords = keep_samples_from_pcoa_data(
            self.jk_coords_header, self.jk_coords_data, ['3', '1'])
        self.assertEqual(out_headers, [['1', '3'], ['1', '3'],
                                       ['1', '3'], ['1', '3']])
        assert_almost_equal(out_coords, [array([[1.2, 0.1, -1.2],
                                                [0.11, 5.33, -0.23]]),
                                         array([[-1.4, 0.05, 1.3],
                                                [0.14, 2.00, -1.11]]),
                                         array([[-1.5, 0.05, 1.6],
                                                [1.0, -0.8, 0.01]]),
                                         array([[-1.5, 0.05, 1.6],
                                                [2, 0, 1.11111]])])


COORDS_DATA = array([
    [-0.2, -0.1, 0.06, -0.06],
    [-0.3, 0.04, -0.1, 0.15],
    [0.1, -0.1, -0.2, 0.08],
    [0.04, -0.01, 0.06, -0.34]])

if __name__ == "__main__":
    main()
