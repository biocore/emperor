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

        # note that we don't test with remote=True because the url is resolved
        # by emperor.util.resolve_stable_url, so it is bound to change
        # depending on the environment executing the test
        self.url = ('https://cdn.rawgit.com/biocore/emperor/new-api/emperor/'
                    'support_files')

        np.random.seed(111)

    def tearDown(self):
        for path in self.files_to_remove:
            if exists(path):
                rmtree(path)

    def test_dimensions(self):
        emp = Emperor(self.ord_res, self.mf)
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
        emp = Emperor(self.ord_res, self.mf, remote=self.url)
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
        self.files_to_remove.append('./something-else')

    def test_custom_axes(self):
        emp = Emperor(self.ord_res, self.mf, remote=self.url)
        obs = emp.make_emperor(custom_axes=['DOB'])

        try:
            self.assertItemsEqual(tcs.HTML_STRING_CUSTOM_AXES.split('\n'),
                                  obs.split('\n'))
        except AttributeError:
            self.assertCountEqual(tcs.HTML_STRING_CUSTOM_AXES.split('\n'),
                                  obs.split('\n'))
        self.assertEqual(tcs.HTML_STRING_CUSTOM_AXES, obs)

    def test_custom_axes_missing_headers(self):
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(KeyError):
            emp.make_emperor(custom_axes=[':L'])

    def test_base_data_checks(self):
        emp = Emperor(self.ord_res, self.mf)
        data = {'20061126': '#ff00ff', '20061218': '#ff0000',
                '20070314': '#00000f', '20071112': '#ee00ee',
                '20071210': '#0000fa', '20080116': '#dedede'}
        obs = emp._base_data_checks('DOB', data, str)
        self.assertEqual(obs, data)

    def test_base_data_checks_with_data_series(self):
        emp = Emperor(self.ord_res, self.mf)
        exp = {'20061126': '#ff00ff', '20061218': '#ff0000',
               '20070314': '#00000f', '20071112': '#ee00ee',
               '20071210': '#0000fa', '20080116': '#dedede'}
        data = pd.Series(exp)

        obs = emp._base_data_checks('DOB', data, str)
        self.assertEqual(obs, exp)

    def test_base_data_checks_with_no_data(self):
        emp = Emperor(self.ord_res, self.mf)
        obs = emp._base_data_checks('DOB', {}, str)
        self.assertEqual(obs, {})
        obs = emp._base_data_checks('DOB', pd.Series(), str)
        self.assertEqual(obs, {})

    def test_base_data_checks_category_with_invalid_more_data(self):
        emp = Emperor(self.ord_res, self.mf)

        data = {'20061126': '#ff00ff', '20061218': '#ff0000',
                '20070314': '#00000f', '20071112': '#ee00ee',
                '20071210': '#0000fa', '20080116': '#dedede', 'foo': '#ff00fb'}
        with self.assertRaises(ValueError):
            emp._base_data_checks('DOB', data, str)

    def test_base_data_checks_category_with_invalid_less_data(self):
        emp = Emperor(self.ord_res, self.mf)
        data = {'20061126': '#ff00ff', '20061218': '#ff0000',
                '20070314': '#00000f', '20071112': '#ee00ee',
                '20071210': '#0000fa', '20080116': '#dedede'}
        del data['20071210']
        with self.assertRaises(ValueError):
            emp._base_data_checks('DOB', data, str)

    def test_base_data_checks_category_does_not_exist(self):
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(KeyError):
            emp._base_data_checks('Boaty McBoatFace', None, str)

    def test_base_data_checks_category_not_str(self):
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(TypeError):
            emp._base_data_checks([], None, str)

        with self.assertRaises(TypeError):
            emp._base_data_checks(11, None, str)

    def test_color_by_category(self):
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)
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
        emp = Emperor(self.ord_res, self.mf)

        with self.assertRaises(TypeError):
            emp.color_by('DOB', colormap=11)

        with self.assertRaises(TypeError):
            emp.color_by('DOB', colormap=[])

        with self.assertRaises(TypeError):
            emp.color_by('DOB', colormap=(1, 2))

    def test_shape_by(self):
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)
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
        emp = Emperor(self.ord_res, self.mf)
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
        emp = Emperor(self.ord_res, self.mf)
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
        emp = Emperor(self.ord_res, self.mf)
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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

        data = {'20061126': 5.0, '20061218': 1.0, '20070314': 1.0,
                '20071112': 1.0, '20071210': 0.5, '20080116': 1.0}

        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, global_scale=False)
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, global_scale=(1, 2, 3))
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, global_scale=[])

    def test_scale_by_with_data_invalid_scaled(self):
        emp = Emperor(self.ord_res, self.mf)

        data = {'20061126': 5.0, '20061218': 1.0, '20070314': 1.0,
                '20071112': 1.0, '20071210': 0.5, '20080116': 1.0}

        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, scaled=1)
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, scaled=[])
        with self.assertRaises(TypeError):
            emp.scale_by('DOB', data, scaled=(1, 2))

    def test_set_axes(self):
        emp = Emperor(self.ord_res, self.mf)

        obs = emp.set_axes([3, 2, 0])
        exp = {'axes': {"visibleDimensions": [3, 2, 0],
                        "flippedAxes": [False, False, False],
                        "backgroundColor": 'black',
                        "axesColor": 'white'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_axes_flipping(self):
        emp = Emperor(self.ord_res, self.mf)

        obs = emp.set_axes(invert=[True, False, False])
        exp = {'axes': {"visibleDimensions": [0, 1, 2],
                        "flippedAxes": [True, False, False],
                        "backgroundColor": 'black',
                        "axesColor": 'white'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_axes_color(self):
        emp = Emperor(self.ord_res, self.mf)

        obs = emp.set_axes(color='red')
        exp = {'axes': {"visibleDimensions": [0, 1, 2],
                        "flippedAxes": [False, False, False],
                        "backgroundColor": 'black',
                        "axesColor": 'red'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_axes_errors_dimensions(self):
        emp = Emperor(self.ord_res, self.mf)

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
        emp = Emperor(self.ord_res, self.mf)

        obs = emp.set_background_color('yellow')
        exp = {'axes': {"visibleDimensions": [0, 1, 2],
                        "flippedAxes": [False, False, False],
                        "backgroundColor": 'yellow',
                        "axesColor": 'white'
                        }
               }
        self.assertEqual(obs.settings['axes'], exp['axes'])

    def test_set_background_and_axes(self):
        emp = Emperor(self.ord_res, self.mf)

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

        emp = Emperor(self.ord_res, self.mf)

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

        emp = Emperor(self.ord_res, self.mf)
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
                                                '20080116': False}}
                        }

        emp = Emperor(self.ord_res, self.mf)
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

        emp = Emperor(self.ord_res, self.mf)
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

        emp = Emperor(self.ord_res, self.mf)
        with self.assertRaises(TypeError):
            emp.settings = deepcopy(exp_settings)


if __name__ == "__main__":
    main()
