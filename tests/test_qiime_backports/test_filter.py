#!/usr/bin/env python
# File created on 18 May 2010
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Greg Caporaso", "Jai Ram Rideout", "Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"
 
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from unittest import TestCase, main

from emperor.qiime_backports.parse import (parse_mapping_file,
    parse_metadata_state_descriptions)
from emperor.qiime_backports.filter import (get_sample_ids, filter_mapping_file,
    filter_mapping_file_by_metadata_states,
    sample_ids_from_metadata_description, filter_mapping_file_from_mapping_f)

class FilterTests(TestCase):
    
    def setUp(self):
        self.map_str1 = map_str1
        self.map_str2 = map_str2.split('\n')
        self.map_data, self.map_headers, self.map_comments =\
         parse_mapping_file(StringIO(self.map_str1))
        self.tutorial_mapping_f = StringIO(tutorial_mapping_f)

        # For sample_ids_from_category_state_coverage() tests.
        self.exp_empty = (set([]), 0, set([]))
        self.exp_all = (set(['PC.354', 'PC.355', 'PC.356', 'PC.481', 'PC.593',
                             'PC.607', 'PC.634', 'PC.635', 'PC.636']), 6,
                        set(['Control', 'Fast']))

    def test_filter_mapping_file(self):
        """filter_mapping_file should filter map file according to sample ids"""
        self.assertEqual(filter_mapping_file(self.map_data, self.map_headers,\
         ['a','b','c','d','e','f']), (self.map_headers, self.map_data))
        self.assertEqual(filter_mapping_file(self.map_data, self.map_headers, ['a']),
            (['SampleID','Description'],['a\tx'.split('\t')]))

    def test_filter_mapping_file_from_mapping_f(self):
        """ filter_mapping_file_from_mapping_f functions as expected """
        actual = filter_mapping_file_from_mapping_f(self.tutorial_mapping_f,["PC.354","PC.355"])
        expected = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
PC.354	AGCACGAGCCTA	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._354
PC.355	AACTCGTCGATG	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._355"""
        self.assertEqual(actual,expected)

    def test_filter_mapping_file_from_mapping_f_negate(self):
        """ filter_mapping_file_from_mapping_f functions as expected when negate is True """
        actual = filter_mapping_file_from_mapping_f(self.tutorial_mapping_f,
         ["PC.356", "PC.481", "PC.593", "PC.607", "PC.634", "PC.635", "PC.636"],
         negate=True)
        expected = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
PC.354	AGCACGAGCCTA	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._354
PC.355	AACTCGTCGATG	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._355"""
        self.assertEqual(actual,expected)

    def test_filter_mapping_file_by_metadata_states(self):
        """ filter_mapping_file_by_metadata_states functions as expected """
        actual = filter_mapping_file_by_metadata_states(self.tutorial_mapping_f,"Treatment:Control")
        expected = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
PC.354	AGCACGAGCCTA	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._354
PC.355	AACTCGTCGATG	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._355
PC.356	ACAGACCACTCA	YATGCTGCCTCCCGTAGGAGT	Control	20061126	Control_mouse_I.D._356
PC.481	ACCAGCGACTAG	YATGCTGCCTCCCGTAGGAGT	Control	20070314	Control_mouse_I.D._481
PC.593	AGCAGCACTTGT	YATGCTGCCTCCCGTAGGAGT	Control	20071210	Control_mouse_I.D._593"""
        self.assertEqual(actual,expected)


    def test_sample_ids_from_metadata_description(self):
        """Testing sample_ids_from_metadata_description fails on an empty set"""
        self.assertRaises(ValueError, sample_ids_from_metadata_description,
            self.tutorial_mapping_f, "Treatment:Foo")
        self.tutorial_mapping_f.seek(0)
        self.assertRaises(ValueError, sample_ids_from_metadata_description,
            self.tutorial_mapping_f, "DOB:!20061218,!20070314,!20071112,"
            "!20080116")

    def test_get_sample_ids(self):
        """get_sample_ids should return sample ids matching criteria."""
        self.assertEqual(get_sample_ids(self.map_data, self.map_headers,\
            parse_metadata_state_descriptions('Study:Twin')), [])
        self.assertEqual(get_sample_ids(self.map_data, self.map_headers,\
            parse_metadata_state_descriptions('Study:Dog')), ['a','b'])
        self.assertEqual(get_sample_ids(self.map_data, self.map_headers,\
            parse_metadata_state_descriptions('Study:*,!Dog')), ['c','d','e'])
        self.assertEqual(get_sample_ids(self.map_data, self.map_headers,\
            parse_metadata_state_descriptions('Study:*,!Dog;BodySite:Stool')), ['e'])
        self.assertEqual(get_sample_ids(self.map_data, self.map_headers,\
            parse_metadata_state_descriptions('BodySite:Stool')), ['a','b','e'])

map_str1 = """#SampleID\tStudy\tBodySite\tDescription
a\tDog\tStool\tx
b\tDog\tStool\ty
c\tHand\tPalm\tz
d\tWholeBody\tPalm\ta
e\tWholeBody\tStool\tb"""

map_str2 = """#SampleID\tIndividual\tTime\tBodySite\tDescription
a\tI1\t2\tPalm\tx
b\tI2\t3\tStool\ty
c\tI1\t1\tStool\tz
d\tI3\t3\tStool\ta
e\tI3\t1\tPalm\tb
f\tI1\t3\tPalm\tc
g\tI1\t2\tStool\td"""

tutorial_mapping_f = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
#Example mapping file for the QIIME analysis package.  These 9 samples are from a study of the effects of exercise and diet on mouse cardiac physiology (Crawford, et al, PNAS, 2009).
PC.354	AGCACGAGCCTA	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._354
PC.355	AACTCGTCGATG	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._355
PC.356	ACAGACCACTCA	YATGCTGCCTCCCGTAGGAGT	Control	20061126	Control_mouse_I.D._356
PC.481	ACCAGCGACTAG	YATGCTGCCTCCCGTAGGAGT	Control	20070314	Control_mouse_I.D._481
PC.593	AGCAGCACTTGT	YATGCTGCCTCCCGTAGGAGT	Control	20071210	Control_mouse_I.D._593
PC.607	AACTGTGCGTAC	YATGCTGCCTCCCGTAGGAGT	Fast	20071112	Fasting_mouse_I.D._607
PC.634	ACAGAGTCGGCT	YATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse_I.D._634
PC.635	ACCGCAGAGTCA	YATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse_I.D._635
PC.636	ACGGTGAGTGTC	YATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse_I.D._636"""

expected_mapping_f1 = """#SampleID	BarcodeSequence	LinkerPrimerSequence	Treatment	DOB	Description
PC.354	AGCACGAGCCTA	YATGCTGCCTCCCGTAGGAGT	Control	20061218	Control_mouse_I.D._354
PC.636	ACGGTGAGTGTC	YATGCTGCCTCCCGTAGGAGT	Fast	20080116	Fasting_mouse_I.D._636"""

if __name__ == "__main__":
    main()
