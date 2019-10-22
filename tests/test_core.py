# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from unittest import TestCase, main
from copy import deepcopy
from os.path import exists
from shutil import rmtree
from io import StringIO
from skbio import OrdinationResults
from jinja2 import Template

import warnings
import pandas as pd
import numpy as np

from emperor.core import Emperor
from emperor.util import EmperorWarning

# account for what's allowed in python 2 vs PY3K
try:
    from . import _test_core_strings as tcs
except Exception:
    import _test_core_strings as tcs


class TopLevelTests(TestCase):
    def setUp(self):
        self.maxDiff = None
        or_f = StringIO(tcs.PCOA_STRING)
        self.ord_res = OrdinationResults.read(or_f)

        eigvals = self.ord_res.eigvals
        samples = self.ord_res.samples
        props = self.ord_res.proportion_explained

        # make modified copies of the ordinations
        a = OrdinationResults(eigvals=eigvals.copy(),
                              samples=np.abs(samples).copy(),
                              proportion_explained=props.copy(),
                              short_method_name='PCoA',
                              long_method_name='Princpal Coordinates Analysis')
        b = OrdinationResults(eigvals=eigvals.copy(),
                              samples=np.sin(samples).copy(),
                              proportion_explained=props.copy(),
                              short_method_name='PCoA',
                              long_method_name='Princpal Coordinates Analysis')
        c = OrdinationResults(eigvals=eigvals.copy(),
                              samples=np.cos(samples.copy()),
                              proportion_explained=props.copy(),
                              short_method_name='PCoA',
                              long_method_name='Princpal Coordinates Analysis')

        # biplot ordination with 5 features
        features = np.abs(samples / 2.0).copy()[:5]
        features.index = 'f.' + features.index

        biplot_scores = np.ones((9, 5))
        d = OrdinationResults(eigvals=eigvals.copy(),
                              samples=samples.copy(),
                              features=features,
                              biplot_scores=biplot_scores,
                              proportion_explained=props.copy(),
                              short_method_name='RDA',
                              long_method_name='Redundancy Analysis')

        self.biplot = d

        feature_mf = pd.DataFrame(index=['f.PC.636', 'f.PC.635', 'f.PC.356',
                                         'f.PC.481', 'f.PC.354'])
        feature_mf['Category'] = ['foo', 'bar', 'baz', 'foo', 'foo']
        feature_mf['Second'] = ['No', 'Yes', 'Noes', 'Noooo', 'Yep']
        self.feature_mf = feature_mf

        self.jackknifed = [a, b, c]

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

        # note that we don't test with remote=True because the url is resolved
        # by emperor.util.resolve_stable_url, so it is bound to change
        # depending on the environment executing the test
        self.url = ('https://cdn.rawgit.com/biocore/emperor/new-api/emperor/'
                    'support_files')

        self.expected_metadata = [['PC.636', 'Fast', '20080116',
                                   'Fasting_mouse_I.D._636'],
                                  ['PC.635', 'Fast', '20080116',
                                   'Fasting_mouse_I.D._635'],
                                  ['PC.356', 'Control', '20061126',
                                   'Control_mouse_I.D._356'],
                                  ['PC.481', 'Control', '20070314',
                                   'Control_mouse_I.D._481'],
                                  ['PC.354', 'Control', '20061218',
                                   'Ctrol_mouse_I.D._354'],
                                  ['PC.593', 'Control', '20071210',
                                   'Control_mouse_I.D._593'],
                                  ['PC.355', 'Control', '20061218',
                                   'Control_mouse_I.D._355'],
                                  ['PC.607', 'Fast', '20071112',
                                   'Fasting_mouse_I.D._607'],
                                  ['PC.634', 'Fast', '20080116',
                                   'Fasting_mouse_I.D._634']]

        self.expected_coords = [[-0.65199581, -0.3417785, 0.15713116,
                                 -0.15964022, 0.415116],
                                [-0.5603277, 0.10857736, -0.32567899,
                                 0.37501378, -0.58348783],
                                [0.53948353, -0.30683242, -0.67700431,
                                 0.2038205, 0.10443355],
                                [0.09964195, -0.03293232, 0.14978637,
                                 -0.81603885, -0.30134308],
                                [0.66108924, -0.01417628, 0.05537096,
                                 -0.11036488, -0.34569241],
                                [0.54903768, 0.32957521, 0.76122421,
                                 0.43227217, 0.0482525],
                                [0.40202459, -0.45765549, -0.07284389,
                                 0.04670223, 0.36567513],
                                [-0.21532605, 1., -0.31976502, -0.13561209,
                                 0.35686552],
                                [-0.82362744, -0.28477756, 0.27177951,
                                 0.16384737, -0.05981938]]

        self.expected_biplot_coords = [
            [0.7989764321707692, 0.41882625725119405, 0.19255353093594343,
             0.19562821395993216, 0.5086963730424037],
            [0.6866434036312, 0.1330541540144393, 0.39909740671082994,
             0.45955382957848684, 0.7150245690992273],
            [0.6611002961979922, 0.37600222318672283, 0.8296226448056473,
             0.24976813456784003, 0.12797619689815815],
            [0.12210441648907923, 0.04035631834856271, 0.18355298799796177,
             1.0, 0.3692754065598425],
            [0.8101198147298804, 0.01737206462987538, 0.06785333685041521,
             0.135244634257307, 0.4236224898810244]]

        np.random.seed(111)

    def tearDown(self):
        for path in self.files_to_remove:
            if exists(path):
                rmtree(path)

    def test_plot_width_and_height(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        emp.width = '111px'
        emp.height = '111px'

        self.assertEqual(emp.width, '111px')
        self.assertEqual(emp.height, '111px')

    def test_initial(self):
        emp = Emperor(self.ord_res, self.mf, remote=self.url)

        self.assertEqual(emp.width, '100%')
        self.assertEqual(emp.height, '500px')
        self.assertEqual(emp.settings, {})

        self.assertEqual(emp.base_url, 'https://cdn.rawgit.com/biocore/emperor'
                                       '/new-api/emperor/support_files')

        self.assertEqual(emp.jackknifed, [])
        self.assertEqual(emp.procrustes, [])
        self.assertEqual(emp.procrustes_names, [])

        self.assertEqual(emp.custom_axes, [])
        self.assertEqual(emp.jackknifing_method, 'IQR')
        emp.jackknifing_method = 'sdev'
        self.assertEqual(emp.jackknifing_method, 'sdev')

    def test_initial_biplots(self):
        emp = Emperor(self.biplot, self.mf, self.feature_mf, remote=self.url)

        self.assertEqual(emp.width, '100%')
        self.assertEqual(emp.height, '500px')
        self.assertEqual(emp.settings, {})

        self.assertEqual(emp.jackknifed, [])
        self.assertEqual(emp.procrustes, [])
        self.assertEqual(emp.procrustes_names, [])

        self.assertEqual(emp.custom_axes, [])
        self.assertEqual(emp.jackknifing_method, 'IQR')

        feature_mf = pd.DataFrame(index=['f.PC.636', 'f.PC.635', 'f.PC.356',
                                         'f.PC.481', 'f.PC.354'])
        feature_mf['Category'] = ['foo', 'bar', 'baz', 'foo', 'foo']
        feature_mf['Second'] = ['No', 'Yes', 'Noes', 'Noooo', 'Yep']

        # it is redundant, but the mapping file should remain untouched
        pd.util.testing.assert_frame_equal(feature_mf, emp.feature_mf,
                                           check_names=False)

        self.assertEqual(emp.base_url, 'https://cdn.rawgit.com/biocore/emperor'
                                       '/new-api/emperor/support_files')

    def test_initial_biplots_no_metadata(self):
        emp = Emperor(self.biplot, self.mf, remote=self.url)

        self.assertEqual(emp.width, '100%')
        self.assertEqual(emp.height, '500px')
        self.assertEqual(emp.settings, {})

        self.assertEqual(emp.jackknifed, [])
        self.assertEqual(emp.procrustes, [])
        self.assertEqual(emp.procrustes_names, [])

        empty_mf = pd.DataFrame(index=['f.PC.636', 'f.PC.635', 'f.PC.356',
                                       'f.PC.481', 'f.PC.354'])
        empty_mf['all'] = 'All elements'

        pd.util.testing.assert_frame_equal(empty_mf, emp.feature_mf,
                                           check_names=False)

        self.assertEqual(emp.base_url, 'https://cdn.rawgit.com/biocore/emperor'
                                       '/new-api/emperor/support_files')

    def test_one_dimensional(self):
        self.ord_res.samples = self.ord_res.samples.iloc[:, :1].copy()
        self.ord_res.eigvals = self.ord_res.eigvals.iloc[:1].copy()
        self.ord_res.proportion_explained = \
            self.ord_res.proportion_explained[:1].copy()

        with self.assertRaisesRegexp(ValueError, "Ordinations with less than "
                                     "two dimensions are not supported"):
            Emperor(self.ord_res, self.mf, remote=False)

    def test_initial_unbalanced_more_than_five(self):
        mf = self.mf.copy()
        mf.drop(['PC.354', 'PC.355', 'PC.356', 'PC.481', 'PC.607', 'PC.636'],
                inplace=True)
        with self.assertRaisesRegexp(KeyError, "There are samples not "
                                     "included in the sample mapping file. "
                                     "Override this error by using the "
                                     "`ignore_missing_samples` argument. "
                                     "Showing only the first 5 samples out of "
                                     "6: PC.354, PC.355, PC.356, PC.481, "
                                     "PC.607 ..."):
            Emperor(self.ord_res, mf, remote=self.url)

    def test_initial_unbalanced(self):
        mf = self.mf.copy()
        mf.drop(['PC.354'], inplace=True)
        with self.assertRaisesRegexp(KeyError, "There are samples not "
                                     "included in the sample mapping file. "
                                     "Override this error by using the "
                                     "`ignore_missing_samples` argument. "
                                     "Offending samples: PC.354"):
            Emperor(self.ord_res, mf, remote=self.url)

        # test feature metadata
        fmf = self.feature_mf.copy()
        fmf.drop(['f.PC.636'], inplace=True)
        with self.assertRaisesRegexp(KeyError, "There are features not "
                                     "included in the feature mapping file. "
                                     "Override this error by using the "
                                     "`ignore_missing_samples` argument. "
                                     "Offending features: f.PC.636"):
            Emperor(self.biplot, self.mf, fmf, remote=self.url)

    def test_initial_unbalanced_ignore(self):
        expected = self.mf.copy()

        mf = self.mf.copy()
        mf.drop(['PC.634'], inplace=True)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            emp = Emperor(self.ord_res, mf, remote=self.url,
                          ignore_missing_samples=True)

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, EmperorWarning))
            self.assertEqual("1 out of 9 samples have no metadata and are "
                             "being included with a placeholder value.",
                             str(w[-1].message))

            expected.loc['PC.634'] = ['This element has no metadata'] * 3

            pd.util.testing.assert_frame_equal(expected.sort_index(),
                                               emp.mf.sort_index(),
                                               check_names=False)

        expected = self.feature_mf.copy()

        fmf = self.feature_mf.copy()
        fmf.drop(['f.PC.636'], inplace=True)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            emp = Emperor(self.biplot, self.mf, fmf, remote=self.url,
                          ignore_missing_samples=True)

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, EmperorWarning))
            self.assertEqual("1 out of 5 features have no metadata and are "
                             "being included with a placeholder value.",
                             str(w[-1].message))

            expected.loc['f.PC.636'] = ['This element has no metadata'] * 2

            pd.util.testing.assert_frame_equal(expected.sort_index(),
                                               emp.feature_mf.sort_index(),
                                               check_names=False)

    def test_no_overlap(self):
        mf = self.mf.copy()
        mf.index = mf.index + '.not'

        with self.assertRaisesRegexp(ValueError, 'None of the sample '
                                     'identifiers match between the metadata '
                                     'and the coordinates. Verify that you are'
                                     ' using metadata and coordinates '
                                     'corresponding to the same dataset.'):
            Emperor(self.ord_res, mf, remote=self.url)

        fmf = self.feature_mf.copy()
        fmf.index = fmf.index + '.not'

        with self.assertRaisesRegexp(ValueError, 'None of the feature '
                                     'identifiers match between the metadata '
                                     'and the coordinates. Verify that you are'
                                     ' using metadata and coordinates '
                                     'corresponding to the same dataset.'):
            Emperor(self.biplot, self.mf, fmf, remote=self.url)

    def test_get_template(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        obs = emp._get_template(False)

        self.assertTrue(isinstance(obs, Template))
        self.assertTrue(obs.filename.endswith('/jupyter-template.html'))

    def test_get_template_standalone(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        obs = emp._get_template(True)

        self.assertTrue(isinstance(obs, Template))
        self.assertTrue(obs.filename.endswith('/standalone-template.html'))

    def test_formatting(self):
        emp = Emperor(self.ord_res, self.mf, remote=self.url)

        obs = str(emp)

        try:
            self.assertItemsEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))
        self.assertEqual(tcs.HTML_STRING, obs)

    def test_formatting_standalone(self):
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

    def test_remote_url(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        self.assertEqual(emp.base_url, "/nbextensions/emperor/support_files")

    def test_remote_url_custom(self):
        emp = Emperor(self.ord_res, self.mf, remote='/foobersurus/bar/')
        self.assertEqual(emp.base_url, '/foobersurus/bar/')

    def test_unnamed_index(self):
        self.mf.index.name = None
        emp = Emperor(self.ord_res, self.mf, remote=self.url)
        obs = str(emp)

        try:
            self.assertItemsEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(tcs.HTML_STRING.split('\n'), obs.split('\n'))

        self.assertEqual(tcs.HTML_STRING, obs)

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
        self.files_to_remove.append('./something-else')

    def test_process_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=self.url)

        (coord_ids, coords, pct_var, ci, headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = emp._process_data([], 'IQR')

        self.assertEqual(coord_ids, ['PC.636', 'PC.635', 'PC.356', 'PC.481',
                         'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634'])

        np.testing.assert_array_almost_equal(coords, self.expected_coords)

        obs_pct_var = np.array([26.688705, 16.25637, 13.775413, 11.217216,
                                10.024775])
        np.testing.assert_array_almost_equal(pct_var, obs_pct_var)

        np.testing.assert_array_almost_equal(ci, [])

        self.assertEqual(headers, ['SampleID', 'Treatment', 'DOB',
                         'Description'])

        self.assertEqual(metadata, self.expected_metadata)
        self.assertEqual(names, [0, 1, 2, 3, 4])

        self.assertEqual(edges, [])

        self.assertTrue(bi_coords is None)
        self.assertTrue(bi_ids is None)
        self.assertTrue(bi_headers is None)
        self.assertTrue(bi_metadata is None)

    def test_process_data_issue_700(self):
        self.mf.drop(['Treatment', 'DOB', 'Description'], axis=1, inplace=True)

        emp = Emperor(self.ord_res, self.mf, remote=self.url)

        (coord_ids, coords, pct_var, ci, headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = emp._process_data([], 'IQR')

        self.assertEqual(coord_ids, ['PC.636', 'PC.635', 'PC.356', 'PC.481',
                         'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634'])

        np.testing.assert_array_almost_equal(coords, self.expected_coords)

        obs_pct_var = np.array([26.688705, 16.25637, 13.775413, 11.217216,
                                10.024775])
        np.testing.assert_array_almost_equal(pct_var, obs_pct_var)

        np.testing.assert_array_almost_equal(ci, [])

        self.assertEqual(headers, ['SampleID'])
        ids = ['PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593',
               'PC.355', 'PC.607', 'PC.634']
        self.assertEqual(metadata, [[i] for i in ids])
        self.assertEqual(names, [0, 1, 2, 3, 4])

        self.assertEqual(edges, [])

        self.assertTrue(bi_coords is None)
        self.assertTrue(bi_ids is None)
        self.assertTrue(bi_headers is None)
        self.assertTrue(bi_metadata is None)

    def test_process_data_biplots(self):
        emp = Emperor(self.biplot, self.mf, self.feature_mf, remote=self.url)

        (coord_ids, coords, pct_var, ci, headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = emp._process_data([], 'IQR')

        self.assertEqual(coord_ids, ['PC.636', 'PC.635', 'PC.356', 'PC.481',
                         'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634'])

        np.testing.assert_array_almost_equal(coords, self.expected_coords)

        obs_pct_var = np.array([26.688705, 16.25637, 13.775413, 11.217216,
                                10.024775])
        np.testing.assert_array_almost_equal(pct_var, obs_pct_var)

        np.testing.assert_array_almost_equal(ci, [])

        self.assertEqual(headers, ['SampleID', 'Treatment', 'DOB',
                         'Description'])

        self.assertEqual(metadata, self.expected_metadata)
        self.assertEqual(names, [0, 1, 2, 3, 4])

        self.assertEqual(edges, [])

        np.testing.assert_array_almost_equal(bi_coords,
                                             self.expected_biplot_coords)
        self.assertEqual(bi_ids, ['f.PC.636', 'f.PC.635', 'f.PC.356',
                                  'f.PC.481', 'f.PC.354'])
        self.assertEqual(bi_headers, ['SampleID', 'Category', 'Second'])
        self.assertEqual(bi_metadata, [['f.PC.636', 'foo', 'No'],
                                       ['f.PC.635', 'bar', 'Yes'],
                                       ['f.PC.356', 'baz', 'Noes'],
                                       ['f.PC.481', 'foo', 'Noooo'],
                                       ['f.PC.354', 'foo', 'Yep']])

    def test_process_data_biplots_no_metadata(self):
        emp = Emperor(self.biplot, self.mf, remote=self.url)

        (coord_ids, coords, pct_var, ci, headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = emp._process_data([], 'IQR')

        self.assertEqual(coord_ids, ['PC.636', 'PC.635', 'PC.356', 'PC.481',
                         'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634'])

        np.testing.assert_array_almost_equal(coords, self.expected_coords)

        obs_pct_var = np.array([26.688705, 16.25637, 13.775413, 11.217216,
                                10.024775])
        np.testing.assert_array_almost_equal(pct_var, obs_pct_var)

        np.testing.assert_array_almost_equal(ci, [])

        self.assertEqual(headers, ['SampleID', 'Treatment', 'DOB',
                         'Description'])

        self.assertEqual(metadata, self.expected_metadata)
        self.assertEqual(names, [0, 1, 2, 3, 4])

        self.assertEqual(edges, [])

        np.testing.assert_array_almost_equal(bi_coords,
                                             self.expected_biplot_coords)
        self.assertEqual(bi_ids,
                         ['f.PC.636', 'f.PC.635', 'f.PC.356', 'f.PC.481',
                          'f.PC.354'])
        self.assertEqual(bi_headers, ['id', 'all'])
        self.assertEqual(bi_metadata, [['f.PC.636', 'All elements'],
                                       ['f.PC.635', 'All elements'],
                                       ['f.PC.356', 'All elements'],
                                       ['f.PC.481', 'All elements'],
                                       ['f.PC.354', 'All elements']])

    def test_process_data_custom_axes(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        (coord_ids, coords, pct_var, ci, headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = emp._process_data(['DOB'], 'IQR')

        self.assertEqual(coord_ids, ['PC.636', 'PC.635', 'PC.356', 'PC.481',
                         'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634'])

        obs_coords = [[1.322178487895014, -0.651995810831719,
                       -0.3417784983371589, 0.15713116241738878,
                       -0.15964022322388774, 0.41511600449567154],
                      [1.322178487895014, -0.5603276951316744,
                       0.10857735915373172, -0.32567898978232684,
                       0.3750137797216106, -0.583487828830988],
                      [-0.8236274360749414, 0.5394835270542403,
                       -0.3068324227225251, -0.6770043110217822,
                       0.203820501907719, 0.1044335488558445],
                      [0.21458556178898447, 0.09964194790906594,
                       -0.03293232371368659, 0.14978636968698092,
                       -0.8160388524355932, -0.301343079001781],
                      [-0.813231746501206, 0.661089243947507,
                       -0.014176279685000464, 0.05537095913733857,
                       -0.11036487613740434, -0.3456924105084198],
                      [0.3158305385071034, 0.5490376828031979,
                       0.32957520954888647, 0.7612242145083941,
                       0.4322721667939822, 0.04825249860931067],
                      [-0.813231746501206, 0.40202458647314415,
                       -0.4576554852461752, -0.0728438902229666,
                       0.04670222577076932, 0.36567512814466946],
                      [0.30475686917855915, -0.21532604614952783,
                       1.0, -0.31976501999316115, -0.13561208920603846,
                       0.35686551552017187],
                      [1.322178487895014, -0.8236274360749414,
                       -0.2847775589983077, 0.27177950526966277,
                       0.16384736680860681, -0.05981937728235736]]
        np.testing.assert_array_almost_equal(coords, obs_coords)

        obs_pct_var = np.array([-1, 26.688705, 16.25637, 13.775413,
                                11.217216, 10.024775])
        np.testing.assert_array_almost_equal(pct_var, obs_pct_var)

        np.testing.assert_array_almost_equal(ci, [])

        self.assertEqual(headers, ['SampleID', 'Treatment', 'DOB',
                         'Description'])

        self.assertEqual(metadata, self.expected_metadata)
        self.assertEqual(names, ['DOB', 0, 1, 2, 3, 4])

        self.assertEqual(edges, [])

        self.assertTrue(bi_coords is None)
        self.assertTrue(bi_ids is None)
        self.assertTrue(bi_headers is None)
        self.assertTrue(bi_metadata is None)

    def test_custom_axes_missing_headers(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        emp.custom_axes.append(':L')
        with self.assertRaises(KeyError):
            emp.make_emperor()

    def test_custom_axes_no_errors(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        emp.custom_axes.append('DOB')
        obs = emp.make_emperor()

        self.assertTrue(tcs.CUSTOM_AXES_JSON in obs)

    def test_process_jackknifed_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False,
                      jackknifed=self.jackknifed)

        aligned = emp.ordination.samples.index.tolist()
        self.assertEqual(emp.jackknifed[0].samples.index.tolist(), aligned)
        self.assertEqual(emp.jackknifed[1].samples.index.tolist(), aligned)
        self.assertEqual(emp.jackknifed[2].samples.index.tolist(), aligned)

        (coord_ids, coords, pct_var, ci, headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = emp._process_data([], 'IQR')

        self.assertEqual(coord_ids, ['PC.636', 'PC.635', 'PC.356', 'PC.481',
                         'PC.354', 'PC.593', 'PC.355', 'PC.607', 'PC.634'])

        exp_coords = [[-0.7323613329748839, -0.5060247387342096,
                       -0.2089936328022944, -0.37035261848213485,
                       0.560102816456614],
                      [-0.6661577075069334, -0.2217737083659365,
                       -0.4941091848938413, -0.15063086060307557,
                       0.09357800544502778],
                      [-0.10569658584110184, -0.48014086845608406,
                       -0.7503173511199889, -0.1966206523190892,
                       0.3288752279579067],
                      [-0.22411555303555486, -0.27493123505908496,
                       -0.21093271404078504, -0.8492821018569516,
                       0.170533519951784],
                      [-0.07213012997049714, -0.26074072466344955,
                       -0.23567021423219342, -0.3333389086029676,
                       0.1585709413204667],
                      [-0.10306839954771646, -0.16292503176450995,
                       -0.04434218589935773, -0.13505953366377238,
                       0.28651010070387867],
                      [-0.14329582402904856, -0.5913156123027754,
                       -0.30507284380173166, -0.23792313971010245,
                       0.5236822252933244],
                      [-0.4120286058174356, 0.022148368606006386,
                       -0.48972825402724274, -0.35231914529852637,
                       0.5171767480000304],
                      [-0.854640407334614, -0.4637682017836408,
                       -0.1784746008049904, -0.20721872788742415,
                       0.2345128716772838]]
        np.testing.assert_array_almost_equal(coords, exp_coords)

        obs_pct_var = np.array([26.688705, 16.25637, 13.775413,
                                11.217216, 10.024775])
        np.testing.assert_array_almost_equal(pct_var, obs_pct_var)

        exp_ci = [[0.1607310442863299, 0.3284924807941013, 0.7369418623398015,
                   0.4214247905164943, 0.28997362392188486],
                  [0.21166002475051793, 0.6639877588405441, 0.3368603902230289,
                   1.0611463515656554, 1.3658809960217244],
                  [1.302042601434282, 0.34661689146711805, 0.14662608019641343,
                   0.8068627424977899, 0.44888335820412445],
                  [0.6505359617817268, 0.4839978226907967, 0.7259215378704654,
                   0.06648649884271707, 0.9521368980788267],
                  [1.4777914186973813, 0.4931288899568982, 0.5837728328749483,
                   0.4459480649311265, 1.017838290883758],
                  [1.3159259248471549, 0.9939885504306211, 1.6208853472661828,
                   1.1454098437746723, 0.47651520418913607],
                  [1.1009478227467375, 0.2673202541132003, 0.46445790715753016,
                   0.5706778359138301, 0.31601419429730987],
                  [0.3934051193358155, 1.9557032627879871, 0.3399264680681631,
                   0.4334141121849759, 0.32062246495971714],
                  [0.062025942519345234, 0.3579812855706662,
                   0.9082115096900578, 0.7470141115975886, 0.5904898479721775]]
        np.testing.assert_array_almost_equal(ci, exp_ci)

        self.assertEqual(headers, ['SampleID', 'Treatment', 'DOB',
                         'Description'])

        self.assertEqual(metadata, self.expected_metadata)
        self.assertEqual(names, [0, 1, 2, 3, 4])

        self.assertEqual(edges, [])

        self.assertTrue(bi_coords is None)
        self.assertTrue(bi_ids is None)
        self.assertTrue(bi_headers is None)
        self.assertTrue(bi_metadata is None)

    def test_jackknifed_method_sdev(self):
        emp = Emperor(self.ord_res, self.mf, remote=False,
                      jackknifed=self.jackknifed)
        emp.jackknifing_method = 'sdev'

        observed = emp._to_dict(emp._process_data(emp.custom_axes,
                                                  emp.jackknifing_method))
        expected = tcs.JACKKNIFED_SDEV

        # the arrays need to be almost equal
        obs_coord = observed['plot']['decomposition']['coordinates']
        exp_coord = expected['plot']['decomposition']['coordinates']
        np.testing.assert_array_almost_equal(obs_coord, exp_coord)

        obs_ci = observed['plot']['decomposition']['ci']
        exp_ci = expected['plot']['decomposition']['ci']
        np.testing.assert_array_almost_equal(obs_ci, exp_ci)

        # everything else should be pretty close
        for key in ['axes_names', 'edges', 'percents_explained', 'sample_ids']:
            self.assertEqual(observed['plot']['decomposition'][key],
                             expected['plot']['decomposition'][key])

        for key in ['metadata_headers', 'settings', 'type']:
            self.assertEqual(observed['plot'][key],
                             expected['plot'][key])

    def test_process_procrustes_data(self):
        ordinations = self.jackknifed[1:]
        emp = Emperor(self.ord_res, self.mf, remote=False,
                      procrustes=ordinations)

        aligned = emp.ordination.samples.index.tolist()
        self.assertEqual(emp.jackknifed, [])
        self.assertEqual(emp.procrustes[0].samples.index.tolist(), aligned)
        self.assertEqual(emp.procrustes[1].samples.index.tolist(), aligned)

        (coord_ids, coords, pct_var, ci, headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = emp._process_data([], 'IQR')

        self.assertEqual(coord_ids,
                         ['PC.636_0', 'PC.635_0', 'PC.356_0', 'PC.481_0',
                          'PC.354_0', 'PC.593_0', 'PC.355_0', 'PC.607_0',
                          'PC.634_0',
                          'PC.636_1', 'PC.635_1', 'PC.356_1', 'PC.481_1',
                          'PC.354_1', 'PC.593_1', 'PC.355_1', 'PC.607_1',
                          'PC.634_1',
                          'PC.636_2', 'PC.635_2', 'PC.356_2', 'PC.481_2',
                          'PC.354_2', 'PC.593_2', 'PC.355_2', 'PC.607_2',
                          'PC.634_2'])
        np.testing.assert_array_almost_equal(coords, tcs.PROCRUSTES_COORDS)

        obs_pct_var = np.array([26.688705, 16.25637, 13.775413,
                                11.217216, 10.024775])
        np.testing.assert_array_almost_equal(pct_var, obs_pct_var)

        exp_ci = []
        np.testing.assert_array_almost_equal(ci, exp_ci)

        self.assertEqual(headers, ['SampleID', 'Treatment', 'DOB',
                         'Description', '__Procrustes_Names__'])

        self.assertEqual(metadata, tcs.PROCRUSTES_MAP)
        self.assertEqual(names, [0, 1, 2, 3, 4])

        self.assertEqual(edges, [['PC.636_0', 'PC.636_1'],
                         ['PC.635_0', 'PC.635_1'], ['PC.356_0', 'PC.356_1'],
                         ['PC.481_0', 'PC.481_1'], ['PC.354_0', 'PC.354_1'],
                         ['PC.593_0', 'PC.593_1'], ['PC.355_0', 'PC.355_1'],
                         ['PC.607_0', 'PC.607_1'], ['PC.634_0', 'PC.634_1'],
                         ['PC.636_0', 'PC.636_2'], ['PC.635_0', 'PC.635_2'],
                         ['PC.356_0', 'PC.356_2'], ['PC.481_0', 'PC.481_2'],
                         ['PC.354_0', 'PC.354_2'], ['PC.593_0', 'PC.593_2'],
                         ['PC.355_0', 'PC.355_2'], ['PC.607_0', 'PC.607_2'],
                         ['PC.634_0', 'PC.634_2']])
        self.assertTrue(bi_coords is None)
        self.assertTrue(bi_ids is None)
        self.assertTrue(bi_headers is None)
        self.assertTrue(bi_metadata is None)

    def test_jackknifed_bad_data(self):
        with self.assertRaises(TypeError):
            Emperor(self.ord_res, self.mf, jackknifed=[1])

        with self.assertRaises(TypeError):
            Emperor(self.ord_res, self.mf, jackknifed=self.jackknifed + [1])

    def test_jackknifed_bad_data_sample_ids(self):
        self.jackknifed[0].samples.index = pd.Series(list('abcdefghi'))
        with self.assertRaises(ValueError):
            Emperor(self.ord_res, self.mf, jackknifed=self.jackknifed)

    def test_jackknifed_and_procrustes(self):
        a, b, c = self.jackknifed
        with self.assertRaises(ValueError):
            Emperor(self.ord_res, self.mf, jackknifed=[a, b],
                    procrustes=[c])


class EmperorSettingsTests(TestCase):
    """Extensively test the settings property and methods"""
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

    def test_base_data_checks(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        data = {'20061126': '#ff00ff', '20061218': '#ff0000',
                '20070314': '#00000f', '20071112': '#ee00ee',
                '20071210': '#0000fa', '20080116': '#dedede'}
        obs = emp._base_data_checks('DOB', data, str)
        self.assertEqual(obs, data)

    def test_base_data_checks_with_data_series(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        exp = {'20061126': '#ff00ff', '20061218': '#ff0000',
               '20070314': '#00000f', '20071112': '#ee00ee',
               '20071210': '#0000fa', '20080116': '#dedede'}
        data = pd.Series(exp)

        obs = emp._base_data_checks('DOB', data, str)
        self.assertEqual(obs, exp)

    def test_base_data_checks_with_no_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        obs = emp._base_data_checks('DOB', {}, str)
        self.assertEqual(obs, {})
        obs = emp._base_data_checks('DOB', pd.Series(), str)
        self.assertEqual(obs, {})

    def test_base_data_checks_category_with_invalid_more_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        data = {'20061126': '#ff00ff', '20061218': '#ff0000',
                '20070314': '#00000f', '20071112': '#ee00ee',
                '20071210': '#0000fa', '20080116': '#dedede', 'foo': '#ff00fb'}
        with self.assertRaises(ValueError):
            emp._base_data_checks('DOB', data, str)

    def test_base_data_checks_category_with_invalid_less_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        data = {'20061126': '#ff00ff', '20061218': '#ff0000',
                '20070314': '#00000f', '20071112': '#ee00ee',
                '20071210': '#0000fa', '20080116': '#dedede'}
        del data['20071210']
        with self.assertRaises(ValueError):
            emp._base_data_checks('DOB', data, str)

    def test_base_data_checks_category_does_not_exist(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        with self.assertRaises(KeyError):
            emp._base_data_checks('Boaty McBoatFace', None, str)

    def test_base_data_checks_category_not_str(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        with self.assertRaises(TypeError):
            emp._base_data_checks([], None, str)

        with self.assertRaises(TypeError):
            emp._base_data_checks(11, None, str)

    def test_color_by_category(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.color_by('DOB')
        exp = {'color': {"category": 'DOB',
                         "colormap": 'discrete-coloring-qiime',
                         "continuous": False,
                         "data": {}
                         }
               }
        self.assertEqual(emp.settings['color'], exp['color'])
        self.assertEqual(obs.settings['color'], exp['color'])

    def test_color_by_category_and_colormap(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.color_by('DOB', colormap='Dark2')
        exp = {'color': {"category": 'DOB',
                         "colormap": 'Dark2',
                         "continuous": False,
                         "data": {}
                         }
               }
        self.assertEqual(emp.settings['color'], exp['color'])
        self.assertEqual(obs.settings['color'], exp['color'])

    def test_color_by_category_continuous(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.color_by('Treatment', colormap='Dark2', continuous=True)
        exp = {'color': {"category": 'Treatment',
                         "colormap": 'Dark2',
                         "continuous": True,
                         "data": {}
                         }
               }
        self.assertEqual(emp.settings['color'], exp['color'])
        self.assertEqual(obs.settings['color'], exp['color'])

    def test_color_by_category_with_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        data = {'20061126': '#ff00ff', '20061218': '#ff0000',
                '20070314': '#00000f', '20071112': '#ee00ee',
                '20071210': '#0000fa', '20080116': '#dedede'}

        obs = emp.color_by('Treatment', colors=data, colormap='Dark2',
                           continuous=True)
        exp = {'color': {"category": 'Treatment',
                         "colormap": 'Dark2',
                         "continuous": True,
                         "data": {'20061126': '#ff00ff',
                                  '20061218': '#ff0000',
                                  '20070314': '#00000f',
                                  '20071112': '#ee00ee',
                                  '20071210': '#0000fa',
                                  '20080116': '#dedede'
                                  }
                         }
               }
        self.assertEqual(emp.settings['color'], exp['color'])
        self.assertEqual(obs.settings['color'], exp['color'])

    def test_color_by_colormap_not_str(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        with self.assertRaises(TypeError):
            emp.color_by('DOB', colormap=11)

        with self.assertRaises(TypeError):
            emp.color_by('DOB', colormap=[])

        with self.assertRaises(TypeError):
            emp.color_by('DOB', colormap=(1, 2))

    def test_shape_by(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.shape_by('DOB')
        exp = {'shape': {"category": 'DOB',
                         "data": {}
                         }
               }
        self.assertEqual(emp.settings['shape'], exp['shape'])
        self.assertEqual(obs.settings['shape'], exp['shape'])

        obs = emp.shape_by('Treatment')
        exp = {'shape': {"category": 'Treatment',
                         "data": {}
                         }
               }
        self.assertEqual(emp.settings['shape'], exp['shape'])
        self.assertEqual(obs.settings['shape'], exp['shape'])

    def test_shape_by_with_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        exp = {'shape': {"category": 'DOB',
                         "data": {'20061126': 'Sphere',
                                  '20061218': 'Cube',
                                  '20070314': 'Cylinder',
                                  '20071112': 'Cube',
                                  '20071210': 'Sphere',
                                  '20080116': 'Icosahedron'
                                  }
                         }
               }
        data = exp['shape']['data']
        obs = emp.shape_by('DOB', data)
        self.assertEqual(emp.settings['shape'], exp['shape'])
        self.assertEqual(obs.settings['shape'], exp['shape'])

    def test_shape_by_with_series_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        exp = {'shape': {"category": 'DOB',
                         "data": {'20061126': 'Sphere',
                                  '20061218': 'Cube',
                                  '20070314': 'Cylinder',
                                  '20071112': 'Cube',
                                  '20071210': 'Sphere',
                                  '20080116': 'Icosahedron'
                                  }
                         }
               }
        data = pd.Series(exp['shape']['data'])
        obs = emp.shape_by('DOB', data)
        self.assertEqual(emp.settings['shape'], exp['shape'])
        self.assertEqual(obs.settings['shape'], exp['shape'])

    def test_visibility_by(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.visibility_by('DOB')
        exp = {'visibility': {"category": 'DOB',
                              "data": {}
                              }
               }
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

        obs = emp.visibility_by('Treatment')
        exp = {'visibility': {"category": 'Treatment',
                              "data": {}
                              }
               }
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_visibility_by_with_list(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        obs = emp.visibility_by('DOB', ['20070314', '20071210'])
        exp = {'visibility': {"category": 'DOB',
                              "data": {'20061126': False,
                                       '20061218': False,
                                       '20070314': True,
                                       '20071112': False,
                                       '20071210': True,
                                       '20080116': False
                                       }
                              }
               }
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_visibility_by_with_empty_list(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        obs = emp.visibility_by('DOB', ['20070314', '20071210'])
        exp = {'visibility': {"category": 'DOB',
                              "data": {'20061126': False,
                                       '20061218': False,
                                       '20070314': True,
                                       '20071112': False,
                                       '20071210': True,
                                       '20080116': False
                                       }
                              }
               }
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_visibility_by_with_list_negate(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        obs = emp.visibility_by('DOB', ['20070314', '20071210'], negate=True)
        exp = {'visibility': {"category": 'DOB',
                              "data": {'20061126': True,
                                       '20061218': True,
                                       '20070314': False,
                                       '20071112': True,
                                       '20071210': False,
                                       '20080116': True
                                       }
                              }
               }
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_visibility_by_with_empty_list_negate(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)
        obs = emp.visibility_by('DOB', [], negate=True)
        exp = {'visibility': {"category": 'DOB',
                              "data": {'20061126': True,
                                       '20061218': True,
                                       '20070314': True,
                                       '20071112': True,
                                       '20071210': True,
                                       '20080116': True
                                       }
                              }
               }
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_visibility_by_and_negate(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        exp = {'visibility': {"category": 'DOB',
                              "data": {'20061126': True,
                                       '20061218': True,
                                       '20070314': False,
                                       '20071112': True,
                                       '20071210': False,
                                       '20080116': True
                                       }
                              }
               }
        data = {'20061126': False, '20061218': False, '20070314': True,
                '20071112': False, '20071210': True, '20080116': False}

        obs = emp.visibility_by('DOB', data, negate=True)

        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_visibility_by_with_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        exp = {'visibility': {"category": 'DOB',
                              "data": {'20061126': False,
                                       '20061218': False,
                                       '20070314': True,
                                       '20071112': False,
                                       '20071210': True,
                                       '20080116': False
                                       }
                              }
               }
        data = exp['visibility']['data']
        obs = emp.visibility_by('DOB', data)
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_visibility_by_with_series_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        exp = {'visibility': {"category": 'DOB',
                              "data": {'20061126': False,
                                       '20061218': False,
                                       '20070314': True,
                                       '20071112': False,
                                       '20071210': True,
                                       '20080116': False
                                       }
                              }
               }
        data = pd.Series(exp['visibility']['data'])
        obs = emp.visibility_by('DOB', data)
        self.assertEqual(emp.settings['visibility'], exp['visibility'])
        self.assertEqual(obs.settings['visibility'], exp['visibility'])

    def test_scale_by(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.scale_by('DOB')
        exp = {'scale': {"category": 'DOB',
                         "data": {},
                         "globalScale": "1.0",
                         "scaleVal": False
                         }
               }
        self.assertEqual(emp.settings['scale'], exp['scale'])
        self.assertEqual(obs.settings['scale'], exp['scale'])

        obs = emp.scale_by('Treatment')
        exp = {'scale': {"category": 'Treatment',
                         "data": {},
                         "globalScale": "1.0",
                         "scaleVal": False
                         }
               }
        self.assertEqual(emp.settings['scale'], exp['scale'])
        self.assertEqual(obs.settings['scale'], exp['scale'])

        obs = emp.scale_by('Treatment', global_scale=3.5)
        exp = {'scale': {"category": 'Treatment',
                         "data": {},
                         "globalScale": "3.5",
                         "scaleVal": False
                         }
               }
        self.assertEqual(emp.settings['scale'], exp['scale'])
        self.assertEqual(obs.settings['scale'], exp['scale'])

        obs = emp.scale_by('Treatment', global_scale=3.5, scaled=True)
        exp = {'scale': {"category": 'Treatment',
                         "data": {},
                         "globalScale": "3.5",
                         "scaleVal": True
                         }
               }
        self.assertEqual(emp.settings['scale'], exp['scale'])
        self.assertEqual(obs.settings['scale'], exp['scale'])

    def test_scale_by_with_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        exp = {'scale': {"category": 'DOB',
                         "data": {'20061126': 5.0,
                                  '20061218': 1.0,
                                  '20070314': 1.0,
                                  '20071112': 1.0,
                                  '20071210': 0.5,
                                  '20080116': 1.0
                                  },
                         "globalScale": "1.0",
                         "scaleVal": False
                         }
               }
        data = exp['scale']['data']
        obs = emp.scale_by('DOB', data)
        self.assertEqual(emp.settings['scale'], exp['scale'])
        self.assertEqual(obs.settings['scale'], exp['scale'])

    def test_scale_by_with_series_data(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        exp = {'scale': {"category": 'DOB',
                         "data": {'20061126': 1.0,
                                  '20061218': 4.0,
                                  '20070314': 3.0,
                                  '20071112': 2.0,
                                  '20071210': 1.0,
                                  '20080116': 1.0
                                  },
                         "globalScale": "1.0",
                         "scaleVal": False
                         }
               }
        data = pd.Series(exp['scale']['data'])
        obs = emp.scale_by('DOB', data)
        self.assertEqual(emp.settings['scale'], exp['scale'])
        self.assertEqual(obs.settings['scale'], exp['scale'])

    def test_scale_by_with_data_invalid_scale(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        data = {'20061126': 5.0, '20061218': 1.0, '20070314': 1.0,
                '20071112': 1.0, '20071210': 0.5, '20080116': 1.0}

        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, global_scale=False)
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, global_scale=(1, 2, 3))
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, global_scale=[])

    def test_scale_by_with_data_invalid_scaled(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        data = {'20061126': 5.0, '20061218': 1.0, '20070314': 1.0,
                '20071112': 1.0, '20071210': 0.5, '20080116': 1.0}

        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, scaled=1)
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, scaled=[])
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, scaled=(1, 2))

    def test_opacity_by(self):
        emp = Emperor(self.ord_res, self.mf)

        obs = emp.opacity_by('DOB')
        exp = {'opacity': {"category": 'DOB',
                           "data": {},
                           "globalScale": "1.0",
                           "scaleVal": False
                           }
               }
        self.assertEqual(emp.settings['opacity'], exp['opacity'])
        self.assertEqual(obs.settings['opacity'], exp['opacity'])

        obs = emp.opacity_by('Treatment')
        exp = {'opacity': {"category": 'Treatment',
                           "data": {},
                           "globalScale": "1.0",
                           "scaleVal": False
                           }
               }
        self.assertEqual(emp.settings['opacity'], exp['opacity'])
        self.assertEqual(obs.settings['opacity'], exp['opacity'])

        obs = emp.opacity_by('Treatment', global_scale=0.35)
        exp = {'opacity': {"category": 'Treatment',
                           "data": {},
                           "globalScale": "0.35",
                           "scaleVal": False
                           }
               }
        self.assertEqual(emp.settings['opacity'], exp['opacity'])
        self.assertEqual(obs.settings['opacity'], exp['opacity'])

        obs = emp.opacity_by('Treatment', global_scale=0.35, scaled=True)
        exp = {'opacity': {"category": 'Treatment',
                           "data": {},
                           "globalScale": "0.35",
                           "scaleVal": True
                           }
               }
        self.assertEqual(emp.settings['opacity'], exp['opacity'])
        self.assertEqual(obs.settings['opacity'], exp['opacity'])

    def test_opacity_by_with_data(self):
        emp = Emperor(self.ord_res, self.mf)

        exp = {'opacity': {"category": 'DOB',
                           "data": {'20061126': 0.50,
                                    '20061218': 0.10,
                                    '20070314': 0.10,
                                    '20071112': 0.10,
                                    '20071210': 0.05,
                                    '20080116': 0.10
                                    },
                           "globalScale": "1.0",
                           "scaleVal": False
                           }
               }
        data = exp['opacity']['data']
        obs = emp.opacity_by('DOB', data)
        self.assertEqual(emp.settings['opacity'], exp['opacity'])
        self.assertEqual(obs.settings['opacity'], exp['opacity'])

    def test_opacity_by_with_series_data(self):
        emp = Emperor(self.ord_res, self.mf)

        exp = {'opacity': {"category": 'DOB',
                           "data": {'20061126': 0.1,
                                    '20061218': 0.4,
                                    '20070314': 0.3,
                                    '20071112': 0.2,
                                    '20071210': 0.1,
                                    '20080116': 1
                                    },
                           "globalScale": "1.0",
                           "scaleVal": False
                           }
               }
        data = pd.Series(exp['opacity']['data'])
        obs = emp.opacity_by('DOB', data)
        self.assertEqual(emp.settings['opacity'], exp['opacity'])
        self.assertEqual(obs.settings['opacity'], exp['opacity'])

    def test_opacity_by_with_data_invalid_scale(self):
        emp = Emperor(self.ord_res, self.mf)

        data = {'20061126': 1.0, '20061218': 1.0, '20070314': 1.0,
                '20071112': 1.0, '20071210': 0.5, '20080116': 1.0}

        with self.assertRaises(TypeError):
            emp.opacity_by('DOB', data, global_scale=False)
        with self.assertRaises(TypeError):
            emp.opacity_by('DOB', data, global_scale=(1, 2, 3))
        with self.assertRaises(TypeError):
            emp.opacity_by('DOB', data, global_scale=[])

    def test_opacity_by_with_data_invalid_scaled(self):
        emp = Emperor(self.ord_res, self.mf)

        data = {'20061126': 1.0, '20061218': 1.0, '20070314': 1.0,
                '20071112': 1.0, '20071210': 0.5, '20080116': 1.0}

        with self.assertRaises(TypeError):
            emp.opacity_by('DOB', data, scaled=1)
        with self.assertRaises(TypeError):
            emp.opacity_by('DOB', data, scaled=[])
        with self.assertRaises(TypeError):
            emp.opacity_by('DOB', data, scaled=(1, 2))

    def test_animations_by(self):
        emp = Emperor(self.ord_res, self.mf)

        exp = {'animations': {"gradientCategory": 'DOB',
                              "trajectoryCategory": 'Treatment',
                              "speed": 1,
                              "radius": 1,
                              "colors": {"Fast": "red", "Control": "blue"}
                              }
               }
        obs = emp.animations_by('DOB', 'Treatment',
                                {"Fast": "red", "Control": "blue"})
        self.assertEqual(emp.settings['animations'], exp['animations'])
        self.assertEqual(obs.settings['animations'], exp['animations'])

        exp = {'animations': {"gradientCategory": 'Treatment',
                              "trajectoryCategory": 'DOB',
                              "speed": 3.3,
                              "radius": 4,
                              "colors": {"Fast": "red", "Control": "blue"}
                              }
               }
        obs = emp.animations_by('Treatment', 'DOB',
                                {"Fast": "red", "Control": "blue"}, 3.3, 4)
        self.assertEqual(emp.settings['animations'], exp['animations'])
        self.assertEqual(obs.settings['animations'], exp['animations'])

    def test_animations_by_exceptions(self):
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(KeyError):
            emp.animations_by('Animals', 'DOB',
                              {"Fast": "red", "Control": "blue"})

    def test_animations_by_exceptions_one(self):
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(KeyError):
            emp.animations_by('DOB', 'Animals',
                              {"Fast": "red", "Control": "blue"})

    def test_animations_by_exceptions_two(self):
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(TypeError):
            emp.animations_by('DOB', 'Treatment',
                              {"Fast": "red", "Control": "blue"}, speed='1.0')

    def test_animations_by_exceptions_three(self):
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(TypeError):
            emp.animations_by('DOB', 'Treatment',
                              {"Fast": "red", "Control": "blue"}, radius='1.0')

    def test_set_axes(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.set_axes([3, 2, 0])
        exp = {'axes': {"visibleDimensions": [3, 2, 0],
                        "flippedAxes": [False, False, False],
                        "backgroundColor": 'black',
                        "axesColor": 'white'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_axes_flipping(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.set_axes(invert=[True, False, False])
        exp = {'axes': {"visibleDimensions": [0, 1, 2],
                        "flippedAxes": [True, False, False],
                        "backgroundColor": 'black',
                        "axesColor": 'white'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_axes_color(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.set_axes(color='red')
        exp = {'axes': {"visibleDimensions": [0, 1, 2],
                        "flippedAxes": [False, False, False],
                        "backgroundColor": 'black',
                        "axesColor": 'red'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_axes_errors_dimensions(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        with self.assertRaises(ValueError):
            emp.set_axes([3, 2, 0, 1])

        with self.assertRaises(ValueError):
            emp.set_axes([3, 2])

        with self.assertRaises(ValueError):
            emp.set_axes([3, 2, 11111])

        with self.assertRaises(ValueError):
            emp.set_axes([-3, -2, -1])

        with self.assertRaises(TypeError):
            emp.set_axes([1.1, 2, 3.0])

    def test_set_background_color(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.set_background_color('yellow')
        exp = {'axes': {"visibleDimensions": [0, 1, 2],
                        "flippedAxes": [False, False, False],
                        "backgroundColor": 'yellow',
                        "axesColor": 'white'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_background_and_axes(self):
        emp = Emperor(self.ord_res, self.mf, remote=False)

        obs = emp.set_axes([3, 2, 0], [False, True, True], 'red')
        self.assertEqual(obs, emp)

        obs = emp.set_background_color('green')
        self.assertEqual(obs, emp)

        exp = {'axes': {"visibleDimensions": [3, 2, 0],
                        "flippedAxes": [False, True, True],
                        "backgroundColor": 'green',
                        "axesColor": 'red'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_del_settings(self):
        exp_settings = {'scale': {"category": 'DOB',
                                  "data": {'20061126': 5.0,
                                           '20061218': 1.0,
                                           '20070314': 1.0,
                                           '20071112': 1.0,
                                           '20071210': 0.5,
                                           '20080116': 1.0
                                           },
                                  "globalScale": "1.0",
                                  "scaleVal": False},
                        'axes': {"visibleDimensions": [3, 2, 0],
                                 "flippedAxes": [False, True, True],
                                 "backgroundColor": 'blue',
                                 "axesColor": 'red'
                                 }
                        }

        emp = Emperor(self.ord_res, self.mf, remote=False)

        emp.set_axes([3, 2, 0], [False, True, True], 'red')
        emp.set_background_color('blue')
        emp.scale_by('DOB', exp_settings['scale']['data'])

        self.assertEqual(emp.settings, exp_settings)
        emp.settings = None
        self.assertEqual(emp.settings, {})

        del emp.settings
        self.assertEqual(emp.settings, {})

    def test_set_settings(self):
        exp_settings = {'scale': {"category": 'DOB',
                                  "data": {'20061126': 5.0,
                                           '20061218': 1.0,
                                           '20070314': 1.0,
                                           '20071112': 1.0,
                                           '20071210': 0.5,
                                           '20080116': 1.0
                                           },
                                  "globalScale": "1.0",
                                  "scaleVal": False},
                        'axes': {"visibleDimensions": [3, 2, 0],
                                 "flippedAxes": [False, True, True],
                                 "backgroundColor": 'blue',
                                 "axesColor": 'red'
                                 }
                        }

        emp = Emperor(self.ord_res, self.mf, remote=False)
        emp.settings = deepcopy(exp_settings)

        self.assertEqual(emp.settings, exp_settings)

    def test_set_settings_all_keys(self):
        exp_settings = {'scale': {"category": 'DOB',
                                  "data": {'20061126': 5.0,
                                           '20061218': 1.0,
                                           '20070314': 1.0,
                                           '20071112': 1.0,
                                           '20071210': 0.5,
                                           '20080116': 1.0
                                           },
                                  "globalScale": "1.0",
                                  "scaleVal": False},
                        'axes': {"visibleDimensions": [3, 2, 0],
                                 "flippedAxes": [False, True, True],
                                 "backgroundColor": 'blue',
                                 "axesColor": 'red'
                                 },
                        'color': {"category": 'DOB',
                                  "colormap": 'discrete-coloring-qiime',
                                  "continuous": False,
                                  "data": {}},
                        'shape': {"category": 'DOB',
                                  "data": {'20061126': 'Sphere',
                                           '20061218': 'Cube',
                                           '20070314': 'Cylinder',
                                           '20071112': 'Cube',
                                           '20071210': 'Sphere',
                                           '20080116': 'Icosahedron'}},
                        'visibility': {"category": 'DOB',
                                       "data": {'20061126': False,
                                                '20061218': False,
                                                '20070314': True,
                                                '20071112': False,
                                                '20071210': True,
                                                '20080116': False}},
                        'opacity': {"category": 'DOB',
                                    "data": {},
                                    "globalScale": "1.0",
                                    "scaleVal": False},
                        'animations': {"gradientCategory": 'DOB',
                                       "trajectoryCategory": 'Treatment',
                                       "speed": 1,
                                       "radius": 1,
                                       "colors": {"Fast": "red",
                                                  "Control": "blue"}
                                       }
                        }

        emp = Emperor(self.ord_res, self.mf, remote=False)
        emp.settings = deepcopy(exp_settings)
        self.assertEqual(emp.settings, exp_settings)

    def test_set_settings_invalid(self):
        exp_settings = {'boaty': {"category": 'DOB',
                                  "data": {'20061126': 5.0,
                                           '20061218': 1.0,
                                           '20070314': 1.0,
                                           '20071112': 1.0,
                                           '20071210': 0.5,
                                           '20080116': 1.0
                                           },
                                  "globalScale": "1.0",
                                  "scaleVal": False},
                        'axes': {"visibleDimensions": [3, 2, 0],
                                 "flippedAxes": [False, True, True],
                                 "backgroundColor": 'blue',
                                 "axesColor": 'red'
                                 }
                        }

        emp = Emperor(self.ord_res, self.mf, remote=False)
        with self.assertRaises(KeyError):
            emp.settings = deepcopy(exp_settings)

    def test_set_settings_invalid_inner_value(self):
        # 200000 should be invalid
        exp_settings = {'scale': {"category": 200000,
                                  "data": {'20061126': 5.0,
                                           '20061218': 1.0,
                                           '20070314': 1.0,
                                           '20071112': 1.0,
                                           '20071210': 0.5,
                                           '20080116': 1.0
                                           },
                                  "globalScale": "1.0",
                                  "scaleVal": False},
                        'axes': {"visibleDimensions": [3, 2, 0],
                                 "flippedAxes": [False, True, True],
                                 "backgroundColor": 'blue',
                                 "axesColor": 'red'
                                 }
                        }

        emp = Emperor(self.ord_res, self.mf, remote=False)
        with self.assertRaises(TypeError):
            emp.settings = deepcopy(exp_settings)


if __name__ == "__main__":
    main()
