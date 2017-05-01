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
import pandas as pd

from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from emperor import __version__ as emperor_version
from emperor.util import (get_emperor_support_files_dir,
                          validate_and_process_custom_axes, resolve_stable_url)
from emperor.qiime_backports.make_3d_plots import (get_custom_coords,
                                                   remove_nans,
                                                   scale_custom_coords)

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
    remote: bool or str, optional
        This parameter can have one of the following three behaviors according
        to the value: (1) ``str`` - load the resources from a user-specified
        remote location, (2) ``False`` - load the resources from the
        nbextensions folder in the Jupyter installation or (3) ``True`` - load
        the resources from the GitHub repository. This parameter defaults to
        ``True``. See the Notes section for more information.

    Attributes
    ----------
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
    def __init__(self, ordination, mapping_file, dimensions=5, remote=True):
        self.ordination = ordination

        self.mf = mapping_file.copy()

        # filter all metadata that we may have for which we don't have any
        # coordinates this also ensures that the coordinates are in the
        # same order as the metadata
        self.mf = self.mf.loc[ordination.samples.index]

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

        self._settings = {}

    def __str__(self):
        return self.make_emperor()

    def _repr_html_(self):
        """Used to display a plot in the Jupyter notebook"""

        # we import here as IPython shouldn't be a dependency of Emperor
        # however if this method is called it will be from an IPython notebook
        # otherwise the developer is responsible for calling this method
        from IPython.display import display, HTML

        return display(HTML(str(self)))

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

    def make_emperor(self, standalone=False, custom_axes=None):
        """Build an emperor plot

        Parameters
        ----------
        standalone : bool
            Whether or not the produced plot should be a standalone HTML file.
        custom_axes : list of str, optional
            Custom axes to embed in the ordination.

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

        # based on: http://stackoverflow.com/a/6196098
        loader = FileSystemLoader(join(get_emperor_support_files_dir(),
                                       'templates'))

        if standalone:
            main_path = basename(STANDALONE_PATH)
        else:
            main_path = basename(JUPYTER_PATH)
        env = Environment(loader=loader)

        main_template = env.get_template(main_path)

        # there's a bug in old versions of Pandas that won't allow us to rename
        # a DataFrame's index, newer versions i.e 0.18 work just fine but 0.14
        # would overwrite the name and simply set it as None
        if self.mf.index.name is None:
            index_name = 'SampleID'
        else:
            index_name = self.mf.index.name

        # format the metadata
        headers = list(map(str, [index_name] + self.mf.columns.tolist()))
        metadata = self.mf.apply(lambda x: [str(x.name)] +
                                 x.astype('str').tolist(),
                                 axis=1).values.tolist()

        # format the coordinates
        d = self.dimensions

        # normalize the coordinates
        coords = self.ordination.samples.values[:, :d]
        coords /= np.max(np.abs(coords))
        coords = coords.tolist()

        # convert to a list from the values property as old versions of pandas
        # do not convert the elements of the Series/DataFrames to the nearest
        # python type, causing errors when seralizing to JSON.
        pct_var = (self.ordination.proportion_explained[:d] * 100)
        pct_var = pct_var.values.tolist()
        names = self.ordination.samples.columns[:d].values.tolist()

        # avoid unicode strings
        coord_ids = list(map(str, self.mf.index.tolist()))

        # TODO: This will be removed once the custom axes creation is moved to
        # the graphical user interface i.e. to the Axes tab.
        if custom_axes:
            mf = validate_and_process_custom_axes(self.mf, custom_axes)

            data = mf.apply(lambda x: [x.name] + x.tolist(),
                            axis=1).values.tolist()

            # vestigial qiime structures for metadata and coordinates
            mapping_file = [headers] + data
            coords_file = [coord_ids, coords]

            # sequence ported from qiime/scripts/make_3d_plots.py @ 9115351
            get_custom_coords(custom_axes, mapping_file, coords_file)
            remove_nans(coords_file)
            scale_custom_coords(custom_axes, coords_file)

            # arguments are modified, so put them back out
            _, coords = coords_file
            coords = coords.tolist()

            # custom axes are assigned -1 percent explained
            pct_var = ([-1] * len(custom_axes)) + pct_var
            names = custom_axes + names

        # yes, we could have used UUID, but we couldn't find an easier way to
        # test that deterministically and with this approach we can seed the
        # random number generator and test accordingly
        plot_id = 'emperor-notebook-' + str(hex(np.random.randint(2**32)))

        plot = main_template.render(coords_ids=coord_ids, coords=coords,
                                    pct_var=pct_var, md_headers=headers,
                                    metadata=metadata, base_url=self.base_url,
                                    plot_id=plot_id,
                                    logic_template_path=basename(LOGIC_PATH),
                                    style_template_path=basename(STYLE_PATH),
                                    axes_names=names,
                                    width=self.width,
                                    height=self.height,
                                    settings=self.settings)

        return plot

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
        emperor.core.Emperor.scale_by
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
            else:
                raise KeyError('Unrecognized settings key: %s' % key)

    @settings.deleter
    def settings(self):
        self._settings = {}
