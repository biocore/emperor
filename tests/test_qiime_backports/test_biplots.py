#!/usr/bin/env python
# File created on 1 Apr 2010
from __future__ import division

__author__ = "Justin Kuczynski"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Justin Kuczynski"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Justin Kuczynski"
__email__ = "justinak@gmail.com"
__status__ = "Development"

import emperor.qiime_backports.biplots as bp
import numpy as np

from os import system
from unittest import TestCase, main
from numpy.testing import assert_almost_equal, assert_array_almost_equal

class BiplotTests(TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_taxa_coords(self):
        otu_table = np.array([  [2,0,0,1],
                                [1,1,1,1],
                                [0,2,2,1]],float)
        sample_names = list('WXYZ')
        otu_names = list('abc')
    
        res = bp.get_taxa_coords(otu_table, [.4,.2,.1,.9])
        otu_coords= list(range(3))
        otu_coords[0] = .4*2/3 + .9*1/3
        otu_coords[1] = .4*1/4 + .2*1/4 + .1*1/4 + .9*1/4
        otu_coords[2] = .4*0/5 + .2*2/5 + .1*2/5 + .9*1/5
        assert_almost_equal(res, otu_coords)
    
    def test_get_taxa_prevalence(self):
        otu_table = np.array([  [2,0,0,1],
                                [1,1,1,1],
                                [0,0,0,0]],float)
        sample_weights = [3,1,1,2]
        res = bp.get_taxa_prevalence(otu_table)
        # print res
        # self.assertFloatEqual(res, np.array([(2/3) + 1/2, 1/3+1+1+1/2, 0])/4) 
        assert_almost_equal(res, np.array([(2/3) + 1/2, 1/3+1+1+1/2, 0])/4\
            * 4/(2.5+1/3))                    
        otu_table = np.array([  [2,0,0,1],
                                [1,1,1,1],
                                [0,2,2,1]],float)
        res = bp.get_taxa_prevalence(otu_table)
        # print res
        # self.assertFloatEqual(res, np.array([3,4,5])/12) # if no normalize
        assert_almost_equal(res, [0,.5,1])


    def test_make_biplot_scores_output(self):
        """make_biplot_scores_output correctly formats biplot scores"""
        taxa = {}
        taxa['lineages'] = list('ABC')
        taxa['coord'] = np.array([  [2.1,0.2,0.2,1.4],
                                 [1.1,1.2,1.3,1.5],
                                 [-.3,-2,2.5,1.9]],float)
        res = bp.make_biplot_scores_output(taxa)
        exp = ['#Taxon\tpc1\tpc2\tpc3\tpc4',
               'A\t2.1\t0.2\t0.2\t1.4',
               'B\t1.1\t1.2\t1.3\t1.5',
               'C\t-0.3\t-2.0\t2.5\t1.9',
              ]
        self.assertEqual(res, exp)


if __name__ == "__main__":
    main()
