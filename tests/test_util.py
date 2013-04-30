#!/usr/bin/env python
# File created on 25 Jan 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from numpy import array
from shutil import rmtree
from os.path import exists, join
from cogent.util.unit_test import TestCase, main
from qiime.util import get_qiime_temp_dir, get_tmp_filename
from emperor.util import (copy_support_files, keep_columns_from_mapping_file,
    preprocess_mapping_file, preprocess_coords_file,
    fill_mapping_field_from_mapping_file, sanitize_mapping_file)

class TopLevelTests(TestCase):

    def setUp(self):
        self.mapping_file_data = MAPPING_FILE_DATA
        self.mapping_file_headers = ['SampleID', 'BarcodeSequence',
            'LinkerPrimerSequence', 'Treatment', 'DOB', 'Description']
        self.valid_columns = ['Treatment', 'DOB']
        self.support_files_filename = get_qiime_temp_dir()

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
        self.jk_mapping_file_data = [['1', 'a', 'b', 'c'], ['2', 'd', 'e', 'f'],
            ['3', 'g', 'h', 'i']]
        self.jk_coords_header = [['1', '2', '3'], ['1', '2', '3'],
            ['1', '2', '3'], ['1', '2', '3']]
        self.jk_coords_data = [array([[1.2, 0.1, -1.2],[-2.5, -4.0, 4.5]]),
            array([[-1.4, 0.05, 1.3],[2.6, 4.1, -4.7]]),
            array([[-1.5, 0.05, 1.6],[2.4, 4.0, -4.8]]),
            array([[-1.5, 0.05, 1.6],[2.4, 4.0, -4.8]])]
        self.jk_coords_eigenvalues = [array([0.80, .11, 0.09]), array([0.76,
            .20,0.04]), array([0.84, .14, 0.02]), array([0.84, .11, 0.05])]
        self.jk_coords_pcts = [array([0.80, .10, 0.10]), array([0.76, .21,
            0.03]), array([0.84, .11, 0.05]), array([0.84, .15, 0.01])]

        self.jk_mapping_file_data_gradient = MAPPING_FILE_DATA_GRADIENT
        self.jk_mapping_file_headers_gradient = ['SampleID', 'Treatment','Time',
            'Weight', 'Description']
        self.jk_coords_header_gradient = [['PC.354','PC.355','PC.635','PC.636'],
            ['PC.354','PC.355','PC.635','PC.636'], ['PC.354','PC.355','PC.635',
            'PC.636'], ['PC.354','PC.355','PC.635','PC.636']]
        self.jk_coords_data_gradient = [array([[1.2, 0.1, -1.2, 1.1],[-2.5,
            -4.0, 4.5, 0.3], [.5, -0.4, 3.5, 1.001], [0.67, 0.23, 1.01, 2.2]]),
            array([[1.2, 1, -0.2, 0.1],[-2.5, -4.0, 4.5, 3.2], [.5, -0.4, 3.5,
            1.00], [0.57, 0.27, 0.95, 2.1]]), array([[1.0, 1, -1.2, 1.1],[-2.1,
            -2.0, 3.5, 0.3], [.5, 3, 3.5, 2], [0.60, 0.33, 1.3, 2.0]]), array([
            [1.2, 0.1, -1.2, 1.1],[-2.5,-4.0, 4.5, 0.3], [.5, -0.4, 3.5, 1.001],
            [0.69, 0.20, 1.01, 2.2]])]
        self.jk_coords_eigenvalues_gradient = [array([0.80, .11, 0.09, 0.0]),
            array([0.76, .20,0.04, 0.0]), array([0.84, .14, 0.02, 0.0]), array([
            0.84, .11, 0.05, 0.0])]
        self.jk_coords_pcts_gradient = [array([0.80, .10, 0.10, 0.0]), array(
            [0.76, .21, 0.03, 0.0]), array([0.84, .11, 0.05, 0.0]), array([0.84,
            .15, 0.01, 0])]

        self.broken_mapping_file_data = BROKEN_MAPPING_FILE

    def test_copy_support_files(self):
        """Test the support files are correctly copied to a file path"""
        copy_support_files(self.support_files_filename)
        self.assertTrue(exists(join(self.support_files_filename,
            'emperor_required_resources/')))

    def test_preprocess_mapping_file(self):
        """Check correct preprocessing of metadata is done"""

        # test it concatenates columns together correctly
        out_data, out_headers = preprocess_mapping_file(self.mapping_file_data,
            self.mapping_file_headers, ['Treatment', 'DOB', 'Treatment&&DOB'])
        self.assertEquals(out_headers, ['SampleID', 'Treatment', 'DOB',
            'Treatment&&DOB'])
        self.assertEquals(out_data, MAPPING_FILE_DATA_CAT_A)

        # test it filter columns properly
        out_data, out_headers = preprocess_mapping_file(self.mapping_file_data,
            self.mapping_file_headers, ['Treatment'])
        self.assertEquals(out_headers, ['SampleID', 'Treatment'])
        self.assertEquals(out_data, MAPPING_FILE_DATA_CAT_B)

        # check it removes columns with unique values
        out_data, out_headers = preprocess_mapping_file(self.mapping_file_data,
            self.mapping_file_headers, ['SampleID', 'BarcodeSequence',
            'LinkerPrimerSequence', 'Treatment', 'DOB', 'Description'],
            unique=True)
        self.assertEquals(out_headers, ['SampleID', 'LinkerPrimerSequence',
            'Treatment', 'DOB'])
        self.assertEquals(out_data, MAPPING_FILE_DATA_CAT_C)

        # check it removes columns where there is only one value
        out_data, out_headers = preprocess_mapping_file(self.mapping_file_data,
            self.mapping_file_headers, ['SampleID', 'BarcodeSequence',
            'LinkerPrimerSequence', 'Treatment', 'DOB', 'Description'],
            single=True)
        self.assertEquals(out_headers,['SampleID', 'BarcodeSequence',
            'Treatment', 'DOB', 'Description'])
        self.assertEquals(out_data, MAPPING_FILE_DATA_CAT_D)

        # keep only treatment concat treatment and DOB and remove all
        # categories with only one value and all with unique values for field
        out_data, out_headers = preprocess_mapping_file(self.mapping_file_data,
            self.mapping_file_headers, ['Treatment', 'Treatment&&DOB'],
            unique=True, single=True)
        self.assertEquals(out_headers, ['SampleID', 'Treatment',
            'Treatment&&DOB'])
        self.assertEquals(out_data, MAPPING_FILE_DATA_CAT_E)

    def test_keep_columns_from_mapping_file(self):
        """Check correct selection of metadata is being done"""

        # test it returns the same data
        out_data, out_headers = keep_columns_from_mapping_file(
            self.mapping_file_data, self.mapping_file_headers, [])
        self.assertEquals(out_data, [[], [], [], [], [], [], [], [], []])
        self.assertEquals(out_headers, [])

        # test it can filter a list of columns
        out_data, out_headers = keep_columns_from_mapping_file(
            self.mapping_file_data, self.mapping_file_headers, [
            'SampleID', 'LinkerPrimerSequence', 'Description'])
        self.assertEquals(out_headers, ['SampleID', 'LinkerPrimerSequence',
            'Description'])
        self.assertEquals(out_data, PRE_PROCESS_B)

        # test correct negation of filtering
        out_data, out_headers = keep_columns_from_mapping_file(
            self.mapping_file_data, self.mapping_file_headers,
            ['LinkerPrimerSequence', 'Description'], True)
        self.assertEquals(out_data, PRE_PROCESS_A)
        self.assertEquals(out_headers,  ['SampleID', 'BarcodeSequence',
            'Treatment', 'DOB'])

    def test_preprocess_coords_file(self):
        """Check correct processing is applied to the coords"""

        # case with custom axes
        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high = preprocess_coords_file(
            self.coords_header, self.coords_data, self.coords_eigenvalues,
            self.coords_pct, self.mapping_file_headers_gradient,
            self.mapping_file_data_gradient, ['Time'])

        expected_coords_data = array([[ 0.03333333, -0.2, -0.1,0.06, -0.06],
           [0.03333333, -0.3, 0.04, -0.1,0.15],
           [0.2, 0.1, -0.1, -0.2, 0.08],
           [-0.3, 0.04, -0.01,  0.06, -0.34]])

        self.assertEquals(out_coords_header, self.coords_header)
        self.assertEquals(out_coords_high, None)
        self.assertEquals(out_coords_low, None)
        self.assertEquals(self.coords_eigenvalues, array([1, 2, 3, 4]))
        self.assertEquals(self.coords_pct, array([40, 30, 20, 10]))

        # check each individual value because currently cogent assertEquals
        # fails when comparing the whole matrix at once
        for out_el, exp_el in zip(out_coords_data, expected_coords_data):
            for out_el_sub, exp_el_sub in zip(out_el, exp_el):
                self.assertAlmostEquals(out_el_sub, exp_el_sub)        

        # case for jackknifing, based on qiime/tests/test_util.summarize_pcoas
        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high = preprocess_coords_file(
            self.jk_coords_header, self.jk_coords_data,
            self.jk_coords_eigenvalues, self.jk_coords_pcts,
            self.jk_mapping_file_headers, self.jk_mapping_file_data,
            jackknifing_method='sdev')

        self.assertEquals(out_coords_header, ['1', '2', '3'])
        self.assertFloatEqual(out_coords_data, array([[1.46666666667, -0.05,
            -1.5], [-2.46666666667, -4.03333333333, 4.76666666667]]))
        self.assertFloatEqual(out_eigenvals, array([0.813333333333, 0.15,
            0.0366666666667]))
        self.assertFloatEqual(out_pcts, array([0.8, 0.1, 0.1]))

        # test the coords are working fine
        self.assertFloatEqual(out_coords_low, array([[-0.0288675134595,
            -4.24918736097e-18, -0.0866025403784], [-0.057735026919,
            -0.0288675134595, -0.0288675134595]]))
        self.assertFloatEqual(out_coords_high, array([[0.0288675134595,
            4.24918736097e-18, 0.0866025403784], [0.057735026919,
            0.0288675134595, 0.0288675134595]]))

        # test custom axes and jackknifed plots
        out_coords_header, out_coords_data, out_eigenvals, out_pcts,\
            out_coords_low, out_coords_high = preprocess_coords_file(
            self.jk_coords_header_gradient, self.jk_coords_data_gradient,
            self.jk_coords_eigenvalues_gradient, self.jk_coords_pcts_gradient,
            self.jk_mapping_file_headers_gradient,
            self.jk_mapping_file_data_gradient, custom_axes=['Time'],
            jackknifing_method='sdev')


        self.assertEquals(out_coords_header, ['PC.354', 'PC.355', 'PC.635',
            'PC.636'])
        self.assertFloatEqual(out_coords_data, array([[-2.36666667, 1.13333333,
            0.7, -0.86666667, 0.76666667], [ 0.72222222, -2.36666667,
            -3.33333333,  4.16666667,  1.26666667], [ 0.72222222, 0.5,
            0.73333333, 3.5, 1.33366667], [ 2.26666667, 0.62, 0.26666667,
            1.08666667, 2.1]]))
        self.assertFloatEqual(out_eigenvals, array([ 0.81333333, 0.15,
            0.03666667,0.]))
        self.assertFloatEqual(out_pcts, array([ 0.8, 0.1, 0.1, 0.]))

        # test the coords are working fine
        self.assertFloatEqual(out_coords_low, array([[0,-0.25980762,-0.28867513,
            -0.28867513], [0, -0.57735027, -0.28867513, -0.83715789], [0,
            -0.98149546, 0, -0.28853091],[0.,-0.03253204,-0.09358597,-0.05]]))
        self.assertFloatEqual(out_coords_high, array([[1.00000000e-05,
            2.59807621e-01, 2.88675135e-01, 2.88675135e-01], [1.00000000e-05,
            5.77350269e-01, 2.88675135e-01, 8.37157890e-01], [1.00000000e-05,
            9.81495458e-01, 0.00000000e+00, 2.88530905e-01], [1.00000000e-05,
            3.25320355e-02, 9.35859676e-02, 5.00000000e-02]]))

    def test_fill_mapping_field_from_mapping_file(self):
        """Check the values are being correctly filled in"""

        # common usage example
        out_data = fill_mapping_field_from_mapping_file(
            self.broken_mapping_file_data, self.mapping_file_headers_gradient,
            'Time:200;Weight:800')
        self.assertEquals(out_data, [
            ['PC.354', 'Control','3', '40', 'Control20061218'],
            ['PC.355', 'Control','200', '44', 'Control20061218'],
            ['PC.635', 'Fast','9', '800', 'Fast20080116'],
            ['PC.636', 'Fast','12', '37.22', 'Fast20080116']])

        # more than one value to fill empty values with
        self.assertRaises(AssertionError, fill_mapping_field_from_mapping_file,
            self.broken_mapping_file_data, self.mapping_file_headers_gradient,
            'Time:200,300;Weight:800')

        # non-existing header in mapping file
        self.assertRaises(ValueError, fill_mapping_field_from_mapping_file,
            self.broken_mapping_file_data, self.mapping_file_headers_gradient,
            'Spam:Foo')

    def test_sanitize_mapping_file(self):
        """Check the mapping file strings are sanitized for it's use in JS"""

        o_sanitized_headers, o_sanitized_data = sanitize_mapping_file(
            UNSANITZIED_MAPPING_DATA, ['SampleID', 'BarcodeSequence',
            'LinkerPrimerSequence', 'Treatment', 'DOB', 'Descr"""""iption'])

        self.assertEquals(o_sanitized_data, ['SampleID', 'BarcodeSequence',
            'LinkerPrimerSequence', 'Treatment', 'DOB','Description'])
        self.assertEquals(o_sanitized_headers, [
['PC.354', "Dr. Bronners", 'Control', '20061218', 'Control_mouse_I.D._354'],
['PC.355', 'AACTCGTCGATG', "Control", '20061218', 'Control_mouse_I.D._355'],
["PC356", 'ACAGACCACTCA', 'Control', '20061126', 'Control_mouse_I.D._356'],
['PC.481', 'ACAGCACTAG', 'Control', '20070314', 'Control_mouse_I.D._481'],
['PC.593', 'AGCAGCACTTGT', 'Control', '20071210', 'Control_mouse_I.D._593']])


