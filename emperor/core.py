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

from os.path import join, basename
from distutils.dir_util import copy_tree
import numpy as np

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from skbio import OrdinationResults

from emperor import __version__ as emperor_version
from emperor.util import (get_emperor_support_files_dir,
                          preprocess_coords_file, resolve_stable_url,
                          validate_and_process_custom_axes)

# we are going to use this remote location to load external resources
REMOTE_URL = ('https://cdn.rawgit.com/biocore/emperor/%s/emperor'
              '/support_files')
LOCAL_URL = "/nbextensions/emperor/support_files"

STYLE_PATH = join(get_emperor_support_files_dir(), 'templates',
                  'style-template.html')
LOGIC_PATH = join(get_emperor_support_files_dir(), 'templates',
                  'logic-template.html')

STANDALONE_PATH = join(get_emperor_support_files_dir(), 'templates',
                       'standalone-template.html')
JUPYTER_PATH = join(get_emperor_support_files_dir(), 'templates',
                    'jupyter-template.html')


class Emperor(object):
    """Display principal coordinates analysis plots

    Use this object to interactively display a PCoA plot using the Emperor
    GUI. IPython provides a rich display system that will let you display a
    plot inline, without the need of creating a temprorary file or having to
    write to disk.

    Parameters
    ----------
    ordination: skbio.OrdinationResults
        Object containing the computed values for an ordination method in
        scikit-bio.
    mapping_file: pd.DataFrame
        DataFrame object with the metadata associated to the samples in the
        ``ordination`` object, should have an index set and it should match the
        identifiers in the ``ordination`` object.
    dimensions: int, optional
        Number of dimensions to keep from the ordination data, defaults to 5.
        Be aware that this value will determine the number of dimensions for
        all computations.
    remote: bool or str, optional
        This parameter can have one of the following three behaviors according
        to the value: (1) ``str`` - load the resources from a user-specified
        remote location, (2) ``False`` - load the resources from the
        nbextensions folder in the Jupyter installation or (3) ``True`` - load
        the resources from the GitHub repository. This parameter defaults to
        ``True``. See the Notes section for more information.
    jackknifed: list of OrdinationResults, optional
        A list of the OrdinationResults objects with the same sample
        identifiers as the identifiers in ``ordination``.

    Attributes
    ----------
    jackknifed: list
        List of OrdinationResults objects in the same sample-order as
        ``self.ordination``.
    width: str
        Width of the plot when displayed in the Jupyter notebook (in CSS
        units).
    height: str
        Height of the plot when displayed in the Jupyter notebook (in CSS
        units).

    Examples
    --------
    Create an Emperor object and display it from the Jupyter notebook:

    >>> import pandas as pd, numpy as np
    >>> from emperor import Emperor
    >>> from skbio import OrdinationResults

    Ordination plots are almost invariantly associated with a set of data, that
    relates each sample to its scientific context, we refer to this as the
    *sample metadata*, and represent it using Pandas DataFrames. For this
    example we will need some metadata, we start by creating our metadata
    object:

    >>> data = [['PC.354', 'Control', '20061218', 'Control_mouse_I.D._354'],
    ... ['PC.355', 'Control', '20061218', 'Control_mouse_I.D._355'],
    ... ['PC.356', 'Control', '20061126', 'Control_mouse_I.D._356'],
    ... ['PC.481', 'Control', '20070314', 'Control_mouse_I.D._481'],
    ... ['PC.593', 'Control', '20071210', 'Control_mouse_I.D._593'],
    ... ['PC.607', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
    ... ['PC.634', 'Fast', '20080116', 'Fasting_mouse_I.D._634'],
    ... ['PC.635', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
    ... ['PC.636', 'Fast', '20080116', 'Fasting_mouse_I.D._636']]
    >>> columns = ['SampleID', 'Treatment', 'DOB', 'Description']
    >>> mf = pd.DataFrame(columns=columns, data=data)

    Before we can use this mapping file in Emperor, we should set the index
    to be `SampleID`.

    >>> mf.set_index('SampleID', inplace=True)

    Then let's create some artificial ordination data:

    >>> ids = ('PC.636', 'PC.635', 'PC.356', 'PC.481', 'PC.354', 'PC.593',
    ...             'PC.355', 'PC.607', 'PC.634')
    >>> eigvals = np.array([0.47941212, 0.29201496, 0.24744925,
    ...                     0.20149607, 0.18007613, 0.14780677,
    ...                     0.13579593, 0.1122597, 0.])
    >>> eigvals = pd.Series(data=eigvals, index=ids)
    >>> n = eigvals.shape[0]
    >>> samples = np.random.randn(n, n)
    >>> samples = pd.DataFrame(data=site, index=ids)
    >>> p_explained = np.array([0.26688705, 0.1625637, 0.13775413, 0.11217216,
    ...                         0.10024775, 0.08228351, 0.07559712, 0.06249458,
    ...                         0.])
    >>> p_explained = pd.Series(data=p_explained, index=ids)

    And encapsulate it inside an ``OrdinationResults`` object:

    >>> ores = OrdinationResults(eigvals, samples=samples,
    ...                          proportion_explained=p_explained)

    Finally import the Emperor object and display it using Jupyter, note that
    this call will have no effect under a regular Python session:

    >>> Emperor(ores, mf)

    Notes
    -----
    This object currently does not support the full range of actions that the
    GUI does support and should be considered experimental at the moment.

    The ``remote`` parameter is intended for different use-cases, you should
    use the first option "(1) - URL" when you want to load the data from a
    location different than the GitHub repository or your Jupyter notebook
    resources i.e. a custom URL. The second option "(2) - ``False``" loads
    resources from your local Jupyter installation, note that you **need** to
    execute ``nbinstall`` at least once or the application will error, this
    option is ideal for developers modifying the JavaScript source code, and in
    environments of limited internet connection. Finally, the third option "(3)
    - ``True``" should be used if you intend to embed an Emperor plot in a
    notebook and then publish it using http://nbviewer.jupyter.org.

    Raises
    ------
    ValueError
        If the remote argument is not of ``bool`` or ``str`` type.

    References
    ----------
    .. [1] EMPeror: a tool for visualizing high-throughput microbial community
       data Vazquez-Baeza Y, Pirrung M, Gonzalez A, Knight R.  Gigascience.
       2013 Nov 26;2(1):16.

    """
    def __init__(self, ordination, mapping_file, dimensions=5, remote=True,
                 jackknifed=None):

        self.ordination = ordination
        self.jackknifed = jackknifed

        self.mf = mapping_file.copy()

        # filter all metadata that we may have for which we don't have any
        # coordinates this also ensures that the coordinates are in the
        # same order as the metadata
        self.mf = self.mf.loc[ordination.samples.index]

        self._validate_jackknifed()

        self._html = None

        if ordination.proportion_explained.shape[0] < dimensions:
            self.dimensions = ordination.proportion_explained.shape[0]
        else:
            self.dimensions = dimensions

        if isinstance(remote, bool):
            if remote:
                self.base_url = resolve_stable_url(emperor_version,
                                                   REMOTE_URL)
            else:
                self.base_url = LOCAL_URL
        elif isinstance(remote, str):
            self.base_url = remote
        else:
            raise ValueError("Unsupported type for `remote` argument, should "
                             "be a bool or str")

        # dimensions for the div containing the plot in the context of the
        # Jupyter notebook, can be a "percent" or "number of pixels".
        self.width = '100%'
        self.height = '500px'

    def __str__(self):
        return self.make_emperor()

    def _repr_html_(self):
        """Used to display a plot in the Jupyter notebook"""

        # we import here as IPython shouldn't be a dependency of Emperor
        # however if this method is called it will be from an IPython notebook
        # otherwise the developer is responsible for calling this method
        from IPython.display import display, HTML

        return display(HTML(str(self)))

    def _validate_jackknifed(self):
        # bail if the value is non or an empty list
        if self.jackknifed is None or self.jackknifed == []:
            return

        ok = all([isinstance(j, OrdinationResults) for j in self.jackknifed])
        if not ok:
            raise TypeError('All elements in the jackknifed array should be '
                            'OrdinationResults instances.')

        master_ids = self.ordination.samples.index
        master = set(self.ordination.samples.index)

        aligned = []

        for i, ord_res in enumerate(self.jackknifed):
            other = set(ord_res.samples.index)

            # samples must be represented identically
            if master != other:
                raise ValueError('The ordination at index (%d) does not '
                                 'represent the exact same samples. Mismatches'
                                 ' are: %s.' % (i, ', '.join(master - other)))

            # we need to ensure the copy we have is aligned one-to-one with the
            # *master* ordination, making copies might be inefficient for large
            # datasets
            ord_res.samples = ord_res.samples.loc[master_ids].copy()
            aligned.append(ord_res)
        self.jackknifed = aligned

    def copy_support_files(self, target=None):
        """Copies the support files to a target directory

        Parameters
        ----------
        target : str
            The path where resources should be copied to. By default it copies
            the files to ``self.base_url``.
        """
        if target is None:
            target = self.base_url

        # copy the required resources
        copy_tree(get_emperor_support_files_dir(), target)

    def make_emperor(self, standalone=False, custom_axes=None,
                     jackknifing_method='IQR'):
        """Build an emperor plot

        Parameters
        ----------
        standalone : bool
            Whether or not the produced plot should be a standalone HTML file.
        custom_axes : list of str, optional
            Custom axes to embed in the ordination.
        jackknifing_method : {'IQR', 'sdef'}, optional
            Used only when plotting ellipsoids for jackknifed beta diversity
            (i.e. using a directory of coord files instead of a single coord
            file). Valid values are ``"IQR"`` (for inter-quartile ranges) and
            ``"sdev"`` (for standard deviation). This argument is ignored if
            ``self.jackknifed`` is ``None`` or an empty list.

        Returns
        -------
        str
            Formatted emperor plot.

        Raises
        ------
        KeyError
            If one or more of the ``custom_axes`` names are not present in the
            sample information.
        ValueError
            If any of the ``custom_axes`` have non-numeric values.

        Notes
        -----
        The ``standalone`` argument is intended for the different use-cases
        that Emperor can have, either as an embedded widget that lives inside,
        for example, the Jupyter notebook, or alternatively as an HTML file
        that refers to resources locally. In this case you will need to copy
        the support files by calling the ``copy_support_files`` method.

        See Also
        --------
        emperor.core.Emperor.copy_support_files
        """

        if custom_axes is None:
            custom_axes = []

        # based on: http://stackoverflow.com/a/6196098
        loader = FileSystemLoader(join(get_emperor_support_files_dir(),
                                       'templates'))

        if standalone:
            main_path = basename(STANDALONE_PATH)
        else:
            main_path = basename(JUPYTER_PATH)
        env = Environment(loader=loader)

        main_template = env.get_template(main_path)

        coord_ids, coords, pct_var, ci, headers, metadata, names = \
            self._process_data(custom_axes, jackknifing_method)

        # yes, we could have used UUID, but we couldn't find an easier way to
        # test that deterministically and with this approach we can seed the
        # random number generator and test accordingly
        plot_id = 'emperor-notebook-' + str(hex(np.random.randint(2**32)))

        # need to do something about low and high
        plot = main_template.render(coords_ids=coord_ids, coords=coords,
                                    pct_var=pct_var, ci=ci,
                                    md_headers=headers, metadata=metadata,
                                    plot_id=plot_id,
                                    axes_names=names,
                                    base_url=self.base_url,
                                    logic_template_path=basename(LOGIC_PATH),
                                    style_template_path=basename(STYLE_PATH),
                                    width=self.width,
                                    height=self.height)

        return plot

    def _process_data(self, custom_axes, jackknifing_method):
        """Handle the coordinates data

        Parameters
        ----------
        custom_axes : list of str, optional
            Custom axes to embed in the ordination.
        jackknifing_method : {'IQR', 'sdef'}, optional
            Used only when plotting ellipsoids for jackknifed beta diversity
            (i.e. using a directory of coord files instead of a single coord
            file). Valid values are ``"IQR"`` (for inter-quartile ranges) and
            ``"sdev"`` (for standard deviation). This argument is ignored if
            ``self.jackknifed`` is ``None`` or an empty list.

        Returns
        -------
        list of str
            Sample identifiers in the ordination.
        list of lists of floats
            Matrix of coordinates in the ordination data with custom_axes if
            provided.
        list of float
            either the eigenvalues of the input coordinates or the average
            eigenvalues of the multiple coords that were passed in
        list of lists floats
            coordinates representing the span of each ellipse on every axis;
            None if no jackknifing is applied
        list of str
            Name of the metadata columns and the index name.
        list of lists of str
            Data in ``mf``.
        list of str
            Names of the dimensions in the resulting ordination.

        Notes
        -----
        This method is exercised by testing the ``make_emperor`` method, and is
        not intended to be used by end-users.
        """
        if self.jackknifed and len(custom_axes) > 1:
            raise ValueError("Jackknifed plots are limited to one custom "
                             "axis.")

        # turn modern data into legacy data
        dims = self.dimensions

        ci = None

        c_headers, c_data, c_eigenvals, c_pct = [], [], [], []
        if self.jackknifed:
            for data in [self.ordination] + self.jackknifed:
                c_headers.append(data.samples.index.tolist())

                coords = data.samples.values[:, :dims]
                c_data.append(coords / np.max(np.abs(coords)))

                c_eigenvals.append(data.eigvals.values[:dims])

                c_pct.append(data.proportion_explained[:dims] * 100)
        else:
            data = self.ordination
            c_headers = data.samples.index.tolist()

            coords = self.ordination.samples.values[:, :dims]
            c_data = (coords / np.max(np.abs(coords)))

            c_eigenvals = data.eigvals.values[:dims]

            c_pct = data.proportion_explained[:dims] * 100

        headers, metadata = self._to_legacy_map(custom_axes)

        c_headers, c_data, _, c_pct, low, high, _ = \
            preprocess_coords_file(c_headers, c_data, c_eigenvals, c_pct,
                                   headers, metadata, custom_axes,
                                   jackknifing_method, False)

        names = self.ordination.samples.columns[:dims].tolist()
        c_pct = c_pct.tolist()

        if custom_axes:
            names = custom_axes + names

            c_pct = ([-1] * len(custom_axes)) + c_pct

        if low is not None or high is not None:
            ci = np.abs(high - low).tolist()

        return (self.ordination.samples.index.tolist(), c_data.tolist(),
                c_pct, ci, headers, metadata, names)

    def _to_legacy_map(self, custom_axes=None):
        """Helper method to convert Pandas dataframe to legacy QIIME structure

        Parameters
        ----------
        custom_axes : list of str, optional
            Custom axes to embed in the ordination.

        Returns
        -------
        list of str
            Name of the metadata columns and the index name.
        list of list of str
            Data in ``mf``.
        """
        mf = self.mf
        # there's a bug in old versions of Pandas that won't allow us to rename
        # a DataFrame's index, newer versions i.e 0.18 work just fine but 0.14
        # would overwrite the name and simply set it as None
        if mf.index.name is None:
            index_name = 'SampleID'
        else:
            index_name = mf.index.name

        if custom_axes:
            mf = validate_and_process_custom_axes(mf, custom_axes)

        headers = [str(c) for c in [index_name] + mf.columns.tolist()]
        metadata = mf.apply(lambda x: [str(x.name)] +
                            x.astype('str').tolist(),
                            axis=1).values.tolist()
        return headers, metadata
