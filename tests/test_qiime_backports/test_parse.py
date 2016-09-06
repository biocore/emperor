#!/usr/bin/env python
#file test_parse.py

__author__ = "Rob Knight"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Rob Knight", "Justin Kuczynski", "Greg Caporaso",
               "Cathy Lozupone", "Jai Ram Rideout"] #remember to add yourself
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from unittest import TestCase, main

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from numpy import array
from numpy.testing import assert_almost_equal

from emperor.qiime_backports.parse import (parse_mapping_file,
    parse_metadata_state_descriptions, parse_coords, parse_classic_otu_table,
    mapping_file_to_dict, parse_mapping_file_to_dict, QiimeParseError)

class TopLevelTests(TestCase):

    def setUp(self):
        self.otu_table1 = otu_table1
        self.otu_table_without_leading_comment = \
            otu_table_without_leading_comment
        self.otu_table1_floats=otu_table1_floats
        self.legacy_otu_table1 = legacy_otu_table1
        self.expected_lineages1 = expected_lineages1

    def test_parse_mapping_file(self):
        """parse_mapping_file functions as expected"""
        s1 = ['#sample\ta\tb', '#comment line to skip',\
              'x \t y \t z ', ' ', '#more skip', 'i\tj\tk']
        exp = ([['x','y','z'],['i','j','k']],\
               ['sample','a','b'],\
               ['comment line to skip','more skip'])
        obs = parse_mapping_file(s1)
        self.assertEqual(obs, exp)

        # We don't currently support this, but we should soon...
        # # check that first non-comment, non-blank line is used as 
        # # header
        # s1 = ['sample\ta\tb', '#comment line to skip',\
        #       'x \t y \t z ', ' ', '#more skip', 'i\tj\tk']
        # exp = ([['x','y','z'],['i','j','k']],\
        #        ['sample','a','b'],\
        #        ['comment line to skip','more skip'])
        # obs = parse_mapping_file(s1)
        # self.assertEqual(obs, exp)

        #check that we strip double quotes by default
        s2 = ['#sample\ta\tb', '#comment line to skip',\
              '"x "\t" y "\t z ', ' ', '"#more skip"', 'i\t"j"\tk']
        obs = parse_mapping_file(s2)
        self.assertEqual(obs, exp)

    def test_mapping_file_to_dict(self):
        """parse_mapping_file functions as expected"""
        s1 = ['#sample\ta\tb', '#comment line to skip',\
              'x \t y \t z ', ' ', '#more skip', 'i\tj\tk']
        exp = ([['x','y','z'],['i','j','k']],\
               ['sample','a','b'],\
               ['comment line to skip','more skip'])
        mapres = parse_mapping_file(s1) # map_data, header, comments
        mapdict = mapping_file_to_dict(*mapres[:2])
        expdict = {'x':{'a':'y','b':'z'}, 'i':{'a':'j','b':'k'}}
        self.assertEqual(mapdict, expdict)

    def test_parse_mapping_file_to_dict(self):
        """parse_mapping_file functions as expected"""
        s1 = ['#sample\ta\tb', '#comment line to skip',\
              'x \t y \t z ', ' ', '#more skip', 'i\tj\tk']
        exp = ([['x','y','z'],['i','j','k']],\
               ['sample','a','b'],\
               ['comment line to skip','more skip'])
        mapdict, comments = parse_mapping_file_to_dict(s1)
        expdict = {'x':{'a':'y','b':'z'}, 'i':{'a':'j','b':'k'}}
        self.assertEqual(mapdict, expdict)
        self.assertEqual(comments, ['comment line to skip','more skip'])

    def test_parse_metadata_state_descriptions(self):
        """parse_metadata_state_descriptions should return correct states from string."""
        s = ''
        self.assertEqual(parse_metadata_state_descriptions(s), {})
        s = 'Study:Twin,Hand,Dog;BodySite:Palm,Stool'
        self.assertEqual(parse_metadata_state_descriptions(s), {'Study':set([
            'Twin','Hand','Dog']),'BodySite':set(['Palm','Stool'])})

        # category names with colons i. e. ontology-derived
        s = 'Study:Twin,Hand,Dog;site:UBERON:feces,UBERON:ear canal;'+\
            'env_feature:ENVO:farm soil,ENVO:national park'
        self.assertEqual(parse_metadata_state_descriptions(s), {'Study':
            set(['Twin', 'Hand', 'Dog']), 'site':set(['UBERON:feces',
            'UBERON:ear canal']), 'env_feature':set(['ENVO:farm soil',
            'ENVO:national park'])})

        s = "Treatment:A,B,C;env_matter:ENVO:nitsol,ENVO:farm soil;env_biom:"+\
            "ENVO:Tropical dry (including Monsoon forests) and woodlands,"+\
            "ENVO:Forest: including woodlands;country:GAZ:Persnickety Islands"+\
            ",St. Kitt's and Nevis"
        self.assertEqual(parse_metadata_state_descriptions(s), {"country":
            set(["GAZ:Persnickety Islands", "St. Kitt's and Nevis"]),
            "env_biom":set(["ENVO:Tropical dry (including Monsoon forests) "+\
            "and woodlands", "ENVO:Forest: including woodlands"]), "env_matter":
            set(["ENVO:nitsol","ENVO:farm soil"]), 'Treatment':set(["A", "B",
            "C"])})


    def test_parse_coords(self):
        """parse_coords should handle coords file"""
        coords = """pc vector number\t1\t2\t3
A\t0.11\t0.09\t0.23
B\t0.03\t0.07\t-0.26
C\t0.12\t0.06\t-0.32


eigvals\t4.94\t1.79\t1.50
% variation explained\t14.3\t5.2\t4.3


""".splitlines()
        obs = parse_coords(coords)
        exp = (['A','B','C'], 
            array([[.11,.09,.23],[.03,.07,-.26],[.12,.06,-.32]]),
            array([4.94,1.79,1.50]),
            array([14.3,5.2,4.3]))
        # test the header and the values apart from each other
        self.assertEqual(obs[0], exp[0])
        assert_almost_equal(obs[1], exp[1])

    def test_parse_coords_exceptions(self):
        """Check exceptions are raised accordingly with missing information"""

        # missing eigenvalues line
        with self.assertRaises(QiimeParseError):
            out = parse_coords(COORDS_NO_EIGENVALS.splitlines())
        # missing percentages explained line
        with self.assertRaises(QiimeParseError):
            out = parse_coords(COORDS_NO_PCNTS.splitlines())
        # missing vector number line
        with self.assertRaises(QiimeParseError):
            out = parse_coords(COORDS_NO_VECTORS.splitlines())

        # a whole different file (taxa summary)
        with self.assertRaises(QiimeParseError):
            out = parse_coords(taxa_summary1.splitlines())

    def test_parse_classic_otu_table_legacy(self):
        """parse_classic_otu_table functions as expected with legacy OTU table
        """
        data = self.legacy_otu_table1
        data_f = (data.split('\n'))
        obs = parse_classic_otu_table(data_f)
        exp = (['Fing','Key','NA'],
               ['0','1','2','3','4'],
               array([[19111,44536,42],[1216,3500,6],[1803,1184,2],
                      [1722,4903,17], [589,2074,34]]),
               self.expected_lineages1)

        # divide the comparisons into their four elements
        self.assertEqual(obs[0], exp[0])
        self.assertEqual(obs[1], exp[1])
        assert_almost_equal(obs[2], exp[2])
        self.assertEqual(obs[3], exp[3])
        
    def test_parse_classic_otu_table(self):
        """parse_classic_otu_table functions as expected with new-style OTU table
        """
        data = self.otu_table1
        data_f = (data.split('\n'))
        obs = parse_classic_otu_table(data_f)
        exp = (['Fing','Key','NA'],
               ['0','1','2','3','4'],
               array([[19111,44536,42],[1216,3500,6],[1803,1184,2],
                      [1722,4903,17], [589,2074,34]]),
               self.expected_lineages1)

        # divide the comparisons into their four elements
        self.assertEqual(obs[0], exp[0])
        self.assertEqual(obs[1], exp[1])
        assert_almost_equal(obs[2], exp[2])
        self.assertEqual(obs[3], exp[3])

        # test that the modified parse_classic performs correctly on OTU tables
        # without leading comments
        data = self.otu_table_without_leading_comment
        data_f = (data.split('\n'))
        obs = parse_classic_otu_table(data_f)
        sams = ['let-7i','miR-7','miR-17n','miR-18a','miR-19a','miR-22',
            'miR-25','miR-26a']
        otus = ['A2M', 'AAAS', 'AACS', 'AADACL1']
        vals = array([\
            [-0.2,  0.03680505,  0.205,  0.23,  0.66,  0.08,  -0.373,  0.26],
            [-0.09,  -0.25,  0.274,  0.15,  0.12,  0.29,  0.029,  -0.1148452],
            [0.33,  0.19,  0.27,  0.28,  0.19,  0.25,  0.089,  0.14],
            [0.49,  -0.92,  -0.723,  -0.23,  0.08,  0.49,  -0.386,  -0.64]])
        exp = (sams, otus, vals, []) # no lineages
        # because float comps in arrays always errors
        self.assertEqual(obs[0], exp[0])
        self.assertEqual(obs[1], exp[1])
        self.assertEqual(obs[3], exp[3])
        self.assertTrue(all((obs[2]==exp[2]).tolist()))

    def test_parse_classic_otu_table_floats_in_table(self):
        """parse_classic_otu_table functions using an OTU table containing floats
           but cast as int....this will automatically cast into floats"""
           
        data = self.otu_table1_floats
        data_f = (data.split('\n'))
        obs = parse_classic_otu_table(data_f)
        exp = (['Fing','Key','NA'],
               ['0','1','2','3','4'],
               array([[19111.0,44536.0,42.0],[1216.0,3500.0,6.0],
                      [1803.0,1184.0,2.0],[1722.1,4903.2,17.0],
                      [589.6,2074.4,34.5]]),
               self.expected_lineages1)
        # because float comps in arrays always errors
        self.assertEqual(obs[0], exp[0])
        self.assertEqual(obs[1], exp[1])
        self.assertEqual(obs[3], exp[3])
        self.assertTrue(all((obs[2]==exp[2]).tolist()))

    def test_parse_classic_otu_table_float_counts(self):
        """parse_classic_otu_table should return correct result from small table"""
        data = """#Full OTU Counts
#OTU ID	Fing	Key	NA	Consensus Lineage
0	19111	44536	42	Bacteria; Actinobacteria; Actinobacteridae; Propionibacterineae; Propionibacterium
1	1216	3500	6	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Lactobacillales; Lactobacillales; Streptococcaceae; Streptococcus
2	1803	1184	2	Bacteria; Actinobacteria; Actinobacteridae; Gordoniaceae; Corynebacteriaceae
3	1722	4903	17	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Staphylococcaceae
4	589	2074	34	Bacteria; Cyanobacteria; Chloroplasts; vectors"""
        data_f = (data.split('\n'))
        obs = parse_classic_otu_table(data_f,count_map_f=float)
        exp = (['Fing','Key','NA'],
               ['0','1','2','3','4'],
               array([[19111.,44536.,42.],[1216.,3500.,6.],[1803.,1184.,2.],\
                    [1722.,4903.,17.], [589,2074.,34.]]),
               [['Bacteria','Actinobacteria','Actinobacteridae','Propionibacterineae','Propionibacterium'],
                ['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Lactobacillales','Lactobacillales','Streptococcaceae','Streptococcus'],
                ['Bacteria','Actinobacteria','Actinobacteridae','Gordoniaceae','Corynebacteriaceae'],
                ['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Staphylococcaceae'],
                ['Bacteria','Cyanobacteria','Chloroplasts','vectors']])

        # because float comps in arrays always errors
        self.assertEqual(obs[0], exp[0])
        self.assertEqual(obs[1], exp[1])
        self.assertEqual(obs[3], exp[3])
        self.assertTrue(all((obs[2]==exp[2]).tolist()))

    def test_parse_classic_otu_table_file(self):
        """parse_classic_otu_table should return correct result on fileio format object"""
        data = """#Full OTU Counts
#OTU ID	Fing	Key	NA	Consensus Lineage
0	19111	44536	42	Bacteria; Actinobacteria; Actinobacteridae; Propionibacterineae; Propionibacterium
1	1216	3500	6	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Lactobacillales; Lactobacillales; Streptococcaceae; Streptococcus
2	1803	1184	2	Bacteria; Actinobacteria; Actinobacteridae; Gordoniaceae; Corynebacteriaceae
3	1722	4903	17	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Staphylococcaceae
4	589	2074	34	Bacteria; Cyanobacteria; Chloroplasts; vectors"""
        data_f = StringIO(data)
        obs = parse_classic_otu_table(data_f)
        exp = (['Fing','Key','NA'],
               ['0','1','2','3','4'],
               array([[19111,44536,42],[1216,3500,6],[1803,1184,2],\
                    [1722,4903,17], [589,2074,34]]),
               [['Bacteria','Actinobacteria','Actinobacteridae','Propionibacterineae','Propionibacterium'],
                ['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Lactobacillales','Lactobacillales','Streptococcaceae','Streptococcus'],
                ['Bacteria','Actinobacteria','Actinobacteridae','Gordoniaceae','Corynebacteriaceae'],
                ['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Staphylococcaceae'],
                ['Bacteria','Cyanobacteria','Chloroplasts','vectors']])
        # because float comps in arrays always errors
        self.assertEqual(obs[0], exp[0])
        self.assertEqual(obs[1], exp[1])
        self.assertEqual(obs[3], exp[3])
        self.assertTrue(all((obs[2]==exp[2]).tolist()))
        
    def test_parse_classic_otu_table_consensus_lineage(self):
        """parse_classic_otu_table should accept 'consensusLineage'"""
        data = """#Full OTU Counts
#OTU ID	Fing	Key	NA	consensusLineage
0	19111	44536	42	Bacteria; Actinobacteria; Actinobacteridae; Propionibacterineae; Propionibacterium
1	1216	3500	6	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Lactobacillales; Lactobacillales; Streptococcaceae; Streptococcus
2	1803	1184	2	Bacteria; Actinobacteria; Actinobacteridae; Gordoniaceae; Corynebacteriaceae
3	1722	4903	17	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Staphylococcaceae
4	589	2074	34	Bacteria; Cyanobacteria; Chloroplasts; vectors"""
        data_f = StringIO(data)
        obs = parse_classic_otu_table(data_f)
        exp = (['Fing','Key','NA'],
               ['0','1','2','3','4'],
               array([[19111,44536,42],[1216,3500,6],[1803,1184,2],\
                    [1722,4903,17], [589,2074,34]]),
               [['Bacteria','Actinobacteria','Actinobacteridae','Propionibacterineae','Propionibacterium'],
                ['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Lactobacillales','Lactobacillales','Streptococcaceae','Streptococcus'],
                ['Bacteria','Actinobacteria','Actinobacteridae','Gordoniaceae','Corynebacteriaceae'],
                ['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Staphylococcaceae'],
                ['Bacteria','Cyanobacteria','Chloroplasts','vectors']])
        # because float comps in arrays always errors
        self.assertEqual(obs[0], exp[0])
        self.assertEqual(obs[1], exp[1])
        self.assertEqual(obs[3], exp[3])
        self.assertTrue(all((obs[2]==exp[2]).tolist()))