MAPPING_FILE_DATA = [
    ['PC.354','AGCACGAGCCTA','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._354'],
    ['PC.355','AACTCGTCGATG','YATGCTGCCTCCCGTAGGAGT','Control','20061218','Control_mouse_I.D._355'],
    ['PC.356','ACAGACCACTCA','YATGCTGCCTCCCGTAGGAGT','Control','20061126','Control_mouse_I.D._356'],
    ['PC.481','ACCAGCGACTAG','YATGCTGCCTCCCGTAGGAGT','Control','20070314','Control_mouse_I.D._481'],
    ['PC.593','AGCAGCACTTGT','YATGCTGCCTCCCGTAGGAGT','Control','20071210','Control_mouse_I.D._593'],
    ['PC.607','AACTGTGCGTAC','YATGCTGCCTCCCGTAGGAGT','Fast','20071112','Fasting_mouse_I.D._607'],
    ['PC.634','ACAGAGTCGGCT','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._634'],
    ['PC.635','ACCGCAGAGTCA','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._635'],
    ['PC.636','ACGGTGAGTGTC','YATGCTGCCTCCCGTAGGAGT','Fast','20080116','Fasting_mouse_I.D._636']]

PRE_PROCESS_A = [
    ['PC.354','AGCACGAGCCTA', 'Control','20061218'],
    ['PC.355','AACTCGTCGATG', 'Control','20061218'],
    ['PC.356','ACAGACCACTCA', 'Control','20061126'],
    ['PC.481','ACCAGCGACTAG', 'Control','20070314'],
    ['PC.593','AGCAGCACTTGT', 'Control','20071210'],
    ['PC.607','AACTGTGCGTAC', 'Fast','20071112'],
    ['PC.634','ACAGAGTCGGCT', 'Fast','20080116'],
    ['PC.635','ACCGCAGAGTCA', 'Fast','20080116'],
    ['PC.636','ACGGTGAGTGTC', 'Fast','20080116']]

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
    ['PC.354', 'Control','20061218', 'Control20061218'],
    ['PC.355', 'Control','20061218', 'Control20061218'],
    ['PC.356', 'Control','20061126', 'Control20061126'],
    ['PC.481', 'Control','20070314', 'Control20070314'],
    ['PC.593', 'Control','20071210', 'Control20071210'],
    ['PC.607', 'Fast','20071112', 'Fast20071112'],
    ['PC.634', 'Fast','20080116', 'Fast20080116'],
    ['PC.635', 'Fast','20080116', 'Fast20080116'],
    ['PC.636', 'Fast','20080116', 'Fast20080116']]

