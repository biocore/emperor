# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

import pandas as pd
import numpy as np
import warnings

from os.path import abspath, dirname, join

from emperor.qiime_backports.make_3d_plots import (get_custom_coords,
                                                   remove_nans,
                                                   scale_custom_coords)
from emperor.qiime_backports.util import summarize_pcoas


class EmperorSupportFilesError(IOError):
    """Exception for missing support files"""
    pass


class EmperorInputFilesError(IOError):
    """Exception for missing support files"""
    pass


class EmperorUnsupportedComputation(ValueError):
    """Exception for computations that lack a meaning"""
    pass


class EmperorWarning(UserWarning):
    """Generic package warning"""
    pass


def get_emperor_project_dir():
    """ Returns the top-level Emperor directory

    based on qiime.util.get_qiime_project_dir from github.com/qiime/qiime
    """
    # Get the full path of util.py
    current_file_path = abspath(__file__)
    # Get the directory containing util.py
    current_dir_path = dirname(current_file_path)
    # Return the directory containing the directory containing util.py
    return dirname(current_dir_path)


def get_emperor_support_files_dir():
    """Returns the path for the support files of the project """
    return join(get_emperor_project_dir(), 'emperor/support_files/')


def nbinstall(overwrite=False, user=True, prefix=None):
    """Copies resources to the '/nbextensions' folder in your IPython directory

    This function was taken from [1] and modified to match our usecase.

    Parameters
    ----------
    overwrite : bool, optional
        If True, always install the files, regardless of what may already be
        installed. Defaults to False.
    user : bool, optional
        Whether to install to the user's .ipython/nbextensions directory.
        Otherwise do a system-wide install
        (e.g. /usr/local/share/jupyter/nbextensions/emperor). Defaults to
        False.
    prefix : str, optional
        Where the files are copied to, by default they are copied to the
        appropriate Jupyter/IPython folder, alternatively it can be a folder
        where the resources are copied to. Note, that if this parameter is set
        `user` has to be `None`.

    Raises
    ------
    ArgumentConflict
        When `prefix` and `user` are used together.

    Notes
    -----
    After you install emperor, call this function once before attempting to
    call ``Emperor`` in the Jupyter notebook.

    References
    ----------
    .. [1] GitHub repository for qgrid https://github.com/quantopian/qgrid
    """

    # Lazy imports so we don't pollute the namespace.
    try:
        from notebook import install_nbextension
    except ImportError:
        from IPython.html.nbextensions import install_nbextension
    from IPython import version_info

    install_nbextension(
        get_emperor_support_files_dir(),
        overwrite=overwrite,
        symlink=False,
        prefix=prefix,
        verbose=0,
        destination='emperor/support_files',
        **({'user': user} if version_info >= (3, 0, 0, '') else {})
    )


