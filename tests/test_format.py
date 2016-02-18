# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from numpy import array
from emperor.format import (format_pcoa_to_js, format_mapping_file_to_js,
                            format_taxa_to_js, format_vectors_to_js,
                            format_emperor_html_footer_string,
                            EmperorLogicError, format_comparison_bars_to_js,
                            format_emperor_autograph)
from _test_format_strings import (PCOA_JS, PCOA_JS_CUSTOM_AXES,
                                  PCOA_JS_JACKKNIFED, PCOA_JS_SEGMENTS,
                                  MAPPING_FILE_JS,
                                  MAPPING_FILE_JS_WITH_ANIMATABLE_CATEGORIES,
                                  TAXA_JS_STRING, VECTOR_JS_STRING_NO_SORTING,
                                  VECTOR_JS_STRING_SORTING,
                                  COMPARISON_JS_STRING,
                                  COMPARISON_JS_STRING_NON_SERIAL,
                                  COMPARISON_COORDS_HEADERS_ZERO,
                                  EXPECTED_FOOTER_A, EXPECTED_FOOTER_B,
                                  EXPECTED_FOOTER_C, EXPECTED_FOOTER_D,
                                  EXPECTED_FOOTER_E)
from unittest import TestCase, main


class TopLevelTests(TestCase):

    def setUp(self):
        self.pcoa_pct_var = array([2.66887049e+01, 1.62563704e+01,
                                   1.37754129e+01, 1.12172158e+01,
                                   1.00247750e+01, 8.22835130e+00,
                                   7.55971174e+00, 6.24945796e+00,
                                   1.17437419e-14])
        self.pcoa_pct_var_really_low = array([2.66887049e+01, 1.62563704e+01,
                                              0.001, 0.0001, 0.0019, 0.0018,
                                              0.0017, 0.0016, 0.0015])
        self.pcoa_headers = ['PC.355', 'PC.607', 'PC.634', 'PC.635', 'PC.593',
                             'PC.636', 'PC.481', 'PC.354', 'PC.356']
        self.pcoa_coords = PCOA_DATA
        self.pcoa_eigen_values = array([4.79412119e-01, 2.92014956e-01,
                                        2.47449246e-01, 2.01496072e-01,
                                        1.80076128e-01, 1.47806773e-01,
                                        1.35795927e-01, 1.12259696e-01,
                                        2.10954117e-16])

        # data specific for testing the jackknifing
        self.pcoa_jk_headers = ['PC.355', 'PC.607', 'PC.634', 'PC.635']
        self.pcoa_jk_coords = array([[0.3, 0.5, 0.1, 0.3],
                                     [1.1, 1.1, 1.0, 0.8],
                                     [0.1, 3.3, 5.5, 0.1],
                                     [1.0, 2.0, 1.0, 1.0]])
        self.pcoa_jk_eigen_values = array([0.45, 0.32, 0.21, 0.02])
        self.pcoa_jk_pct_var = array([44, 40, 15, 1])
        self.pcoa_jk_coords_low = array([[0.2, 0.3, 0.1, 0.3],
                                         [1.1, 0.1, 0.0, 0.3],
                                         [0.6, 3.1, 1.5, 0.1],
                                         [0.023, 1.0, 0.01, 1.0]])
        self.pcoa_jk_coords_high = array([[0.6, 0.8, 0.9, 0.31],
                                          [1, 2.1, 0.0, 0.8],
                                          [0.9, 3.7, 5.5, 0.1111],
                                          [0.01222, 2.0, 0.033, 2.0]])

        self.mapping_file_data = MAPPING_FILE_DATA
        self.mapping_file_headers = ['SampleID', 'BarcodeSequence',
                                     'LinkerPrimerSequence', 'Treatment',
                                     'DOB', 'Description']
        self.good_columns = ['Treatment', 'LinkerPrimerSequence']
        self.columns_with_gradients = ['Treatment', 'LinkerPrimerSequence',
                                       'DOB']

        self.otu_coords = array([[2.80399118e-01, -6.01282860e-03,
                                  2.34854344e-02, -4.68109475e-02,
                                  -1.46624450e-01, 5.66979125e-03,
                                  -3.54299634e-02, -2.55785794e-01,
                                  -4.84141987e-09],
                                 [2.28820400e-01, -1.30142097e-01,
                                  -2.87149448e-01, 8.64498846e-02,
                                  4.42951919e-02, 2.06042607e-01,
                                  3.10003571e-02, 7.19920437e-02,
                                  -4.84141987e-09],
                                 [-9.13299284e-02, 4.24147148e-01,
                                  -1.35627421e-01, -5.75194809e-02,
                                  1.51363491e-01, -2.53935676e-02,
                                  5.17306152e-02, -3.87382176e-02,
                                  -4.84141987e-09],
                                 [-2.76542164e-01, -1.44964375e-01,
                                  6.66467344e-02, -6.77109454e-02,
                                  1.76070270e-01, 7.29693901e-02,
                                  -2.29889464e-01, -4.65989417e-02,
                                  -4.84141987e-09]])
        self.lineages = ['Root;k__Bacteria;p__Firmicutes',
                         'Root;k__Bacteria;p__Bacteroidetes',
                         'Root;k__Bacteria;p__Tenericutes',
                         'Root;k__Bacteria;Other']
        self.prevalence = array([1., 0.66471926, 0.08193196, 0.04374296])

        # comparison test
        self.comparison_coords_data = \
            array([[-0.0677, -2.036, 0.2726, 1.051, -0.180, -0.698],
                   [-1.782, -0.972, 0.1582, -1.091, 0.531, 0.292],
                   [-0.659, -0.2566, 0.514, -2.698, -0.393, 0.420],
                   [-1.179, -0.968, 2.525, 0.53, -0.529, 0.632],
                   [-0.896, -1.765, 0.274, -0.3235, 0.4009, -0.03497],
                   [-0.0923, 1.414, -0.622, 0.298, 0.5, -0.4580],
                   [-0.972, 0.551, 1.144, 0.3147, -0.476, -0.4279],
                   [1.438, -2.603, -1.39, 1.300, -0.1606, 1.260],
                   [-0.356, 0.0875, 0.772, 0.539, -0.586, -1.431],
                   [1.512, -1.239, -0.0365, -0.682, -0.971, 0.356],
                   [1.17, 1.31, -1.407, 1.6, 0.60, 2.26],
                   [2.618, 0.739, -0.01295, -0.937, 3.079, -2.534],
                   [0.2339, -0.880, -1.753, 0.177, 0.3517, -0.743],
                   [0.436, 2.12, -0.935, -0.476, -0.805, 0.4164],
                   [-0.880, 1.069, 1.069, -0.596, -0.199, 0.306],
                   [0.294, 0.2988, 0.04670, -0.3865, 0.460, -0.431],
                   [1.640, 0.2485, -0.354, 1.43, 1.226, 1.095],
                   [0.821, -1.13, -1.794, -1.171, -1.27, -0.842]])
        self.comparison_coords_headers = ['sampa_0', 'sampb_0', 'sampc_0',
                                          'sampd_0', 'sampe_0', 'sampf_0',
                                          'sampa_1', 'sampb_1', 'sampc_1',
                                          'sampd_1', 'sampe_1', 'sampf_1',
                                          'sampa_2', 'sampb_2', 'sampc_2',
                                          'sampd_2', 'sampe_2', 'sampf_2']
        self.comparison_coords_headers_zero = ['sampa0_0', 'sampb0_0',
                                               'sampc0_0', 'sampd00_0',
                                               'sampe00_0', 'sampf00_0',
                                               'sampa0_1', 'sampb0_1',
                                               'sampc0_1', 'sampd00_1',
                                               'sampe00_1', 'sampf00_1',
                                               'sampa0_2', 'sampb0_2',
                                               'sampc0_2', 'sampd00_2',
                                               'sampe00_2', 'sampf00_2']

    def test_format_pcoa_to_js(self):
        """Test correct formatting of the PCoA file"""
        # test the case with only points and nothing else
        out_js_pcoa_string = \
            format_pcoa_to_js(self.pcoa_headers, self.pcoa_coords,
                              self.pcoa_pct_var)
        self.assertEquals(out_js_pcoa_string, PCOA_JS)

        # test custom axes and the labels
        out_js_pcoa_string = \
            format_pcoa_to_js(self.pcoa_headers, self.pcoa_coords,
                              self.pcoa_pct_var,
                              custom_axes=['Instant'])
        self.assertEquals(out_js_pcoa_string, PCOA_JS_CUSTOM_AXES)

        # test jackknifed pcoa plots
        out_js_pcoa_string = \
            format_pcoa_to_js(self.pcoa_jk_headers, self.pcoa_jk_coords,
                              self.pcoa_jk_pct_var,
                              coords_low=self.pcoa_jk_coords_low,
                              coords_high=self.pcoa_jk_coords_high)
        self.assertEquals(out_js_pcoa_string, PCOA_JS_JACKKNIFED)

        # check it raises an exception when the variation explained on the
        # axes is not greater than 0.01 for at least three of them
        self.assertRaises(EmperorLogicError, format_pcoa_to_js,
                          self.pcoa_headers, self.pcoa_coords,
                          self.pcoa_pct_var_really_low)

        # test segments
        out_js_pcoa_string = \
            format_pcoa_to_js(self.pcoa_jk_headers, self.pcoa_jk_coords,
                              self.pcoa_jk_pct_var,
                              coords_low=self.pcoa_jk_coords_low,
                              coords_high=self.pcoa_jk_coords_high,
                              number_of_segments=14)
        self.assertEquals(out_js_pcoa_string, PCOA_JS_SEGMENTS)

    def test_format_mapping_file_to_js(self):
        """Tests correct formatting of the metadata mapping file"""

        # regular case, no categories that can be animated
        out_js_mapping_file_string = format_mapping_file_to_js(
            self.mapping_file_data, self.mapping_file_headers,
            self.good_columns)
        self.assertEquals(out_js_mapping_file_string, MAPPING_FILE_JS)

        # case with categories that can be animated i. e. that work as
        # gradients
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
                                                    self.mapping_file_headers,
                                                    self.pcoa_coords,
                                                    self.pcoa_headers, None,
                                                    None)
        self.assertEquals(out_js_vector_string, '\nvar g_vectorPositions = new'
                          ' Array();\n')

        # vector string without sorting for the coordinates
        out_js_vector_string = format_vectors_to_js(self.mapping_file_data,
                                                    self.mapping_file_headers,
                                                    self.pcoa_coords,
                                                    self.pcoa_headers,
                                                    'Treatment', None)
        self.assertEquals(out_js_vector_string, VECTOR_JS_STRING_NO_SORTING)

        # vector string sorting by the DOB category
        out_js_vector_string = format_vectors_to_js(self.mapping_file_data,
                                                    self.mapping_file_headers,
                                                    self.pcoa_coords,
                                                    self.pcoa_headers,
                                                    'Treatment', 'DOB')
        self.assertEquals(out_js_vector_string, VECTOR_JS_STRING_SORTING)

    def test_format_comparison_bars_to_js(self):
        """Check the correct strings are created for the two types of inputs"""

        # empty string generation for comparison i. e. no clones
        out_js_comparison_string = \
            format_comparison_bars_to_js(self.comparison_coords_data,
                                         self.comparison_coords_headers, 0,
                                         True)
        self.assertEquals(out_js_comparison_string, '\nvar '
                          'g_comparisonPositions = new Array();\nvar '
                          'g_isSerialComparisonPlot = true;\n')

        out_js_comparison_string = \
            format_comparison_bars_to_js(self.comparison_coords_data,
                                         self.comparison_coords_headers, 3,
                                         True)
        self.assertEquals(out_js_comparison_string, COMPARISON_JS_STRING)

        # empty string generation for comparison i. e. no clones
        out_js_comparison_string = \
            format_comparison_bars_to_js(self.comparison_coords_data,
                                         self.comparison_coords_headers, 0,
                                         False)
        self.assertEquals(out_js_comparison_string, '\nvar '
                          'g_comparisonPositions = new Array();\nvar '
                          'g_isSerialComparisonPlot = false;\n')

        out_js_comparison_string = format_comparison_bars_to_js(
            self.comparison_coords_data, self.comparison_coords_headers, 3,
            False)
        self.assertEquals(out_js_comparison_string,
                          COMPARISON_JS_STRING_NON_SERIAL)

        out_js_comparison_string = format_comparison_bars_to_js(
            self.comparison_coords_data, self.comparison_coords_headers_zero,
            3, False)
        self.assertEquals(out_js_comparison_string,
                          COMPARISON_COORDS_HEADERS_ZERO)

    def test_format_comparison_bars_to_js_exceptions(self):
        """Check the correct exceptions are raised for incorrect inputs"""

        # assertion for wrong length in headers
        self.assertRaises(AssertionError, format_comparison_bars_to_js, [],
                          self.comparison_coords_data, 3)

        # assertion for wrong length in coords data
        self.assertRaises(AssertionError, format_comparison_bars_to_js,
                          self.comparison_coords_headers,
                          self.comparison_coords_data[1::], 3)

        # assertion for wrong number of clones and elements
        self.assertRaises(AssertionError, format_comparison_bars_to_js,
                          self.comparison_coords_headers,
                          self.comparison_coords_data, 11)

    def test_format_emperor_html_footer_string(self):
        """Test correct formatting of the footer string"""
        self.maxDiff = 5000

        # footer for a jackknifed pcoa plot without biplots
        out_string = format_emperor_html_footer_string(False, True)
        self.assertItemsEqual(out_string.split('\n'),
                              EXPECTED_FOOTER_A.split('\n'))
        self.assertEqual(out_string, EXPECTED_FOOTER_A)

        # footer for biplots without jackknifing
        out_string = format_emperor_html_footer_string(True, False)
        self.assertItemsEqual(out_string.split('\n'),
                              EXPECTED_FOOTER_B.split('\n'))
        self.assertEqual(out_string, EXPECTED_FOOTER_B)

        # no biplots nor jackknifing
        out_string = format_emperor_html_footer_string(False, False)
        self.assertItemsEqual(out_string.split('\n'),
                              EXPECTED_FOOTER_C.split('\n'))
        self.assertEqual(out_string, EXPECTED_FOOTER_C)

        #  no biplots no jackknifing but with vectors
        out_string = format_emperor_html_footer_string(False, False, True)
        self.assertItemsEqual(out_string.split('\n'),
                              EXPECTED_FOOTER_D.split('\n'))
        self.assertEqual(out_string, EXPECTED_FOOTER_D)

        # comparison plot
        out_string = format_emperor_html_footer_string(False, False,
                                                       False, True)
        self.assertItemsEqual(out_string.split('\n'),
                              EXPECTED_FOOTER_E.split('\n'))
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
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
                                             'pcoa_unweighted_unifrac.txt',
                                             'Python')
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
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
                                             'pcoa_unweighted_unifrac.txt',
                                             'C')
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
        self.assertTrue("Command executed on " in autograph)

        autograph = format_emperor_autograph('mapping_file.txt',
                                             'pcoa_unweighted_unifrac.txt',
                                             'Bash')
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
        self.assertTrue("Command executed on " in autograph)

        # haskell and cobol are ... not supported
        self.assertRaises(AssertionError, format_emperor_autograph,
                          'mapping_file.txt', 'pcoa.txt', 'Haskell')
        self.assertRaises(AssertionError, format_emperor_autograph,
                          'mapping_file.txt', 'pcoa.txt', 'Cobol')


