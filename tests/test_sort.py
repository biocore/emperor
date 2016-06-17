# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main

from numpy import array
from numpy.testing import assert_almost_equal

from emperor.sort import (sort_taxa_table_by_pcoa_coords,
                          sort_comparison_filenames)


class TopLevelTests(TestCase):
    def setUp(self):
        self.otu_headers = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354',
                            'PC.593', 'PC.355', 'PC.607', 'PC.634']

        self.otu_table = array(
            [[0.02739726, 0.04697987, 0.02, 0.04697987, 0.01, 0.02027027,
              0.01360544, 0.01342282, 0.02666667],
             [0.00684932, 0.02013423, 0.02, 0.00671141,  0., 0.00675676, 0.,
              0., 0.],
             [0.14383562, 0.27516779, 0.65333333, 0.52348993, 0.38926174,
              0.69594595, 0.28571429, 0.0738255, 0.19333333],
             [0., 0.02013423, 0.03333333, 0.01342282, 0., 0.0472973, 0.,
              0., 0.],
             [0.78767123, 0.45637584, 0.22, 0.39597315, 0.41610738, 0.20945946,
              0.70068027, 0.89932886, 0.77333333],
             [0., 0.02013423, 0.01333333, 0.00671141, 0.03355705, 0.00675676,
              0., 0., 0.],
             [0., 0., 0.01333333, 0., 0., 0., 0., 0., 0.],
             [0.03424658, 0.16107383, 0.02666667, 0.00671141, 0.14765101,
              0.01351351, 0., 0.01342282, 0.00666667]])

        self.coords = COORDS
        self.coords_header = ['PC.354', 'PC.356', 'PC.481', 'PC.593', 'PC.355',
                              'PC.607', 'PC.634', 'PC.636', 'PC.635']

        self.coord_fps = [
            'output_data/emperor/bray_curtis_pc_transformed_q1.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q10.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q11.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q12.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q13.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q14.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q15.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q16.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q17.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q18.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q19.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q2.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q20.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q21.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q22.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q23.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q24.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q25.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q26.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q27.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q28.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q29.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q3.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q4.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q5.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q6.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q7.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q8.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q9.txt']

        self.coord_fps_garbage = [
            'output_data/emperor/bray_qurtis_pc_transformed_q1.txt',
            'output_data/emperor/bray_111urtis_q_transformed_q10.txt',
            'output_data/emperor/aaaaaaa.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q12.txt',
            'output_data/emperor/qqq2223_curtis_qc_transformed_q13.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q14.txt',
            'output_data/emperor/bray_curtis_pc_transformed_reference.'
            'txtoutput_data/emperor/bray_curtis_pc_transformed_q15.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q16.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q17.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q18.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q19.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q2.txt',
            'output_data/emperor/boom.txt',
            'output_data/emperor/another_file with some characters '
            'and stuff .txt',
            'output_data/emperor/some_other_file_that_foo_wants_to_'
            'compare.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q23.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q24.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q25.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q26.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q27.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q28.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q29.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q3.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q4.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q5.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q6.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q7.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q8.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q9.txt']

    def test_sort_taxa_table_by_pcoa_coords(self):
        """Make sure OTU table and coordinates are sorted equally"""

        # case with shuffled inputs
        o_headers, o_otu_table = sort_taxa_table_by_pcoa_coords(
            self.coords_header, self.otu_table, self.otu_headers)

        self.assertEqual(o_headers, ['PC.354', 'PC.356', 'PC.481', 'PC.593',
                                     'PC.355', 'PC.607', 'PC.634', 'PC.636',
                                     'PC.635'])
        assert_almost_equal(o_otu_table, OTU_TABLE_A)

        # case with shuffled inputs and fewer samples
        o_headers, o_otu_table = sort_taxa_table_by_pcoa_coords(
            ['PC.354', 'PC.356', 'PC.635'], self.otu_table, self.otu_headers)
        self.assertEqual(o_headers, ['PC.354', 'PC.356', 'PC.635'])
        assert_almost_equal(o_otu_table, array(
            [[0.01, 0.02, 0.04697987],
             [0., 0.02, 0.02013423],
             [0.38926174, 0.65333333, 0.27516779],
             [0., 0.03333333, 0.02013423],
             [0.41610738, 0.22, 0.45637584],
             [0.03355705, 0.01333333, 0.02013423],
             [0., 0.01333333, 0.],
             [0.14765101, 0.02666667, 0.16107383]]))

    def test_sort_comparison_filenames_regular(self):
        """Check filenames are sorted correctly"""

        # check it correctly sorts the files according to the suffix
        out_sorted = sort_comparison_filenames(self.coord_fps)
        self.assertEqual(out_sorted, [
            'output_data/emperor/bray_curtis_pc_transformed_q1.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q2.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q3.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q4.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q5.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q6.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q7.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q8.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q9.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q10.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q11.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q12.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q13.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q14.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q15.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q16.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q17.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q18.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q19.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q20.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q21.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q22.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q23.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q24.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q25.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q26.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q27.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q28.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q29.txt'])

        # if files with garbage are passed in, the sorting should be still
        # consistent,putting the "garbaged" filenames at the beginning
        out_sorted = sort_comparison_filenames(self.coord_fps_garbage)
        self.assertEqual(out_sorted, [
            'output_data/emperor/aaaaaaa.txt',
            'output_data/emperor/boom.txt',
            'output_data/emperor/another_file with some characters and '
            'stuff .txt',
            'output_data/emperor/some_other_file_that_foo_wants_to_'
            'compare.txt',
            'output_data/emperor/bray_qurtis_pc_transformed_q1.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q2.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q3.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q4.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q5.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q6.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q7.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q8.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q9.txt',
            'output_data/emperor/bray_111urtis_q_transformed_q10.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q12.txt',
            'output_data/emperor/qqq2223_curtis_qc_transformed_q13.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q14.txt',
            'output_data/emperor/bray_curtis_pc_transformed_reference.'
            'txtoutput_data/emperor/bray_curtis_pc_transformed_q15.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q16.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q17.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q18.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q19.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q23.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q24.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q25.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q26.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q27.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q28.txt',
            'output_data/emperor/bray_curtis_pc_transformed_q29.txt'])

        # tricky case with extensions in things that are not the filename
        out_sorted = sort_comparison_filenames([
            'output_data_q1.txt/emperor/bray_curtis_pc_transformed_q9.txt',
            'output_data/emperorq11.txt/bray_curtis_pc_transformed_q2.txt',
            'output_data_q44.txt/emperor/bray_curtis_pc_transformed_q11.txt',
            'output_dataq-5.txt/emperor/bray_curtis_pc_transformed_q3.txt',
            'output_data_q511.txt/emperor/bray_curtis_pc_transformed_q1.txt'])
        self.assertEqual(out_sorted, [
            'output_data_q511.txt/emperor/bray_curtis_pc_transformed_q1.txt',
            'output_data/emperorq11.txt/bray_curtis_pc_transformed_q2.txt',
            'output_dataq-5.txt/emperor/bray_curtis_pc_transformed_q3.txt',
            'output_data_q1.txt/emperor/bray_curtis_pc_transformed_q9.txt',
            'output_data_q44.txt/emperor/bray_curtis_pc_transformed_q11.txt'])

        # make sure nothing happens when an empty list is passed
        self.assertEqual(sort_comparison_filenames([]), [])


