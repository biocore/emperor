r"""
Emperor 3D PCoA viewer (:mod:`emperor.core`)
============================================

This module provides an Object to interact and visualize an Emperor plot
from the IPython notebook.

.. currentmodule:: emperor.core

Classes
-------
.. autosummary::
    :toctree: generated/

    Emperor
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from template import TEMPLATE_HTML, TEMPLATE_JS
from jinja2 import Template
import numpy as np
# we are going to use this remote location to load external resources
# RESOURCES_URL = 'http://emperor.microbio.me/master/make_emperor/emperor_outpu\
#t/emperor_required_resources'
#BASE_URL = 'https://cdn.rawgit.com/ElDeveloper/emperor/require-js'


class Emperor(object):
    """Display principal coordinates analysis plots

    Use this object to interactively display a PCoA plot using the Emperor
    GUI. IPython provides a rich display system that will let you display a
    plot inline, without the need of creating a temprorary file or having to
    write to disk.

    Parameters
    ----------
    ordination: skbio.stats.ordination.OrdinationResults
        Object containing the computed values for an ordination method in
        scikit-bio.
    metadata: pd.DataFrame
        Table of metadata where samples correspond to rows and metadata
        variables correspond to columns.


    Examples
    --------
    Create an Emperor object and display it from the IPython notebook:

    >>> data = [['PC.354', 'Control', '20061218', 'Control_mouse_I.D._354'],
    ... ['PC.355', 'Control', '20061218', 'Control_mouse_I.D._355'],
    ... ['PC.356', 'Control', '20061126', 'Control_mouse_I.D._356'],
    ... ['PC.481', 'Control', '20070314', 'Control_mouse_I.D._481'],
    ... ['PC.593', 'Control', '20071210', 'Control_mouse_I.D._593'],
    ... ['PC.607', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
    ... ['PC.634', 'Fast', '20080116', 'Fasting_mouse_I.D._634'],
    ... ['PC.635', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
    ... ['PC.636', 'Fast', '20080116', 'Fasting_mouse_I.D._636']]
    >>> headers = ['SampleID', 'Treatment', 'DOB', 'Description']
    >>> ordination = OrdinationResults.read('unweighted_unifrac_pc.txt')

    Now import the Emperor object and display it using IPython, note that this
    call will have no effect under an interactive Python session:

    >>> from emperor import Emperor
    >>> Emperor(ordination, data, headers)

    Notes
    -----
    This object currently does not support the full range of actions that the
    GUI does support and should be considered experimental at the moment.

    References
    ----------
    .. [1] EMPeror: a tool for visualizing high-throughput microbial community
       data Vazquez-Baeza Y, Pirrung M, Gonzalez A, Knight R.  Gigascience.
       2013 Nov 26;2(1):16.

    """
    def __init__(self, ordination, metadata):

        self.ordination = ordination
        self.metadata = metadata
        self._html = None

    def __str__(self):
        if self._html is None:
            self._make_emperor()
        return self._html

    def _repr_html_(self):
        """Used to be displayed in the IPython notebook"""

        # we import here as IPython shouldn't be a dependency of Emperor
        # however if this method is called it will be from an IPython notebook
        # otherwise the developer is responsible for calling this method
        from IPython.display import display, HTML

        # this provides a string representation that's independent of the
        # filesystem, it will instead retrieve them from the official website

        #output = str(self).replace('emperor_required_resources',
        #                           RESOURCES_URL)
        output = str(self)
        # thanks to the IPython devs for helping me figure this one out
        return display(HTML(output), metadata=dict(isolated=True))

    def _make_emperor(self):
        """Private method to build an Emperor HTML string"""
        # template = Template(TEMPLATE_STRING)
        def listify(a):
            return np.asarray(a, dtype='str').tolist()

        coords_ids = listify(self.ordination.samples.index)
        coords = listify(self.ordination.samples)
        pct_var = listify(self.ordination.proportion_explained)

        md_headers = listify(self.metadata.columns)
        metadata = listify(self.metadata.values)


        full = Template(TEMPLATE_HTML).render(base_URL=BASE_URL)
        full += Template(TEMPLATE_JS).render(coords_ids=coords_ids, coords=coords,
                                             pct_var=pct_var, md_headers=md_headers,
                                             metadata=metadata, base_URL=BASE_URL)
        self._html = full

