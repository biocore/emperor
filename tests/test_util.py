# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main
from os.path import exists, join
from shutil import rmtree
from tempfile import gettempdir

import pandas as pd
import warnings
from numpy import array
from numpy.testing import assert_almost_equal

from emperor.util import (
                          preprocess_coords_file,
                          nbinstall, validate_and_process_custom_axes,
                          resolve_stable_url, EmperorWarning)


warnings.simplefilter('always', category=EmperorWarning)


class TopLevelTests(TestCase):

    def setUp(self):
        self.files_to_delete = []

        self.mapping_file_data = MAPPING_FILE_DATA
        self.mapping_file_headers = ['SampleID', 'BarcodeSequence',
                                     'LinkerPrimerSequence', 'Treatment',
                                     'DOB', 'Description']
        self.valid_columns = ['Treatment', 'DOB']
        self.support_files_filename = gettempdir()
        self.support_files_filename_spaces = join(
            gettempdir(), 'Directory With Spaces/AndNoSpaces')

        # data for the custom axes, contains columns that are gradients
        self.mapping_file_data_gradient = MAPPING_FILE_DATA_GRADIENT
        self.mapping_file_headers_gradient = ['SampleID', 'Treatment', 'Time',
                                              'Weight', 'Description']

        self.coords_header = ['PC.355', 'PC.635', 'PC.636', 'PC.354']
        self.coords_data = COORDS_DATA
        self.coords_eigenvalues = array([1, 2, 3, 4])
        self.coords_pct = array([40, 30, 20, 10])

        # jackknifed test data
        self.jk_mapping_file_headers = ['SampleID', 'C2', 'C3', 'C4']
        self.jk_mapping_file_data = [['1', 'a', 'b', 'c'],
                                     ['2', 'd', 'e', 'f'],
                                     ['3', 'g', 'h', 'i']]
        self.jk_coords_header = [['1', '2', '3'], ['1', '2', '3'],
                                 ['1', '2', '3'], ['1', '2', '3']]
        self.jk_coords_data = [
            array([[1.2, 0.1, -1.2], [-2.5, -4.0, 4.5]]),
            array([[-1.4, 0.05, 1.3], [2.6, 4.1, -4.7]]),
            array([[-1.5, 0.05, 1.6], [2.4, 4.0, -4.8]]),
            array([[-1.5, 0.05, 1.6], [2.4, 4.0, -4.8]])]
        self.jk_coords_eigenvalues = [
            array([0.80, .11, 0.09]),
            array([0.76, .20, 0.04]),
            array([0.84, .14, 0.02]),
            array([0.84, .11, 0.05])]
        self.jk_coords_pcts = [
            array([0.80, .10, 0.10]),
            array([0.76, .21, 0.03]),
            array([0.84, .11, 0.05]),
            array([0.84, .15, 0.01])]

        self.jk_mapping_file_data_gradient = MAPPING_FILE_DATA_GRADIENT
        self.jk_mapping_file_headers_gradient = ['SampleID', 'Treatment',
                                                 'Time', 'Weight',
                                                 'Description']
        self.jk_coords_header_gradient = [
            ['PC.354', 'PC.355', 'PC.635', 'PC.636'],
            ['PC.354', 'PC.355', 'PC.635', 'PC.636'],
            ['PC.354', 'PC.355', 'PC.635', 'PC.636'],
            ['PC.354', 'PC.355', 'PC.635', 'PC.636']]
        self.jk_coords_data_gradient = [
            array([[1.2, 0.1, -1.2, 1.1],
                   [-2.5, -4.0, 4.5, 0.3],
                   [.5, -0.4, 3.5, 1.001],
                   [0.67, 0.23, 1.01, 2.2]]),
            array([[1.2, 1, -0.2, 0.1],
                   [-2.5, -4.0, 4.5, 3.2],
                   [.5, -0.4, 3.5, 1.00],
                   [0.57, 0.27, 0.95, 2.1]]),
            array([[1.0, 1, -1.2, 1.1],
                   [-2.1, -2.0, 3.5, 0.3],
                   [.5, 3, 3.5, 2],
                   [0.60, 0.33, 1.3, 2.0]]),
            array([[1.2, 0.1, -1.2, 1.1],
                   [-2.5, -4.0, 4.5, 0.3],
                   [.5, -0.4, 3.5, 1.001],
                   [0.69, 0.20, 1.01, 2.2]])]
        self.jk_coords_eigenvalues_gradient = [
            array([0.80, .11, 0.09, 0.0]),
            array([0.76, .20, 0.04, 0.0]),
            array([0.84, .14, 0.02, 0.0]),
            array([0.84, .11, 0.05, 0.0])]
        self.jk_coords_pcts_gradient = [
            array([0.80, .10, 0.10, 0.0]),
            array([0.76, .21, 0.03, 0.0]),
            array([0.84, .11, 0.05, 0.0]),
            array([0.84, .15, 0.01, 0])]

        self.broken_mapping_file_data = BROKEN_MAPPING_FILE
        self.broken_mapping_file_data_2_values = BROKEN_MAPPING_FILE_2_VALUES

    def tearDown(self):
        for f in self.files_to_delete:
            rmtree(f)

    def test_preprocess_coords_file(self):
        """Check correct processing is applied to the coords"""

        # case with custom axes
        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high, o_clones = preprocess_coords_file(
                self.coords_header, self.coords_data, self.coords_eigenvalues,
                self.coords_pct, self.mapping_file_headers_gradient,
                self.mapping_file_data_gradient, ['Time'])

        expected_coords_data = array(
            [[0.03333333, -0.2, -0.1, 0.06, -0.06],
             [0.03333333, -0.3, 0.04, -0.1, 0.15],
             [0.2, 0.1, -0.1, -0.2, 0.08],
             [-0.3, 0.04, -0.01,  0.06, -0.34]])

        self.assertEqual(out_coords_header, self.coords_header)
        self.assertEqual(out_coords_high, None)
        self.assertEqual(out_coords_low, None)
        assert_almost_equal(self.coords_eigenvalues, array([1, 2, 3, 4]))
        assert_almost_equal(self.coords_pct, array([40, 30, 20, 10]))
        self.assertEqual(o_clones, 0)

        # check each individual value because currently cogent assertEquals
        # fails when comparing the whole matrix at once
        for out_el, exp_el in zip(out_coords_data, expected_coords_data):
            for out_el_sub, exp_el_sub in zip(out_el, exp_el):
                self.assertAlmostEqual(out_el_sub, exp_el_sub)

        # case for jackknifing, based on qiime/tests/test_util.summarize_pcoas
        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high, o_clones = preprocess_coords_file(
                self.jk_coords_header, self.jk_coords_data,
                self.jk_coords_eigenvalues, self.jk_coords_pcts,
                self.jk_mapping_file_headers, self.jk_mapping_file_data,
                jackknifing_method='sdev', pct_variation_below_one=True)

        self.assertEqual(out_coords_header, ['1', '2', '3'])
        assert_almost_equal(out_coords_data, array([[1.4, -0.0125, -1.425],
                                                    [-2.475, -4.025, 4.7]]))
        assert_almost_equal(out_eigenvals, array([0.81, 0.14, 0.05]))
        assert_almost_equal(out_pcts, array([0.8, 0.1, 0.1]))
        self.assertEqual(o_clones, 0)

        # test the coords are working fine
        assert_almost_equal(out_coords_low,
                            array([[-0.07071068, -0.0375, -0.10307764],
                                   [-0.04787136, -0.025, -0.07071068]]))
        assert_almost_equal(out_coords_high,
                            array([[0.07071068, 0.0375, 0.10307764],
                                   [0.04787136, 0.025, 0.07071068]]))

        # test custom axes and jackknifed plots
        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high, o_clones = preprocess_coords_file(
                self.jk_coords_header_gradient, self.jk_coords_data_gradient,
                self.jk_coords_eigenvalues_gradient,
                self.jk_coords_pcts_gradient,
                self.jk_mapping_file_headers_gradient,
                self.jk_mapping_file_data_gradient, custom_axes=['Time'],
                jackknifing_method='sdev', pct_variation_below_one=True)

        self.assertEqual(out_coords_header,
                         ['PC.354', 'PC.355', 'PC.635', 'PC.636'])
        assert_almost_equal(out_coords_data,
                            array([[-2.4, 1.15, 0.55, -0.95, 0.85],
                                   [0.73333333, -2.4, -3.5, 4.25, 1.025],
                                   [0.73333333, 0.5, 0.45, 3.5, 1.2505],
                                   [2.3, 0.6325, 0.2575, 1.0675, 2.125]]))
        assert_almost_equal(out_eigenvals, array([0.81, 0.14, 0.05, 0.]))
        assert_almost_equal(out_pcts, array([0.8, 0.1, 0.1, 0.]))

        # test the coords are working fine
        assert_almost_equal(
            out_coords_low,
            array([[0., -0.05, -0.25980762, -0.25, -0.25],
                   [0., -0.1, -0.5, -0.25, -0.725],
                   [0., -0., -0.85, -0., -0.24983344],
                   [0., -0.0283945, -0.02809953, -0.07877976, -0.04787136]]))
        assert_almost_equal(
            out_coords_high,
            array([[1.00000000e-05, 5.0000000e-02, 2.59807621e-01,
                    2.50000000e-01, 2.50000000e-01],
                   [1.00000000e-05, 1.0000000e-01, 5.00000000e-01,
                    2.50000000e-01, 7.25000000e-01],
                   [1.00000000e-05, 0.0, 8.50000000e-01, 0.00000000e+00,
                    2.49833445e-01],
                   [1.00000000e-05, 2.83945417e-02, 2.80995255e-02,
                    7.87797563e-02, 4.78713554e-02]]))
        self.assertEqual(o_clones, 0)

        # test that pct_variation_below_one is working
        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high, o_clones = preprocess_coords_file(
                self.jk_coords_header_gradient, self.jk_coords_data_gradient,
                self.jk_coords_eigenvalues_gradient,
                self.jk_coords_pcts_gradient,
                self.jk_mapping_file_headers_gradient,
                self.jk_mapping_file_data_gradient, custom_axes=['Time'],
                jackknifing_method='sdev', pct_variation_below_one=False)

        self.assertEqual(out_coords_header,
                         ['PC.354', 'PC.355', 'PC.635', 'PC.636'])
        assert_almost_equal(
            out_coords_data,
            array([[-2.4, 1.15, 0.55, -0.95, 0.85],
                   [0.73333333, -2.4, -3.5, 4.25, 1.025],
                   [0.73333333, 0.5, 0.45, 3.5, 1.2505],
                   [2.3, 0.6325, 0.2575, 1.0675, 2.125]]))
        assert_almost_equal(out_eigenvals, array([0.81, 0.14, 0.05, 0.]))
        assert_almost_equal(out_pcts, array([80, 10, 10, 0]))

    def test_preprocess_coords_file_comparison(self):
        """Check the cases for comparisons plots and the special usages"""
        # shouldn't allow a comparison computation with only one file
        self.assertRaises(
            AssertionError, preprocess_coords_file,
            self.coords_header, self.coords_data, self.coords_eigenvalues,
            self.coords_pct, self.mapping_file_headers_gradient,
            self.mapping_file_data_gradient, None, None, True)

        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high, o_clones = preprocess_coords_file(
                self.jk_coords_header, self.jk_coords_data,
                self.jk_coords_eigenvalues, self.jk_coords_pcts,
                self.jk_mapping_file_headers, self.jk_mapping_file_data,
                is_comparison=True, pct_variation_below_one=True)

        self.assertEqual(out_coords_header,
                         ['1_0', '2_0', '3_0', '1_1', '2_1', '3_1', '1_2',
                          '2_2', '3_2', '1_3', '2_3', '3_3'])
        assert_almost_equal(
            out_coords_data,
            array([[1.2, 0.1, -1.2],
                   [-2.5, -4., 4.5],
                   [-1.4, 0.05, 1.3],
                   [2.6, 4.1, -4.7],
                   [-1.5, 0.05, 1.6],
                   [2.4, 4., -4.8],
                   [-1.5, 0.05, 1.6],
                   [2.4, 4., -4.8]]))
        assert_almost_equal(out_eigenvals, self.jk_coords_eigenvalues[0])
        assert_almost_equal(out_pcts, self.jk_coords_pcts[0])
        self.assertEqual(out_coords_low, None)
        self.assertEqual(out_coords_high, None)
        self.assertEqual(o_clones, 4)

    def test_nbinstall(self):
        temp_dir = gettempdir()
        target_path = join(temp_dir, 'share/jupyter/nbextensions/emperor/'
                           'support_files')

        # remove the whole tree
        self.files_to_delete.append(join(temp_dir, 'share'))

        nbinstall(prefix=temp_dir, user=None)

        self.assertTrue(exists(target_path))

    def test_custom_axes(self):
        columns = ['SampleID', 'BarcodeSequence', 'LinkerPrimerSequence',
                   'Treatment', 'DOB', 'Description']
        mf = pd.DataFrame(data=MAPPING_FILE_DATA, columns=columns)
        obs = validate_and_process_custom_axes(mf, ['DOB'])
        exp = pd.DataFrame(data=MAPPING_FILE_DATA_CONVERTED, columns=columns)
        pd.util.testing.assert_frame_equal(obs, exp)

    def test_custom_axes_non_existent_names(self):
        columns = ['SampleID', 'BarcodeSequence', 'LinkerPrimerSequence',
                   'Treatment', 'DOB', 'Description']
        mf = pd.DataFrame(data=MAPPING_FILE_DATA, columns=columns)

        with self.assertRaises(KeyError):
            validate_and_process_custom_axes(mf, [':L'])

        with self.assertRaises(KeyError):
            validate_and_process_custom_axes(mf, ['D0B'])

    def test_custom_axes_non_numeric_values(self):
        columns = ['SampleID', 'BarcodeSequence', 'LinkerPrimerSequence',
                   'Treatment', 'DOB', 'Description']
        mf = pd.DataFrame(data=MAPPING_FILE_DATA, columns=columns)

        with self.assertRaises(ValueError):
            validate_and_process_custom_axes(mf, ['Treatment'])

        with self.assertRaises(ValueError):
            validate_and_process_custom_axes(mf, ['SampleID'])

    def test_custom_axes_non_numeric_values_mixed(self):
        columns = ['SampleID', 'huey', 'dewey', 'louie', 'Description']
        mf = pd.DataFrame(data=BROKEN_MAPPING_FILE, columns=columns)

        with self.assertRaises(ValueError):
            validate_and_process_custom_axes(mf, ['louie'])

        with self.assertRaises(ValueError):
            validate_and_process_custom_axes(mf, ['louie', 'dewey'])

    def test_resolve_stable_url_release(self):
        # we test that no warnings are raised
        url = 'https://github.com/biocore/emperor/%s/emperor/support_files'
        with warnings.catch_warnings(record=True) as w:
            obs = resolve_stable_url('1.0.0b7', url)
            self.assertTrue(len(w) == 0)
            self.assertEqual(obs, url % '1.0.0-beta.7')

    def test_resolve_stable_url_release_check_warning(self):
        url = 'https://github.com/biocore/emperor/%s/emperor/support_files'
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            obs = resolve_stable_url('1.0.0b7-dev', url)

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, EmperorWarning))
            self.assertEqual(obs, url % 'new-api')

    def test_resolve_stable_url_release_number_check_warning(self):
        url = 'https://github.com/biocore/emperor/%s/emperor/support_files'
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            obs = resolve_stable_url('1.0.0b7-dev0', url)

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, EmperorWarning))
            self.assertEqual(obs, url % 'new-api')