legacy_otu_table1 = """# some comment goes here
#OTU ID	Fing	Key	NA	Consensus Lineage
0	19111	44536	42	Bacteria; Actinobacteria; Actinobacteridae; Propionibacterineae; Propionibacterium

1	1216	3500	6	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Lactobacillales; Lactobacillales; Streptococcaceae; Streptococcus
2	1803	1184	2	Bacteria; Actinobacteria; Actinobacteridae; Gordoniaceae; Corynebacteriaceae
3	1722	4903	17	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Staphylococcaceae
4	589	2074	34	Bacteria; Cyanobacteria; Chloroplasts; vectors
"""

otu_table1 = """# Some comment




OTU ID	Fing	Key	NA	Consensus Lineage
0	19111	44536	42	Bacteria; Actinobacteria; Actinobacteridae; Propionibacterineae; Propionibacterium
# some other comment
1	1216	3500	6	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Lactobacillales; Lactobacillales; Streptococcaceae; Streptococcus
2	1803	1184	2	Bacteria; Actinobacteria; Actinobacteridae; Gordoniaceae; Corynebacteriaceae
# comments
#    everywhere!
3	1722	4903	17	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Staphylococcaceae
4	589	2074	34	Bacteria; Cyanobacteria; Chloroplasts; vectors
"""

