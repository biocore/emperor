#!/usr/bin/env python
# File created on 25 Jan 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from numpy import array
from emperor.format import format_pcoa_to_js, format_mapping_file_to_js
from cogent.util.unit_test import TestCase, main

class TopLevelTests(TestCase):

    def setUp(self):
        self.pcoa_pct_var = array([2.66887049e+01, 1.62563704e+01,
            1.37754129e+01, 1.12172158e+01, 1.00247750e+01, 8.22835130e+00,
            7.55971174e+00, 6.24945796e+00, 1.17437419e-14])
        self.pcoa_headers = ['PC.355','PC.607','PC.634','PC.635','PC.593',
            'PC.636','PC.481','PC.354','PC.356']
        self.pcoa_coords = PCOA_DATA
        self.pcoa_eigen_values = array([4.79412119e-01, 2.92014956e-01,
            2.47449246e-01, 2.01496072e-01, 1.80076128e-01, 1.47806773e-01,
            1.35795927e-01, 1.12259696e-01, 2.10954117e-16])

        # data specific for testing the jackknifing
        self.pcoa_jk_headers = ['PC.355','PC.607','PC.634','PC.635']
        self.pcoa_jk_coords = array([[0.3, 0.5, 0.1, 0.3],[1.1, 1.1, 1.0, 0.8],
            [0.1, 3.3, 5.5, 0.1], [1.0, 2.0, 1.0, 1.0]])
        self.pcoa_jk_eigen_values = array([0.45, 0.32, 0.21, 0.02])
        self.pcoa_jk_pct_var = array([44, 40, 15, 1])
        self.pcoa_jk_coords_low = array([[0.2, 0.3, 0.1, 0.3],[1.1, 0.1, 0.0, 0.3],
            [0.6, 3.1, 1.5, 0.1], [0.023, 1.0, 0.01, 1.0]])
        self.pcoa_jk_coords_high = array([[0.6, 0.8, 0.9, 0.31],[1, 2.1, 0.0, 0.8],
            [0.9, 3.7, 5.5, 0.1111], [0.01222, 2.0, 0.033, 2.0]])

        self.mapping_file_data = MAPPING_FILE_DATA
        self.mapping_file_headers = ['SampleID', 'BarcodeSequence',
            'LinkerPrimerSequence', 'Treatment', 'DOB', 'Description']
        self.good_columns = ['Treatment', 'LinkerPrimerSequence']

    def test_format_pcoa_to_js(self):
        """Test correct formatting of the PCoA file"""
        # test the case with only points and nothing else
        out_js_pcoa_string = format_pcoa_to_js(self.pcoa_headers,
            self.pcoa_coords, self.pcoa_eigen_values, self.pcoa_pct_var)
        self.assertEquals(out_js_pcoa_string, PCOA_JS)

        # test custom axes and the labels
        out_js_pcoa_string = format_pcoa_to_js(self.pcoa_headers,
            self.pcoa_coords, self.pcoa_eigen_values,
            self.pcoa_pct_var, custom_axes=['Instant'])
        self.assertEquals(out_js_pcoa_string, PCOA_JS_CUSTOM_AXES)

        # test jackknifed pcoa plots
        out_js_pcoa_string = format_pcoa_to_js(self.pcoa_jk_headers,
            self.pcoa_jk_coords, self.pcoa_jk_eigen_values,
            self.pcoa_jk_pct_var, coords_low=self.pcoa_jk_coords_low,
            coords_high=self.pcoa_jk_coords_high)
        self.assertEquals(out_js_pcoa_string, PCOA_JS_JACKKNIFED)

    def test_format_mapping_file_to_js(self):
        """Tests correct formatting of the metadata mapping file"""
        out_js_mapping_file_string = format_mapping_file_to_js(
            self.mapping_file_data, self.mapping_file_headers, self.good_columns)
        self.assertEquals(out_js_mapping_file_string, MAPPING_FILE_JS)