MAPPING_FILE_DATA = [
    ['PC.354', 'AGCACGAGCCTA', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218',
     'Control_mouse_I.D._354'],
    ['PC.355', 'AACTCGTCGATG', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218',
     'Control_mouse_I.D._355'],
    ['PC.356', 'ACAGACCACTCA', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126',
     'Control_mouse_I.D._356'],
    ['PC.481', 'ACCAGCGACTAG', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314',
     'Control_mouse_I.D._481'],
    ['PC.593', 'AGCAGCACTTGT', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210',
     'Control_mouse_I.D._593'],
    ['PC.607', 'AACTGTGCGTAC', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112',
     'Fasting_mouse_I.D._607'],
    ['PC.634', 'ACAGAGTCGGCT', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116',
     'Fasting_mouse_I.D._634'],
    ['PC.635', 'ACCGCAGAGTCA', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116',
     'Fasting_mouse_I.D._635'],
    ['PC.636', 'ACGGTGAGTGTC', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116',
     'Fasting_mouse_I.D._636']]

MAPPING_FILE_DATA_CONVERTED = [
    ['PC.354', 'AGCACGAGCCTA', 'YATGCTGCCTCCCGTAGGAGT', 'Control', 20061218,
     'Control_mouse_I.D._354'],
    ['PC.355', 'AACTCGTCGATG', 'YATGCTGCCTCCCGTAGGAGT', 'Control', 20061218,
     'Control_mouse_I.D._355'],
    ['PC.356', 'ACAGACCACTCA', 'YATGCTGCCTCCCGTAGGAGT', 'Control', 20061126,
     'Control_mouse_I.D._356'],
    ['PC.481', 'ACCAGCGACTAG', 'YATGCTGCCTCCCGTAGGAGT', 'Control', 20070314,
     'Control_mouse_I.D._481'],
    ['PC.593', 'AGCAGCACTTGT', 'YATGCTGCCTCCCGTAGGAGT', 'Control', 20071210,
     'Control_mouse_I.D._593'],
    ['PC.607', 'AACTGTGCGTAC', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', 20071112,
     'Fasting_mouse_I.D._607'],
    ['PC.634', 'ACAGAGTCGGCT', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', 20080116,
     'Fasting_mouse_I.D._634'],
    ['PC.635', 'ACCGCAGAGTCA', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', 20080116,
     'Fasting_mouse_I.D._635'],
    ['PC.636', 'ACGGTGAGTGTC', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', 20080116,
     'Fasting_mouse_I.D._636']]