otu_table1_floats = """# Some comment




OTU ID	Fing	Key	NA	Consensus Lineage
0	19111.0	44536.0	42.0	Bacteria; Actinobacteria; Actinobacteridae; Propionibacterineae; Propionibacterium
# some other comment
1	1216.0	3500.0	6.0	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Lactobacillales; Lactobacillales; Streptococcaceae; Streptococcus
2	1803.0	1184.0	2.0	Bacteria; Actinobacteria; Actinobacteridae; Gordoniaceae; Corynebacteriaceae
# comments
#    everywhere!
3	1722.1	4903.2	17	Bacteria; Firmicutes; Alicyclobacillaceae; Bacilli; Staphylococcaceae
4	589.6	2074.4	34.5	Bacteria; Cyanobacteria; Chloroplasts; vectors
"""


otu_table_without_leading_comment = '#OTU ID\tlet-7i\tmiR-7\tmiR-17n\tmiR-18a\tmiR-19a\tmiR-22\tmiR-25\tmiR-26a\nA2M\t-0.2\t0.03680505\t0.205\t0.23\t0.66\t0.08\t-0.373\t0.26\nAAAS\t-0.09\t-0.25\t0.274\t0.15\t0.12\t0.29\t0.029\t-0.114845199\nAACS\t0.33\t0.19\t0.27\t0.28\t0.19\t0.25\t0.089\t0.14\nAADACL1\t0.49\t-0.92\t-0.723\t-0.23\t0.08\t0.49\t-0.386\t-0.64'

