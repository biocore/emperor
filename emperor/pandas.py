r"""
Pandas Interface for Emperor
============================

This module provides a simple interface to visualize a Pandas DataFrame using
the Emperor.

.. currentmodule:: emperor.pandas

Functions
---------
.. autosummary::
    :toctree: generated/

    scatterplot
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

import numpy as np
import pandas as pd

from emperor.core import Emperor
from skbio import OrdinationResults


def scatterplot(df, x=None, y=None, z=None):
    """

    Notes
    -----
    If a row has missing data, that data pont will be removed from the
    visualizaiton.
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("The argument is not a Pandas DataFrame")

    cols = []
    for col in [x, y, z]:
        if col is None:
            continue

        if col is not None:
            cols.append(col)

        if col not in df.columns:
            raise ValueError("'%s' is not a column in the DataFrame" % col)

        if not np.issubdtype(df[col].dtype, np.number):
            raise ValueError("'%s' is not a numeric column" % col)

    samples = df.select_dtypes(include=[np.number]).copy()
    samples.dropna(axis=0, how='any', inplace=True)

    variance = samples.var().sort_values(ascending=False)

    samples = samples[variance.index].copy()

    if len(samples) < 3:
        raise ValueError("Not enough rows without missing data")

    df = df.loc[samples.index].copy()

    ores = OrdinationResults(short_method_name='Ax', long_method_name='Axis',
                             eigvals=np.zeros_like(samples.columns),
                             samples=samples, proportion_explained=variance)

    df.index.name = '#SampleID'

    return Emperor(ores, df, dimensions=5)
