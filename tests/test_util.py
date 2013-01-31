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


from shutil import rmtree
from os.path import exists, join
from cogent.util.unit_test import TestCase, main
from cogent.util.misc import remove_files, create_dir
from qiime.util import get_qiime_temp_dir, get_tmp_filename
from emperor.util import copy_support_files, process_mapping_file

class TopLevelTests(TestCase):

    def setUp(self):
        self.mapping_file_data = MAPPING_FILE_DATA
        self.mapping_file_headers = ['SampleID', 'BarcodeSequence',
            'LinkerPrimerSequence', 'Treatment', 'DOB', 'Description']
        self.valid_columns = ['Treatment', 'DOB']
        self.support_files_filename = get_qiime_temp_dir()

    def test_copy_support_files(self):
        """Test the support files are correctly copied to a file path"""
        copy_support_files(self.support_files_filename)
        self.assertTrue(exists(join(self.support_files_filename,
            'emperor_required_resources/')))

    def test_process_mapping_file(self):
        """Test a mapping file is correctly processed"""
        # do not add unique columns
        out_data, out_headers = process_mapping_file(self.mapping_file_data,
            self.mapping_file_headers, self.valid_columns)

        expected_data = [['PC.354', 'Control'], ['PC.355', 'Control'],
            ['PC.356', 'Control'], ['PC.481', 'Control'], ['PC.593', 'Control'],
            ['PC.607', 'Fast'], ['PC.634', 'Fast'], ['PC.635', 'Fast'],
            ['PC.636', 'Fast']]
        expected_headers = ['SampleID', 'Treatment']

        self.assertEquals(out_data, expected_data)
        self.assertEquals(out_headers, expected_headers)

        expected_data = [['PC.354', 'AGCACGAGCCTA', 'Control'],
            ['PC.355', 'AACTCGTCGATG', 'Control'],
            ['PC.356', 'ACAGACCACTCA', 'Control'],
            ['PC.481', 'ACCAGCGACTAG', 'Control'],
            ['PC.593', 'AGCAGCACTTGT', 'Control'],
            ['PC.607', 'AACTGTGCGTAC', 'Fast'],
            ['PC.634', 'ACAGAGTCGGCT', 'Fast'],
            ['PC.635', 'ACCGCAGAGTCA', 'Fast'],
            ['PC.636', 'ACGGTGAGTGTC', 'Fast']]

        out_data, out_headers = process_mapping_file(self.mapping_file_data,
            self.mapping_file_headers, self.mapping_file_headers)

        self.assertEquals(out_data, expected_data)
        self.assertEquals(out_headers, ['SampleID', 'BarcodeSequence',
            'Treatment'])

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


if __name__ == "__main__":
    main()