MAPPING_FILE_DATA_CAT_B = [['PC.354', 'Control'], ['PC.355', 'Control'],
    ['PC.356', 'Control'], ['PC.481', 'Control'], ['PC.593', 'Control'],
    ['PC.607', 'Fast'], ['PC.634', 'Fast'], ['PC.635', 'Fast'],
    ['PC.636', 'Fast']]

MAPPING_FILE_DATA_CAT_C = [
    ['PC.354', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
    ['PC.355', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061218'],
    ['PC.356', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20061126'],
    ['PC.481', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20070314'],
    ['PC.593', 'YATGCTGCCTCCCGTAGGAGT', 'Control', '20071210'],
    ['PC.607', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20071112'],
    ['PC.634', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
    ['PC.635', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116'],
    ['PC.636', 'YATGCTGCCTCCCGTAGGAGT', 'Fast', '20080116']]

MAPPING_FILE_DATA_CAT_D = [
    ['PC.354', 'AGCACGAGCCTA', 'Control', '20061218', 'Control_mouse_I.D._354'],
    ['PC.355', 'AACTCGTCGATG', 'Control', '20061218', 'Control_mouse_I.D._355'],
    ['PC.356', 'ACAGACCACTCA', 'Control', '20061126', 'Control_mouse_I.D._356'],
    ['PC.481', 'ACCAGCGACTAG', 'Control', '20070314', 'Control_mouse_I.D._481'],
    ['PC.593', 'AGCAGCACTTGT', 'Control', '20071210', 'Control_mouse_I.D._593'],
    ['PC.607', 'AACTGTGCGTAC', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
    ['PC.634', 'ACAGAGTCGGCT', 'Fast', '20080116', 'Fasting_mouse_I.D._634'],
    ['PC.635', 'ACCGCAGAGTCA', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
    ['PC.636', 'ACGGTGAGTGTC', 'Fast', '20080116', 'Fasting_mouse_I.D._636']]

MAPPING_FILE_DATA_CAT_E = [
    ['PC.354', 'Control', 'Control20061218'],
    ['PC.355', 'Control', 'Control20061218'],
    ['PC.356', 'Control', 'Control20061126'],
    ['PC.481', 'Control', 'Control20070314'],
    ['PC.593', 'Control', 'Control20071210'],
    ['PC.607', 'Fast', 'Fast20071112'],
    ['PC.634', 'Fast', 'Fast20080116'],
    ['PC.635', 'Fast', 'Fast20080116'],
    ['PC.636', 'Fast', 'Fast20080116']]

MAPPING_FILE_DATA_GRADIENT = [
    ['PC.354', 'Control','3', '40', 'Control20061218'],
    ['PC.355', 'Control','9', '44', 'Control20061218'],
    ['PC.635', 'Fast','9', '44', 'Fast20080116'],
    ['PC.636', 'Fast','12', '37.22', 'Fast20080116']]

COORDS_DATA = array([
    [-0.2, -0.1, 0.06, -0.06],
    [-0.3, 0.04, -0.1, 0.15],
    [0.1, -0.1, -0.2, 0.08],
    [0.04, -0.01, 0.06, -0.34]])

BROKEN_MAPPING_FILE = [
    ['PC.354', 'Control','3', '40', 'Control20061218'],
    ['PC.355', 'Control','y', '44', 'Control20061218'],
    ['PC.635', 'Fast','9', 'x', 'Fast20080116'],
    ['PC.636', 'Fast','12', '37.22', 'Fast20080116']]

UNSANITZIED_MAPPING_DATA = [
['PC.354', "Dr. Bronner's", 'Cont"rol', '20061218', 'Control_mouse_I.D._354'],
['PC.355', 'AACTCGTCGATG', "Con''trol", '20061218', 'Control_mouse_I.D._355'],
["PC'356", 'ACAGACCACTCA', 'Control', '20061126', 'Control_mouse_I.D._"356'],
['PC.481', 'AC"AGC"ACTAG', 'Control', '20070314', 'Control_mouse_I.D._481'],
['PC.593', 'AGCAGCACTTGT', 'Control', '20071210', 'Control_mouse_I.D._593']]

if __name__ == "__main__":
    main()