PCOA_DATA = array([[-1.09166142e-01, 8.77774496e-02, 1.15866606e-02,
                    -6.26863896e-02, 2.31533068e-02, 8.76934639e-02,
                    1.37400927e-03, -1.35496063e-05, 1.29849404e-09],
                   [6.88959784e-02, -1.66234067e-01, -9.98300962e-02,
                    -2.90522450e-02, 5.05569953e-02, -2.95200038e-03,
                    -3.25863204e-02, -2.17218431e-02, 1.29849404e-09],
                   [2.04684540e-01, 1.28911236e-01, -2.93614192e-02,
                    1.07657904e-01, 1.78480761e-02, 7.97778676e-03,
                    -2.92003235e-02, -1.23468947e-03, 1.29849404e-09],
                   [1.26131510e-01, -2.66030272e-03, -1.41717093e-01,
                    -9.71089687e-03, -6.94272590e-02, 3.67235068e-03,
                    4.29867599e-02, 6.44276242e-03, 1.29849404e-09],
                   [9.68466168e-02, -1.59388265e-01, 1.35271607e-01,
                    5.12015857e-02, -2.02552984e-02, 3.07034843e-02,
                    1.55159338e-02, 1.42426937e-02, 1.29849404e-09],
                   [2.81534642e-01, 7.10660196e-02, 9.71542020e-02,
                    -8.06472757e-02, 7.04245456e-03, -4.53133767e-02,
                    6.55825124e-03, -1.26412251e-02, 1.29849404e-09],
                   [-1.92382819e-01, 1.47832029e-02, -1.47871039e-02,
                    1.90888050e-02, 7.26409669e-02, -3.73008815e-02,
                    3.94304860e-02, 3.25351917e-02, 1.29849404e-09],
                   [-2.93353176e-01, 1.83956004e-02, 3.29884266e-02,
                    3.15360631e-02, -2.86943531e-02, -1.94225139e-02,
                    8.06272805e-03, -5.58094095e-02, 1.29849404e-09],
                   [-1.83191151e-01, 34912621e-03, 8.69481594e-03,
                    -2.73875510e-02, -5.28648893e-02, -2.50583131e-02,
                    -5.21415245e-02, 3.82000689e-02, 1.29849404e-09]])