PCOA_DATA = array([[ -1.09166142e-01, 8.77774496e-02, 1.15866606e-02, -6.26863896e-02, 2.31533068e-02, 8.76934639e-02, 1.37400927e-03, -1.35496063e-05, 1.29849404e-09],
[6.88959784e-02, -1.66234067e-01, -9.98300962e-02, -2.90522450e-02, 5.05569953e-02, -2.95200038e-03, -3.25863204e-02, -2.17218431e-02, 1.29849404e-09],
[2.04684540e-01, 1.28911236e-01, -2.93614192e-02, 1.07657904e-01, 1.78480761e-02, 7.97778676e-03, -2.92003235e-02, -1.23468947e-03, 1.29849404e-09],
[1.26131510e-01, -2.66030272e-03, -1.41717093e-01, -9.71089687e-03, -6.94272590e-02, 3.67235068e-03, 4.29867599e-02, 6.44276242e-03, 1.29849404e-09],
[9.68466168e-02, -1.59388265e-01, 1.35271607e-01, 5.12015857e-02, -2.02552984e-02, 3.07034843e-02, 1.55159338e-02, 1.42426937e-02, 1.29849404e-09],
[2.81534642e-01, 7.10660196e-02, 9.71542020e-02, -8.06472757e-02, 7.04245456e-03, -4.53133767e-02, 6.55825124e-03, -1.26412251e-02, 1.29849404e-09],
[-1.92382819e-01, 1.47832029e-02, -1.47871039e-02, 1.90888050e-02, 7.26409669e-02, -3.73008815e-02, 3.94304860e-02, 3.25351917e-02, 1.29849404e-09],
[-2.93353176e-01, 1.83956004e-02, 3.29884266e-02, 3.15360631e-02, -2.86943531e-02, -1.94225139e-02, 8.06272805e-03, -5.58094095e-02, 1.29849404e-09],
[-1.83191151e-01, 34912621e-03, 8.69481594e-03, -2.73875510e-02, -5.28648893e-02, -2.50583131e-02, -5.21415245e-02, 3.82000689e-02, 1.29849404e-09]])

PCOA_JS = """
var g_spherePositions = new Array();
g_spherePositions['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x': -0.109166, 'y': 0.087777, 'z': 0.011587 };
g_spherePositions['PC.607'] = { 'name': 'PC.607', 'color': 0, 'x': 0.068896, 'y': -0.166234, 'z': -0.099830 };
g_spherePositions['PC.634'] = { 'name': 'PC.634', 'color': 0, 'x': 0.204685, 'y': 0.128911, 'z': -0.029361 };
g_spherePositions['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x': 0.126132, 'y': -0.002660, 'z': -0.141717 };
g_spherePositions['PC.593'] = { 'name': 'PC.593', 'color': 0, 'x': 0.096847, 'y': -0.159388, 'z': 0.135272 };
g_spherePositions['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x': 0.281535, 'y': 0.071066, 'z': 0.097154 };
g_spherePositions['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x': -0.192383, 'y': 0.014783, 'z': -0.014787 };
g_spherePositions['PC.354'] = { 'name': 'PC.354', 'color': 0, 'x': -0.293353, 'y': 0.018396, 'z': 0.032988 };
g_spherePositions['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x': -0.183191, 'y': 34912.621000, 'z': 0.008695 };

var g_ellipsesDimensions = new Array();
var g_segments = 16, g_rings = 16, g_radius = 0.011498;
var g_xAxisLength = 0.574888;
var g_yAxisLength = 34912.787234;
var g_zAxisLength = 0.276989;
var g_xMaximumValue = 0.281535;
var g_yMaximumValue = 34912.621000;
var g_zMaximumValue = 0.135272;
var g_xMinimumValue = -0.293353;
var g_yMinimumValue = -0.166234;
var g_zMinimumValue = -0.141717;
var g_maximum = 34912.621000;
g_pc1Label = "PC1 (27 %)";
g_pc2Label = "PC2 (16 %)";
g_pc3Label = "PC3 (14 %)";
var g_fractionExplained = [0.266887, 0.162564, 0.137754, 0.112172, 0.100248, 0.082284, 0.075597, 0.062495, 0.000000];
"""

