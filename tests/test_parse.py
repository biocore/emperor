#!/usr/bin/env python

from __future__ import division

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.9.3-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from unittest import TestCase, main

import numpy as np
import numpy.testing as npt

from emperor.parse import parse_coords


class ParseTests(TestCase):

    def test_parse_coords(self):
        """parse_coords should handle skbio's OrdinationResults file"""
        coords = ordination_results_file.splitlines()

        obs = parse_coords(coords)
        exp = (['A', 'B', 'C'],
               np.array([[.11, .09, .23], [.03, .07, -.26], [.12, .06, -.32]]),
               np.array([4.94, 1.79, 1.50]),
               np.array([14.3, 5.2, 4.3]))
        # test the header and the values apart from each other
        self.assertEqual(obs[0], exp[0])
        npt.assert_almost_equal(obs[1], exp[1])

ordination_results_file = """Eigvals\t3
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

if __name__ == '__main__':
    main()
