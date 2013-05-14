#!/usr/bin/env python
# File created on 25 Jan 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza", "Antonio Gonzalez Pena"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from numpy import ndarray, array, ones, zeros

from os.path import abspath, dirname, join, exists

from copy import deepcopy
from qiime.format import format_mapping_file
from qiime.filter import filter_mapping_file
from qiime.parse import mapping_file_to_dict, parse_metadata_state_descriptions
from qiime.util import (qiime_system_call, create_dir, MetadataMap,
    summarize_pcoas)
from qiime.make_3d_plots import (get_custom_coords, remove_nans,
    scale_custom_coords)

class EmperorSupportFilesError(IOError):
    """Exception for missing support files"""
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

def copy_support_files(file_path):
    """Copy the support files to a named destination 

    file_path: path where you want the support files to be copied to

    Will raise EmperorSupportFilesError if a problem is found whilst trying to
    copy the files.
    """
    file_path = join(file_path, 'emperor_required_resources')

    if exists(file_path) == False:
        create_dir(file_path, False)

    # shutil.copytree does not provide an easy way to copy the contents of a
    # directory into another existing directory, hence the system call.
    # use double quotes for the paths to escape any invalid chracter(s)/spaces
    cmd = 'cp -R "%s/"* "%s"' % (get_emperor_support_files_dir(),
        abspath(file_path))
    cmd_o, cmd_e, cmd_r = qiime_system_call(cmd)

    if cmd_e:
        raise EmperorSupportFilesError, "Error found whilst trying to copy " +\
            "the support files:\n%s\n Could not execute: %s" % (cmd_e, cmd)

    return

def preprocess_mapping_file(data, headers, columns, unique=False, single=False):
    """Process a mapping file to expand the data or remove unuseful fields

    Inputs:
    data: mapping file data
    headers: mapping file headers
    columns: list of headers to keep, if one of these headers includes two
    ampersands, this function will create a new column by merging the delimited
    columns.
    unique: keep columns where all values are unique
    single: keep columns where all values are the same

    Outputs:
    data: processed mapping file data
    headers: processed mapping file headers
    """

    # The sample ID must always be there, else it's meaningless data
    if 'SampleID' != columns[0]:
        columns = ['SampleID'] + columns

    # process concatenated columns if needed
    merge = []
    for column in columns:
        if '&&' in column:
            merge.append(column)
    # each element needs several columns to be merged
    for new_column in merge:
        indices = [headers.index(header_name) for header_name in
            new_column.split('&&')]

        # join all the fields of the metadata that are listed in indices
        for line in data:
            line.append(''.join([element for i, element in enumerate(line)
                if i in indices]))
        headers.append(new_column)

    # remove all unique or singled valued columns
    if unique or single:
        columns_to_remove = []
        metadata = MetadataMap(mapping_file_to_dict(data, headers), [])

        # find columns that have values that are all unique
        if unique == True:
            columns_to_remove += [column_name for column_name in headers[1::]
                if metadata.hasUniqueCategoryValues(column_name)]

        # remove categories where there is only one value
        if single == True:
            columns_to_remove += [column_name for column_name in headers[1::]
                if metadata.hasSingleCategoryValue(column_name)]
        columns_to_remove = list(set(columns_to_remove))

        # remove the single or unique columns
        data, headers = keep_columns_from_mapping_file(data, headers,
            columns_to_remove, negate=True)

    # remove anything not specified in the input
    data, headers = keep_columns_from_mapping_file(data, headers, columns)

    # sanitize the mapping file data and headers
    data, headers = sanitize_mapping_file(data, headers)

    return data, headers


def keep_columns_from_mapping_file(data, headers, columns, negate=False):
    """Select the header names to remove/keep from the mapping file

    Inputs:
    data: mapping file data
    headers: mapping file headers names
    columns: header names to keep/remove, see negate
    negate: False will _keep_ the listed columns; True will _remove_ them

    Outputs:
    data: filtered mapping file data
    headers: filtered mapping file headers
    """
    data = deepcopy(data)
    headers = deepcopy(headers)

    if negate:
        indices_of_interest = range(0, len(headers))
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
    keep_elements = lambda elements, indices :[element for i, element in
        enumerate(elements) if i in indices]

    headers = keep_elements(headers, indices_of_interest)
    data = [keep_elements(row, indices_of_interest) for row in data]

    return data, headers

