# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from numpy import ndarray, ones, zeros, vstack

from os import listdir
from os.path import abspath, dirname, join, isdir
from copy import deepcopy

from emperor.qiime_backports.make_3d_plots import (get_custom_coords,
                                                   remove_nans,
                                                   scale_custom_coords)
from emperor.qiime_backports.parse import mapping_file_to_dict
from emperor.qiime_backports.util import MetadataMap, summarize_pcoas


class EmperorSupportFilesError(IOError):
    """Exception for missing support files"""
    pass


class EmperorInputFilesError(IOError):
    """Exception for missing support files"""
    pass


class EmperorUnsupportedComputation(ValueError):
    """Exception for computations that lack a meaning"""
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


def preprocess_mapping_file(data, headers, columns, unique=False, single=False,
                            clones=0):
    """Process a mapping file to expand the data or remove unuseful fields

    Parameters
    ----------
    data: list of list of str
        mapping file data
    headers: list of str
        mapping file headers
    columns: list of str
        headers to keep, if one of these headers includes two ampersands,
        this function will create a new column by merging the delimited columns
    unique: bool, optional
        keep columns where all values are unique. Default: false.
    single: bool, optional
        keep columns where all values are the same. Default: false
    clones: int, optional
        number of times to replicate the metadata. Default: 0

    Returns
    -------
    data: list of list of str
        processed mapping file data
    headers: list of str
        processed mapping file headers
    """

    # The sample ID must always be there, else it's meaningless data
    if 'SampleID' != columns[0]:
        columns = ['SampleID'] + columns

    # process concatenated columns if needed
    merge = []
    for column in columns:
        # the list can contain None so check "if column" before treating as str
        if column and '&&' in column:
            merge.append(column)
    # each element needs several columns to be merged
    for new_column in merge:
        indices = [headers.index(header_name) for header_name in
                   new_column.split('&&')]

        # join all the fields of the metadata that are listed in indices
        for line in data:
            line.append(''.join([line[index] for index in indices]))
        headers.append(new_column)

    # remove all unique or singled valued columns that are not included in
    # the list of categories that should be kept i. e. columns
    if unique or single:
        columns_to_remove = []
        metadata = MetadataMap(mapping_file_to_dict(data, headers), [])

        # the --coloy_by option in the script interface allows the user to
        # specify the categories you want to use in the generated plot, this
        # the default behaviour is to color by all categories that are not
        # unique. If the user specifies a category with with the --color_by
        # option and this category contains a unique values, this category must
        # still be added thus the structure of the next few lines that
        # form the structure for the two different routes. (1) where no value
        # is specified in the CLI (the value of columns will be [None, x1, x2,
        # x3] where x{1,2,3} are categories requested in other CLI options) and
        # (2) where a value is specified in the CLI.
        #
        # TL;DR
        # see https://github.com/biocore/emperor/issues/271
        if None in columns:
            columns = headers[:]
            f_unique = metadata.hasUniqueCategoryValues
            f_single = metadata.hasSingleCategoryValue
        else:
            def f_unique(x):
                return metadata.hasUniqueCategoryValues(x) and x not in columns

            def f_single(x):
                return metadata.hasSingleCategoryValue(x) and x not in columns

        # find columns that have values that are all unique
        if unique:
            for c in headers[1::]:
                if f_unique(c):
                    columns_to_remove.append(c)
        # remove categories where there is only one value
        if single:
            for c in headers[1::]:
                if f_single(c):
                    columns_to_remove.append(c)
        columns_to_remove = list(set(columns_to_remove))

        # remove the single or unique columns
        data, headers = keep_columns_from_mapping_file(data, headers,
                                                       columns_to_remove,
                                                       negate=True)
    else:
        # when a None is contained in columns, we imply we want to use all the
        # available categories in the mapping file, thus just overwrite the
        # value
        if None in columns:
            columns = headers[:]

    # remove anything not specified in the input
    data, headers = keep_columns_from_mapping_file(data, headers, columns)

    # sanitize the mapping file data and headers
    data, headers = sanitize_mapping_file(data, headers)

    # clones mean: replicate the metadata retagging the sample ids with a
    # suffix
    if clones:
        out_data = []
        for index in range(0, clones):
            out_data.extend([[element[0]+'_%d' % index]+element[1::]
                             for element in data])
        data = out_data

    return data, headers


def keep_columns_from_mapping_file(data, headers, columns, negate=False):
    """Select the header names to remove/keep from the mapping file

    Parameters
    ----------
    data: list of list of str
        mapping file data
    headers: list of str
        mapping file headers names
    columns: list of str
        header names to keep/remove, see negate
    negate: bool, optional
        False will _keep_ the listed columns; True will _remove_ them.
        Default: False

    Returns
    -------
    data: list of list of str
        filtered mapping file data
    headers: list of str
        filtered mapping file headers
    """
    data = deepcopy(data)
    headers = deepcopy(headers)

    if negate:
        indices_of_interest = list(range(0, len(headers)))
    else:
        indices_of_interest = []

    # get the indices that you want to keep; either by removing the
    # indices listed (negate is True) or by adding them (negate is False)
    for column in columns:
        try:
            if negate:
                del indices_of_interest[indices_of_interest.index(
                    headers.index(column))]
            else:
                indices_of_interest.append(headers.index(column))
        except ValueError:
            continue

    # keep the elements at the positions indices
    def keep_elements(elements, indices):
        return [element for i, element in enumerate(elements) if i in indices]

    headers = keep_elements(headers, indices_of_interest)
    data = [keep_elements(row, indices_of_interest) for row in data]

    return data, headers


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

    if custom_axes and type(coords_data) == ndarray:
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
            coords_low[:, 0:axes] = zeros([coords_low.shape[0], axes])
            coords_high[:, 0:axes] = ones([coords_high.shape[0], axes])*0.00001
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
                out_coords = vstack((out_coords, coords_i))

        coords_file = [out_headers, out_coords]

        if custom_axes:
            # this condition deals with the fact that in order for the custom
            # axes to be added into the original coordinates, we have to add
            # the suffix for the sample identifiers that the coordinates have
            if clones:
                out_data = []
                for index in range(0, clones):
                    out_data.extend([[element[0]+'_%d' % index]+element[1::]
                                     for element in mapping_data])
                mapping_file = [mapping_header] + out_data

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


