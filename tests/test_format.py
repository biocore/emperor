#!/usr/bin/env python
# File created on 25 Jan 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "0.9.4"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Release"


from numpy import array
from emperor.format import (format_pcoa_to_js, format_mapping_file_to_js,
    format_taxa_to_js, format_vectors_to_js, format_emperor_html_footer_string,
    EmperorLogicError, format_comparison_bars_to_js, format_emperor_autograph)
from unittest import TestCase, main

class TopLevelTests(TestCase):

    def setUp(self):
        self.pcoa_pct_var = array([2.66887049e+01, 1.62563704e+01,
            1.37754129e+01, 1.12172158e+01, 1.00247750e+01, 8.22835130e+00,
            7.55971174e+00, 6.24945796e+00, 1.17437419e-14])
        self.pcoa_pct_var_really_low = array([2.66887049e+01, 1.62563704e+01,
            0.001, 0.0001, 0.0019, 0.0018, 0.0017, 0.0016, 0.0015])
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
        self.columns_with_gradients = ['Treatment', 'LinkerPrimerSequence',
                                       'DOB']

        self.otu_coords = array([[2.80399118e-01, -6.01282860e-03,
            2.34854344e-02, -4.68109475e-02, -1.46624450e-01, 5.66979125e-03,
            -3.54299634e-02, -2.55785794e-01, -4.84141987e-09], [2.28820400e-01,
            -1.30142097e-01, -2.87149448e-01, 8.64498846e-02, 4.42951919e-02,
            2.06042607e-01, 3.10003571e-02, 7.19920437e-02, -4.84141987e-09],
            [-9.13299284e-02, 4.24147148e-01, -1.35627421e-01, -5.75194809e-02,
            1.51363491e-01, -2.53935676e-02, 5.17306152e-02, -3.87382176e-02,
            -4.84141987e-09], [-2.76542164e-01, -1.44964375e-01, 6.66467344e-02,
            -6.77109454e-02, 1.76070270e-01, 7.29693901e-02, -2.29889464e-01,
            -4.65989417e-02,-4.84141987e-09]])
        self.lineages = ['Root;k__Bacteria;p__Firmicutes',
            'Root;k__Bacteria;p__Bacteroidetes',
            'Root;k__Bacteria;p__Tenericutes', 'Root;k__Bacteria;Other']
        self.prevalence = array([ 1., 0.66471926, 0.08193196, 0.04374296])

        # comparison test
        self.comparison_coords_data = array([[-0.0677, -2.036, 0.2726, 1.051,
            -0.180, -0.698], [-1.782, -0.972, 0.1582, -1.091, 0.531, 0.292],
            [-0.659, -0.2566, 0.514, -2.698, -0.393, 0.420], [-1.179, -0.968,
            2.525, 0.53, -0.529, 0.632],[-0.896, -1.765, 0.274, -0.3235, 0.4009,
            -0.03497], [-0.0923, 1.414, -0.622, 0.298, 0.5, -0.4580], [-0.972,
            0.551, 1.144, 0.3147, -0.476, -0.4279], [1.438, -2.603, -1.39,
            1.300, -0.1606, 1.260], [-0.356, 0.0875, 0.772, 0.539, -0.586,
            -1.431], [1.512, -1.239, -0.0365, -0.682, -0.971, 0.356],
            [1.17, 1.31, -1.407, 1.6, 0.60, 2.26], [2.618, 0.739, -0.01295,
            -0.937, 3.079, -2.534], [0.2339, -0.880, -1.753, 0.177, 0.3517,
            -0.743], [0.436, 2.12, -0.935, -0.476, -0.805, 0.4164], [-0.880,
            1.069, 1.069, -0.596, -0.199, 0.306], [0.294, 0.2988, 0.04670,
            -0.3865, 0.460, -0.431], [1.640, 0.2485, -0.354, 1.43, 1.226,
            1.095], [0.821, -1.13, -1.794, -1.171, -1.27, -0.842]])
        self.comparison_coords_headers = ['sampa_0', 'sampb_0', 'sampc_0',
            'sampd_0', 'sampe_0', 'sampf_0', 'sampa_1', 'sampb_1', 'sampc_1',
            'sampd_1', 'sampe_1', 'sampf_1', 'sampa_2', 'sampb_2', 'sampc_2',
            'sampd_2', 'sampe_2', 'sampf_2']
        self.comparison_coords_headers_zero = ['sampa0_0', 'sampb0_0', 'sampc0_0',
            'sampd00_0', 'sampe00_0', 'sampf00_0', 'sampa0_1', 'sampb0_1', 'sampc0_1',
            'sampd00_1', 'sampe00_1', 'sampf00_1', 'sampa0_2', 'sampb0_2', 'sampc0_2',
            'sampd00_2', 'sampe00_2', 'sampf00_2']

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

        # check it raises an exception when the variation explained on the
        # axes is not greater than 0.01 for at least three of them
        self.assertRaises(EmperorLogicError, format_pcoa_to_js,
            self.pcoa_headers, self.pcoa_coords, self.pcoa_eigen_values,
            self.pcoa_pct_var_really_low)
            
        # test segments
        out_js_pcoa_string = format_pcoa_to_js(self.pcoa_jk_headers,
            self.pcoa_jk_coords, self.pcoa_jk_eigen_values,
            self.pcoa_jk_pct_var, coords_low=self.pcoa_jk_coords_low,
            coords_high=self.pcoa_jk_coords_high, number_of_segments=14)
        self.assertEquals(out_js_pcoa_string, PCOA_JS_SEGMENTS)


    def test_format_mapping_file_to_js(self):
        """Tests correct formatting of the metadata mapping file"""

        # regular case, no categories that can be animated
        out_js_mapping_file_string = format_mapping_file_to_js(
            self.mapping_file_data, self.mapping_file_headers,
            self.good_columns)
        self.assertEquals(out_js_mapping_file_string, MAPPING_FILE_JS)

        # case with categories that can be animated i. e. that work as gradients
        out_js_mapping_file_string = format_mapping_file_to_js(
            self.mapping_file_data, self.mapping_file_headers,
            self.columns_with_gradients)
        self.assertEquals(out_js_mapping_file_string,
                          MAPPING_FILE_JS_WITH_ANIMATABLE_CATEGORIES)


    def test_format_taxa_to_js(self):
        """Tests correct formatting of the taxa"""
        out_js_taxa_string = format_taxa_to_js(self.otu_coords, self.lineages,
            self.prevalence)
        self.assertEquals(out_js_taxa_string, TAXA_JS_STRING)

        # case with empty data
        out_js_taxa_string = format_taxa_to_js([], [], [])
        self.assertEquals(out_js_taxa_string, "\nvar g_taxaPositions = "
            "new Array();\n\n")

    def test_format_vectors_to_js(self):
        """Tests correct formatting of the vectors from the coords"""

        # test that only the variable declaration gets returned
        out_js_vector_string = format_vectors_to_js(self.mapping_file_data,
            self.mapping_file_headers, self.pcoa_coords, self.pcoa_headers,
            None, None)
        self.assertEquals(out_js_vector_string, '\nvar g_vectorPositions = new '
            'Array();\n')

        # vector string without sorting for the coordinates
        out_js_vector_string = format_vectors_to_js(self.mapping_file_data,
            self.mapping_file_headers, self.pcoa_coords, self.pcoa_headers,
            'Treatment', None)
        self.assertEquals(out_js_vector_string, VECTOR_JS_STRING_NO_SORTING)

        # vector string sorting by the DOB category
        out_js_vector_string = format_vectors_to_js(self.mapping_file_data,
            self.mapping_file_headers, self.pcoa_coords, self.pcoa_headers,
            'Treatment', 'DOB')
        self.assertEquals(out_js_vector_string, VECTOR_JS_STRING_SORTING)

    def test_format_comparison_bars_to_js(self):
        """Check the correct strings are created for the two types of inputs"""

        # empty string generation for comparison i. e. no clones
        out_js_comparison_string = format_comparison_bars_to_js(
            self.comparison_coords_data, self.comparison_coords_headers, 0,
            True)
        self.assertEquals(out_js_comparison_string, '\nvar '
            'g_comparisonPositions = new Array();\nvar g_isSerialComparisonPlot'
            ' = true;\n')

        out_js_comparison_string = format_comparison_bars_to_js(
            self.comparison_coords_data, self.comparison_coords_headers, 3,
            True)
        self.assertEquals(out_js_comparison_string, COMPARISON_JS_STRING)

        # empty string generation for comparison i. e. no clones
        out_js_comparison_string = format_comparison_bars_to_js(
            self.comparison_coords_data, self.comparison_coords_headers, 0,
            False)
        self.assertEquals(out_js_comparison_string, '\nvar '
            'g_comparisonPositions = new Array();\nvar g_isSerialComparisonPlot'
            ' = false;\n')

        out_js_comparison_string = format_comparison_bars_to_js(
            self.comparison_coords_data, self.comparison_coords_headers, 3,
            False)
        self.assertEquals(out_js_comparison_string,
            COMPARISON_JS_STRING_NON_SERIAL)
            
        out_js_comparison_string = format_comparison_bars_to_js(
            self.comparison_coords_data, self.comparison_coords_headers_zero, 3,
            False)
        self.assertEquals(out_js_comparison_string, COMPARISON_COORDS_HEADERS_ZERO)         

    def test_format_comparison_bars_to_js_exceptions(self):
        """Check the correct exceptions are raised for incorrect inputs"""

        # assertion for wrong length in headers
        self.assertRaises(AssertionError, format_comparison_bars_to_js, [],
            self.comparison_coords_data, 3)

        # assertion for wrong length in coords data
        self.assertRaises(AssertionError, format_comparison_bars_to_js,
            self.comparison_coords_headers, self.comparison_coords_data[1::], 3)

        # assertion for wrong number of clones and elements
        self.assertRaises(AssertionError, format_comparison_bars_to_js,
            self.comparison_coords_headers, self.comparison_coords_data, 11)

    def test_format_emperor_html_footer_string(self):
        """Test correct formatting of the footer string"""
        # footer for a jackknifed pcoa plot without biplots
        out_string = format_emperor_html_footer_string(False, True)
        self.assertEqual(out_string, EXPECTED_FOOTER_A)

        # footer for biplots without jackknifing
        out_string = format_emperor_html_footer_string(True, False)
        self.assertEqual(out_string, EXPECTED_FOOTER_B)

        # no biplots nor jackknifing
        out_string = format_emperor_html_footer_string(False, False)
        self.assertEqual(out_string, EXPECTED_FOOTER_C)

        #  no biplots no jackknifing but with vectors
        out_string = format_emperor_html_footer_string(False, False, True)
        self.assertEqual(out_string, EXPECTED_FOOTER_D)

        # comparison plot
        out_string = format_emperor_html_footer_string(False, False, False,True)
        self.assertEqual(out_string, EXPECTED_FOOTER_E)

    def test_format_emperor_autograph(self):
        """Test signatures are created correctly for each of language"""

        autograph = format_emperor_autograph('mapping_file.txt',
            'pcoa_unweighted_unifrac.txt')

        # check for comment open and comment close
        self.assertTrue('<!--' in autograph)
        self.assertTrue('-->' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("QIIME Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
            'pcoa_unweighted_unifrac.txt','Python')
        # check for comment open and comment close
        self.assertTrue('"""' in autograph)
        self.assertTrue('"""' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("QIIME Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
            'pcoa_unweighted_unifrac.txt','C')
        # check for comment open and comment close
        self.assertTrue('/*' in autograph)
        self.assertTrue('*/' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("QIIME Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
            'pcoa_unweighted_unifrac.txt','Bash')
        # check for comment open and comment close
        self.assertTrue('<<COMMENT' in autograph)
        self.assertTrue('COMMENT' in autograph)
        # check for fields since we cannot check for the specifics
        self.assertTrue("*Summary of Emperor's Information*" in autograph)
        self.assertTrue('Metadata:' in autograph)
        self.assertTrue('Coordinates:' in autograph)
        self.assertTrue('HostName:' in autograph)
        self.assertTrue("Command:" in autograph)
        self.assertTrue("Emperor Version: " in autograph)
        self.assertTrue("QIIME Version: " in autograph)
        self.assertTrue("Command executed on " in autograph)

        # haskell and cobol are ... not supported
        self.assertRaises(AssertionError, format_emperor_autograph,
            'mapping_file.txt', 'pcoa.txt', 'Haskell')
        self.assertRaises(AssertionError, format_emperor_autograph,
            'mapping_file.txt', 'pcoa.txt', 'Cobol')
        

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
g_spherePositions['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x': -0.109166, 'y': 0.087777, 'z': 0.011587, 'P1': -0.109166, 'P2': 0.087777, 'P3': 0.011587, 'P4': -0.062686, 'P5': 0.023153, 'P6': 0.087693, 'P7': 0.001374, 'P8': -0.000014 };
g_spherePositions['PC.607'] = { 'name': 'PC.607', 'color': 0, 'x': 0.068896, 'y': -0.166234, 'z': -0.099830, 'P1': 0.068896, 'P2': -0.166234, 'P3': -0.099830, 'P4': -0.029052, 'P5': 0.050557, 'P6': -0.002952, 'P7': -0.032586, 'P8': -0.021722 };
g_spherePositions['PC.634'] = { 'name': 'PC.634', 'color': 0, 'x': 0.204685, 'y': 0.128911, 'z': -0.029361, 'P1': 0.204685, 'P2': 0.128911, 'P3': -0.029361, 'P4': 0.107658, 'P5': 0.017848, 'P6': 0.007978, 'P7': -0.029200, 'P8': -0.001235 };
g_spherePositions['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x': 0.126132, 'y': -0.002660, 'z': -0.141717, 'P1': 0.126132, 'P2': -0.002660, 'P3': -0.141717, 'P4': -0.009711, 'P5': -0.069427, 'P6': 0.003672, 'P7': 0.042987, 'P8': 0.006443 };
g_spherePositions['PC.593'] = { 'name': 'PC.593', 'color': 0, 'x': 0.096847, 'y': -0.159388, 'z': 0.135272, 'P1': 0.096847, 'P2': -0.159388, 'P3': 0.135272, 'P4': 0.051202, 'P5': -0.020255, 'P6': 0.030703, 'P7': 0.015516, 'P8': 0.014243 };
g_spherePositions['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x': 0.281535, 'y': 0.071066, 'z': 0.097154, 'P1': 0.281535, 'P2': 0.071066, 'P3': 0.097154, 'P4': -0.080647, 'P5': 0.007042, 'P6': -0.045313, 'P7': 0.006558, 'P8': -0.012641 };
g_spherePositions['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x': -0.192383, 'y': 0.014783, 'z': -0.014787, 'P1': -0.192383, 'P2': 0.014783, 'P3': -0.014787, 'P4': 0.019089, 'P5': 0.072641, 'P6': -0.037301, 'P7': 0.039430, 'P8': 0.032535 };
g_spherePositions['PC.354'] = { 'name': 'PC.354', 'color': 0, 'x': -0.293353, 'y': 0.018396, 'z': 0.032988, 'P1': -0.293353, 'P2': 0.018396, 'P3': 0.032988, 'P4': 0.031536, 'P5': -0.028694, 'P6': -0.019423, 'P7': 0.008063, 'P8': -0.055809 };
g_spherePositions['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x': -0.183191, 'y': 34912.621000, 'z': 0.008695, 'P1': -0.183191, 'P2': 34912.621000, 'P3': 0.008695, 'P4': -0.027388, 'P5': -0.052865, 'P6': -0.025058, 'P7': -0.052142, 'P8': 0.038200 };

var g_ellipsesDimensions = new Array();
var g_segments = 8, g_rings = 8, g_radius = 0.006899;
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
var g_pc1Label = "PC1 (26.69 %)";
var g_pc2Label = "PC2 (16.26 %)";
var g_pc3Label = "PC3 (13.78 %)";
var g_number_of_custom_axes = 0;
var g_fractionExplained = [0.266887, 0.162564, 0.137754, 0.112172, 0.100248, 0.082284, 0.075597, 0.062495];
var g_fractionExplainedRounded = [26.69, 16.26, 13.78, 11.22, 10.02, 8.23, 7.56, 6.25];
"""

PCOA_JS_CUSTOM_AXES = """
var g_spherePositions = new Array();
g_spherePositions['PC.355'] = { 'name': 'PC.355', 'color': 0, 'x': -0.109166, 'y': 0.087777, 'z': 0.011587, 'P1': -0.109166, 'P2': 0.087777, 'P3': 0.011587, 'P4': -0.062686, 'P5': 0.023153, 'P6': 0.087693, 'P7': 0.001374, 'P8': -0.000014 };
g_spherePositions['PC.607'] = { 'name': 'PC.607', 'color': 0, 'x': 0.068896, 'y': -0.166234, 'z': -0.099830, 'P1': 0.068896, 'P2': -0.166234, 'P3': -0.099830, 'P4': -0.029052, 'P5': 0.050557, 'P6': -0.002952, 'P7': -0.032586, 'P8': -0.021722 };
g_spherePositions['PC.634'] = { 'name': 'PC.634', 'color': 0, 'x': 0.204685, 'y': 0.128911, 'z': -0.029361, 'P1': 0.204685, 'P2': 0.128911, 'P3': -0.029361, 'P4': 0.107658, 'P5': 0.017848, 'P6': 0.007978, 'P7': -0.029200, 'P8': -0.001235 };
g_spherePositions['PC.635'] = { 'name': 'PC.635', 'color': 0, 'x': 0.126132, 'y': -0.002660, 'z': -0.141717, 'P1': 0.126132, 'P2': -0.002660, 'P3': -0.141717, 'P4': -0.009711, 'P5': -0.069427, 'P6': 0.003672, 'P7': 0.042987, 'P8': 0.006443 };
g_spherePositions['PC.593'] = { 'name': 'PC.593', 'color': 0, 'x': 0.096847, 'y': -0.159388, 'z': 0.135272, 'P1': 0.096847, 'P2': -0.159388, 'P3': 0.135272, 'P4': 0.051202, 'P5': -0.020255, 'P6': 0.030703, 'P7': 0.015516, 'P8': 0.014243 };
g_spherePositions['PC.636'] = { 'name': 'PC.636', 'color': 0, 'x': 0.281535, 'y': 0.071066, 'z': 0.097154, 'P1': 0.281535, 'P2': 0.071066, 'P3': 0.097154, 'P4': -0.080647, 'P5': 0.007042, 'P6': -0.045313, 'P7': 0.006558, 'P8': -0.012641 };
g_spherePositions['PC.481'] = { 'name': 'PC.481', 'color': 0, 'x': -0.192383, 'y': 0.014783, 'z': -0.014787, 'P1': -0.192383, 'P2': 0.014783, 'P3': -0.014787, 'P4': 0.019089, 'P5': 0.072641, 'P6': -0.037301, 'P7': 0.039430, 'P8': 0.032535 };
g_spherePositions['PC.354'] = { 'name': 'PC.354', 'color': 0, 'x': -0.293353, 'y': 0.018396, 'z': 0.032988, 'P1': -0.293353, 'P2': 0.018396, 'P3': 0.032988, 'P4': 0.031536, 'P5': -0.028694, 'P6': -0.019423, 'P7': 0.008063, 'P8': -0.055809 };
g_spherePositions['PC.356'] = { 'name': 'PC.356', 'color': 0, 'x': -0.183191, 'y': 34912.621000, 'z': 0.008695, 'P1': -0.183191, 'P2': 34912.621000, 'P3': 0.008695, 'P4': -0.027388, 'P5': -0.052865, 'P6': -0.025058, 'P7': -0.052142, 'P8': 0.038200 };

var g_ellipsesDimensions = new Array();
var g_segments = 8, g_rings = 8, g_radius = 0.006899;
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
var g_pc1Label = "Instant";
var g_pc2Label = "PC1 (26.69 %)";
var g_pc3Label = "PC2 (16.26 %)";
var g_number_of_custom_axes = 1;
var g_fractionExplained = [0.266887, 0.266887, 0.162564, 0.137754, 0.112172, 0.100248, 0.082284, 0.075597, 0.062495];
var g_fractionExplainedRounded = [26.69, 26.69, 16.26, 13.78, 11.22, 10.02, 8.23, 7.56, 6.25];
"""

PCOA_JS_JACKKNIFED = """
var g_spherePositions = new Array();
g_spherePositions[\'PC.355\'] = { \'name\': \'PC.355\', \'color\': 0, \'x\': 0.300000, \'y\': 0.500000, \'z\': 0.100000, \'P1\': 0.300000, \'P2\': 0.500000, \'P3\': 0.100000, \'P4\': 0.300000 };
g_spherePositions[\'PC.607\'] = { \'name\': \'PC.607\', \'color\': 0, \'x\': 1.100000, \'y\': 1.100000, \'z\': 1.000000, \'P1\': 1.100000, \'P2\': 1.100000, \'P3\': 1.000000, \'P4\': 0.800000 };
g_spherePositions[\'PC.634\'] = { \'name\': \'PC.634\', \'color\': 0, \'x\': 0.100000, \'y\': 3.300000, \'z\': 5.500000, \'P1\': 0.100000, \'P2\': 3.300000, \'P3\': 5.500000, \'P4\': 0.100000 };
g_spherePositions[\'PC.635\'] = { \'name\': \'PC.635\', \'color\': 0, \'x\': 1.000000, \'y\': 2.000000, \'z\': 1.000000, \'P1\': 1.000000, \'P2\': 2.000000, \'P3\': 1.000000, \'P4\': 1.000000 };

var g_ellipsesDimensions = new Array();
g_ellipsesDimensions[\'PC.355\'] = { \'name\': \'PC.355\', \'color\': 0, \'width\': 0.400000, \'height\': 0.500000, \'length\': 0.800000 , \'x\': 0.300000, \'y\': 0.500000, \'z\': 0.100000, \'P1\': 0.300000, \'P2\': 0.500000, \'P3\': 0.100000, \'P4\': 0.300000 }
g_ellipsesDimensions[\'PC.607\'] = { \'name\': \'PC.607\', \'color\': 0, \'width\': 0.100000, \'height\': 2.000000, \'length\': 0.000000 , \'x\': 1.100000, \'y\': 1.100000, \'z\': 1.000000, \'P1\': 1.100000, \'P2\': 1.100000, \'P3\': 1.000000, \'P4\': 0.800000 }
g_ellipsesDimensions[\'PC.634\'] = { \'name\': \'PC.634\', \'color\': 0, \'width\': 0.300000, \'height\': 0.600000, \'length\': 4.000000 , \'x\': 0.100000, \'y\': 3.300000, \'z\': 5.500000, \'P1\': 0.100000, \'P2\': 3.300000, \'P3\': 5.500000, \'P4\': 0.100000 }
g_ellipsesDimensions[\'PC.635\'] = { \'name\': \'PC.635\', \'color\': 0, \'width\': 0.010780, \'height\': 1.000000, \'length\': 0.023000 , \'x\': 1.000000, \'y\': 2.000000, \'z\': 1.000000, \'P1\': 1.000000, \'P2\': 2.000000, \'P3\': 1.000000, \'P4\': 1.000000 }
var g_segments = 8, g_rings = 8, g_radius = 0.012000;
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
var g_pc1Label = "PC1 (44.00 %)";
var g_pc2Label = "PC2 (40.00 %)";
var g_pc3Label = "PC3 (15.00 %)";
var g_number_of_custom_axes = 0;
var g_fractionExplained = [0.440000, 0.400000, 0.150000, 0.010000];
var g_fractionExplainedRounded = [44.00, 40.00, 15.00, 1.00];
"""

PCOA_JS_SEGMENTS = """
var g_spherePositions = new Array();
g_spherePositions[\'PC.355\'] = { \'name\': \'PC.355\', \'color\': 0, \'x\': 0.300000, \'y\': 0.500000, \'z\': 0.100000, \'P1\': 0.300000, \'P2\': 0.500000, \'P3\': 0.100000, \'P4\': 0.300000 };
g_spherePositions[\'PC.607\'] = { \'name\': \'PC.607\', \'color\': 0, \'x\': 1.100000, \'y\': 1.100000, \'z\': 1.000000, \'P1\': 1.100000, \'P2\': 1.100000, \'P3\': 1.000000, \'P4\': 0.800000 };
g_spherePositions[\'PC.634\'] = { \'name\': \'PC.634\', \'color\': 0, \'x\': 0.100000, \'y\': 3.300000, \'z\': 5.500000, \'P1\': 0.100000, \'P2\': 3.300000, \'P3\': 5.500000, \'P4\': 0.100000 };
g_spherePositions[\'PC.635\'] = { \'name\': \'PC.635\', \'color\': 0, \'x\': 1.000000, \'y\': 2.000000, \'z\': 1.000000, \'P1\': 1.000000, \'P2\': 2.000000, \'P3\': 1.000000, \'P4\': 1.000000 };

var g_ellipsesDimensions = new Array();
g_ellipsesDimensions[\'PC.355\'] = { \'name\': \'PC.355\', \'color\': 0, \'width\': 0.400000, \'height\': 0.500000, \'length\': 0.800000 , \'x\': 0.300000, \'y\': 0.500000, \'z\': 0.100000, \'P1\': 0.300000, \'P2\': 0.500000, \'P3\': 0.100000, \'P4\': 0.300000 }
g_ellipsesDimensions[\'PC.607\'] = { \'name\': \'PC.607\', \'color\': 0, \'width\': 0.100000, \'height\': 2.000000, \'length\': 0.000000 , \'x\': 1.100000, \'y\': 1.100000, \'z\': 1.000000, \'P1\': 1.100000, \'P2\': 1.100000, \'P3\': 1.000000, \'P4\': 0.800000 }
g_ellipsesDimensions[\'PC.634\'] = { \'name\': \'PC.634\', \'color\': 0, \'width\': 0.300000, \'height\': 0.600000, \'length\': 4.000000 , \'x\': 0.100000, \'y\': 3.300000, \'z\': 5.500000, \'P1\': 0.100000, \'P2\': 3.300000, \'P3\': 5.500000, \'P4\': 0.100000 }
g_ellipsesDimensions[\'PC.635\'] = { \'name\': \'PC.635\', \'color\': 0, \'width\': 0.010780, \'height\': 1.000000, \'length\': 0.023000 , \'x\': 1.000000, \'y\': 2.000000, \'z\': 1.000000, \'P1\': 1.000000, \'P2\': 2.000000, \'P3\': 1.000000, \'P4\': 1.000000 }
var g_segments = 14, g_rings = 14, g_radius = 0.012000;
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
var g_pc1Label = "PC1 (44.00 %)";
var g_pc2Label = "PC2 (40.00 %)";
var g_pc3Label = "PC3 (15.00 %)";
var g_number_of_custom_axes = 0;
var g_fractionExplained = [0.440000, 0.400000, 0.150000, 0.010000];
var g_fractionExplainedRounded = [44.00, 40.00, 15.00, 1.00];
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
var g_mappingFileData = { 'PC.636': ['ACGGTGAGTGTC','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._636'],'PC.355': ['AACTCGTCGATG','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._355'],'PC.607': ['AACTGTGCGTAC','YATGCTGCCTCCCGTAGGAGT','Fast','20071112','Fasting_mouse_I.D._607'],'PC.634': ['ACAGAGTCGGCT','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._634'],'PC.635': ['ACCGCAGAGTCA','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._635'],'PC.593': ['AGCAGCACTTGT','YATGCTGCCTCCCGTAGGAGT','Control','20071210','Control_mouse_I.D._593'],'PC.356': ['ACAGACCACTCA','YATGCTGCCTCCCGTAGGAGT','Control','20061126','Control_mouse_I.D._356'],'PC.481': ['ACCAGCGACTAG','YATGCTGCCTCCCGTAGGAGT','Control','20070314','Control_mouse_I.D._481'],'PC.354': ['AGCACGAGCCTA','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._354'] };
var g_animatableMappingFileHeaders = [];
"""

MAPPING_FILE_JS_WITH_ANIMATABLE_CATEGORIES = """var g_mappingFileHeaders = ['BarcodeSequence','LinkerPrimerSequence','Treatment','DOB','Description'];
var g_mappingFileData = { 'PC.636': ['ACGGTGAGTGTC','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._636'],'PC.355': ['AACTCGTCGATG','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._355'],'PC.607': ['AACTGTGCGTAC','YATGCTGCCTCCCGTAGGAGT','Fast','20071112','Fasting_mouse_I.D._607'],'PC.634': ['ACAGAGTCGGCT','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._634'],'PC.635': ['ACCGCAGAGTCA','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._635'],'PC.593': ['AGCAGCACTTGT','YATGCTGCCTCCCGTAGGAGT','Control','20071210','Control_mouse_I.D._593'],'PC.356': ['ACAGACCACTCA','YATGCTGCCTCCCGTAGGAGT','Control','20061126','Control_mouse_I.D._356'],'PC.481': ['ACCAGCGACTAG','YATGCTGCCTCCCGTAGGAGT','Control','20070314','Control_mouse_I.D._481'],'PC.354': ['AGCACGAGCCTA','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._354'] };
var g_animatableMappingFileHeaders = ['DOB'];
"""


TAXA_JS_STRING = """
var g_taxaPositions = new Array();
g_taxaPositions['0'] = { 'lineage': 'Root;k__Bacteria;p__Firmicutes', 'x': 0.280399, 'y': -0.006013, 'z': 0.023485, 'radius': 5.000000};
g_taxaPositions['1'] = { 'lineage': 'Root;k__Bacteria;p__Bacteroidetes', 'x': 0.228820, 'y': -0.130142, 'z': -0.287149, 'radius': 3.491237};
g_taxaPositions['2'] = { 'lineage': 'Root;k__Bacteria;p__Tenericutes', 'x': -0.091330, 'y': 0.424147, 'z': -0.135627, 'radius': 0.868694};
g_taxaPositions['3'] = { 'lineage': 'Root;k__Bacteria;Other', 'x': -0.276542, 'y': -0.144964, 'z': 0.066647, 'radius': 0.696843};

"""

VECTOR_JS_STRING_NO_SORTING = """
var g_vectorPositions = new Array();
g_vectorPositions['Control'] = new Array();
g_vectorPositions['Control']['PC.354'] = [-0.293353176, 0.0183956004, 0.0329884266];
g_vectorPositions['Control']['PC.355'] = [-0.109166142, 0.0877774496, 0.0115866606];
g_vectorPositions['Control']['PC.356'] = [-0.183191151, 34912.621, 0.00869481594];
g_vectorPositions['Control']['PC.481'] = [-0.192382819, 0.0147832029, -0.0147871039];
g_vectorPositions['Control']['PC.593'] = [0.0968466168, -0.159388265, 0.135271607];
g_vectorPositions['Fast'] = new Array();
g_vectorPositions['Fast']['PC.607'] = [0.0688959784, -0.166234067, -0.0998300962];
g_vectorPositions['Fast']['PC.634'] = [0.20468454, 0.128911236, -0.0293614192];
g_vectorPositions['Fast']['PC.635'] = [0.12613151, -0.00266030272, -0.141717093];
g_vectorPositions['Fast']['PC.636'] = [0.281534642, 0.0710660196, 0.097154202];
"""

VECTOR_JS_STRING_SORTING = """
var g_vectorPositions = new Array();
g_vectorPositions['Control'] = new Array();
g_vectorPositions['Control']['PC.356'] = [-0.183191151, 34912.621, 0.00869481594];
g_vectorPositions['Control']['PC.354'] = [-0.293353176, 0.0183956004, 0.0329884266];
g_vectorPositions['Control']['PC.355'] = [-0.109166142, 0.0877774496, 0.0115866606];
g_vectorPositions['Control']['PC.481'] = [-0.192382819, 0.0147832029, -0.0147871039];
g_vectorPositions['Control']['PC.593'] = [0.0968466168, -0.159388265, 0.135271607];
g_vectorPositions['Fast'] = new Array();
g_vectorPositions['Fast']['PC.607'] = [0.0688959784, -0.166234067, -0.0998300962];
g_vectorPositions['Fast']['PC.634'] = [0.20468454, 0.128911236, -0.0293614192];
g_vectorPositions['Fast']['PC.635'] = [0.12613151, -0.00266030272, -0.141717093];
g_vectorPositions['Fast']['PC.636'] = [0.281534642, 0.0710660196, 0.097154202];
"""

COMPARISON_JS_STRING = """
var g_comparisonPositions = new Array();
var g_isSerialComparisonPlot = true;
g_comparisonPositions['sampa'] = [[-0.0677, -2.036, 0.2726], [-0.972, 0.551, 1.144], [0.2339, -0.88, -1.753]];
g_comparisonPositions['sampb'] = [[-1.782, -0.972, 0.1582], [1.438, -2.603, -1.39], [0.436, 2.12, -0.935]];
g_comparisonPositions['sampc'] = [[-0.659, -0.2566, 0.514], [-0.356, 0.0875, 0.772], [-0.88, 1.069, 1.069]];
g_comparisonPositions['sampd'] = [[-1.179, -0.968, 2.525], [1.512, -1.239, -0.0365], [0.294, 0.2988, 0.0467]];
g_comparisonPositions['sampe'] = [[-0.896, -1.765, 0.274], [1.17, 1.31, -1.407], [1.64, 0.2485, -0.354]];
g_comparisonPositions['sampf'] = [[-0.0923, 1.414, -0.622], [2.618, 0.739, -0.01295], [0.821, -1.13, -1.794]];
"""

COMPARISON_JS_STRING_NON_SERIAL = """
var g_comparisonPositions = new Array();
var g_isSerialComparisonPlot = false;
g_comparisonPositions['sampa'] = [[-0.0677, -2.036, 0.2726], [-0.972, 0.551, 1.144], [0.2339, -0.88, -1.753]];
g_comparisonPositions['sampb'] = [[-1.782, -0.972, 0.1582], [1.438, -2.603, -1.39], [0.436, 2.12, -0.935]];
g_comparisonPositions['sampc'] = [[-0.659, -0.2566, 0.514], [-0.356, 0.0875, 0.772], [-0.88, 1.069, 1.069]];
g_comparisonPositions['sampd'] = [[-1.179, -0.968, 2.525], [1.512, -1.239, -0.0365], [0.294, 0.2988, 0.0467]];
g_comparisonPositions['sampe'] = [[-0.896, -1.765, 0.274], [1.17, 1.31, -1.407], [1.64, 0.2485, -0.354]];
g_comparisonPositions['sampf'] = [[-0.0923, 1.414, -0.622], [2.618, 0.739, -0.01295], [0.821, -1.13, -1.794]];
"""

COMPARISON_COORDS_HEADERS_ZERO = """
var g_comparisonPositions = new Array();
var g_isSerialComparisonPlot = false;
g_comparisonPositions['sampa0'] = [[-0.0677, -2.036, 0.2726], [-0.972, 0.551, 1.144], [0.2339, -0.88, -1.753]];
g_comparisonPositions['sampb0'] = [[-1.782, -0.972, 0.1582], [1.438, -2.603, -1.39], [0.436, 2.12, -0.935]];
g_comparisonPositions['sampc0'] = [[-0.659, -0.2566, 0.514], [-0.356, 0.0875, 0.772], [-0.88, 1.069, 1.069]];
g_comparisonPositions['sampd00'] = [[-1.179, -0.968, 2.525], [1.512, -1.239, -0.0365], [0.294, 0.2988, 0.0467]];
g_comparisonPositions['sampe00'] = [[-0.896, -1.765, 0.274], [1.17, 1.31, -1.407], [1.64, 0.2485, -0.354]];
g_comparisonPositions['sampf00'] = [[-0.0923, 1.414, -0.622], [2.618, 0.739, -0.01295], [0.821, -1.13, -1.794]];
"""

EXPECTED_FOOTER_A =\
"""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>

<div id="overlay">
    <div>
    <img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="small-logo"/>
        <h1>WebGL is not enabled!</h1>
        <p>Emperor's visualization framework is WebGL based, it seems that your system doesn't have this resource available. Here is what you can do:</p>
        <p id="explanation"><strong>Chrome:</strong> Type "chrome://flags/" into the address bar, then search for "Disable WebGL". Disable this option if you haven't already. <em>Note:</em> If you follow these steps and still don't see an image, go to "chrome://flags/" and then search for "Override software rendering list" and enable this option.</p>
        <p id="explanation"><strong>Safari:</strong> Open Safari's menu and select Preferences. Click on the advanced tab, and then check "Show Developer" menu. Then open the "Developer" menu and select "Enable WebGL".</p>
        <p id="explanation"><strong>Firefox:</strong> Go to Options through Firefox > Options or Tools > Options. Go to Advanced, then General. Check "Use hardware acceleration when available" and restart Firefox.</p>
        <p id="explanation"><strong>Other browsers:</strong> The only browsers that support WebGL are Chrome, Safari, and Firefox. Please switch to these browsers when using Emperor.</p>
        <p id="explanation"><em>Note:</em> Once you went through these changes, reload the page and it should work!</p>
        <p id="source">Sources: Instructions for <a href="https://www.biodigitalhuman.com/home/enabling-webgl.html">Chrome and Safari</a>, and <a href="http://www.infewbytes.com/?p=144">Firefox</a></p>
    </div>
</div>

<div id="emperor-plot-toggle">
    <form>
      <div id="plottype">
        <input id="pcoa" type="radio" id="pcoa" name="plottype" checked="checked" /><label for="pcoa">PCoA</label>
        <input id="parallel" type="radio" id="parallel" name="plottype" /><label for="parallel">Parallel</label>
      </div>
    </form>
</div>
<div id="pcoaPlotWrapper" class="emperor-plot-wrapper">
    <label id="pointCount" class="ontop">
    </label>

    <div id="finder" class="arrow-right">
    </div>

    <div id="labels" class="unselectable">
    </div>

    <div id="taxalabels" class="unselectable">
    </div>

    <div id="axislabels" class="axis-labels">
    </div>

    <div id="main-plot">
    </div>
</div>

<div id="parallelPlotWrapper" class="emperor-plot-wrapper">
</div>

<div id="emperor-separator" class="emperor-separator" ondblclick="separatorDoubleClick()"></div>

<div id="emperor-menu">
    <div id="emperor-menu-tabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#scalingby">Scaling</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#axes">Axes</a></li>
            <li><a href="#animations">Animations</a></li>
            <li><a href="#options">Options</a></li>
        </ul>
        <div id="keytab" class="emperor-tab-div">
            <form name="keyFilter">
                <label>Filter  </label><input name="filterBox" id="searchBox" type="text" onkeyup="filterKey()"></input>
            </form>
            <div id="key">
            </div>
        </div>
        <div id="colorby" class="emperor-tab-div">
            <input type="checkbox" onchange="toggleContinuousAndDiscreteColors(this)" id="discreteorcontinuouscolors" name="discreteorcontinuouscolors">  Use gradient colors</input>
            <br><br>
            <select id="colorbycombo" onchange="colorByMenuChanged()" size="3" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="showbycombo" onchange="showByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="showbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereopacity" class="text">Global Sphere Opacity</label>
                        <label id="sphereopacity" class="slidervalue"></label>
                        <div id="sopacityslider" class="slider-range-max"></div>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <button id="toggle-visibility-selection-button" onClick="toggleVisibleCategories()">Invert Selected</button>
                    </td>
                </tr>
            </table>
        </div>
        <div id="scalingby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="scalingbycombo" onchange="scalingByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="scalingbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereradius" class="text">Global Sphere Scale</label>
                        <label id="sphereradius" class="slidervalue"></label>
                        <div id="sradiusslider" class="slider-range-max"></div>
                    </td>
                </tr>
            </table>
        </div>
        <div id="labelby" class="emperor-tab-div">
            <div id="labels-top">
                <form name="plotoptions">
                    <input type="checkbox" onClick="toggleLabels()">Samples Label Visibility</input>
                </form>
                <br>
                <label for="labelopacity" class="text">Label Opacity</label>
                <label id="labelopacity" class="slidervalue"></label>
                <div id="lopacityslider" class="slider-range-max"></div>
                <div id="label-color-holder clearfix">
                    <table class="emperor-tab-table">
                        <tr><td><div id="labelColor" class="colorbox"></div></td><td><label>Master Label Color</label></td></tr>
                        <br><br>
                </table></div>
            </div>
            <br>
            <select id="labelcombo" onchange="labelMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="label-list">
            </div>
        </div>
        <div id="axes" class="emperor-tab-div">
            <div id="pcoaaxes">
                <div class="list" id="axeslist">
                </div>
            </div>
        </div>
        <div id="animations" class="emperor-tab-div">
            <table class="emperor-tab-table-with-sliders">
                <tr>
                    <td>
                        <a id="reset-button" class="media-button" href="javascript:void(0);" onclick="javascript:resetAnimation()"><img src="emperor_required_resources/img/reset.png" ></img></a>
                        <a id="play-button" class="media-button" href="javascript:void(0);" onclick="javascript:playAnimation()"><img src="emperor_required_resources/img/play.png"></img></a>
                        <a id="pause-button" class="media-button" href="javascript:void(0);" onclick="javascript:pauseAnimation()"><img src="emperor_required_resources/img/pause.png"></img></a>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="animation-speed" class="text">Speed</label>
                        <label id="animation-speed" class="slidervalue"></label>
                        <div id="animation-speed-slider" class="slider-range-max"></div>
                        <div id="labelColorHolder clearfix">
                    </td>
                </tr>
                <tr>
                    <td>
                        <br><label for="gradient-category-drop-down" class="text">Gradient Category</label><br>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="gradient-category-drop-down" class="emperor-tab-drop-down"></select><br>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="trajectory-category-drop-down" class="text">Trajectory Category</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="trajectory-category-drop-down" class="emperor-tab-drop-down" onchange="colorAnimationsByCategoryChanged()"></select>
                    </td>
                </tr>
                <tr>
                    <td id="emperor-animation-color-selector">
                    </td>
                </tr>
            </table>
        </div>
        <div id="options" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr><td><div id="axeslabelscolor" class="colorbox" name="axeslabelscolor"></div></td><td title="Axes Labels Color">Axes Labels Color</td></tr>
                <tr><td><div id="axescolor" class="colorbox" name="axescolor"></div></td><td title="Axes Color Title">Axes Color</td></tr>
                <tr><td><div id="rendererbackgroundcolor" class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
                <tr><td colspan="2">
                        <div id="pcoaviewoptions" class="">
            <br>
            <label for="ellipseopacity" class="text">Ellipse Opacity</label>
            <label id="ellipseopacity" class="slidervalue"></label>
            <div id="eopacityslider" class="slider-range-max"></div>
                            <form name="settingsoptionscolor">
                            </form>
                            <div id="pcoaoptions" class="">
                                <form name="settingsoptions">
                                    <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
                                </form>
                            </div>
                            <br><input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
                            <br><br>
                            <hr class='section-break'>
                            <br>Filename <small>(only letters, numbers, ., - and _)</small>:
                            <br><input name="saveas_name" id="saveas_name" value="screenshot" type="text"/>
                            <br><input id="saveas_legends" class="checkbox" type="checkbox" style=""> Create legend
                            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()"/>
                            <br><br>For a PNG, simply press 'ctrl+p'.
                            <div id="paralleloptions" class="">
                            </div>
                        </div>
                        <br>
                </td></tr>
            </table>
        </div>
    </div>  
</div>
</body>

</html>
"""

EXPECTED_FOOTER_B =\
"""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>

<div id="overlay">
    <div>
    <img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="small-logo"/>
        <h1>WebGL is not enabled!</h1>
        <p>Emperor's visualization framework is WebGL based, it seems that your system doesn't have this resource available. Here is what you can do:</p>
        <p id="explanation"><strong>Chrome:</strong> Type "chrome://flags/" into the address bar, then search for "Disable WebGL". Disable this option if you haven't already. <em>Note:</em> If you follow these steps and still don't see an image, go to "chrome://flags/" and then search for "Override software rendering list" and enable this option.</p>
        <p id="explanation"><strong>Safari:</strong> Open Safari's menu and select Preferences. Click on the advanced tab, and then check "Show Developer" menu. Then open the "Developer" menu and select "Enable WebGL".</p>
        <p id="explanation"><strong>Firefox:</strong> Go to Options through Firefox > Options or Tools > Options. Go to Advanced, then General. Check "Use hardware acceleration when available" and restart Firefox.</p>
        <p id="explanation"><strong>Other browsers:</strong> The only browsers that support WebGL are Chrome, Safari, and Firefox. Please switch to these browsers when using Emperor.</p>
        <p id="explanation"><em>Note:</em> Once you went through these changes, reload the page and it should work!</p>
        <p id="source">Sources: Instructions for <a href="https://www.biodigitalhuman.com/home/enabling-webgl.html">Chrome and Safari</a>, and <a href="http://www.infewbytes.com/?p=144">Firefox</a></p>
    </div>
</div>

<div id="emperor-plot-toggle">
    <form>
      <div id="plottype">
        <input id="pcoa" type="radio" id="pcoa" name="plottype" checked="checked" /><label for="pcoa">PCoA</label>
        <input id="parallel" type="radio" id="parallel" name="plottype" /><label for="parallel">Parallel</label>
      </div>
    </form>
</div>
<div id="pcoaPlotWrapper" class="emperor-plot-wrapper">
    <label id="pointCount" class="ontop">
    </label>

    <div id="finder" class="arrow-right">
    </div>

    <div id="labels" class="unselectable">
    </div>

    <div id="taxalabels" class="unselectable">
    </div>

    <div id="axislabels" class="axis-labels">
    </div>

    <div id="main-plot">
    </div>
</div>

<div id="parallelPlotWrapper" class="emperor-plot-wrapper">
</div>

<div id="emperor-separator" class="emperor-separator" ondblclick="separatorDoubleClick()"></div>

<div id="emperor-menu">
    <div id="emperor-menu-tabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#scalingby">Scaling</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#axes">Axes</a></li>
            <li><a href="#animations">Animations</a></li>
            <li><a href="#options">Options</a></li>
        </ul>
        <div id="keytab" class="emperor-tab-div">
            <form name="keyFilter">
                <label>Filter  </label><input name="filterBox" id="searchBox" type="text" onkeyup="filterKey()"></input>
            </form>
            <div id="key">
            </div>
        </div>
        <div id="colorby" class="emperor-tab-div">
            <input type="checkbox" onchange="toggleContinuousAndDiscreteColors(this)" id="discreteorcontinuouscolors" name="discreteorcontinuouscolors">  Use gradient colors</input>
            <br>
            <table>
                <tr><td><div id="taxaspherescolor" class="colorbox" name="taxaspherescolor"></div></td><td title="taxacolor">Taxa Spheres Color</td></tr>
            </table>
            <br>
            <br><br>
            <select id="colorbycombo" onchange="colorByMenuChanged()" size="3" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby" class="emperor-tab-div">
            <br>
            <form name="biplotsvisibility">
            <input type="checkbox" onClick="toggleBiplotVisibility()" checked>Biplots Visibility</input>
            </form>
            <br>
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="showbycombo" onchange="showByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="showbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereopacity" class="text">Global Sphere Opacity</label>
                        <label id="sphereopacity" class="slidervalue"></label>
                        <div id="sopacityslider" class="slider-range-max"></div>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <button id="toggle-visibility-selection-button" onClick="toggleVisibleCategories()">Invert Selected</button>
                    </td>
                </tr>
            </table>
        </div>
        <div id="scalingby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="scalingbycombo" onchange="scalingByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="scalingbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereradius" class="text">Global Sphere Scale</label>
                        <label id="sphereradius" class="slidervalue"></label>
                        <div id="sradiusslider" class="slider-range-max"></div>
                    </td>
                </tr>
            </table>
        </div>
        <div id="labelby" class="emperor-tab-div">
            <div id="labels-top">
                <form name="plotoptions">
                    <input type="checkbox" onClick="toggleLabels()">Samples Label Visibility</input>
                </form>
            <form name="biplotoptions">
            <input type="checkbox" onClick="toggleTaxaLabels()">Biplots Label Visibility</input>
            </form>
                <br>
                <label for="labelopacity" class="text">Label Opacity</label>
                <label id="labelopacity" class="slidervalue"></label>
                <div id="lopacityslider" class="slider-range-max"></div>
                <div id="label-color-holder clearfix">
                    <table class="emperor-tab-table">
                        <tr><td><div id="labelColor" class="colorbox"></div></td><td><label>Master Label Color</label></td></tr>
            <tr><td><div id="taxalabelcolor" class="colorbox"></div></td><td><label>Taxa Label Color</label></td></tr>

                        <br><br>
                </table></div>
            </div>
            <br>
            <select id="labelcombo" onchange="labelMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="label-list">
            </div>
        </div>
        <div id="axes" class="emperor-tab-div">
            <div id="pcoaaxes">
                <div class="list" id="axeslist">
                </div>
            </div>
        </div>
        <div id="animations" class="emperor-tab-div">
            <table class="emperor-tab-table-with-sliders">
                <tr>
                    <td>
                        <a id="reset-button" class="media-button" href="javascript:void(0);" onclick="javascript:resetAnimation()"><img src="emperor_required_resources/img/reset.png" ></img></a>
                        <a id="play-button" class="media-button" href="javascript:void(0);" onclick="javascript:playAnimation()"><img src="emperor_required_resources/img/play.png"></img></a>
                        <a id="pause-button" class="media-button" href="javascript:void(0);" onclick="javascript:pauseAnimation()"><img src="emperor_required_resources/img/pause.png"></img></a>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="animation-speed" class="text">Speed</label>
                        <label id="animation-speed" class="slidervalue"></label>
                        <div id="animation-speed-slider" class="slider-range-max"></div>
                        <div id="labelColorHolder clearfix">
                    </td>
                </tr>
                <tr>
                    <td>
                        <br><label for="gradient-category-drop-down" class="text">Gradient Category</label><br>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="gradient-category-drop-down" class="emperor-tab-drop-down"></select><br>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="trajectory-category-drop-down" class="text">Trajectory Category</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="trajectory-category-drop-down" class="emperor-tab-drop-down" onchange="colorAnimationsByCategoryChanged()"></select>
                    </td>
                </tr>
                <tr>
                    <td id="emperor-animation-color-selector">
                    </td>
                </tr>
            </table>
        </div>
        <div id="options" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr><td><div id="axeslabelscolor" class="colorbox" name="axeslabelscolor"></div></td><td title="Axes Labels Color">Axes Labels Color</td></tr>
                <tr><td><div id="axescolor" class="colorbox" name="axescolor"></div></td><td title="Axes Color Title">Axes Color</td></tr>
                <tr><td><div id="rendererbackgroundcolor" class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
                <tr><td colspan="2">
                        <div id="pcoaviewoptions" class="">
                            <form name="settingsoptionscolor">
                            </form>
                            <div id="pcoaoptions" class="">
                                <form name="settingsoptions">
                                    <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
                                </form>
                            </div>
                            <br><input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
                            <br><br>
                            <hr class='section-break'>
                            <br>Filename <small>(only letters, numbers, ., - and _)</small>:
                            <br><input name="saveas_name" id="saveas_name" value="screenshot" type="text"/>
                            <br><input id="saveas_legends" class="checkbox" type="checkbox" style=""> Create legend
                            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()"/>
                            <br><br>For a PNG, simply press 'ctrl+p'.
                            <div id="paralleloptions" class="">
                            </div>
                        </div>
                        <br>
                </td></tr>
            </table>
        </div>
    </div>  
</div>
</body>

</html>
"""

EXPECTED_FOOTER_C =\
"""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>

<div id="overlay">
    <div>
    <img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="small-logo"/>
        <h1>WebGL is not enabled!</h1>
        <p>Emperor's visualization framework is WebGL based, it seems that your system doesn't have this resource available. Here is what you can do:</p>
        <p id="explanation"><strong>Chrome:</strong> Type "chrome://flags/" into the address bar, then search for "Disable WebGL". Disable this option if you haven't already. <em>Note:</em> If you follow these steps and still don't see an image, go to "chrome://flags/" and then search for "Override software rendering list" and enable this option.</p>
        <p id="explanation"><strong>Safari:</strong> Open Safari's menu and select Preferences. Click on the advanced tab, and then check "Show Developer" menu. Then open the "Developer" menu and select "Enable WebGL".</p>
        <p id="explanation"><strong>Firefox:</strong> Go to Options through Firefox > Options or Tools > Options. Go to Advanced, then General. Check "Use hardware acceleration when available" and restart Firefox.</p>
        <p id="explanation"><strong>Other browsers:</strong> The only browsers that support WebGL are Chrome, Safari, and Firefox. Please switch to these browsers when using Emperor.</p>
        <p id="explanation"><em>Note:</em> Once you went through these changes, reload the page and it should work!</p>
        <p id="source">Sources: Instructions for <a href="https://www.biodigitalhuman.com/home/enabling-webgl.html">Chrome and Safari</a>, and <a href="http://www.infewbytes.com/?p=144">Firefox</a></p>
    </div>
</div>

<div id="emperor-plot-toggle">
    <form>
      <div id="plottype">
        <input id="pcoa" type="radio" id="pcoa" name="plottype" checked="checked" /><label for="pcoa">PCoA</label>
        <input id="parallel" type="radio" id="parallel" name="plottype" /><label for="parallel">Parallel</label>
      </div>
    </form>
</div>
<div id="pcoaPlotWrapper" class="emperor-plot-wrapper">
    <label id="pointCount" class="ontop">
    </label>

    <div id="finder" class="arrow-right">
    </div>

    <div id="labels" class="unselectable">
    </div>

    <div id="taxalabels" class="unselectable">
    </div>

    <div id="axislabels" class="axis-labels">
    </div>

    <div id="main-plot">
    </div>
</div>

<div id="parallelPlotWrapper" class="emperor-plot-wrapper">
</div>

<div id="emperor-separator" class="emperor-separator" ondblclick="separatorDoubleClick()"></div>

<div id="emperor-menu">
    <div id="emperor-menu-tabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#scalingby">Scaling</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#axes">Axes</a></li>
            <li><a href="#animations">Animations</a></li>
            <li><a href="#options">Options</a></li>
        </ul>
        <div id="keytab" class="emperor-tab-div">
            <form name="keyFilter">
                <label>Filter  </label><input name="filterBox" id="searchBox" type="text" onkeyup="filterKey()"></input>
            </form>
            <div id="key">
            </div>
        </div>
        <div id="colorby" class="emperor-tab-div">
            <input type="checkbox" onchange="toggleContinuousAndDiscreteColors(this)" id="discreteorcontinuouscolors" name="discreteorcontinuouscolors">  Use gradient colors</input>
            <br><br>
            <select id="colorbycombo" onchange="colorByMenuChanged()" size="3" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="showbycombo" onchange="showByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="showbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereopacity" class="text">Global Sphere Opacity</label>
                        <label id="sphereopacity" class="slidervalue"></label>
                        <div id="sopacityslider" class="slider-range-max"></div>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <button id="toggle-visibility-selection-button" onClick="toggleVisibleCategories()">Invert Selected</button>
                    </td>
                </tr>
            </table>
        </div>
        <div id="scalingby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="scalingbycombo" onchange="scalingByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="scalingbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereradius" class="text">Global Sphere Scale</label>
                        <label id="sphereradius" class="slidervalue"></label>
                        <div id="sradiusslider" class="slider-range-max"></div>
                    </td>
                </tr>
            </table>
        </div>
        <div id="labelby" class="emperor-tab-div">
            <div id="labels-top">
                <form name="plotoptions">
                    <input type="checkbox" onClick="toggleLabels()">Samples Label Visibility</input>
                </form>
                <br>
                <label for="labelopacity" class="text">Label Opacity</label>
                <label id="labelopacity" class="slidervalue"></label>
                <div id="lopacityslider" class="slider-range-max"></div>
                <div id="label-color-holder clearfix">
                    <table class="emperor-tab-table">
                        <tr><td><div id="labelColor" class="colorbox"></div></td><td><label>Master Label Color</label></td></tr>
                        <br><br>
                </table></div>
            </div>
            <br>
            <select id="labelcombo" onchange="labelMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="label-list">
            </div>
        </div>
        <div id="axes" class="emperor-tab-div">
            <div id="pcoaaxes">
                <div class="list" id="axeslist">
                </div>
            </div>
        </div>
        <div id="animations" class="emperor-tab-div">
            <table class="emperor-tab-table-with-sliders">
                <tr>
                    <td>
                        <a id="reset-button" class="media-button" href="javascript:void(0);" onclick="javascript:resetAnimation()"><img src="emperor_required_resources/img/reset.png" ></img></a>
                        <a id="play-button" class="media-button" href="javascript:void(0);" onclick="javascript:playAnimation()"><img src="emperor_required_resources/img/play.png"></img></a>
                        <a id="pause-button" class="media-button" href="javascript:void(0);" onclick="javascript:pauseAnimation()"><img src="emperor_required_resources/img/pause.png"></img></a>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="animation-speed" class="text">Speed</label>
                        <label id="animation-speed" class="slidervalue"></label>
                        <div id="animation-speed-slider" class="slider-range-max"></div>
                        <div id="labelColorHolder clearfix">
                    </td>
                </tr>
                <tr>
                    <td>
                        <br><label for="gradient-category-drop-down" class="text">Gradient Category</label><br>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="gradient-category-drop-down" class="emperor-tab-drop-down"></select><br>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="trajectory-category-drop-down" class="text">Trajectory Category</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="trajectory-category-drop-down" class="emperor-tab-drop-down" onchange="colorAnimationsByCategoryChanged()"></select>
                    </td>
                </tr>
                <tr>
                    <td id="emperor-animation-color-selector">
                    </td>
                </tr>
            </table>
        </div>
        <div id="options" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr><td><div id="axeslabelscolor" class="colorbox" name="axeslabelscolor"></div></td><td title="Axes Labels Color">Axes Labels Color</td></tr>
                <tr><td><div id="axescolor" class="colorbox" name="axescolor"></div></td><td title="Axes Color Title">Axes Color</td></tr>
                <tr><td><div id="rendererbackgroundcolor" class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
                <tr><td colspan="2">
                        <div id="pcoaviewoptions" class="">
                            <form name="settingsoptionscolor">
                            </form>
                            <div id="pcoaoptions" class="">
                                <form name="settingsoptions">
                                    <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
                                </form>
                            </div>
                            <br><input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
                            <br><br>
                            <hr class='section-break'>
                            <br>Filename <small>(only letters, numbers, ., - and _)</small>:
                            <br><input name="saveas_name" id="saveas_name" value="screenshot" type="text"/>
                            <br><input id="saveas_legends" class="checkbox" type="checkbox" style=""> Create legend
                            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()"/>
                            <br><br>For a PNG, simply press 'ctrl+p'.
                            <div id="paralleloptions" class="">
                            </div>
                        </div>
                        <br>
                </td></tr>
            </table>
        </div>
    </div>  
</div>
</body>

</html>
"""

EXPECTED_FOOTER_D =\
"""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>

<div id="overlay">
    <div>
    <img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="small-logo"/>
        <h1>WebGL is not enabled!</h1>
        <p>Emperor's visualization framework is WebGL based, it seems that your system doesn't have this resource available. Here is what you can do:</p>
        <p id="explanation"><strong>Chrome:</strong> Type "chrome://flags/" into the address bar, then search for "Disable WebGL". Disable this option if you haven't already. <em>Note:</em> If you follow these steps and still don't see an image, go to "chrome://flags/" and then search for "Override software rendering list" and enable this option.</p>
        <p id="explanation"><strong>Safari:</strong> Open Safari's menu and select Preferences. Click on the advanced tab, and then check "Show Developer" menu. Then open the "Developer" menu and select "Enable WebGL".</p>
        <p id="explanation"><strong>Firefox:</strong> Go to Options through Firefox > Options or Tools > Options. Go to Advanced, then General. Check "Use hardware acceleration when available" and restart Firefox.</p>
        <p id="explanation"><strong>Other browsers:</strong> The only browsers that support WebGL are Chrome, Safari, and Firefox. Please switch to these browsers when using Emperor.</p>
        <p id="explanation"><em>Note:</em> Once you went through these changes, reload the page and it should work!</p>
        <p id="source">Sources: Instructions for <a href="https://www.biodigitalhuman.com/home/enabling-webgl.html">Chrome and Safari</a>, and <a href="http://www.infewbytes.com/?p=144">Firefox</a></p>
    </div>
</div>

<div id="emperor-plot-toggle">
    <form>
      <div id="plottype">
        <input id="pcoa" type="radio" id="pcoa" name="plottype" checked="checked" /><label for="pcoa">PCoA</label>
        <input id="parallel" type="radio" id="parallel" name="plottype" /><label for="parallel">Parallel</label>
      </div>
    </form>
</div>
<div id="pcoaPlotWrapper" class="emperor-plot-wrapper">
    <label id="pointCount" class="ontop">
    </label>

    <div id="finder" class="arrow-right">
    </div>

    <div id="labels" class="unselectable">
    </div>

    <div id="taxalabels" class="unselectable">
    </div>

    <div id="axislabels" class="axis-labels">
    </div>

    <div id="main-plot">
    </div>
</div>

<div id="parallelPlotWrapper" class="emperor-plot-wrapper">
</div>

<div id="emperor-separator" class="emperor-separator" ondblclick="separatorDoubleClick()"></div>

<div id="emperor-menu">
    <div id="emperor-menu-tabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#scalingby">Scaling</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#axes">Axes</a></li>
            <li><a href="#animations">Animations</a></li>
            <li><a href="#options">Options</a></li>
        </ul>
        <div id="keytab" class="emperor-tab-div">
            <form name="keyFilter">
                <label>Filter  </label><input name="filterBox" id="searchBox" type="text" onkeyup="filterKey()"></input>
            </form>
            <div id="key">
            </div>
        </div>
        <div id="colorby" class="emperor-tab-div">
            <input type="checkbox" onchange="toggleContinuousAndDiscreteColors(this)" id="discreteorcontinuouscolors" name="discreteorcontinuouscolors">  Use gradient colors</input>
            <br><br>
            <select id="colorbycombo" onchange="colorByMenuChanged()" size="3" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="showbycombo" onchange="showByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="showbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereopacity" class="text">Global Sphere Opacity</label>
                        <label id="sphereopacity" class="slidervalue"></label>
                        <div id="sopacityslider" class="slider-range-max"></div>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <button id="toggle-visibility-selection-button" onClick="toggleVisibleCategories()">Invert Selected</button>
                    </td>
                </tr>
            </table>
        </div>
        <div id="scalingby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="scalingbycombo" onchange="scalingByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="scalingbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereradius" class="text">Global Sphere Scale</label>
                        <label id="sphereradius" class="slidervalue"></label>
                        <div id="sradiusslider" class="slider-range-max"></div>
                    </td>
                </tr>
            </table>
        </div>
        <div id="labelby" class="emperor-tab-div">
            <div id="labels-top">
                <form name="plotoptions">
                    <input type="checkbox" onClick="toggleLabels()">Samples Label Visibility</input>
                </form>
                <br>
                <label for="labelopacity" class="text">Label Opacity</label>
                <label id="labelopacity" class="slidervalue"></label>
                <div id="lopacityslider" class="slider-range-max"></div>
                <div id="label-color-holder clearfix">
                    <table class="emperor-tab-table">
                        <tr><td><div id="labelColor" class="colorbox"></div></td><td><label>Master Label Color</label></td></tr>
                        <br><br>
                </table></div>
            </div>
            <br>
            <select id="labelcombo" onchange="labelMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="label-list">
            </div>
        </div>
        <div id="axes" class="emperor-tab-div">
            <div id="pcoaaxes">
                <div class="list" id="axeslist">
                </div>
            </div>
        </div>
        <div id="animations" class="emperor-tab-div">
            <table class="emperor-tab-table-with-sliders">
                <tr>
                    <td>
                        <a id="reset-button" class="media-button" href="javascript:void(0);" onclick="javascript:resetAnimation()"><img src="emperor_required_resources/img/reset.png" ></img></a>
                        <a id="play-button" class="media-button" href="javascript:void(0);" onclick="javascript:playAnimation()"><img src="emperor_required_resources/img/play.png"></img></a>
                        <a id="pause-button" class="media-button" href="javascript:void(0);" onclick="javascript:pauseAnimation()"><img src="emperor_required_resources/img/pause.png"></img></a>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="animation-speed" class="text">Speed</label>
                        <label id="animation-speed" class="slidervalue"></label>
                        <div id="animation-speed-slider" class="slider-range-max"></div>
                        <div id="labelColorHolder clearfix">
                    </td>
                </tr>
                <tr>
                    <td>
                        <br><label for="gradient-category-drop-down" class="text">Gradient Category</label><br>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="gradient-category-drop-down" class="emperor-tab-drop-down"></select><br>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="trajectory-category-drop-down" class="text">Trajectory Category</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="trajectory-category-drop-down" class="emperor-tab-drop-down" onchange="colorAnimationsByCategoryChanged()"></select>
                    </td>
                </tr>
                <tr>
                    <td id="emperor-animation-color-selector">
                    </td>
                </tr>
            </table>
        </div>
        <div id="options" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr><td><div id="axeslabelscolor" class="colorbox" name="axeslabelscolor"></div></td><td title="Axes Labels Color">Axes Labels Color</td></tr>
                <tr><td><div id="axescolor" class="colorbox" name="axescolor"></div></td><td title="Axes Color Title">Axes Color</td></tr>
                <tr><td><div id="rendererbackgroundcolor" class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
                <tr><td colspan="2">
                        <div id="pcoaviewoptions" class="">
            <br>
            <label for="vectorsopacity" class="text">Vectors Opacity</label>
            <label id="vectorsopacity" class="slidervalue"></label>
            <div id="vopacityslider" class="slider-range-max"></div>
                            <form name="settingsoptionscolor">
                            </form>
                            <div id="pcoaoptions" class="">
                                <form name="settingsoptions">
                                    <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
                                </form>
                            </div>
                            <br><input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
                            <br><br>
                            <hr class='section-break'>
                            <br>Filename <small>(only letters, numbers, ., - and _)</small>:
                            <br><input name="saveas_name" id="saveas_name" value="screenshot" type="text"/>
                            <br><input id="saveas_legends" class="checkbox" type="checkbox" style=""> Create legend
                            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()"/>
                            <br><br>For a PNG, simply press 'ctrl+p'.
                            <div id="paralleloptions" class="">
                            </div>
                        </div>
                        <br>
                </td></tr>
            </table>
        </div>
    </div>  
</div>
</body>

</html>
"""

EXPECTED_FOOTER_E =\
"""document.getElementById("logo").style.display = 'none';
document.getElementById("logotable").style.display = 'none';

 </script>
</head>

<body>

<div id="overlay">
    <div>
    <img src="emperor_required_resources/img/emperor.png" alt="Emperor" id="small-logo"/>
        <h1>WebGL is not enabled!</h1>
        <p>Emperor's visualization framework is WebGL based, it seems that your system doesn't have this resource available. Here is what you can do:</p>
        <p id="explanation"><strong>Chrome:</strong> Type "chrome://flags/" into the address bar, then search for "Disable WebGL". Disable this option if you haven't already. <em>Note:</em> If you follow these steps and still don't see an image, go to "chrome://flags/" and then search for "Override software rendering list" and enable this option.</p>
        <p id="explanation"><strong>Safari:</strong> Open Safari's menu and select Preferences. Click on the advanced tab, and then check "Show Developer" menu. Then open the "Developer" menu and select "Enable WebGL".</p>
        <p id="explanation"><strong>Firefox:</strong> Go to Options through Firefox > Options or Tools > Options. Go to Advanced, then General. Check "Use hardware acceleration when available" and restart Firefox.</p>
        <p id="explanation"><strong>Other browsers:</strong> The only browsers that support WebGL are Chrome, Safari, and Firefox. Please switch to these browsers when using Emperor.</p>
        <p id="explanation"><em>Note:</em> Once you went through these changes, reload the page and it should work!</p>
        <p id="source">Sources: Instructions for <a href="https://www.biodigitalhuman.com/home/enabling-webgl.html">Chrome and Safari</a>, and <a href="http://www.infewbytes.com/?p=144">Firefox</a></p>
    </div>
</div>

<div id="emperor-plot-toggle">
    <form>
      <div id="plottype">
        <input id="pcoa" type="radio" id="pcoa" name="plottype" checked="checked" /><label for="pcoa">PCoA</label>
        <input id="parallel" type="radio" id="parallel" name="plottype" /><label for="parallel">Parallel</label>
      </div>
    </form>
</div>
<div id="pcoaPlotWrapper" class="emperor-plot-wrapper">
    <label id="pointCount" class="ontop">
    </label>

    <div id="finder" class="arrow-right">
    </div>

    <div id="labels" class="unselectable">
    </div>

    <div id="taxalabels" class="unselectable">
    </div>

    <div id="axislabels" class="axis-labels">
    </div>

    <div id="main-plot">
    </div>
</div>

<div id="parallelPlotWrapper" class="emperor-plot-wrapper">
</div>

<div id="emperor-separator" class="emperor-separator" ondblclick="separatorDoubleClick()"></div>

<div id="emperor-menu">
    <div id="emperor-menu-tabs">
        <ul>
            <li><a href="#keytab">Key</a></li>
            <li><a href="#colorby">Colors</a></li>
            <li><a href="#showby">Visibility</a></li>
            <li><a href="#scalingby">Scaling</a></li>
            <li><a href="#labelby">Labels</a></li>
            <li><a href="#axes">Axes</a></li>
            <li><a href="#animations">Animations</a></li>
            <li><a href="#options">Options</a></li>
        </ul>
        <div id="keytab" class="emperor-tab-div">
            <form name="keyFilter">
                <label>Filter  </label><input name="filterBox" id="searchBox" type="text" onkeyup="filterKey()"></input>
            </form>
            <div id="key">
            </div>
        </div>
        <div id="colorby" class="emperor-tab-div">
            <input type="checkbox" onchange="toggleContinuousAndDiscreteColors(this)" id="discreteorcontinuouscolors" name="discreteorcontinuouscolors">  Use gradient colors</input>
            <br><br>
            <select id="colorbycombo" onchange="colorByMenuChanged()" size="3" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="colorbylist">
            </div>
        </div>
        <div id="showby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="showbycombo" onchange="showByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="showbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereopacity" class="text">Global Sphere Opacity</label>
                        <label id="sphereopacity" class="slidervalue"></label>
                        <div id="sopacityslider" class="slider-range-max"></div>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <button id="toggle-visibility-selection-button" onClick="toggleVisibleCategories()">Invert Selected</button>
                    </td>
                </tr>
            </table>
        </div>
        <div id="scalingby" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr>
                    <td align="center">
                        <select id="scalingbycombo" onchange="scalingByMenuChanged()" class="emperor-tab-drop-down">
                        </select>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div class="list" id="scalingbylist" style="height:100%%;width:100%%">
                        </div>
                    </td>
                </tr>
                <tr>
                    <td style="padding-left: 12px; padding-right:12px;">
                        <hr class='section-break'>
                        <br>
                        <label for="sphereradius" class="text">Global Sphere Scale</label>
                        <label id="sphereradius" class="slidervalue"></label>
                        <div id="sradiusslider" class="slider-range-max"></div>
                    </td>
                </tr>
            </table>
        </div>
        <div id="labelby" class="emperor-tab-div">
            <div id="labels-top">
                <form name="plotoptions">
                    <input type="checkbox" onClick="toggleLabels()">Samples Label Visibility</input>
                </form>
                <br>
                <label for="labelopacity" class="text">Label Opacity</label>
                <label id="labelopacity" class="slidervalue"></label>
                <div id="lopacityslider" class="slider-range-max"></div>
                <div id="label-color-holder clearfix">
                    <table class="emperor-tab-table">
                        <tr><td><div id="labelColor" class="colorbox"></div></td><td><label>Master Label Color</label></td></tr>
                        <br><br>
                </table></div>
            </div>
            <br>
            <select id="labelcombo" onchange="labelMenuChanged()" class="emperor-tab-drop-down">
            </select>
            <div class="list" id="label-list">
            </div>
        </div>
        <div id="axes" class="emperor-tab-div">
            <div id="pcoaaxes">
                <div class="list" id="axeslist">
                </div>
            </div>
        </div>
        <div id="animations" class="emperor-tab-div">
            <table class="emperor-tab-table-with-sliders">
                <tr>
                    <td>
                        <a id="reset-button" class="media-button" href="javascript:void(0);" onclick="javascript:resetAnimation()"><img src="emperor_required_resources/img/reset.png" ></img></a>
                        <a id="play-button" class="media-button" href="javascript:void(0);" onclick="javascript:playAnimation()"><img src="emperor_required_resources/img/play.png"></img></a>
                        <a id="pause-button" class="media-button" href="javascript:void(0);" onclick="javascript:pauseAnimation()"><img src="emperor_required_resources/img/pause.png"></img></a>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="animation-speed" class="text">Speed</label>
                        <label id="animation-speed" class="slidervalue"></label>
                        <div id="animation-speed-slider" class="slider-range-max"></div>
                        <div id="labelColorHolder clearfix">
                    </td>
                </tr>
                <tr>
                    <td>
                        <br><label for="gradient-category-drop-down" class="text">Gradient Category</label><br>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="gradient-category-drop-down" class="emperor-tab-drop-down"></select><br>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="trajectory-category-drop-down" class="text">Trajectory Category</label>
                    </td>
                </tr>
                <tr>
                    <td>
                        <select id="trajectory-category-drop-down" class="emperor-tab-drop-down" onchange="colorAnimationsByCategoryChanged()"></select>
                    </td>
                </tr>
                <tr>
                    <td id="emperor-animation-color-selector">
                    </td>
                </tr>
            </table>
        </div>
        <div id="options" class="emperor-tab-div">
            <table class="emperor-tab-table">
                <tr><td><div id="axeslabelscolor" class="colorbox" name="axeslabelscolor"></div></td><td title="Axes Labels Color">Axes Labels Color</td></tr>
                <tr><td><div id="axescolor" class="colorbox" name="axescolor"></div></td><td title="Axes Color Title">Axes Color</td></tr>
                <tr><td><div id="rendererbackgroundcolor" class="colorbox" name="rendererbackgroundcolor"></div></td><td title="Background Color Title">Background Color</td></tr>
            <tr><td><div id="edgecolorselector_a" class="colorbox" name="edgecolorselector_a"></div></td><td title="edgecolor_a">Edge Color Selector A</td></tr>
            <tr><td><div id="edgecolorselector_b" class="colorbox" name="edgecolorselector_b"></div></td><td title="edgecolor_b">Edge Color Selector B</td></tr>

                <tr><td colspan="2">
                        <div id="pcoaviewoptions" class="">
            <br>
            <form name="edgesvisibility">
            <input type="checkbox" onClick="toggleEdgesVisibility()" checked>Edges Visibility</input>
            </form>
            <br>
                            <form name="settingsoptionscolor">
                            </form>
                            <div id="pcoaoptions" class="">
                                <form name="settingsoptions">
                                    <input type="checkbox" onchange="toggleScaleCoordinates(this)" id="scale_checkbox" name="scale_checkbox">Scale coords by percent explained</input>
                                </form>
                            </div>
                            <br><input id="reset" class="button" type="submit" value="Recenter Camera" style="" onClick="resetCamera()">
                            <br><br>
                            <hr class='section-break'>
                            <br>Filename <small>(only letters, numbers, ., - and _)</small>:
                            <br><input name="saveas_name" id="saveas_name" value="screenshot" type="text"/>
                            <br><input id="saveas_legends" class="checkbox" type="checkbox" style=""> Create legend
                            <input id="saveas" class="button" type="submit" value="Save as SVG" style="" onClick="saveSVG()"/>
                            <br><br>For a PNG, simply press 'ctrl+p'.
                            <div id="paralleloptions" class="">
                            </div>
                        </div>
                        <br>
                </td></tr>
            </table>
        </div>
    </div>  
</div>
</body>

</html>
"""

if __name__ == "__main__":
    main()
