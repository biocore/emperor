# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main
from StringIO import StringIO
from skbio.stats.ordination import OrdinationResults

from emperor.core import Emperor
from _test_core_strings import PCOA_STRING, HTML_STRING


class TopLevelTests(TestCase):
    def setUp(self):
        or_f = StringIO(PCOA_STRING)
        self.ord_res = OrdinationResults.read(or_f)

        self.data = \
            [['PC.354', 'Control', '20061218', 'Ctrol_mouse_I.D._354'],
             ['PC.355', 'Control', '20061218', 'Control_mouse_I.D._355'],
             ['PC.356', 'Control', '20061126', 'Control_mouse_I.D._356'],
             ['PC.481', 'Control', '20070314', 'Control_mouse_I.D._481'],
             ['PC.593', 'Control', '20071210', 'Control_mouse_I.D._593'],
             ['PC.607', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
             ['PC.634', 'Fast', '20080116', 'Fasting_mouse_I.D._634'],
             ['PC.635', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
             ['PC.636', 'Fast', '20080116', 'Fasting_mouse_I.D._636']]
        self.headers = ['SampleID', 'Treatment', 'DOB', 'Description']

    def test_str(self):
        emp = Emperor(self.ord_res, self.data, self.headers)
        self.assertItemsEqual(HTML_STRING.split('\n'), str(emp).split('\n'))
        self.assertEqual(HTML_STRING, str(emp))

    def test_ids(self):
        emp = Emperor(self.ord_res, self.data, self.headers)
        self.assertEqual(['PC.354', 'PC.355', 'PC.356', 'PC.481', 'PC.593',
                          'PC.607', 'PC.634', 'PC.635', 'PC.636'],
                         emp.ids)


if __name__ == "__main__":
    main()
