from unittest import TestCase, main

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from emperor.flat_plots import (_two_dimensional_gradient, 
                                _two_dimensional_discrete,
                                _legend_discrete,
                                _legend_gradient, plot_3x3,
                                _pcoa_label)


class mock:
    pass


class PlotTests(TestCase):
    def test_pcoa_label(self):
        ordination = mock()
        ordination.proportion_explained = [0.1, 0.2, 0.3]
        exp = "PC1 (10.00%)"
        obs = _pcoa_label(0, ordination)
        self.assertEqual(obs, exp)

    def test_plot_3x3(TestCase):
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3, 1, 2, 3, 1, 2, 3], 
                                           [4, 5, 6, 1, 2, 3, 1, 2, 3], 
                                           [7, 8, 9, 1, 2, 3, 1, 2, 3]],
                                          columns=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        ordination.proportion_explained = [i for i in np.arange(0.1, 0.9, 0.1)]
        plot_3x3(ordination, 0, df, 'foo', 'viridis')

    def test_two_dimensional_gradient(self):
        fig = plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])
        _two_dimensional_gradient(ax, 'foo', df, ordination, 0, 1, 'viridis',
                                  {}, {})

    def test_two_dimensional_discrete(self):
        fig = plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])
        _two_dimensional_discrete(ax, 'foo', df, ordination, 0, 1, 
                                  {1: 'red', 4: 'green', 7: 'blue'},
                                  {}, {})


    def test_legend_discrete(self):
        fig = plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])
        _legend_discrete(ax, 'foo', df, ordination, {1: 'red', 
                                                    4:'green', 
                                                    7: 'blue'}, {})

    def test_legend_gradient(self):
        fig = plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])
        _legend_gradient(ax, 'foo', df, ordination, 'viridis', {})


if __name__ == '__main__':
    main()