MAPPING_FILE_DATA = [['PC.354', 'AGCACGAGCCTA', 'YATGCTGCCTCCCGTAGGAGT',
                      'Control', '20061218', 'Control_mouse_I.D._354'],
                     ['PC.355', 'AACTCGTCGATG', 'YATGCTGCCTCCCGTAGGAGT',
                      'Control', '20061218', 'Control_mouse_I.D._355'],
                     ['PC.356', 'ACAGACCACTCA', 'YATGCTGCCTCCCGTAGGAGT',
                      'Control', '20061126', 'Control_mouse_I.D._356'],
                     ['PC.481', 'ACCAGCGACTAG', 'YATGCTGCCTCCCGTAGGAGT',
                      'Control', '20070314', 'Control_mouse_I.D._481'],
                     ['PC.593', 'AGCAGCACTTGT', 'YATGCTGCCTCCCGTAGGAGT',
                      'Control', '20071210', 'Control_mouse_I.D._593'],
                     ['PC.607', 'AACTGTGCGTAC', 'YATGCTGCCTCCCGTAGGAGT',
                      'Fast', '20071112', 'Fasting_mouse_I.D._607'],
                     ['PC.634', 'ACAGAGTCGGCT', 'YATGCTGCCTCCCGTAGGAGT',
                      'Fast', '20080116', 'Fasting_mouse_I.D._634'],
                     ['PC.635', 'ACCGCAGAGTCA', 'YATGCTGCCTCCCGTAGGAGT',
                      'Fast', '20080116', 'Fasting_mouse_I.D._635'],
                     ['PC.636', 'ACGGTGAGTGTC', 'YATGCTGCCTCCCGTAGGAGT',
                      'Fast', '20080116', 'Fasting_mouse_I.D._636']]


if __name__ == "__main__":
    main()