expected_lineages1 = [['Bacteria','Actinobacteria','Actinobacteridae','Propionibacterineae','Propionibacterium'],
['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Lactobacillales','Lactobacillales','Streptococcaceae','Streptococcus'],
['Bacteria','Actinobacteria','Actinobacteridae','Gordoniaceae','Corynebacteriaceae'],
['Bacteria','Firmicutes','Alicyclobacillaceae','Bacilli','Staphylococcaceae'],
['Bacteria','Cyanobacteria','Chloroplasts','vectors']]


COORDS_NO_VECTORS = """A\t0.11\t0.09\t0.23
B\t0.03\t0.07\t-0.26
C\t0.12\t0.06\t-0.32
eigvals\t4.94\t1.79\t1.50
% variation explained\t14.3\t5.2\t4.3"""

COORDS_NO_EIGENVALS = """pc vector number\t1\t2\t3
A\t0.11\t0.09\t0.23
B\t0.03\t0.07\t-0.26
C\t0.12\t0.06\t-0.32
foo\t4.94\t1.79\t1.50
% variation explained\t14.3\t5.2\t4.3"""

COORDS_NO_PCNTS = """pc vector number\t1\t2\t3
A\t0.11\t0.09\t0.23
B\t0.03\t0.07\t-0.26
C\t0.12\t0.06\t-0.32
eigvals\t4.94\t1.79\t1.50"""

taxa_summary1 = """#Full OTU Counts
Taxon\tEven1\tEven2\tEven3
Bacteria;Actinobacteria;Actinobacteria(class);Actinobacteridae\t0.0880247251673\t0.0721968465746\t0.081371761759
Bacteria;Bacteroidetes/Chlorobigroup;Bacteroidetes;Bacteroidia\t0.192137761955\t0.191095101593\t0.188504131885
Bacteria;Firmicutes;Bacilli;Lactobacillales\t0.0264895739603\t0.0259942669171\t0.0318460745596
# some comment
Bacteria;Firmicutes;Clostridia;Clostridiales\t0.491800007824\t0.526186212556\t0.49911159984
Bacteria;Firmicutes;Erysipelotrichi;Erysipelotrichales\t0.0311411916592\t0.0184083913576\t0.0282325481054
Bacteria;Proteobacteria;Gammaproteobacteria;Enterobacteriales\t0.166137214246\t0.163087129528\t0.168923372865
No blast hit;Other\t0.00426952518811\t0.00303205147361\t0.0020105109874"""

if __name__ == '__main__':
    main()