PCOA_JS_CUSTOM_AXES = """
var g_spherePositions = new Array();
g_spherePositions[\'PC.355\'] = { \'name\': \'PC.355\', \'color\': 0, \'x\': -0.109166, \'y\': 0.087777, \'z\': 0.011587 };
g_spherePositions[\'PC.607\'] = { \'name\': \'PC.607\', \'color\': 0, \'x\': 0.068896, \'y\': -0.166234, \'z\': -0.099830 };
g_spherePositions[\'PC.634\'] = { \'name\': \'PC.634\', \'color\': 0, \'x\': 0.204685, \'y\': 0.128911, \'z\': -0.029361 };
g_spherePositions[\'PC.635\'] = { \'name\': \'PC.635\', \'color\': 0, \'x\': 0.126132, \'y\': -0.002660, \'z\': -0.141717 };
g_spherePositions[\'PC.593\'] = { \'name\': \'PC.593\', \'color\': 0, \'x\': 0.096847, \'y\': -0.159388, \'z\': 0.135272 };
g_spherePositions[\'PC.636\'] = { \'name\': \'PC.636\', \'color\': 0, \'x\': 0.281535, \'y\': 0.071066, \'z\': 0.097154 };
g_spherePositions[\'PC.481\'] = { \'name\': \'PC.481\', \'color\': 0, \'x\': -0.192383, \'y\': 0.014783, \'z\': -0.014787 };
g_spherePositions[\'PC.354\'] = { \'name\': \'PC.354\', \'color\': 0, \'x\': -0.293353, \'y\': 0.018396, \'z\': 0.032988 };
g_spherePositions[\'PC.356\'] = { \'name\': \'PC.356\', \'color\': 0, \'x\': -0.183191, \'y\': 34912.621000, \'z\': 0.008695 };

var g_ellipsesDimensions = new Array();
var g_segments = 16, g_rings = 16, g_radius = 0.011498;
var g_xAxisLength = 0.574888;
var g_yAxisLength = 34912.787234;
var g_zAxisLength = 0.276989;
var g_xMaximumValue = 0.281535;
var g_yMaximumValue = 34912.621000;
var g_zMaximumValue = 0.135272;
var g_xMinimumValue = -0.293353;
var g_yMinimumValue = -0.166234;
var g_zMinimumValue = -0.141717;
var g_maximum = 34912.621000;
g_pc1Label = "Instant";
g_pc2Label = "PC1 (27 %)";
g_pc3Label = "PC2 (16 %)";
var g_fractionExplained = [0.266887, 0.266887, 0.162564, 0.137754, 0.112172, 0.100248, 0.082284, 0.075597, 0.062495, 0.000000];
"""