PRE_PROCESS_A = [
    ['PC.354', 'AGCACGAGCCTA', 'Control', '20061218'],
    ['PC.355', 'AACTCGTCGATG', 'Control', '20061218'],
    ['PC.356', 'ACAGACCACTCA', 'Control', '20061126'],
    ['PC.481', 'ACCAGCGACTAG', 'Control', '20070314'],
    ['PC.593', 'AGCAGCACTTGT', 'Control', '20071210'],
    ['PC.607', 'AACTGTGCGTAC', 'Fast', '20071112'],
    ['PC.634', 'ACAGAGTCGGCT', 'Fast', '20080116'],
    ['PC.635', 'ACCGCAGAGTCA', 'Fast', '20080116'],
    ['PC.636', 'ACGGTGAGTGTC', 'Fast', '20080116']]

PRE_PROCESS_B = [
    ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control_mouse_I.D._354'],
    ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control_mouse_I.D._355'],
    ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Control_mouse_I.D._356'],
    ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Control_mouse_I.D._481'],
    ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Control_mouse_I.D._593'],
    ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Fasting_mouse_I.D._607'],
    ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Fasting_mouse_I.D._634'],
    ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fasting_mouse_I.D._635'],
    ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Fasting_mouse_I.D._636']]

MAPPING_FILE_DATA_CAT_A = [
    ['PC.354', 'Control', '20061218', 'Control20061218'],
    ['PC.355', 'Control', '20061218', 'Control20061218'],
    ['PC.356', 'Control', '20061126', 'Control20061126'],
    ['PC.481', 'Control', '20070314', 'Control20070314'],
    ['PC.593', 'Control', '20071210', 'Control20071210'],
    ['PC.607', 'Fast', '20071112', 'Fast20071112'],
    ['PC.634', 'Fast', '20080116', 'Fast20080116'],
    ['PC.635', 'Fast', '20080116', 'Fast20080116'],
    ['PC.636', 'Fast', '20080116', 'Fast20080116']]

MAPPING_FILE_DATA_CAT_B = [
    ['PC.354', 'Control', '20061218', '20061218Control'],
    ['PC.355', 'Control', '20061218', '20061218Control'],
    ['PC.356', 'Control', '20061126', '20061126Control'],
    ['PC.481', 'Control', '20070314', '20070314Control'],
    ['PC.593', 'Control', '20071210', '20071210Control'],
    ['PC.607', 'Fast', '20071112', '20071112Fast'],
    ['PC.634', 'Fast', '20080116', '20080116Fast'],
    ['PC.635', 'Fast', '20080116', '20080116Fast'],
    ['PC.636', 'Fast', '20080116', '20080116Fast']]

MAPPING_FILE_DATA_CAT_C = [
    ['PC.354', 'Control'], ['PC.355', 'Control'], ['PC.356', 'Control'],
    ['PC.481', 'Control'], ['PC.593', 'Control'], ['PC.607', 'Fast'],
    ['PC.634', 'Fast'], ['PC.635', 'Fast'], ['PC.636', 'Fast']]

MAPPING_FILE_DATA_CAT_D = [
    ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
    ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
    ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'],
    ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
    ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
    ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
    ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
    ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
    ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116']]

MAPPING_FILE_DATA_CAT_E = [
    ['PC.354', 'AGCACGAGCCTA', 'Control', '20061218',
     'Control_mouse_I.D._354'],
    ['PC.355', 'AACTCGTCGATG', 'Control', '20061218',
     'Control_mouse_I.D._355'],
    ['PC.356', 'ACAGACCACTCA', 'Control', '20061126',
     'Control_mouse_I.D._356'],
    ['PC.481', 'ACCAGCGACTAG', 'Control', '20070314',
     'Control_mouse_I.D._481'],
    ['PC.593', 'AGCAGCACTTGT', 'Control', '20071210',
     'Control_mouse_I.D._593'],
    ['PC.607', 'AACTGTGCGTAC', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
    ['PC.634', 'ACAGAGTCGGCT', 'Fast', '20080116', 'Fasting_mouse_I.D._634'],
    ['PC.635', 'ACCGCAGAGTCA', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
    ['PC.636', 'ACGGTGAGTGTC', 'Fast', '20080116', 'Fasting_mouse_I.D._636']]

MAPPING_FILE_DATA_CAT_F = [
    ['PC.354', 'Control', 'Control20061218'],
    ['PC.355', 'Control', 'Control20061218'],
    ['PC.356', 'Control', 'Control20061126'],
    ['PC.481', 'Control', 'Control20070314'],
    ['PC.593', 'Control', 'Control20071210'],
    ['PC.607', 'Fast', 'Fast20071112'],
    ['PC.634', 'Fast', 'Fast20080116'],
    ['PC.635', 'Fast', 'Fast20080116'],
    ['PC.636', 'Fast', 'Fast20080116']]

MAPPING_FILE_DATA_CAT_G = [
    ['PC.354', 'AGCACGAGCCTA', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218',
     'Control_mouse_I.D._354'],
    ['PC.355', 'AACTCGTCGATG', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218',
     'Control_mouse_I.D._355'],
    ['PC.356', 'ACAGACCACTCA', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126',
     'Control_mouse_I.D._356'],
    ['PC.481', 'ACCAGCGACTAG', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314',
     'Control_mouse_I.D._481'],
    ['PC.593', 'AGCAGCACTTGT', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210',
     'Control_mouse_I.D._593'],
    ['PC.607', 'AACTGTGCGTAC', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112',
     'Fasting_mouse_I.D._607'],
    ['PC.634', 'ACAGAGTCGGCT', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116',
     'Fasting_mouse_I.D._634'],
    ['PC.635', 'ACCGCAGAGTCA', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116',
     'Fasting_mouse_I.D._635'],
    ['PC.636', 'ACGGTGAGTGTC', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116',
     'Fasting_mouse_I.D._636']]

MAPPING_FILE_DATA_CAT_H = [
    ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
    ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
    ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'],
    ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
    ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
    ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
    ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
    ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
    ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116']]

MAPPING_FILE_DATA_GRADIENT = [
    ['PC.354', 'Control', '3', '40', 'Control20061218'],
    ['PC.355', 'Control', '9', '44', 'Control20061218'],
    ['PC.635', 'Fast', '9', '44', 'Fast20080116'],
    ['PC.636', 'Fast', '12', '37.22', 'Fast20080116']]

MAPPING_FILE_DATA_DUPLICATED = [
    ['PC.354_0', 'Control', '20061218'],
    ['PC.355_0', 'Control', '20061218'],
    ['PC.356_0', 'Control', '20061126'],
    ['PC.481_0', 'Control', '20070314'],
    ['PC.593_0', 'Control', '20071210'],
    ['PC.607_0', 'Fast', '20071112'],
    ['PC.634_0', 'Fast', '20080116'],
    ['PC.635_0', 'Fast', '20080116'],
    ['PC.636_0', 'Fast', '20080116'],
    ['PC.354_1', 'Control', '20061218'],
    ['PC.355_1', 'Control', '20061218'],
    ['PC.356_1', 'Control', '20061126'],
    ['PC.481_1', 'Control', '20070314'],
    ['PC.593_1', 'Control', '20071210'],
    ['PC.607_1', 'Fast', '20071112'],
    ['PC.634_1', 'Fast', '20080116'],
    ['PC.635_1', 'Fast', '20080116'],
    ['PC.636_1', 'Fast', '20080116'],
    ['PC.354_2', 'Control', '20061218'],
    ['PC.355_2', 'Control', '20061218'],
    ['PC.356_2', 'Control', '20061126'],
    ['PC.481_2', 'Control', '20070314'],
    ['PC.593_2', 'Control', '20071210'],
    ['PC.607_2', 'Fast', '20071112'],
    ['PC.634_2', 'Fast', '20080116'],
    ['PC.635_2', 'Fast', '20080116'],
    ['PC.636_2', 'Fast', '20080116']]

COORDS_DATA = array([
    [-0.2, -0.1, 0.06, -0.06],
    [-0.3, 0.04, -0.1, 0.15],
    [0.1, -0.1, -0.2, 0.08],
    [0.04, -0.01, 0.06, -0.34]])

BROKEN_MAPPING_FILE = [
    ['PC.354', 'Control', '3', '40', 'Control20061218'],
    ['PC.355', 'Control', 'y', '44', 'Control20061218'],
    ['PC.635', 'Fast', '9', 'x', 'Fast20080116'],
    ['PC.636', 'Fast', '12', '37.22', 'Fast20080116']]

BROKEN_MAPPING_FILE_2_VALUES = [
    ['PC.354', 'Control', '3', '40', 'Control20061218'],
    ['PC.355', 'Control', 'NA', '44', 'Control20061218'],
    ['PC.635', 'Fast', 'NA', 'x', 'Fast20080116'],
    ['PC.636', 'Fast', '12', '37.22', 'Fast20080116']]

UNSANITZIED_MAPPING_DATA = [
    ['PC.354', "Dr. Bronner's", 'Cont"rol', '20061218',
     'Control_mouse_I.D._354'],
    ['PC.355', 'AACTCGTCGATG', "Con''trol", '20061218',
     'Control_mouse_I.D._355'],
    ["PC'356", 'ACAGACCACTCA', 'Control', '20061126',
     'Control_mouse_I.D._"356'],
    ['PC.481', 'AC"AGC"ACTAG', 'Control', '20070314',
     'Control_mouse_I.D._481'],
    ['PC.593', 'AGCAGCACTTGT', 'Control', '20071210',
     'Control_mouse_I.D._593']]

if __name__ == "__main__":
    main()
