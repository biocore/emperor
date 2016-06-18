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
from builtins import chr as py_unichr

from scipy.spatial import procrustes

from emperor.qiime_backports.parse import (parse_mapping_file_to_dict,
    QiimeParseError)
from emperor.qiime_backports.util import (MetadataMap, is_valid_git_sha1,
    is_valid_git_refname, summarize_pcoas, _flip_vectors,
    _compute_jn_pcoa_avg_ranges, matrix_IQR, idealfourths, IQR)


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


class MetadataMapTests(TestCase):
    """Tests for the MetadataMap class."""

    def setUp(self):
        """Create MetadataMap objects that will be used in the tests."""
        # Create a map using the overview tutorial mapping file.
        self.overview_map_str = [
                "#SampleID\tBarcodeSequence\tTreatment\tDOB\tDescription",
                "PC.354\tAGCACGAGCCTA\tControl\t20061218\t354",
                "PC.355\tAACTCGTCGATG\tControl\t20061218\t355",
                "PC.356\tACAGACCACTCA\tControl\t20061126\t356",
                "PC.481\tACCAGCGACTAG\tControl\t20070314\t481",
                "PC.593\tAGCAGCACTTGT\tControl\t20071210\t593",
                "PC.607\tAACTGTGCGTAC\tFast\t20071112\t607",
                "PC.634\tACAGAGTCGGCT\tFast\t20080116\t634",
                "PC.635\tACCGCAGAGTCA\tFast\t20080116\t635",
                "PC.636\tACGGTGAGTGTC\tFast\t20080116\t636"]
        self.overview_map = MetadataMap(
            *parse_mapping_file_to_dict(self.overview_map_str))

        # Create the same overview tutorial map, but this time with some
        # comments.
        self.comment = "# Some comments about this mapping file"
        self.map_with_comments_str = self.overview_map_str[:]
        self.map_with_comments_str.insert(1, self.comment)
        self.map_with_comments = MetadataMap(*parse_mapping_file_to_dict(
            self.map_with_comments_str))

        # Create a MetadataMap object that has no metadata (i.e. no sample IDs,
        # so no metadata about samples).
        self.empty_map = MetadataMap({}, [])

        # Create a MetadataMap object that has samples (i.e. sample IDs) but
        # not associated metadata (i.e. no columns other than SampleID).
        self.no_metadata_str = ["#SampleID",
                                "PC.354",
                                "PC.355",
                                "PC.356",
                                "PC.481",
                                "PC.593",
                                "PC.607",
                                "PC.634",
                                "PC.635",
                                "PC.636"]
        self.no_metadata = MetadataMap(*parse_mapping_file_to_dict(
            self.no_metadata_str))

        # Create a MetadataMap object that has a category with only one value
        # throughout the entire column.
        self.single_value_str = ["#SampleID\tFoo",
                                "PC.354\tfoo",
                                "PC.355\tfoo",
                                "PC.356\tfoo",
                                "PC.481\tfoo",
                                "PC.593\tfoo",
                                "PC.607\tfoo",
                                "PC.634\tfoo",
                                "PC.635\tfoo",
                                "PC.636\tfoo"]
        self.single_value = MetadataMap(*parse_mapping_file_to_dict(
            self.single_value_str))

    def test_parseMetadataMap(self):
        """Test parsing a mapping file into a MetadataMap instance."""
        obs = MetadataMap.parseMetadataMap(self.overview_map_str)
        self.assertEqual(obs, self.overview_map)

    def test_parseMetadataMap_empty(self):
        """Test parsing empty mapping file contents."""
        self.assertRaises(QiimeParseError, MetadataMap.parseMetadataMap, [])

    def test_eq(self):
        """Test whether two MetadataMaps are equal."""
        self.assertTrue(self.empty_map == MetadataMap({}, []))
        self.assertTrue(self.overview_map == MetadataMap(
            self.overview_map._metadata, self.overview_map.Comments))

    def test_ne(self):
        """Test whether two MetadataMaps are not equal."""
        self.assertTrue(self.empty_map != MetadataMap({}, ["foo"]))
        self.assertTrue(self.overview_map != MetadataMap(
            self.overview_map._metadata, ["foo"]))
        self.assertTrue(self.overview_map != MetadataMap({},
            self.overview_map.Comments))
        self.assertTrue(self.overview_map != self.empty_map)
        self.assertTrue(self.overview_map != self.map_with_comments)
        self.assertTrue(self.overview_map != self.no_metadata)

    def test_getSampleMetadata(self):
        """Test metadata by sample ID accessor with valid sample IDs."""
        exp = {'BarcodeSequence': 'AGCACGAGCCTA', 'Treatment': 'Control',
                'DOB': '20061218', 'Description': '354'}
        obs = self.overview_map.getSampleMetadata('PC.354')
        self.assertEqual(obs, exp)

        exp = {'BarcodeSequence': 'ACCAGCGACTAG', 'Treatment': 'Control',
                'DOB': '20070314', 'Description': '481'}
        obs = self.map_with_comments.getSampleMetadata('PC.481')
        self.assertEqual(obs, exp)

        exp = {'BarcodeSequence': 'ACGGTGAGTGTC', 'Treatment': 'Fast',
                'DOB': '20080116', 'Description': '636'}
        obs = self.map_with_comments.getSampleMetadata('PC.636')
        self.assertEqual(obs, exp)

        exp = {}
        obs = self.no_metadata.getSampleMetadata('PC.636')
        self.assertEqual(obs, exp)

    def test_getSampleMetadata_bad_sample_id(self):
        """Test metadata by sample ID accessor with invalid sample IDs."""
        # Nonexistent sample ID.
        self.assertRaises(KeyError, self.overview_map.getSampleMetadata,
            'PC.000')
        self.assertRaises(KeyError, self.no_metadata.getSampleMetadata,
            'PC.000')
        # Integer sample ID.
        self.assertRaises(KeyError, self.overview_map.getSampleMetadata, 42)
        # Sample ID of type None.
        self.assertRaises(KeyError, self.overview_map.getSampleMetadata, None)

        # Sample ID on empty map.
        self.assertRaises(KeyError, self.empty_map.getSampleMetadata, 's1')
        # Integer sample ID on empty map.
        self.assertRaises(KeyError, self.empty_map.getSampleMetadata, 1)
        # Sample ID of None on empty map.
        self.assertRaises(KeyError, self.empty_map.getSampleMetadata, None)

    def test_getCategoryValue(self):
        """Test category value by sample ID/category name accessor."""
        exp = "Fast"
        obs = self.overview_map.getCategoryValue('PC.634', 'Treatment')
        self.assertEqual(obs, exp)

        exp = "20070314"
        obs = self.overview_map.getCategoryValue('PC.481', 'DOB')
        self.assertEqual(obs, exp)

        exp = "ACGGTGAGTGTC"
        obs = self.map_with_comments.getCategoryValue(
                'PC.636', 'BarcodeSequence')
        self.assertEqual(obs, exp)

    def test_getCategoryValues(self):
        """Test category value list by sample ID/category name accessor."""
        smpl_ids = ['PC.354', 'PC.355', 'PC.356', 'PC.481', 'PC.593', 'PC.607',
                    'PC.634', 'PC.635', 'PC.636']

        exp = ['Control','Control','Control','Control','Control','Fast'
                    ,'Fast','Fast','Fast']
        obs = self.overview_map.getCategoryValues(smpl_ids, 'Treatment')
        self.assertEqual(obs, exp)

    def test_isNumericCategory(self):
        """Test checking if a category is numeric."""
        obs = self.overview_map.isNumericCategory('Treatment')
        self.assertEqual(obs, False)

        obs = self.overview_map.isNumericCategory('DOB')
        self.assertEqual(obs, True)

    def test_hasUniqueCategoryValues(self):
        """Test checking if a category has unique values."""
        obs = self.overview_map.hasUniqueCategoryValues('Treatment')
        self.assertEqual(obs, False)

        obs = self.overview_map.hasUniqueCategoryValues('DOB')
        self.assertEqual(obs, False)

        obs = self.overview_map.hasUniqueCategoryValues('Description')
        self.assertEqual(obs, True)

    def test_hasSingleCategoryValue(self):
        """Test checking if a category has only a single value."""
        obs = self.overview_map.hasSingleCategoryValue('Treatment')
        self.assertEqual(obs, False)

        obs = self.single_value.hasSingleCategoryValue('Foo')
        self.assertEqual(obs, True)

    def test_getCategoryValue_bad_sample_id(self):
        """Test category value by sample ID accessor with bad sample IDs."""
        # Nonexistent sample ID.
        self.assertRaises(KeyError, self.overview_map.getCategoryValue,
            'PC.000', 'Treatment')
        self.assertRaises(KeyError, self.no_metadata.getCategoryValue,
            'PC.000', 'Treatment')
        # Integer sample ID.
        self.assertRaises(KeyError, self.overview_map.getCategoryValue, 42,
            'DOB')
        # Sample ID of type None.
        self.assertRaises(KeyError, self.overview_map.getCategoryValue, None,
            'Treatment')

        # Sample ID on empty map.
        self.assertRaises(KeyError, self.empty_map.getCategoryValue, 's1',
            'foo')
        # Integer sample ID on empty map.
        self.assertRaises(KeyError, self.empty_map.getCategoryValue, 1,
            'bar')
        # Sample ID of None on empty map.
        self.assertRaises(KeyError, self.empty_map.getCategoryValue, None,
            'baz')

    def test_getCategoryValue_bad_category(self):
        """Test category value by sample ID accessor with bad categories."""
        # Nonexistent category.
        self.assertRaises(KeyError, self.overview_map.getCategoryValue,
            'PC.354', 'foo')
        # Integer category.
        self.assertRaises(KeyError, self.overview_map.getCategoryValue,
            'PC.354', 42)
        # Category of type None.
        self.assertRaises(KeyError, self.overview_map.getCategoryValue,
            'PC.354', None)

        # Category on map with no metadata, but that has sample IDs.
        self.assertRaises(KeyError, self.no_metadata.getCategoryValue,
            'PC.354', 'Treatment')
        # Integer category on map with no metadata.
        self.assertRaises(KeyError, self.no_metadata.getCategoryValue,
            'PC.354', 34)
        # Category of type None on map with no metadata.
        self.assertRaises(KeyError, self.no_metadata.getCategoryValue,
            'PC.354', None)

    def test_SampleIds(self):
        """Test sample IDs accessor."""
        exp = ["PC.354", "PC.355", "PC.356", "PC.481", "PC.593", "PC.607",
               "PC.634", "PC.635", "PC.636"]
        obs = self.overview_map.SampleIds
        self.assertEqual(obs, exp)

        obs = self.no_metadata.SampleIds
        self.assertEqual(obs, exp)

        obs = self.empty_map.SampleIds
        self.assertEqual(obs, [])

    def test_CategoryNames(self):
        """Test category names accessor."""
        exp = ["BarcodeSequence", "DOB", "Description", "Treatment"]
        obs = self.overview_map.CategoryNames
        self.assertEqual(obs, exp)

        obs = self.no_metadata.CategoryNames
        self.assertEqual(obs, [])

        obs = self.empty_map.CategoryNames
        self.assertEqual(obs, [])

    def test_filterSamples(self):
        """Test filtering out samples from metadata map."""
        exp = ['PC.356', 'PC.593']
        self.overview_map.filterSamples(['PC.593', 'PC.356'])
        obs = self.overview_map.SampleIds
        self.assertEqual(obs, exp)

        self.overview_map.filterSamples([])
        self.assertEqual(self.overview_map.SampleIds, [])

    def test_filterSamples_strict(self):
        """Test strict checking of sample prescence when filtering."""
        with self.assertRaises(ValueError):
            self.overview_map.filterSamples(['PC.356', 'abc123'])

        with self.assertRaises(ValueError):
            self.empty_map.filterSamples(['foo'])

    def test_filterSamples_no_strict(self):
        """Test missing samples does not raise error."""
        self.overview_map.filterSamples(['PC.356', 'abc123'], strict=False)
        self.assertEqual(self.overview_map.SampleIds, ['PC.356'])

        self.empty_map.filterSamples(['foo'], strict=False)
        self.assertEqual(self.empty_map.SampleIds, [])


    def test_is_valid_git_refname(self):
        """Test correct validation of refnames"""
        # valid branchnames
        self.assertTrue(is_valid_git_refname('master'))
        self.assertTrue(is_valid_git_refname('debuggatron_2000'))
        self.assertTrue(is_valid_git_refname('refname/bar'))
        self.assertTrue(is_valid_git_refname('ref.nameslu/_eggs_/spam'))
        self.assertTrue(is_valid_git_refname('valid{0}char'.format(
            py_unichr(40))))
        self.assertTrue(is_valid_git_refname('master@head'))
        self.assertTrue(is_valid_git_refname('bar{thing}foo'))

        # case happening with git < 1.6.6
        self.assertFalse(is_valid_git_refname(
            '--abbrev-ref\nbaa350d7b7063d585ca293fc16ef15e0765dc9ee'))

        # different invalid refnames, for a description of each group see the
        # man page of git check-ref-format
        self.assertFalse(is_valid_git_refname('bar/.spam/eggs'))
        self.assertFalse(is_valid_git_refname('bar.lock/spam/eggs'))
        self.assertFalse(is_valid_git_refname('bar.lock'))
        self.assertFalse(is_valid_git_refname('.foobar'))

        self.assertFalse(is_valid_git_refname('ref..name'))

        self.assertFalse(is_valid_git_refname(u'invalid{0}char'.format(
            py_unichr(177))))
        self.assertFalse(is_valid_git_refname('invalid{0}char'.format(
            py_unichr(39))))
        self.assertFalse(is_valid_git_refname('ref~name/bar'))
        self.assertFalse(is_valid_git_refname('refname spam'))
        self.assertFalse(is_valid_git_refname('bar/foo/eggs~spam'))
        self.assertFalse(is_valid_git_refname('bar:_spam_'))
        self.assertFalse(is_valid_git_refname('eggtastic^2'))

        self.assertFalse(is_valid_git_refname('areyourandy?'))
        self.assertFalse(is_valid_git_refname('bar/*/spam'))
        self.assertFalse(is_valid_git_refname('bar[spam]/eggs'))

        self.assertFalse(is_valid_git_refname('/barfooeggs'))
        self.assertFalse(is_valid_git_refname('barfooeggs/'))
        self.assertFalse(is_valid_git_refname('bar/foo//////eggs'))

        self.assertFalse(is_valid_git_refname('dotEnding.'))

        self.assertFalse(is_valid_git_refname('@{branch'))

        self.assertFalse(is_valid_git_refname('contains\\slash'))

        self.assertFalse(is_valid_git_refname('$newbranch'))

    def test_is_valid_git_sha1(self):
        """ """

        # valid sha1 strings
        self.assertTrue(is_valid_git_sha1(
            '65a9ba2ef4b126fb5b054ea6b89b457463db4ec6'))
        self.assertTrue(is_valid_git_sha1(
            'a29a9911e41253405494c43889925a6d79ca26db'))
        self.assertTrue(is_valid_git_sha1(
            'e099cd5fdea89eba929d6051fbd26cc9e7a0c961'))
        self.assertTrue(is_valid_git_sha1(
            '44235d322c3386bd5ce872d9d7ea2e10d27c86cb'))
        self.assertTrue(is_valid_git_sha1(
            '7d2fc23E04540EE92c742948cca9ed5bc54d08d1'))
        self.assertTrue(is_valid_git_sha1(
            'fb5dc0285a8b11f199c4f3a7547a2da38138373f'))
        self.assertTrue(is_valid_git_sha1(
            '0b2abAEb195ba7ebc5cfdb53213a66fbaddefdb8'))

        # invalid length
        self.assertFalse(is_valid_git_sha1('cca9ed5bc54d08d1'))
        self.assertFalse(is_valid_git_sha1(''))

        # invalid characters
        self.assertFalse(is_valid_git_sha1(
            'fb5dy0f85a8b11f199c4f3a75474a2das8138373'))
        self.assertFalse(is_valid_git_sha1(
            '0x5dcc816fbc1c2e8eX087d7d2ed8d2950a7c16b'))

#run unit tests if run from command-line
if __name__ == '__main__':
    main()
