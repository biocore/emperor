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

from copy import deepcopy
from os.path import join, basename
from distutils.dir_util import copy_tree
import warnings
import numpy as np
import pandas as pd

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from skbio import OrdinationResults

from emperor import __version__ as emperor_version
from emperor.util import (get_emperor_support_files_dir,
                          preprocess_coords_file, resolve_stable_url,
                          validate_and_process_custom_axes, EmperorWarning)

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
        scikit-bio. Currently supports skbio.stats.ordination.PCoA and
        skbio.stats.ordination.RDA results.
    mapping_file: pd.DataFrame
        DataFrame object with the metadata associated to the samples in the
        ``ordination`` object, should have an index set and it should match the
        identifiers in the ``ordination`` object.
    feature_mapping_file: pd.DataFrame, optional
        DataFrame object with the metadata associated to the features in the
        ``ordination`` object, should have an index set and it should match the
        identifiers in the ``ordination.features`` object.
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
    procrustes: list of OrdinationResults, optional
        A list of the OrdinationResults objects with the same sample
        identifiers as the identifiers in ``ordination``.
    ignore_missing_samples: bool, optional
        If set to `True` samples and features without metadata are included by
        setting all metadata values to: ``This element has no metadata``. By
        default an exception will be raised if missing elements are
        encountered. Note, this flag only takes effect if there's at least one
        overlapping element.

    Attributes
    ----------
    jackknifed: list
        List of OrdinationResults objects in the same sample-order as
        ``self.ordination``.
    procrustes: list
        List of OrdinationResults objects in the same sample-order as
        ``self.ordination``.
    procrustes_names: list
        A list of names that will be used to distinguish samples from each
        ordination in a procrustes plot. The GUI will display a category
        labeled ``__Procrustes_Names__``.
    width: str
        Width of the plot when displayed in the Jupyter notebook (in CSS
        units).
    height: str
        Height of the plot when displayed in the Jupyter notebook (in CSS
        units).
    settings: dict
        A dictionary of settings that is loaded when a plot is displayed.
        Settings generated from the graphical user interface are stored as JSON
        files that can be loaded, and directly set to this attribute.
        Alternatively, each aspect of the plot can be changed with dedicated
        methods, for example see ``color_by``, ``set_background_color``, etc.
        This attribute can also be serialized as a JSON string and loaded from
        the GUI.
    feature_mf: pd.DataFrame
        DataFrame object with the metadata associated to the features in the
        ``ordination`` object, should have an index set and it should match the
        identifiers in the ``ordination.features`` property.
    custom_axes : list of str, optional
        Custom axes to embed in the ordination.
    jackknifing_method : {'IQR', 'sdev'}, optional
        Used only when plotting ellipsoids for jackknifed beta diversity
        (i.e. using a directory of coord files instead of a single coord
        file). Valid values are ``"IQR"`` (for inter-quartile ranges) and
        ``"sdev"`` (for standard deviation). This argument is ignored if
        ``self.jackknifed`` is ``None`` or an empty list.

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
        If none of the samples in the ordination matrix are in the metadata.
        If the data is one-dimensional.
    KeyError
        If there's samples in the ordination matrix but not in the metadata.

    References
    ----------
    .. [1] EMPeror: a tool for visualizing high-throughput microbial community
       data Vazquez-Baeza Y, Pirrung M, Gonzalez A, Knight R.  Gigascience.
       2013 Nov 26;2(1):16.

    """
    def __init__(self, ordination, mapping_file, feature_mapping_file=None,
                 dimensions=5, remote=True, jackknifed=None, procrustes=None,
                 ignore_missing_samples=False):

        if ordination.samples.shape[1] < 2:
            raise ValueError('Ordinations with less than two dimensions are'
                             ' not supported.')

        self.ordination = ordination
        self.jackknifed = jackknifed if jackknifed is not None else []
        self.procrustes = procrustes if procrustes is not None else []

        self.mf = mapping_file.copy()

        self.mf = self._validate_metadata(self.mf, self.ordination.samples,
                                          ignore_missing_samples)

        # if biplots are to be visualized
        if self.ordination.features is not None:
            self.feature_mf = \
                self._validate_metadata(feature_mapping_file,
                                        self.ordination.features,
                                        ignore_missing_samples, kind='feature')

        self._validate_ordinations()

        self._html = None

        if self.ordination.proportion_explained.shape[0] < dimensions:
            self.dimensions = self.ordination.proportion_explained.shape[0]
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

        self._settings = {}

        self.custom_axes = []

        # label each ordination by index
        self.procrustes_names = []
        self.jackknifing_method = 'IQR'
        if self.procrustes:
            self.procrustes_names = ['Ordination %d' % i
                                     for i in range(len(self.procrustes) + 1)]

    def __str__(self):
        return self.make_emperor()

    def _repr_html_(self):
        """Used to display a plot in the Jupyter notebook"""

        # we import here as IPython shouldn't be a dependency of Emperor
        # however if this method is called it will be from an IPython notebook
        # otherwise the developer is responsible for calling this method
        from IPython.display import display, HTML

        return display(HTML(str(self)))

    def _validate_metadata(self, metadata, matrix, ignore_missing_samples,
                           kind='sample'):

        if kind not in {'sample', 'feature'}:
            raise ValueError('Unsupported "kind" value %s' % kind)

        # metadata is optional for biplots, so we just create an empty table
        if metadata is None:
            metadata = pd.DataFrame(index=pd.Index(matrix.index, name='id'))
            metadata['all'] = 'All elements'
            return metadata

        ordination_elements = set(matrix.index)
        difference = ordination_elements - set(metadata.index)

        if difference == ordination_elements:
            raise ValueError('None of the %s identifiers match between the'
                             ' metadata and the coordinates. Verify that you '
                             'are using metadata and coordinates corresponding'
                             ' to the same dataset.' % kind)

        if difference and not ignore_missing_samples:
            # sort the elements so we have a deterministic output
            difference = sorted([str(i) for i in difference])

            # if there's more than 5 missing elements, truncate the list
            if len(difference) > 5:
                elements = ', '.join(difference[:5])
                suffix = ("Showing only the first 5 %ss out of %d: %s ..." %
                          (kind, len(difference), elements))
            else:
                elements = ', '.join(difference)
                suffix = ("Offending %ss: %s" % (kind, elements))

            raise KeyError("There are %ss not included in the %s mapping "
                           "file. Override this error by using the "
                           "`ignore_missing_samples` argument. %s" %
                           (kind, kind, suffix))
        elif difference and ignore_missing_samples:
            warnings.warn("%d out of %d %ss have no metadata and are being"
                          " included with a placeholder value." %
                          (len(difference), len(ordination_elements), kind),
                          EmperorWarning)

            # pad the missing elements
            pad = pd.DataFrame(index=difference, columns=metadata.columns,
                               dtype=str)
            pad.fillna('This element has no metadata', inplace=True)
            metadata = pd.concat([metadata, pad])

        # filter all metadata that we may have for which we don't have any
        # coordinates this also ensures that the coordinates are in the
        # same order as the metadata
        metadata = metadata.loc[matrix.index]

        return metadata

    def _validate_ordinations(self):
        # bail if the value is non or an empty list
        if self.jackknifed == [] and self.procrustes == []:
            return
        # error if the user tries to create a jackknifed procrustes plot
        if len(self.jackknifed) > 0 and len(self.procrustes) > 0:
            raise ValueError('Cannot plot a procrustes and a jackknifed plot')

        ordinations = self.jackknifed if self.jackknifed else self.procrustes

        ok = all([isinstance(j, OrdinationResults) for j in ordinations])
        if not ok:
            raise TypeError('All elements in the jackknifed array should be '
                            'OrdinationResults instances.')

        master_ids = self.ordination.samples.index
        master = set(self.ordination.samples.index)

        aligned = []

        for i, ord_res in enumerate(ordinations):
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

        # need to test this carefully i.e. that when one is set the other one
        # doesn't have anything or is none
        if self.jackknifed:
            self.jackknifed = aligned
        elif self.procrustes:
            self.procrustes = aligned

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

    def make_emperor(self, standalone=False):
        """Build an emperor plot

        Parameters
        ----------
        standalone : bool
            Whether or not the produced plot should be a standalone HTML file.

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
        main_template = self._get_template(standalone)

        # _process_data does a lot of munging to the coordinates data and
        # _to_dict puts the data into a dictionary-like object for consumption
        data = self._to_dict(self._process_data(self.custom_axes,
                                                self.jackknifing_method))

        # yes, we could have used UUID, but we couldn't find an easier way to
        # test that deterministically and with this approach we can seed the
        # random number generator and test accordingly
        plot_id = 'emperor-notebook-' + str(hex(np.random.randint(2**32)))

        # need to do something about low and high
        plot = main_template.render(data=data, plot_id=plot_id,
                                    logic_template_path=basename(LOGIC_PATH),
                                    style_template_path=basename(STYLE_PATH),
                                    base_url=self.base_url,
                                    width=self.width,
                                    height=self.height)

        return plot

    def _to_dict(self, data):
        """Convert processed data into a dictionary of decompositions

        Parameters
        ----------
        data : tuple
            The output of _process_data. Should contain information about the
            scatter plot and the biplot.

        Returns
        -------
        dict
            A dictionary describing the plots contained in the ordination
            object and the sample + feature metadata.
        """
        # data is a tuple as returned by _process_data
        (coord_ids, coords, pct_var, ci,
         headers, metadata, names,
         edges,
         bi_coords, bi_ids,
         bi_headers, bi_metadata) = data

        data = {
            'plot': {
                'decomposition': {
                    'sample_ids': coord_ids,
                    'coordinates': coords,
                    'axes_names': names,
                    'percents_explained': pct_var,
                    'ci': ci,
                    'edges': edges
                },
                'type': 'scatter',
                'metadata_headers': headers,
                'metadata': metadata,
                'settings': self.settings,
            }
        }

        # we can rely on the fact that the dictionary above will exist
        if self.ordination.features is not None:
            data['biplot'] = deepcopy(data['plot'])
            data['biplot']['decomposition']['ci'] = []
            data['biplot']['decomposition']['edges'] = []
            data['biplot']['type'] = 'arrow'
            data['biplot']['settings'] = None

            data['biplot']['metadata'] = bi_metadata
            data['biplot']['metadata_headers'] = bi_headers
            data['biplot']['decomposition']['sample_ids'] = bi_ids
            data['biplot']['decomposition']['coordinates'] = bi_coords

        return data

    def _get_template(self, standalone=False):
        """Get the jinja template object

        Parameters
        ----------
        standalone: bool, optional
            Whether or not the generated plot will load resources locally
            (``True``), or from a specified URL (``False``).

        Returns
        -------
        jinja2.Template
            Template where the plot is created.
        """
        # based on: http://stackoverflow.com/a/6196098
        loader = FileSystemLoader(join(get_emperor_support_files_dir(),
                                       'templates'))

        if standalone:
            main_path = basename(STANDALONE_PATH)
        else:
            main_path = basename(JUPYTER_PATH)
        env = Environment(loader=loader)

        return env.get_template(main_path)

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
        list of list of str
            An edge list for procrustes plots
        list of list of float
            Arrow locations for the biplots.
        list of str
            Arrow identifiers for biplots.
        list of str
            Header names for biplot metadata.
        list of list of str
            Metadata for the biplots.

        Notes
        -----
        This method is exercised by testing the ``make_emperor`` method, and is
        not intended to be used by end-users.
        """
        if (self.jackknifed or self.procrustes) and len(custom_axes) > 1:
            raise ValueError("Jackknifed and Procrustes plots are limited to "
                             "one custom axis.")

        # turn modern data into legacy data
        dims = self.dimensions

        ci = None
        bi_coords, bi_ids, bi_headers, bi_metadata = None, None, None, None

        c_headers, c_data, c_eigenvals, c_pct, edges = [], [], [], [], []
        ordinations = []

        if self.jackknifed or self.procrustes:
            ordinations = [self.ordination] + self.procrustes + self.jackknifed

            for data in ordinations:
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

        # repeats is only dependant on procrustes
        headers, metadata = self._to_legacy_map(self.mf, custom_axes,
                                                len(self.procrustes))

        # make an edge list for the procrustes plot
        if self.procrustes:
            for i in range(len(self.procrustes)):
                for sample in self.mf.index:
                    edges.append([sample + '_0', sample + '_%d' % (i + 1)])

        c_headers, c_data, _, c_pct, low, high, _ = \
            preprocess_coords_file(c_headers, c_data, c_eigenvals, c_pct,
                                   headers, metadata, custom_axes,
                                   jackknifing_method,
                                   is_comparison=bool(self.procrustes))

        names = self.ordination.samples.columns[:dims].values.tolist()
        c_pct = c_pct.tolist()

        if custom_axes:
            names = custom_axes + names

            c_pct = ([-1] * len(custom_axes)) + c_pct

        if low is not None or high is not None:
            ci = np.abs(high - low).tolist()

        if self.ordination.features is not None:
            bi_coords = self.ordination.features.values[:, :dims]
            bi_coords = bi_coords / np.max(np.abs(bi_coords))
            bi_coords = bi_coords.tolist()
            bi_ids = self.ordination.features.index.values.tolist()

            bi_headers, bi_metadata = self._to_legacy_map(self.feature_mf)

        return (c_headers, c_data.tolist(),
                c_pct, ci, headers, metadata, names,
                edges,
                bi_coords, bi_ids,
                bi_headers, bi_metadata)

    def _to_legacy_map(self, mf, custom_axes=None, repeats=0):
        """Helper method to convert Pandas dataframe to legacy QIIME structure

        Parameters
        ----------
        mf : pd.DataFrame
            DataFrame with the metadata, this can be feature or sample
            metadata. If the index name is ``None``, then it will be set as
            ``'SampleID'``, otherwise it will be left untouched.
        custom_axes : list of str, optional
            Custom axes to embed in the ordination.
        repeats : int
            Number of times that the sample ids should be repeated. This is
            used exclusively for procrustes plots. If the procrustes_names
            property is available a column will be added with each procrustes
            name.

        Returns
        -------
        list of str
            Name of the metadata columns and the index name.
        list of list of str
            Data in ``mf``.
        """
        # there's a bug in old versions of Pandas that won't allow us to rename
        # a DataFrame's index, newer versions i.e 0.18 work just fine but 0.14
        # would overwrite the name and simply set it as None
        if mf.index.name is None:
            index_name = 'SampleID'
        else:
            index_name = mf.index.name

        if custom_axes:
            mf = validate_and_process_custom_axes(mf, custom_axes)

        if repeats:
            mfs = []
            # repeats and the original
            for i in range(repeats + 1):
                mfs.append(mf.copy())
                mfs[i].index = pd.Index(mfs[i].index + '_%d' % i,
                                        name=mfs[i].index.name)

                # add to be able to differentiate between ordinations
                if self.procrustes_names:
                    mfs[i]['__Procrustes_Names__'] = self.procrustes_names[i]

            mf = pd.concat(mfs)

        # create a list of lists representation for the entire dataframe
        headers = [index_name] + mf.columns.astype(str).tolist()
        metadata = mf.reset_index().astype(str).values.tolist()
        return headers, metadata

    def _base_data_checks(self, category, data, d_type):
        """Perform common checks in the methods that modify the plot

        Parameters
        ----------
        category: str
            The metadata category used for this attribute.
        data: dict or pd.Series
            Mapping of metadata value to attribute.
        d_type: object
            The required type in the ``data`` mappings.

        Returns
        -------
        dict
            Validated and consumable dictionary of attribute mappings.
        """

        if not isinstance(category, str):
            raise TypeError('Metadata category must be a string')

        if category not in self.mf.columns:
            raise KeyError('The category %s is not present in your metadata' %
                           category)

        if isinstance(data, pd.Series):
            data = data.to_dict()

        # if no data is provide just return an empty dictionary
        if data is None or not data:
            return {}

        present = set(self.mf[category].value_counts().index)
        given = set(data.keys())

        if present != given:
            if present.issubset(given):
                raise ValueError('More categories present in the provided '
                                 'data, the following categories were '
                                 'not found in the metadata: %s.' %
                                 ', '.join(given - present))
            elif given.issubset(present):
                raise ValueError('The following categories are not present'
                                 ' in the provided data: %s' %
                                 ', '.join(present - given))

        # isinstance won't recognize numpy dtypes that are still valid
        if not all(np.issubdtype(type(v), d_type) for v in data.values()):
            raise TypeError('Values in the provided data must be '
                            'of %s' % d_type)

        return data

    def color_by(self, category, colors=None, colormap=None, continuous=False):
        """Set the coloring settings for the plot elements

        Parameters
        ----------
        category: str
            Name of the metadata column.
        colors: dict or pd.Series, optional
            Mapping of categories to a CSS color attribute. Defaults to the
            colors described by ``colormap``.
        colormap: str, optional
            Name of the colormap to use. Supports continuous and discrete
            colormaps, see the notes section. Defaults to QIIME's discrete
            colorscheme.
        continuous: bool, optional
            Whether or not the ``category`` should be interpreted as numeric.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Raises
        ------
        KeyError
            If ``category`` is not part of the metadata.
        TypeError
            If ``category`` is not a string.
        ValueError
            If ``colors`` describes fewer or more categories than the ones
            present in the ``category`` column.
            If ``colors`` has colors in a non-string format.

        Notes
        -----
        Valid colormaps are listed below (under the `Code` column), for
        examples see [1]_ or [2]_.

        +----------+---------------------+------------+
        | Code     | Name                | Type       |
        +==========+=====================+============+
        | Paired   | Paired              | Discrete   |
        +----------+---------------------+------------+
        | Accent   | Accent              | Discrete   |
        +----------+---------------------+------------+
        | Dark2    | Dark                | Discrete   |
        +----------+---------------------+------------+
        | Set1     | Set1                | Discrete   |
        +----------+---------------------+------------+
        | Set2     | Set2                | Discrete   |
        +----------+---------------------+------------+
        | Set3     | Set3                | Discrete   |
        +----------+---------------------+------------+
        | Pastel1  | Pastel1             | Discrete   |
        +----------+---------------------+------------+
        | Pastel2  | Pastel2             | Discrete   |
        +----------+---------------------+------------+
        | Viridis  | Viridis             | Sequential |
        +----------+---------------------+------------+
        | Reds     | Reds                | Sequential |
        +----------+---------------------+------------+
        | RdPu     | Red-Purple          | Sequential |
        +----------+---------------------+------------+
        | Oranges  | Oranges             | Sequential |
        +----------+---------------------+------------+
        | OrRd     | Orange-Red          | Sequential |
        +----------+---------------------+------------+
        | YlOrBr   | Yellow-Orange-Brown | Sequential |
        +----------+---------------------+------------+
        | YlOrRd   | Yellow-Orange-Red   | Sequential |
        +----------+---------------------+------------+
        | YlGn     | Yellow-Green        | Sequential |
        +----------+---------------------+------------+
        | YlGnBu   | Yellow-Green-Blue   | Sequential |
        +----------+---------------------+------------+
        | Greens   | Greens              | Sequential |
        +----------+---------------------+------------+
        | GnBu     | Green-Blue          | Sequential |
        +----------+---------------------+------------+
        | Blues    | Blues               | Sequential |
        +----------+---------------------+------------+
        | BuGn     | Blue-Green          | Sequential |
        +----------+---------------------+------------+
        | BuPu     | Blue-Purple         | Sequential |
        +----------+---------------------+------------+
        | Purples  | Purples             | Sequential |
        +----------+---------------------+------------+
        | PuRd     | Purple-Red          | Sequential |
        +----------+---------------------+------------+
        | PuBuGn   | Purple-Blue-Green   | Sequential |
        +----------+---------------------+------------+
        | Greys    | Greys               | Sequential |
        +----------+---------------------+------------+
        | Spectral | Spectral            | Diverging  |
        +----------+---------------------+------------+
        | RdBu     | Red-Blue            | Diverging  |
        +----------+---------------------+------------+
        | RdYlGn   | Red-Yellow-Green    | Diverging  |
        +----------+---------------------+------------+
        | RdYlB    | Red-Yellow-Blue     | Diverging  |
        +----------+---------------------+------------+
        | RdGy     | Red-Grey            | Diverging  |
        +----------+---------------------+------------+
        | PiYG     | Pink-Yellow-Green   | Diverging  |
        +----------+---------------------+------------+
        | BrBG     | Brown-Blue-Green    | Diverging  |
        +----------+---------------------+------------+
        | PuOr     | Purple-Orange       | Diverging  |
        +----------+---------------------+------------+
        | PRGn     | Purple-Green        | Diverging  |
        +----------+---------------------+------------+

        See Also
        --------
        emperor.core.Emperor.visibility_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.opacity_by
        emperor.core.Emperor.shape_by
        emperor.core.Emperor.set_background_color
        emperor.core.Emperor.set_axes

        References
        ----------
        .. [1] https://matplotlib.org/examples/color/colormaps_reference.html
        .. [2] http://colorbrewer2.org/
        """
        colors = self._base_data_checks(category, colors, str)

        if colormap is None:
            colormap = 'discrete-coloring-qiime'
        elif not isinstance(colormap, str):
            raise TypeError('The colormap argument must be a string')

        self._settings.update({"color": {
            "category": category,
            "colormap": colormap,
            "continuous": continuous,
            "data": colors
        }})

        return self

    def visibility_by(self, category, visibilities=None, negate=False):
        """Set the visibility settings for the plot elements

        Parameters
        ----------
        category: str
            Name of the metadata column.
        visibilities: dict, list or pd.Series, optional
            When this argument is a ``dict`` or ``pd.Series``, it is a mapping
            of categories to a boolean values determining whether or not that
            category should be visible. When this argument is a ``list``, only
            categories present will be visible in the plot.
        negate: bool
            Whether or not to negate the values in ``visibilities``.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Raises
        ------
        KeyError
            If ``category`` is not part of the metadata.
        TypeError
            If ``category`` is not a string.
        ValueError
            If ``visibilities`` describes fewer or more categories than the
            ones present in the ``category`` column.
            If ``visibilities`` has visibilities in a non-string format.

        See Also
        --------
        emperor.core.Emperor.color_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.opacity_by
        emperor.core.Emperor.shape_by
        emperor.core.Emperor.set_background_color
        emperor.core.Emperor.set_axes
        """
        if isinstance(visibilities, list) and category in self.mf:
            cats = self.mf[category].unique()
            visibilities = {c: c in visibilities for c in cats}

        visibilities = self._base_data_checks(category, visibilities, bool)

        # negate visibilities using XOR
        visibilities = {k: v ^ negate for k, v in visibilities.items()}

        self._settings.update({"visibility": {
            "category": category,
            "data": visibilities
        }})

        return self

    def scale_by(self, category, scales=None, global_scale=1.0, scaled=False):
        """Set the scaling settings for the plot elements

        Parameters
        ----------
        category: str
            Name of the metadata column.
        scales: dict or pd.Series, optional
            Mapping of categories to numbers determining the size of the
            elements in each category.
        global_scale: int or float, optional
            The size of all the elements.
        scaled: bool
            Whether or not the values in ``scales`` should be assumed to be
            numeric and scaled in size according to their value.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Raises
        ------
        KeyError
            If ``category`` is not part of the metadata.
        TypeError
            If ``category`` is not a string.
            If ``global_scale`` is not a number.
            If ``scaled`` is not a boolean value.
        ValueError
            If ``scales`` describes fewer or more categories than the ones
            present in the ``category`` column.
            If ``scales`` has sizes in a non-numeric format.

        See Also
        --------
        emperor.core.Emperor.visibility_by
        emperor.core.Emperor.color_by
        emperor.core.Emperor.shape_by
        emperor.core.Emperor.set_background_color
        emperor.core.Emperor.set_axes
        """
        scales = self._base_data_checks(category, scales, float)

        if (not isinstance(global_scale, (float, int)) or
           isinstance(global_scale, bool)):
            raise TypeError('The global scale argument must be a float or int')

        if not isinstance(scaled, bool):
            raise TypeError('The scaled argument must be a bool')

        self._settings.update({"scale": {
            "category": category,
            "globalScale": str(global_scale),
            "scaleVal": scaled,
            "data": scales
        }})

        return self

    def opacity_by(self, category, opacities=None, global_scale=1.0,
                   scaled=False):
        """Set the scaling settings for the plot elements

        Parameters
        ----------
        category: str
            Name of the metadata column.
        opacities: dict or pd.Series, optional
            Mapping of categories to numbers determining the opacity of the
            elements in each category.
        global_scale: int or float, optional
            The size of all the elements.
        scaled: bool
            Whether or not the values in ``opacities`` should be assumed to be
            numeric and scaled in size according to their value.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Raises
        ------
        KeyError
            If ``category`` is not part of the metadata.
        TypeError
            If ``category`` is not a string.
            If ``global_scale`` is not a number.
            If ``scaled`` is not a boolean value.
        ValueError
            If ``opacities`` describes fewer or more categories than the ones
            present in the ``category`` column.
            If ``opacities`` has sizes in a non-numeric format.

        See Also
        --------
        emperor.core.Emperor.visibility_by
        emperor.core.Emperor.color_by
        emperor.core.Emperor.shape_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.set_background_color
        emperor.core.Emperor.set_axes
        """
        opacities = self._base_data_checks(category, opacities, float)

        if (not isinstance(global_scale, (float, int)) or
           isinstance(global_scale, bool)):
            raise TypeError('The global scale argument must be a float or int')

        if not isinstance(scaled, bool):
            raise TypeError('The scaled argument must be a bool')

        self._settings.update({"opacity": {
            "category": category,
            "globalScale": str(global_scale),
            "scaleVal": scaled,
            "data": opacities
        }})

        return self

    def shape_by(self, category, shapes=None):
        """Set the shape settings for the plot elements

        Parameters
        ----------
        category: str
            Name of the metadata column.
        shapes: dict or pd.Series, optional
            Mapping of categories to string values determining the shape of
            the objects. See the notes for the valid options.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Raises
        ------
        KeyError
            If ``category`` is not part of the metadata.
        TypeError
            If ``category`` is not a string.
        ValueError
            If ``shapes`` describes fewer or more categories than the
            ones present in the ``category`` column.
            If ``shapes`` has shapes in a non-string format.

        Notes
        -----
        The valid shape names are ``"Sphere"``, ``"Cube"``, ``"Cone"``,
        ``"Icosahedron"`` and ``"Cylinder"``.

        See Also
        --------
        emperor.core.Emperor.color_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.opacity_by
        emperor.core.Emperor.visibility_by
        emperor.core.Emperor.set_background_color
        emperor.core.Emperor.set_axes
        """
        shapes = self._base_data_checks(category, shapes, str)

        self._settings.update({"shape": {
            "category": category,
            "data": shapes
        }})

        return self

    def animations_by(self, gradient, trajectory, colors, speed=1, radius=1):
        """Set the shape settings for the plot elements

        Parameters
        ----------
        gradient: str
            Name of the metadata column that orders samples.
        trajectory: str
            Name of the metadata column that groups samples.
        colors: dict or pd.Series
            Mapping of trajectory categories to a CSS color attribute.
        speed: float
            How fast the animation should go.
        radius: float
            The radius of the animated traces.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Raises
        ------
        KeyError
            If ``gradient`` or ``trajectory`` are not part of the metadata.
        TypeError
            If ``speed`` or ``radius`` are not numbers.

        See Also
        --------
        emperor.core.Emperor.color_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.shape_by
        emperor.core.Emperor.opacity_by
        emperor.core.Emperor.visibility_by
        emperor.core.Emperor.set_background_color
        emperor.core.Emperor.set_axes
        """

        if gradient not in self.mf.columns:
            raise KeyError('The gradient category is not present in your '
                           'metadata')
        if trajectory not in self.mf.columns:
            raise KeyError('The trajectory category is not present in your '
                           'metadata')

        if not isinstance(speed, (float, int)):
            raise TypeError('Speed is not a number')
        if not isinstance(radius, (float, int)):
            raise TypeError('Radius is not a number')

        colors = self._base_data_checks(trajectory, colors, str)

        self._settings.update({"animations": {
            "gradientCategory": gradient,
            "trajectoryCategory": trajectory,
            "speed": speed,
            "radius": radius,
            "colors": colors
        }})

        return self

    def set_axes(self, visible=None, invert=None, color='white'):
        """Change visual aspects about visible dimensions in a plot

        Parameters
        ----------
        visible: list of thee ints, optional
            List of three indices of the dimensions that will be visible.
        invert: list of bools, optional
            List of three bools that determine whether each axis is inverted or
            not.
        color: str
            Color of the axes lines in the plot, should be a name or value in
            CSS format.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Raises
        ------
        ValueError
            If the ``visible`` or ``invert`` arrays don't have exactly three
            elements.
            If the ``visible`` elements are out of range i.e. if an index is
            not contained in the space defined by the dimensions property.
        TypeError
            If the indices in ``visible`` are not all integers.
            If the values of ``invert`` are not all boolean.
            If ``color`` is not a string.

        Notes
        -----
        This method is internally coupled to the ``set_background_color``
        method.

        See Also
        --------
        emperor.core.Emperor.color_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.opacity_by
        emperor.core.Emperor.shape_by
        emperor.core.Emperor.set_background_color
        """
        if visible is None:
            visible = [0, 1, 2]
        if invert is None:
            invert = [False, False, False]

        if len(visible) != 3:
            raise ValueError('Exactly three elements must be contained in the'
                             ' visible array')
        if len(invert) != 3:
            raise ValueError('Exactly three elements must be contained in the'
                             ' invert array')

        if any([v >= self.dimensions or v < 0 for v in visible]):
            raise ValueError('One or more of your visible dimensions are out '
                             'of range.')

        # prevent obscure JavaScript errors by validating the data
        if any([not isinstance(v, int) for v in visible]):
            raise TypeError('All axes indices should be integers')
        if any([not isinstance(i, bool) for i in invert]):
            raise TypeError('The elements in the invert argument should all '
                            'be boolean')
        if not isinstance(color, str):
            raise TypeError('Colors should be a CSS color as a string')

        # the background color and axes information are intertwined, so before
        # updating the data, we need to retrieve the color if it exists
        # see the code in set_background_color
        bc = self.settings.get('axes', {}).get('backgroundColor', 'black')

        self._settings.update({'axes': {
            'visibleDimensions': visible,
            'flippedAxes': invert,
            'axesColor': color,
            'backgroundColor': bc
        }})

        return self

    def set_background_color(self, color='black'):
        """Changes the background color of the plot

        Parameters
        ----------
        color: str, optional
            The background color. Color name or value in the CSS format.
            Defaults to black.

        Returns
        -------
        emperor.Emperor
            Emperor object with updated settings.

        Notes
        -----
        This method is tightly coupled to ``set_axes``.

        Raises
        ------
        TypeError
            If the color is not a string.

        See Also
        --------
        emperor.core.Emperor.color_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.scale_by
        emperor.core.Emperor.shape_by
        emperor.core.Emperor.set_axes
        """

        if not isinstance(color, str):
            raise TypeError('The background color has to be a string')

        # the background color and axes information are intertwined, so before
        # updating the data, we need to make sure we have other values present
        # see the code in set_axes
        if 'axes' not in self.settings:
            self.set_axes()

        self._settings["axes"]["backgroundColor"] = color

        return self

    @property
    def settings(self):
        """Dictionary to load default settings from, when displaying a plot"""
        return self._settings

    @settings.setter
    def settings(self, setts):
        if setts is None:
            del self.settings
            return

        for key, val in setts.items():
            if key == 'shape':
                self.shape_by(val['category'], val['data'])
            elif key == 'visibility':
                self.visibility_by(val['category'], val['data'])
            elif key == 'scale':
                self.scale_by(val['category'], val['data'],
                              float(val['globalScale']),
                              val['scaleVal'])
            elif key == 'axes':
                self.set_axes(val['visibleDimensions'], val['flippedAxes'],
                              val['axesColor'])
                self.set_background_color(val['backgroundColor'])
            elif key == 'color':
                self.color_by(val['category'], val['data'], val['colormap'],
                              val['continuous'])
            elif key == 'opacity':
                self.opacity_by(val['category'], val['data'],
                                float(val['globalScale']), val['scaleVal'])
            elif key == 'animations':
                self.animations_by(val['gradientCategory'],
                                   val['trajectoryCategory'], val['colors'],
                                   val['speed'], val['radius'])
            else:
                raise KeyError('Unrecognized settings key: %s' % key)

    @settings.deleter
    def settings(self):
        self._settings = {}