def preprocess_coords_file(coords_header, coords_data, coords_eigenvals,
                           coords_pct, mapping_header, mapping_data,
                           custom_axes=None, jackknifing_method=None,
                           is_comparison=False,
                           pct_variation_below_one=False):
    """Process a PCoA data and handle customizations in the contents

    This controller function handles any customization that has to be done to
    the PCoA data prior to the formatting. Note that the first element in each
    list (coords, headers, eigenvalues & percents) will be considered the
    master set of coordinates.

    Parameters
    ----------
    coords_header: 1d or 2d array of str
        If 1d array of str, the sample identifiers in the PCoA file
        If 2d array of str, the sample identifiers for each coordinate
        file (if jackknifing or comparing plots)
    coords_data: 2d array of float or list of 2d array of float
        If 2d array of float, matrix of coordinates in the PCoA file
        If list of 2d array of float,  with coordinates for each file
        (if jackknifing or comparing plots)
    coords_eigenvals: 1d or 2d array of float
        If 1d array, eigenvalues for the coordinates file
        If 2d array, list of  arrays with the eigenvalues
        (if jackknifing or comparing plots)
    coords_pct: 1d or 2d array of float
        If 1d array, the percent explained by each principal coordinates axis
        If 2d array, a list of lists with numpy arrays (if jackknifing or
        comparing plots)
    mapping_header: list of str
        mapping file headers names
    mapping_data: list of lists of str
        mapping file data
    custom_axes: str, optional
        name of the mapping data fields to add to coords_data. Default: None
    jackknifing_method: {'sdev', 'IRQ', None}, optional
        For more info see qiime.util.summarize_pcoas. Default: None
    is_comparison: bool, optional
        whether or not the inputs should be considered as the ones for a
        comparison plot. Default: false
    pct_variation_below_one: bool, optional
        boolean to allow percet variation of the axes be under one.
        Default: false

    Returns
    -------
    coords_header: list of str
        Sample identifiers in the PCoA file
    coords_data: 2d array of float
        matrix of coordinates in the PCoA file with custom_axes if provided
    coords_eigenvals: array of float
        either the eigenvalues of the input coordinates or the average
        eigenvalues of the multiple coords that were passed in
    coords_pct: array of float
        list of percents explained by each axis as given by the master
        coordinates i. e. the center around where the values revolve
    coords_low: 2d array of float
        coordinates representing the lower edges of an ellipse; None if no
        jackknifing is applied
    coords_high: 2d array of float
        coordinates representing the highere edges of an ellipse; None if no
        jackknifing is applied
    clones: int
        total number of input files

    Raises
    ------
    AssertionError
        if a comparison plot is requested but a list of data is not passed
        as input
    """

    # prevent obscure and obfuscated errors
    if is_comparison:
        assert type(coords_data) == list, ("Cannot process a comparison with "
                                           "the data from a single "
                                           "coordinates file")

    mapping_file = [mapping_header] + mapping_data
    coords_file = [coords_header, coords_data]

    # number PCoA files; zero for any case except for comparison plots
    clones = 0

    if custom_axes and type(coords_data) == np.ndarray:
        # sequence ported from qiime/scripts/make_3d_plots.py @ 9115351
        get_custom_coords(custom_axes, mapping_file, coords_file)
        remove_nans(coords_file)
        scale_custom_coords(custom_axes, coords_file)
    elif type(coords_data) == list and not is_comparison:
        # take the first pcoa file as the master set of coordinates
        master_pcoa = [coords_header[0], coords_data[0],
                       coords_eigenvals[0], coords_pct[0]]

        # support pcoas must be a list of lists where each list contain
        # all the elements that compose a coordinates file
        support_pcoas = [[h, d, e, p] for h, d, e, p in zip(coords_header,
                         coords_data, coords_eigenvals, coords_pct)]

        # do not apply procrustes, at least not for now
        coords_data, coords_low, coords_high, eigenvalues_average,\
            identifiers = summarize_pcoas(master_pcoa, support_pcoas,
                                          method=jackknifing_method,
                                          apply_procrustes=False)

        # custom axes and jackknifing is a tricky thing to do, you only have to
        # add the custom values to the master file which is represented as the
        # coords_data return value. Since there is really no variation in that
        # axis then you have to change the values of coords_high and of
        # coords_low to something really small so that WebGL work properly
        if custom_axes:
            coords_file = [master_pcoa[0], coords_data]
            get_custom_coords(custom_axes, mapping_file, coords_file)
            remove_nans(coords_file)
            scale_custom_coords(custom_axes, coords_file)

            # this opens support for as many custom axes as needed
            axes = len(custom_axes)

            coords_low = np.hstack([np.zeros((coords_low.shape[0], axes)),
                                    coords_low])
            coords_high = np.hstack([np.full((coords_low.shape[0], axes),
                                             fill_value=0.00001),
                                     coords_high])

            coords_data = coords_file[1]

        if master_pcoa[3][0] < 1.0 and not pct_variation_below_one:
            master_pcoa[3] = master_pcoa[3]*100

        # return a value containing coords_low and coords_high
        return identifiers, coords_data, eigenvalues_average, master_pcoa[3],\
            coords_low, coords_high, clones
    # comparison plots are processed almost individually
    elif type(coords_data) == list and is_comparison:

        # indicates the number of files that were totally processed so other
        # functions/APIs are aware of how many times to replicate the metadata
        clones = len(coords_data)
        out_headers, out_coords = [], []

        for index in range(0, clones):
            headers_i = coords_header[index]
            coords_i = coords_data[index]

            # tag each header with the the number in which those coords came in
            out_headers.extend([element+'_%d' % index for element in
                                headers_i])

            if index == 0:
                # numpy can only stack things if they have the same shape
                out_coords = coords_i

                # the eigenvalues and percents explained are really the ones
                # belonging to the the first set of coordinates that was passed
                coords_eigenvals = coords_eigenvals[index]
                coords_pct = coords_pct[index]
            else:
                out_coords = np.vstack((out_coords, coords_i))

        coords_file = [out_headers, out_coords]

        if custom_axes:
            # sequence ported from qiime/scripts/make_3d_plots.py @ 9115351
            get_custom_coords(custom_axes, mapping_file, coords_file)
            remove_nans(coords_file)
            scale_custom_coords(custom_axes, coords_file)

    if coords_pct[0] < 1.0 and not pct_variation_below_one:
        coords_pct = coords_pct*100

    # if no coords summary is applied, return None in the corresponding values
    # note that the value of clones will be != 0 for a comparison plot
    return coords_file[0], coords_file[1], coords_eigenvals, coords_pct, None,\
        None, clones