def _is_numeric(x):
    """Return true if x is a numeric value, return false else

    Parameters
    ----------
    x : str
        string to test whether something is or not a number

    Returns
    -------
    bool
        whether something is or not a number
    """
    try:
        float(x)
    except:
        return False
    return True


def fill_mapping_field_from_mapping_file(data, headers, values,
                                         criteria=_is_numeric):
    """
    Parameters
    ----------
    data : list of list of str
        mapping file data
    headers : list of str
        mapping file headers
    values : str
        string with the format a format of
        Category:ValueToFill;Category:ValueToFill ...
        or
        Category:ColumnToSearch==ValueWithinTheColumnToSearch=ValueToFill
    criteria : function, optional
        function that takes a value and returns true or false, default is
        to check if the inputed value is numeric or not (_is_numeric).

    Returns
    -------
    data: list of list of str
        Filled in mapping file data

    Raises
    ------
    EmperorInputFilesError
        If a header is not found in the mapping file or it wasn't used for
        processing.
    """
    out_data = deepcopy(data)

    # parsing the input values
    values = [val.strip() for val in values.split(';')]
    values_dict = {}
    for v in values:
        colname, vals = [val for val in v.split(':', 1)]
        vals = [val.strip() for val in vals.split(',')]
        assert len(vals) == 1, ("You can only pass 1 replacement value:"
                                " {}".format(vals))
        if colname not in values_dict:
            values_dict[colname] = []
        values_dict[colname].extend(vals)

    for key, v in values_dict.items():
        for value in v:
            # variable that is going to contain the name of the column for
            # multiple subtitutions
            column = None
            # variable to control if the values with in a column exist
            used_column_index = False

            try:
                header_index = headers.index(key)
            except ValueError:
                raise EmperorInputFilesError(
                    "The header {} does not exist in the mapping "
                    "file".format(key))

            # for the special case of multiple entries
            if '==' in value and '=' in value:
                arrow_index = value.index('==')
                equal_index = value.rindex('=')
                assert(arrow_index+2) != equal_index and\
                      (arrow_index+1) != equal_index,\
                    "Not properly formatted: {}".format(value)

                column = value[:arrow_index]
                column_value = value[arrow_index+2:equal_index]
                new_value = value[equal_index+1:]

                try:
                    column_index = headers.index(column)
                except ValueError:
                    raise EmperorInputFilesError(
                        "The header {} does not exist in the mapping "
                        "file".format(column))

            # fill in the data
            fill_the_data = False
            for line in out_data:
                if criteria(line[header_index]) is False:
                    if not column:
                        line[header_index] = value
                        used_column_index = True
                        fill_the_data = True
                    else:
                        if line[column_index] == column_value:
                            line[header_index] = new_value
                            used_column_index = True
                            fill_the_data = True

            if not used_column_index and fill_the_data:
                raise EmperorInputFilesError(
                    "This value '{}' does not exist in '{}' or it wasn't used "
                    "forprocessing".format(column_value, column))

    return out_data


def sanitize_mapping_file(data, headers):
    """Clean the strings in the mapping file for use with javascript

    This function will remove all the ocurrences of characters like ' or ".

    Parameters
    ----------
    data : list of lists of str
        the mapping file data
    headers : list of str
        the mapping file headers

    Returns
    -------
    s_data : list of lists of str
        sanitized version of the input mapping file data
    s_headers : list of str
        sanitized version of the input mapping file headers
    """
    all_lines = [headers] + data
    out_lines = []

    # replace single and double quotes with escaped versions of them
    for line in all_lines:
        out_lines.append([element.replace("'", "").replace('"', '')
                          for element in line])

    return out_lines[1::], out_lines[0]


def guess_coordinates_files(dir_path):
    """Given a directory return the file paths that can contain coordinates

    Parameters
    ----------
    dir_path : str
        path to the directory where coordinate files are contained

    Returns
    -------
    list of str
        list of filepaths pointing to the coordinates files

    Notes
    -----
    If a path inside dir_path meets any of the following criteria, it will be
    ignored:
    - Is a hidden file
    - Is named `Icon?`.
    - Is folder
    - Is part of the procrustes results from QIIME, see
      transform_coordinate_matrices.py
    """
    coord_fps = []

    for filepath in listdir(dir_path):
        if filepath.startswith('.'):
            continue
        if filepath.startswith('Icon?'):
            continue

        # we need the full path for the next check
        filepath = join(abspath(dir_path), filepath)

        if isdir(filepath):
            continue
        if filepath.endswith('procrustes_results.txt'):
            continue

        coord_fps.append(filepath)

    return coord_fps
