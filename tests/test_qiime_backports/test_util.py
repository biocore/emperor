#!/usr/bin/env python
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME Project"
#remember to add yourself if you make changes
__credits__ = ["Rob Knight", "Daniel McDonald", "Greg Caporaso", 
               "Justin Kuczynski", "Catherine Lozupone",
               "Jai Ram Rideout", "Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"


from unittest import TestCase, main

from numpy.testing import assert_almost_equal
from numpy import array, isnan, asarray, arange

from scipy.spatial import procrustes

from emperor.qiime_backports.util import (summarize_pcoas, _flip_vectors,
                                          _compute_jn_pcoa_avg_ranges,
                                          matrix_IQR, idealfourths, IQR)


class TopLevelTests(TestCase):
    def setup(self):
        pass


    def test_flip_vectors(self):
        """_flip_vectors makes a new PCA matrix with correct signs"""
        m_matrix = array([[1.0, 0.0, 1.0], [2.0, 4.0, 4.0]])
        jn_matrix = array([[1.2, 0.1, -1.2], [2.5, 4.0, -4.5]])
        new_matrix = _flip_vectors(jn_matrix, m_matrix)
        assert_almost_equal(new_matrix, array([[1.2, 0.1, 1.2], [2.5, 4.0, 4.5]]))

    def test_compute_jn_pcoa_avg_ranges(self):
        """_compute_jn_pcoa_avg_ranges works
        """
        jn_flipped_matrices = [array([[2.0,4.0, -4.5],[-1.2,-0.1,1.2]]),\
                array([[3.0,4.0, -4.5],[-1.2,-0.1,1.2]]),\
                array([[4.0,4.0, -4.5],[-1.2,-0.1,1.2]]),\
                array([[5.0,4.0, -4.5],[-1.2,-0.1,1.2]]),\
                array([[6.0,4.0, -4.5],[-1.2,-0.1,1.2]]),\
                array([[7.0,4.0, -4.5],[-1.2,-0.1,1.2]]),\
                array([[1.0,4.0, -4.5],[-1.2,-0.1,1.2]])]
        avg_matrix, low_matrix, high_matrix = _compute_jn_pcoa_avg_ranges(\
                jn_flipped_matrices, 'ideal_fourths')
        assert_almost_equal(avg_matrix[(0,0)], 4.0)
        assert_almost_equal(avg_matrix[(0,2)], -4.5)
        assert_almost_equal(low_matrix[(0,0)], 2.16666667)
        assert_almost_equal(high_matrix[(0,0)], 5.83333333)

        avg_matrix, low_matrix, high_matrix = _compute_jn_pcoa_avg_ranges(\
                jn_flipped_matrices, 'sdev')
        x = array([m[0,0] for m in jn_flipped_matrices])
        self.assertEqual(x.mean(),avg_matrix[0,0])
        self.assertEqual(-x.std(ddof=1)/2,low_matrix[0,0])
        self.assertEqual(x.std(ddof=1)/2,high_matrix[0,0])
        
    def test_summarize_pcoas(self):
        """summarize_pcoas works
        """
        master_pcoa = [['1', '2', '3'], \
            array([[-1.0, 0.0, 1.0], [2.0, 4.0, -4.0]]), \
            array([.76, .24])]
        jn1 = [['1', '2', '3'], \
            array([[1.2, 0.1, -1.2],[-2.5, -4.0, 4.5]]), \
            array([0.80, .20])]
        jn2 = [['1', '2', '3'], \
            array([[-1.4, 0.05, 1.3],[2.6, 4.1, -4.7]]), \
            array([0.76, .24])]
        jn3 = [['1', '2', '3'], \
            array([[-1.5, 0.05, 1.6],[2.4, 4.0, -4.8]]), \
            array([0.84, .16])]
        jn4 = [['1', '2', '3'], \
            array([[-1.5, 0.05, 1.6],[2.4, 4.0, -4.8]]), \
            array([0.84, .16])]
        support_pcoas = [jn1, jn2, jn3, jn4]
        #test with the ideal_fourths option
        matrix_average, matrix_low, matrix_high, eigval_average, m_names = \
            summarize_pcoas(master_pcoa, support_pcoas, 'ideal_fourths',
                            apply_procrustes=False)
        self.assertEqual(m_names, ['1', '2', '3'])
        assert_almost_equal(matrix_average[(0,0)], -1.4)
        assert_almost_equal(matrix_average[(0,1)], 0.0125)
        assert_almost_equal(matrix_low[(0,0)], -1.5)
        assert_almost_equal(matrix_high[(0,0)], -1.28333333)
        assert_almost_equal(matrix_low[(0,1)], -0.0375)
        assert_almost_equal(matrix_high[(0,1)], 0.05)
        assert_almost_equal(eigval_average[0], 0.81)
        assert_almost_equal(eigval_average[1], 0.19)
        #test with the IQR option
        matrix_average, matrix_low, matrix_high, eigval_average, m_names = \
            summarize_pcoas(master_pcoa, support_pcoas, method='IQR',
                            apply_procrustes=False)
        assert_almost_equal(matrix_low[(0,0)], -1.5)
        assert_almost_equal(matrix_high[(0,0)], -1.3)

        #test with procrustes option followed by sdev
        m, m1, msq = procrustes(master_pcoa[1],jn1[1])
        m, m2, msq = procrustes(master_pcoa[1],jn2[1])
        m, m3, msq = procrustes(master_pcoa[1],jn3[1])
        m, m4, msq = procrustes(master_pcoa[1],jn4[1])
        matrix_average, matrix_low, matrix_high, eigval_average, m_names = \
            summarize_pcoas(master_pcoa, support_pcoas, method='sdev',
                            apply_procrustes=True)

        x = array([m1[0,0],m2[0,0],m3[0,0],m4[0,0]])
        self.assertEqual(x.mean(),matrix_average[0,0])
        self.assertEqual(-x.std(ddof=1)/2,matrix_low[0,0])
        self.assertEqual(x.std(ddof=1)/2,matrix_high[0,0])

    def test_IQR(self):
        "IQR returns the interquartile range for list x"
        #works for odd with odd split
        x = [2,3,4,5,6,7,1]
        minv, maxv = IQR(x)
        self.assertEqual(minv, 2)
        self.assertEqual(maxv, 6)
        #works for even with odd split
        x = [1,2,3,4,5,6]
        minv, maxv = IQR(x)
        self.assertEqual(minv, 2)
        self.assertEqual(maxv, 5)
        #works for even with even split
        x = [1,2,3,4,5,6,7,8]
        minv, maxv = IQR(x)
        self.assertEqual(minv, 2.5)
        self.assertEqual(maxv, 6.5)
        #works with array
        #works for odd with odd split
        x = array([2,3,4,5,6,7,1])
        minv, maxv = IQR(x)
        self.assertEqual(minv, 2)
        self.assertEqual(maxv, 6)
        #works for even with odd split
        x = array([1,2,3,4,5,6])
        minv, maxv = IQR(x)
        self.assertEqual(minv, 2)
        self.assertEqual(maxv, 5)
        #works for even with even split
        x = array([1,2,3,4,5,6,7,8])
        minv, maxv = IQR(x)
        self.assertEqual(minv, 2.5)
        self.assertEqual(maxv, 6.5)
        
    def test_matrix_IQR(self):
        """matrix_IQR calcs the IQR for each column in an array correctly
        """
        x = array([[1,2,3],[4,5,6],[7,8,9], [10,11,12]])
        min_vals, max_vals = matrix_IQR(x)
        assert_almost_equal(min_vals, array([2.5,3.5,4.5]))
        assert_almost_equal(max_vals, array([8.5,9.5,10.5]))

    def test_idealfourths(self):
        """idealfourths: tests the ideal-fourths function which was imported from scipy
        at the following location (http://projects.scipy.org/scipy/browser/trunk/scipy/stats/tests/test_mmorestats.py?rev=4154)
        """
        test = arange(100)
        self.assertEqual(idealfourths(test),
                            [24.416666666666668, 74.583333333333343])
        test_2D = test.repeat(3).reshape(-1,3)
        
        # used to be assertAlmostEqualRel but assert_almost_equal from numpy
        # seems to be working just fine
        assert_almost_equal(asarray(idealfourths(test_2D, axis=0)),\
                    array([[24.41666667, 24.41666667, 24.41666667], \
                                 [74.58333333, 74.58333333, 74.58333333]]))
        
        assert_almost_equal(idealfourths(test_2D, axis=1),
                            test.repeat(2).reshape(-1,2))
        test = [0,0]
        _result = idealfourths(test)
        self.assertEqual(isnan(_result).all(), True)


#run unit tests if run from command-line
if __name__ == '__main__':
    main()