def validate_and_process_custom_axes(mf, custom_axes):
    """Validate and process mapping file for custom axes

    Parameters
    ----------
    mf : pd.DataFrame
        The sample metadata.
    custom_axes : list of str
        The custom axes to extract from the metadata.

    Returns
    -------
    pd.DataFrame
        A resulting DataFrame with the custom axes as numeric types.

    Raises
    ------
    KeyError
        When the category names in `custom_axes` are not present in `mf`.
    ValueError
        When there are non-numeric values in the categories selected by
        `custom_axes`.
    """
    # avoid side-effects
    mf = mf.copy()

    headers = [mf.index.name] + mf.columns.tolist()
    missing_headers = set(custom_axes).difference(set(headers))

    if missing_headers:
        raise KeyError("One or more custom axes headers are not present in the"
                       " sample information: %s" % ', '.join(missing_headers))

    for axis in custom_axes:
        temp = pd.to_numeric(mf[axis], errors='coerce')
        nans = np.isnan(temp)

        if np.any(nans):
            # summarize the values that were not converted into a float
            summary = mf[nans][axis].value_counts(dropna=False).to_string()
            raise ValueError("All values in a custom axis must be numeric, "
                             "this summary shows the invalid values and the "
                             "number of times they were found in column '%s':"
                             "\n%s" % (axis, summary))

        mf[axis] = temp

    return mf


def resolve_stable_url(version, base_url):
    """Resolve a stable URL for release versions of Emperor

    If the plot is produced using a release version of Emperor, then we
    point the URL to the release version, otherwise we point to the
    development version of Emperor.

    Parameters
    ----------
    version : str
        Current version of emperor.
    base_url : str
        The URL where we pull resources from.

    Returns
    -------
    str
        A URL that points to the emperor's resources.

    Notes
    -----
    An EmperorWarning is shown when development URLs are used.
    """
    if 'dev' in version:
        warnings.warn("Plots generated with `remote=True` using a development "
                      "version of Emperor, may fail to load in the future "
                      "(only the logo may be displayed instead of the plot). "
                      "To avoid this, use a release version of Emperor.",
                      EmperorWarning)

        # this will need to be fixed when new-api is merged to master
        return base_url % 'new-api'
    else:
        # version names are changed for git tags from betaxx to -beta.xx
        if 'b' in version:
            version = version.replace('b', '-beta.')
        return base_url % version