PCOA_JS_JACKKNIFED = """
var g_spherePositions = new Array();
g_spherePositions[\'PC.355\'] = { \'name\': \'PC.355\', \'color\': 0, \'x\': 0.300000, \'y\': 0.500000, \'z\': 0.100000 };
g_spherePositions[\'PC.607\'] = { \'name\': \'PC.607\', \'color\': 0, \'x\': 1.100000, \'y\': 1.100000, \'z\': 1.000000 };
g_spherePositions[\'PC.634\'] = { \'name\': \'PC.634\', \'color\': 0, \'x\': 0.100000, \'y\': 3.300000, \'z\': 5.500000 };
g_spherePositions[\'PC.635\'] = { \'name\': \'PC.635\', \'color\': 0, \'x\': 1.000000, \'y\': 2.000000, \'z\': 1.000000 };

var g_ellipsesDimensions = new Array();
g_ellipsesDimensions[\'PC.355\'] = { \'name\': \'PC.355\', \'color\': 0, \'width\': 0.400000, \'height\': 0.500000, \'length\': 0.800000 , \'x\': 0.300000, \'y\': 0.500000, \'z\': 0.100000 }
g_ellipsesDimensions[\'PC.607\'] = { \'name\': \'PC.607\', \'color\': 0, \'width\': 0.100000, \'height\': 2.000000, \'length\': 0.000000 , \'x\': 1.100000, \'y\': 1.100000, \'z\': 1.000000 }
g_ellipsesDimensions[\'PC.634\'] = { \'name\': \'PC.634\', \'color\': 0, \'width\': 0.300000, \'height\': 0.600000, \'length\': 4.000000 , \'x\': 0.100000, \'y\': 3.300000, \'z\': 5.500000 }
g_ellipsesDimensions[\'PC.635\'] = { \'name\': \'PC.635\', \'color\': 0, \'width\': 0.010780, \'height\': 1.000000, \'length\': 0.023000 , \'x\': 1.000000, \'y\': 2.000000, \'z\': 1.000000 }
var g_segments = 16, g_rings = 16, g_radius = 0.020000;
var g_xAxisLength = 1.200000;
var g_yAxisLength = 3.800000;
var g_zAxisLength = 5.600000;
var g_xMaximumValue = 1.100000;
var g_yMaximumValue = 3.300000;
var g_zMaximumValue = 5.500000;
var g_xMinimumValue = 0.100000;
var g_yMinimumValue = 0.500000;
var g_zMinimumValue = 0.100000;
var g_maximum = 5.500000;
g_pc1Label = "PC1 (44 %)";
g_pc2Label = "PC2 (40 %)";
g_pc3Label = "PC3 (15 %)";
var g_fractionExplained = [0.440000, 0.400000, 0.150000, 0.010000];
"""

MAPPING_FILE_DATA = [\
    ['PC.354','AGCACGAGCCTA','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._354'],
    ['PC.355','AACTCGTCGATG','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._355'],
    ['PC.356','ACAGACCACTCA','YATGCTGCCTCCCGTAGGAGT','Control','20061126','Control_mouse_I.D._356'],
    ['PC.481','ACCAGCGACTAG','YATGCTGCCTCCCGTAGGAGT','Control','20070314','Control_mouse_I.D._481'],
    ['PC.593','AGCAGCACTTGT','YATGCTGCCTCCCGTAGGAGT','Control','20071210','Control_mouse_I.D._593'],
    ['PC.607','AACTGTGCGTAC','YATGCTGCCTCCCGTAGGAGT','Fast','20071112','Fasting_mouse_I.D._607'],
    ['PC.634','ACAGAGTCGGCT','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._634'],
    ['PC.635','ACCGCAGAGTCA','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._635'],
    ['PC.636','ACGGTGAGTGTC','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._636']]

MAPPING_FILE_JS = """var g_mappingFileHeaders = ['BarcodeSequence','LinkerPrimerSequence','Treatment','DOB','Description'];
var g_mappingFileData = { 'PC.481': ['ACCAGCGACTAG','YATGCTGCCTCCCGTAGGAGT','Control','20070314','Control_mouse_I.D._481'],'PC.607': ['AACTGTGCGTAC','YATGCTGCCTCCCGTAGGAGT','Fast','20071112','Fasting_mouse_I.D._607'],'PC.634': ['ACAGAGTCGGCT','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._634'],'PC.635': ['ACCGCAGAGTCA','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._635'],'PC.593': ['AGCAGCACTTGT','YATGCTGCCTCCCGTAGGAGT','Control','20071210','Control_mouse_I.D._593'],'PC.636': ['ACGGTGAGTGTC','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._636'],'PC.355': ['AACTCGTCGATG','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._355'],'PC.354': ['AGCACGAGCCTA','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._354'],'PC.356': ['ACAGACCACTCA','YATGCTGCCTCCCGTAGGAGT','Control','20061126','Control_mouse_I.D._356'] };
"""

if __name__ == "__main__":
    main()