def preprocess_coords_file(coords_header, coords_data, coords_eigenvals,
                        coords_pct, mapping_header, mapping_data,
                        custom_axes=None, jackknifing_method=None):
    """Process a PCoA data and handle customizations in the contents

    Inputs:
    coords_header: list of sample identifiers in the PCoA file _or_ list of
    lists with sample identifiers for each coordinate file (if jackknifing)
    coords_data: matrix of coordinates in the PCoA file _or_ list of numpy
    arrays with coordinates for each file (if jackknifing)
    coords_eigenvals: numpy array with eigenvalues for the coordinates file _or_
    list of numpy arrays with the eigenvalues (if jackknifing)
    coords_pct: numpy array with a the percent explained by each principal
    coordinates axis _or_ a list of lists with numpy arrays (if jackknifing)
    mapping_header: mapping file headers names
    mapping_data: mapping file data
    custom_axes: name of the mapping data fields to add to coords_data
    jackknifing_method: one of 'sdev' or 'IRQ', defaults to None, for more info
    see qiime.util.summarize_pcoas

    Outputs:
    coords_header: list of sample identifiers in the PCoA file
    coords_data: matrix of coordinates in the PCoA file with custom_axes if
    provided
    coords_eigenvalues: either the eigenvalues of the input coordinates or the
    average eigenvalues of the multiple coords that were passed in
    coords_pct: list of percents explained by each axis as given by the master
    coordinates i. e. the center around where the values revolve
    coords_low: coordinates representing the lower edges of an ellipse; None if
    no jackknifing is applied
    coords_high: coordinates representing the highere edges of an ellipse; None
    if no jackknifing is applied

    This controller function handles any customization that has to be done to
    the PCoA data prior to the formatting. Note that the first element in each
    list (coords, headers, eigenvalues & percents) will be considered the master
    set of coordinates.
    """
    mapping_file = [mapping_header] + mapping_data
    coords_file = [coords_header, coords_data]

    if custom_axes and type(coords_data) == ndarray:
            # sequence ported from qiime/scripts/make_3d_plots.py @ 9115351
            get_custom_coords(custom_axes, mapping_file, coords_file)
            remove_nans(coords_file)
            scale_custom_coords(custom_axes, coords_file)
    if type(coords_data) == list:
        # take the first pcoa file as the master set of coordinates
        master_pcoa = [coords_header.pop(0), coords_data.pop(0),
            coords_eigenvals.pop(0), coords_pct.pop(0)]

        # support pcoas must be a list of lists where each list contain
        # all the elements that compose a coordinates file
        support_pcoas = [[h, d, e, p] for h, d, e, p in zip(coords_header,
            coords_data, coords_eigenvals, coords_pct)]

        # do not apply procrustes, at least not for now
        coords_data, coords_low, coords_high, eigenvalues_average,\
            identifiers = summarize_pcoas(master_pcoa, support_pcoas,
                method=jackknifing_method, apply_procrustes=False)

        # custom axes an jackknifing is a tricky thing to do, you only have to
        # add the custom values to the master file which is represented as the
        # coords_data return value. Since there is really no variation in that
        # axis then you have to change the values of coords_high and of
        # coords_low to something really small so the WebGL work properly
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

        # return a value containing coords_low and coords_high
        return identifiers, coords_data, eigenvalues_average, master_pcoa[3],\
            coords_low, coords_high,

    # if no coords summary is applied, return None in the correspoinding values
    return coords_file[0], coords_file[1], coords_eigenvals, coords_pct, None,\
        None

def _is_numeric(x):
    """Return true if x is a numeric value, return false else

    Inputs:
    x: string to test whether something is or not a number
    """
    try:
        float(x)
    except:
        return False
    return True

def fill_mapping_field_from_mapping_file(data, headers, values,
                                        criteria=_is_numeric):
    """
    Inputs:
    data: mapping file data
    headers: mapping file headers
    values: string with the format a format of
    Category:ValueToFill;Category:ValueToFill ...
    criteria: function that takes a value and returns true or false, default is
    to check if the inputed value is numeric or not.

    Output:
    data: Filled in mapping file data

    """
    out_data = deepcopy(data)

    # since this is a hack, assert the lengths are made of only one element
    values_dict = parse_metadata_state_descriptions(values)

    for key, value in values_dict.items():
        value = list(value)

        # this function can parse more than one value, but make sure it's only 1
        assert len(value) == 1, ("Missing values cannot be padded with more "
            "than one value. Verify '%s' has a single value." % key)

        # in case the mapping file header is not in the headers
        try:
            header_index = headers.index(key)
        except ValueError:
            raise ValueError,("The header %s does not exist in the mapping file"
                % key)

        # fill in the data
        for line in out_data:
            if criteria(line[header_index]) == False:
                line[header_index] = value[0]

    return out_data

def sanitize_mapping_file(data, headers):
    """Clean the strings in the mapping file for use with javascript

    Inputs:
    data: list of lists with the mapping file data
    headers: list of strings with the mapping file headers

    Outputs:
    s_data: sanitized version of the input mapping file data
    s_headers: sanitized version of the input mapping file headers

    This function will remove all the ocurrences of characters like ' or ".
    """
    all_lines = [headers] + data
    out_lines = []

    # replace single and double quotes with escaped versions of them
    for line in all_lines:
        out_lines.append([element.replace("'","").replace('"','')
            for element in line])

    return out_lines[1::], out_lines[0]
