#!/usr/bin/env python
#file test_make_3d_plots.py

__author__ = "Dan Knights"
__copyright__ = "Copyright 2011, The QIIME Project" #consider project name
__credits__ = ["Dan Knights"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from numpy import array, nan
from unittest import TestCase, main
from numpy.testing import assert_almost_equal
from emperor.qiime_backports.make_3d_plots import (get_custom_coords,
    remove_nans, scale_custom_coords)

class TopLevelTests(TestCase):
    """Tests of top-level functions"""

    def setUp(self):
        """define some top-level data"""
        self.coord_header=["Sample1","Sample2","Sample3"]
        self.coords=array([[-0.219044992,0.079674486,0.09233683],[-0.042258081,
                        0.000204041,0.024837603],[0.080504323,-0.212014503,
                        -0.088353435]])
        self.pct_var=array([25.00,30.00,35.00])
        self.mapping=[["Sample-ID","Day","Type"],["Sample1","Day1","Soil"],
                    ["Sample2","Day1","Soil"],["Sample3","Day1","Soil"]]
        self.mapping2=[["Sample-ID","Day","Type","Height","Weight"],
                        ["Sample1","Day1","Soil","10","60"],
                        ["Sample2","Day1","Soil","20","55"],
                        ["Sample3","Day1","Soil","30","50"]]

        self.prefs_vectors={}
        self.prefs_vectors['Sample']={}   
        self.prefs_vectors['Sample']['column']="Type"
        self.coords2 = array([[0, -0.219044992,0.079674486,0.09233683],
                              [1, -0.042258081, 0.000204041, 0.024837603],
                              [2, 0.080504323, -0.212014503, -0.088353435],
                              [3, 0.012345551, -0.124512513, -1142356135]])
        self.custom_axes = ['Height']
        self.add_vectors = {'vectors_algorithm': 'trajectory', 'vectors_axes': 3,\
                                'vectors': ['Height'], 'vectors_path': 'vectors_test',\
                                'eigvals': array([ 0, 2.44923871, 1.11678013, 1.01533255]),\
                                'vectors_output': {},\
                                'weight_by_vector' : False,\
                                'window_size': 1}
        self.filename_vectors = 'vectors_test'
        self.file_path_vectors = 'vectors_test_dir'

    def test_get_custom_coords(self):
        """get_custom_coords: Gets custom axis coords from the mapping file."""
        exp = 1
        custom_axes = ['Height','Weight']
        coords = [self.coord_header, self.coords]
        get_custom_coords(custom_axes, self.mapping2, coords)
        exp = array([[10,60,-0.219044992,0.079674486,0.09233683],
                           [20,55,-0.042258081, 0.000204041,0.024837603],
                           [30,50,0.080504323,-0.212014503,-0.088353435]])
        assert_almost_equal(coords[1],exp)

    def test_scale_custom_coords(self):
        """scale_custom_coords: \
        Scales custom coordinates to match min/max of PC1"""
        custom_axes = ['Height','Weight']
        coord_data = array([[10,60,-0.219044992,0.079674486,0.09233683],
                            [20,55,-0.042258081, 0.000204041,0.024837603],
                            [30,50,0.080504323,-0.212014503,-0.088353435]])
        coords = [self.coord_header, coord_data]
        scale_custom_coords(custom_axes,coords)
        # calculate results
        mn = coord_data[2,].min()
        mx = coord_data[2,].max()
        h = array([10.0,20.0,30.0])
        h = (h-min(h))/(max(h)-min(h))
        h = h * (mx-mn) + mn
        w = array([60.0,55.0,50.0])
        w = (w-min(w))/(max(w)-min(w))
        w = w * (mx-mn) + mn
        exp = array([[h[0],w[0],-0.219044992,0.079674486,0.09233683],
                            [h[1],w[1],-0.042258081, 0.000204041,0.024837603],
                            [h[2],w[2],0.080504323,-0.212014503,-0.088353435]])
        assert_almost_equal(coords[1],exp)

    def test_remove_nans(self):
        """remove_nans: Deletes any samples with NANs in their coordinates"""
        coord_data = array([[10,60,-0.219044992,0.079674486,0.09233683],
                            [20,55,-0.042258081, nan,0.024837603],
                            [30,50,0.080504323,-0.212014503,-0.088353435]])
        coords = [self.coord_header, coord_data]
        remove_nans(coords)

        exp_header = ["Sample1","Sample3"]
        exp_coords = array([[10,60,-0.219044992,0.079674486,0.09233683],
                            [30,50,0.080504323,-0.212014503,-0.088353435]])
        self.assertEqual(coords[0],exp_header)
        assert_almost_equal(coords[1],exp_coords)


#run tests if called from command line
if __name__ == "__main__":
    main()
