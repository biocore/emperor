# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main
from tempfile import mkstemp
from os import close
try:
    from StringIO import StringIO
except:
    from io import StringIO

import numpy as np
import numpy.testing as npt

from emperor.parse import parse_coords


class ParseTests(TestCase):

    def test_parse_coords_ordination_results(self):
        """parse_coords should handle skbio's OrdinationResults file"""
        coords = StringIO(ordination_results_file)

        obs = parse_coords(coords)
        exp = (['A', 'B', 'C'],
               np.array([[.11, .09, .23], [.03, .07, -.26], [.12, .06, -.32]]),
               np.array([4.94, 1.79, 1.50]),
               np.array([14.3, 5.2, 4.3]))
        # test the header and the values apart from each other
        self.assertEqual(obs[0], exp[0])
        npt.assert_almost_equal(obs[1], exp[1])
        npt.assert_almost_equal(obs[2], exp[2])
        npt.assert_almost_equal(obs[3], exp[3])

    def test_parse_coords_qiime(self):
        """parse_coords should handle old qiime PCoA coords format"""
        coords = StringIO(qiime_pcoa_file)
        obs = parse_coords(coords)
        exp = (['A', 'B', 'C'],
               np.array([[.11, .09, .23], [.03, .07, -.26], [.12, .06, -.32]]),
               np.array([4.94, 1.79, 1.50]),
               np.array([14.3, 5.2, 4.3]))
        # test the header and the values apart from each other
        self.assertEqual(obs[0], exp[0])
        npt.assert_almost_equal(obs[1], exp[1])
        npt.assert_almost_equal(obs[2], exp[2])
        npt.assert_almost_equal(obs[3], exp[3])

    def test_parse_coords_qiime_file(self):
        """parse_coords should handle old qiime PCoA coords file"""
        fd, fp = mkstemp()
        close(fd)

        with open(fp, 'w') as f:
            f.write(qiime_pcoa_file)

        with open(fp, 'r') as f:
            obs = parse_coords(f)

        exp = (['A', 'B', 'C'],
               np.array([[.11, .09, .23], [.03, .07, -.26], [.12, .06, -.32]]),
               np.array([4.94, 1.79, 1.50]),
               np.array([14.3, 5.2, 4.3]))
        # test the header and the values apart from each other
        self.assertEqual(obs[0], exp[0])
        npt.assert_almost_equal(obs[1], exp[1])
        npt.assert_almost_equal(obs[2], exp[2])
        npt.assert_almost_equal(obs[3], exp[3])

ordination_results_file = u"""Eigvals\t3
4.94\t1.79\t1.50

Proportion explained\t3
14.3\t5.2\t4.3

Species\t0\t0

Site\t3\t3
A\t.11\t.09\t.23
B\t.03\t.07\t-.26
C\t.12\t.06\t-.32

Biplot\t0\t0

Site constraints\t0\t0"""

qiime_pcoa_file = """pc vector number\t1\t2\t3
A\t0.11\t0.09\t0.23
B\t0.03\t0.07\t-0.26
C\t0.12\t0.06\t-0.32


eigvals\t4.94\t1.79\t1.50
% variation explained\t14.3\t5.2\t4.3


"""

if __name__ == '__main__':
    main()
