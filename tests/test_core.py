# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main
from io import StringIO
from skbio import OrdinationResults

import pandas as pd
import numpy as np

from emperor.core import Emperor
from _test_core_strings import PCOA_STRING, HTML_STRING


class TopLevelTests(TestCase):
    def setUp(self):
        or_f = StringIO(PCOA_STRING)
        self.ord_res = OrdinationResults.read(or_f)

        data = \
            [['PC.354', 'Control', '20061218', 'Ctrol_mouse_I.D._354'],
             ['PC.355', 'Control', '20061218', 'Control_mouse_I.D._355'],
             ['PC.356', 'Control', '20061126', 'Control_mouse_I.D._356'],
             ['PC.481', 'Control', '20070314', 'Control_mouse_I.D._481'],
             ['PC.593', 'Control', '20071210', 'Control_mouse_I.D._593'],
             ['PC.607', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
             ['PC.634', 'Fast', '20080116', 'Fasting_mouse_I.D._634'],
             ['PC.635', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
             ['PC.636', 'Fast', '20080116', 'Fasting_mouse_I.D._636']]
        headers = ['SampleID', 'Treatment', 'DOB', 'Description']
        self.mf = pd.DataFrame(data=data, columns=headers)
        self.mf.set_index('SampleID', inplace=True)

        np.random.seed(111)

    def test_str(self):
        emp = Emperor(self.ord_res, self.mf)
        self.assertEqual(emp.base_url, 'https://cdn.rawgit.com/biocore/emperor'
                                       '/new-api/emperor/support_files')

        obs = str(emp)

        try:
            self.assertItemsEqual(HTML_STRING.split('\n'), obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(HTML_STRING.split('\n'), obs.split('\n'))
        self.assertEqual(HTML_STRING, obs)

    def test_remote_url(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        self.assertEqual(emp.base_url, "/nbextensions/emperor/support_files")

    def test_remote_url_custom(self):
        emp = Emperor(self.ord_res, self.mf, remote='/foobersurus/bar/')
        self.assertEqual(emp.base_url, '/foobersurus/bar/')

    def test_unnamed_index(self):
        self.mf.index.name = None
        emp = Emperor(self.ord_res, self.mf)
        obs = str(emp)

        try:
            self.assertItemsEqual(HTML_STRING.split('\n'), obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(HTML_STRING.split('\n'), obs.split('\n'))

        self.assertEqual(HTML_STRING, obs)


if __name__ == "__main__":
    main()
