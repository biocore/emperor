# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main
from os.path import exists
from shutil import rmtree
from io import StringIO
from skbio import OrdinationResults

import pandas as pd
import numpy as np

from emperor.core import Emperor

# account for what's allowed in python 2 vs PY3K
try:
    from . import _test_core_strings as tcs
except:
    import _test_core_strings as tcs


class TopLevelTests(TestCase):
    def setUp(self):
        or_f = StringIO(tcs.PCOA_STRING)
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
        self.files_to_remove = []

        np.random.seed(111)

    def tearDown(self):
        for path in self.files_to_remove:
            if exists(path):
                rmtree(path)

    def test_str(self):
        emp = Emperor(self.ord_res, self.mf)
        self.assertEqual(emp.base_url, 'https://cdn.rawgit.com/biocore/emperor'
                                       '/new-api/emperor/support_files')

        obs = str(emp)

        try:
            self.assertItemsEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))
        self.assertEqual(tcs.HTML_STRING, obs)

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
            self.assertItemsEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))

        self.assertEqual(tcs.HTML_STRING, obs)

    def test_standalone(self):
        local_path = './some-local-path/'

        emp = Emperor(self.ord_res, self.mf, remote=local_path)
        self.assertEqual(emp.base_url, local_path)

        obs = emp.make_emperor(standalone=True)

        try:
            self.assertItemsEqual(tcs.STANDALONE_HTML_STRING.split('\n'),
                                  obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(tcs.STANDALONE_HTML_STRING.split('\n'),
                                  obs.split('\n'))
        self.assertEqual(tcs.STANDALONE_HTML_STRING, obs)

    def test_copy_support_files_use_base(self):
        local_path = './some-local-path/'

        emp = Emperor(self.ord_res, self.mf, remote=local_path)
        self.assertEqual(emp.base_url, local_path)

        emp.copy_support_files()

        self.assertTrue(exists(local_path))

        self.files_to_remove.append(local_path)

    def test_copy_support_files_use_target(self):
        local_path = './some-local-path/'

        emp = Emperor(self.ord_res, self.mf, remote=local_path)
        self.assertEqual(emp.base_url, local_path)

        emp.copy_support_files(target='./something-else')

        self.assertTrue(exists('./something-else'))

        self.files_to_remove.append(local_path)

if __name__ == "__main__":
    main()