COORDS = array(
    [[0.280399117569, -0.0060128286014, 0.0234854344148, -0.0468109474823,
      -0.146624450094, 0.00566979124596, -0.0354299634191, -0.255785794275,
      -4.84141986706e-09],
     [0.228820399536, -0.130142097093, -0.287149447883, 0.0864498846421,
      0.0442951919304, 0.20604260722, 0.0310003571386, 0.0719920436501,
      -4.84141986706e-09],
     [0.0422628480532, -0.0139681511889, 0.0635314615517, -0.346120552134,
      -0.127813807608, 0.0139350721063, 0.0300206887328, 0.140147849223,
      -4.84141986706e-09],
     [0.232872767451, 0.139788385269, 0.322871079774, 0.18334700682,
      0.0204661596818, 0.0540589147147, -0.0366250872041, 0.0998235721267,
      -4.84141986706e-09],
     [0.170517581885, -0.194113268955, -0.0308965283066, 0.0198086158783,
      0.155100062794, -0.279923941712, 0.0576092515759, 0.0242481862127,
      -4.84141986706e-09],
     [-0.0913299284215, 0.424147148265, -0.135627421345, -0.057519480907,
      0.151363490722, -0.0253935675552, 0.0517306152066, -0.038738217609,
      -4.84141986706e-09],
     [-0.349339228244, -0.120787589539, 0.115274502117, 0.0694953933826,
      -0.0253722182853, 0.067853201946, 0.244447634756, -0.0598827706386,
      -4.84141986706e-09],
     [-0.276542163845, -0.144964375408, 0.0666467344429, -0.0677109454288,
      0.176070269506, 0.072969390136, -0.229889463523, -0.0465989416581,
      -4.84141986706e-09],
     [-0.237661393984, 0.0460527772512, -0.138135814766, 0.159061025229,
      -0.247484698646, -0.115211468101, -0.112864033263, 0.0647940729676,
      -4.84141986706e-09]])

OTU_TABLE_A = array(
    [[0.01, 0.02, 0.04697987, 0.02027027, 0.01360544, 0.01342282, 0.02666667,
      0.02739726, 0.04697987],
     [0., 0.02, 0.00671141, 0.00675676, 0., 0., 0., 0.00684932, 0.02013423],
     [0.38926174, 0.65333333, 0.52348993, 0.69594595, 0.28571429, 0.0738255,
      0.19333333, 0.14383562, 0.27516779],
     [0., 0.03333333, 0.01342282, 0.0472973, 0., 0., 0., 0., 0.02013423],
     [0.41610738, 0.22, 0.39597315, 0.20945946, 0.70068027, 0.89932886,
      0.77333333, 0.78767123, 0.45637584],
     [0.03355705, 0.01333333, 0.00671141, 0.00675676, 0., 0., 0., 0.,
      0.02013423],
     [0., 0.01333333, 0., 0., 0., 0., 0., 0., 0.],
     [0.14765101, 0.02666667, 0.00671141, 0.01351351, 0., 0.01342282,
      0.00666667, 0.03424658, 0.16107383]])


if __name__ == "__main__":
    main()
