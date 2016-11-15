from unittest import TestCase, main

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import numpy.testing as npt

from emperor.flat_plots import (two_dimensional_gradient,
                                two_dimensional_discrete,
                                legend_discrete,
                                legend_gradient, plot_3x3,
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

    def test_plot_3x3(self):
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3, 1, 2, 3, 1, 2, 3],
                                           [4, 5, 6, 1, 2, 3, 1, 2, 3],
                                           [7, 8, 9, 1, 2, 3, 1, 2, 3]],
                                          columns=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        ordination.proportion_explained = [i for i in np.arange(0.1, 0.9, 0.1)]
        fig, grid = plot_3x3(ordination, 0, df, 'foo', 'viridis')
        self.assertEqual(grid.shape, (3, 4))

        exp_row0 = [np.array([[2, 1], [5, 4], [8, 7]]),
                    np.array([[3, 1], [6, 4], [9, 7]]),
                    np.array([[1, 1], [1, 4], [1, 7]])]
        exp_row0_ylabel = 'PC1 (10.00%)'
        exp_row0_xlabels = ['PC2 (20.00%)', 'PC3 (30.00%)', 'PC4 (40.00%)']

        self.assertEqual(grid[0, 0].get_ylabel(), exp_row0_ylabel)
        for j in range(3):
            self.assertEqual(grid[0, j].get_xlabel(), exp_row0_xlabels[j])
            null, gradient = grid[0, j].collections
            self.assertEqual(null.get_offsets().shape, (0, 2))
            npt.assert_equal(gradient.get_offsets(), exp_row0[j])

    def test_two_dimensional_gradient(self):
        plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])
        two_dimensional_gradient(ax, 'foo', df, ordination, 0, 1, 'viridis',
                                 {}, {})

        null, gradient = ax.collections
        npt.assert_equal(gradient.get_offsets(), np.array([[1, 2],
                                                           [4, 5],
                                                           [7, 8]]))
        npt.assert_equal(null.get_offsets(), np.zeros((0, 2)))

    def test_two_dimensional_discrete(self):
        plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])
        two_dimensional_discrete(ax, 'foo', df, ordination, 0, 1,
                                 {1: 'red', 4: 'green', 7: 'blue'},
                                 {}, {})

        null, red, green, blue = ax.collections
        npt.assert_equal(red.get_offsets(), np.array([[1, 2]]))
        npt.assert_equal(green.get_offsets(), np.array([[4, 5]]))
        npt.assert_equal(blue.get_offsets(), np.array([[7, 8]]))
        npt.assert_equal(null.get_offsets(), np.zeros((0, 2)))

    def test_legend_discrete(self):
        plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])
        legend_discrete(ax, 'foo', df, ordination,
                        {1: 'red', 4: 'green', 7: 'blue'}, {})
        texts = [i.get_text() for i in ax.get_legend().get_texts()]
        self.assertEqual(texts, ['1', '4', '7'])

    def test_legend_gradient(self):
        plt.figure()
        ax = plt.gca()
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                          columns=['foo', 'bar', 'baz'])
        ordination = mock()
        ordination.samples = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                                          columns=[0, 1, 2])

        legend_gradient(ax, 'foo', df, ordination, 'viridis', {})

        gradient = np.ones(256)
        gradient[:255] = np.arange(0, 1, 1.0 / 255)
        obs_gradient = ax.get_images()[0].get_array()[0].data
        npt.assert_equal(obs_gradient, gradient)

        left, right = ax.patches
        self.assertEqual(left.get_width(), 3)
        self.assertEqual(left.get_height(), 1)
        self.assertEqual(right.get_width(), 3)
        self.assertEqual(right.get_height(), 2)


if __name__ == '__main__':
    main()
