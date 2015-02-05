#!/usr/bin/env python
# File created on 25 Jan 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza", "Antonio Gonzalez Pena"]
__license__ = "BSD"
__version__ = "0.9.51"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Release"


from numpy import ndarray, array, ones, zeros, vstack
from string import strip

from os import makedirs
from os.path import abspath, dirname, join, exists
from copy import deepcopy

from qcli.util import qcli_system_call

from emperor.qiime_backports.format import format_mapping_file
from emperor.qiime_backports.filter import filter_mapping_file
from emperor.qiime_backports.make_3d_plots import (get_custom_coords,
    remove_nans, scale_custom_coords)
from emperor.qiime_backports.parse import (mapping_file_to_dict,
    parse_metadata_state_descriptions)
from emperor.qiime_backports.util import (MetadataMap, is_valid_git_refname,
    is_valid_git_sha1, summarize_pcoas)

from emperor import __version__ as emperor_library_version

class EmperorSupportFilesError(IOError):
    """Exception for missing support files"""
    pass

class EmperorInputFilesError(IOError):
    """Exception for missing support files"""
    pass

class EmperorUnsupportedComputation(ValueError):
    """Exception for computations that lack a meaning"""
    pass

# Based on qiime/qiime/util.py
def get_emperor_library_version():
    """Get Emperor version and the git SHA + current branch (if applicable)"""
    emperor_dir = get_emperor_project_dir()
    emperor_version = emperor_library_version

    # more information could be retrieved following this pattern
    sha_cmd = 'git --git-dir %s/.git rev-parse HEAD' % (emperor_dir)
    sha_o, sha_e, sha_r = qcli_system_call(sha_cmd)
    git_sha = sha_o.strip()

    branch_cmd = 'git --git-dir %s/.git rev-parse --abbrev-ref HEAD' %\
        (emperor_dir)
    branch_o, branch_e, branch_r = qcli_system_call(branch_cmd)
    git_branch = branch_o.strip()

    # validate the output from both command calls
    if is_valid_git_refname(git_branch) and is_valid_git_sha1(git_sha):
        return '%s, %s@%s' % (emperor_version, git_branch, git_sha[0:7])
    else:
        return '%s' % emperor_version

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

    if not exists(file_path):
        makedirs(file_path)

    # shutil.copytree does not provide an easy way to copy the contents of a
    # directory into another existing directory, hence the system call.
    # use double quotes for the paths to escape any invalid chracter(s)/spaces
    cmd = 'cp -R "%s/"* "%s"' % (get_emperor_support_files_dir(),
        abspath(file_path))
    cmd_o, cmd_e, cmd_r = qcli_system_call(cmd)

    if cmd_e:
        raise EmperorSupportFilesError, "Error found whilst trying to copy " +\
            "the support files:\n%s\n Could not execute: %s" % (cmd_e, cmd)

    return

def preprocess_mapping_file(data, headers, columns, unique=False, single=False,
                            clones=0):
    """Process a mapping file to expand the data or remove unuseful fields

    Inputs:
    data: mapping file data
    headers: mapping file headers
    columns: list of headers to keep, if one of these headers includes two
    ampersands, this function will create a new column by merging the delimited
    columns.
    unique: keep columns where all values are unique
    single: keep columns where all values are the same
    clones: number of times to replicate the metadata

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
            f_unique = lambda x: metadata.hasUniqueCategoryValues(x) and\
                                 x not in columns
            f_single = lambda x: metadata.hasSingleCategoryValue(x) and\
                                 x not in columns

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
            columns_to_remove, negate=True)
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

    # clones mean: replicate the metadata retagging the sample ids with a suffix
    if clones:
        out_data = []
        for index in range(0, clones):
            out_data.extend([[element[0]+'_%d' % index]+element[1::]
                for element in data])
        data = out_data

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
                        custom_axes=None, jackknifing_method=None,
                        is_comparison=False,
                        pct_variation_below_one=False):
    """Process a PCoA data and handle customizations in the contents

    Inputs:
    coords_header: list of sample identifiers in the PCoA file _or_ list of
    lists with sample identifiers for each coordinate file (if jackknifing or
    comparing plots)
    coords_data: matrix of coordinates in the PCoA file _or_ list of numpy
    arrays with coordinates for each file (if jackknifing or comparing plots)
    coords_eigenvals: numpy array with eigenvalues for the coordinates file _or_
    list of numpy arrays with the eigenvalues (if jackknifing or comparing plots
    )
    coords_pct: numpy array with a the percent explained by each principal
    coordinates axis _or_ a list of lists with numpy arrays (if jackknifing or
    comparing plots)
    mapping_header: mapping file headers names
    mapping_data: mapping file data
    custom_axes: name of the mapping data fields to add to coords_data
    jackknifing_method: one of 'sdev' or 'IRQ', defaults to None, for more info
    see qiime.util.summarize_pcoas
    is_comparison: whether or not the inputs should be considered as the ones
    for a comparison plot
    pct_variation_below_one: boolean to allow percet variation of the axes
    be under one

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
    clones: total number of input files

    This controller function handles any customization that has to be done to
    the PCoA data prior to the formatting. Note that the first element in each
    list (coords, headers, eigenvalues & percents) will be considered the master
    set of coordinates.

    Raises: AssertionError if a comparison plot is requested but a list of data
    is not passed as input
    """

    # prevent obscure and obfuscated errors
    if is_comparison:
        assert type(coords_data) == list, "Cannot process a comparison with "+\
            "the data from a single coordinates file"

    mapping_file = [mapping_header] + mapping_data
    coords_file = [coords_header, coords_data]

    # number PCoA files; zero for any case except for comparison plots
    clones = 0

    if custom_axes and type(coords_data) == ndarray:
            # sequence ported from qiime/scripts/make_3d_plots.py @ 9115351
            get_custom_coords(custom_axes, mapping_file, coords_file)
            remove_nans(coords_file)
            scale_custom_coords(custom_axes, coords_file)
    elif type(coords_data) == list and is_comparison == False:
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
                method=jackknifing_method, apply_procrustes=False)

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

        if master_pcoa[3][0]<1.0 and not pct_variation_below_one:
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
            out_headers.extend([element+'_%d' % index for element in headers_i])

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
            # axes to be added into the original coordinates, we have to add the
            # suffix for the sample identifiers that the coordinates have
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

    if coords_pct[0]<1.0 and not pct_variation_below_one:
        coords_pct = coords_pct*100

    # if no coords summary is applied, return None in the corresponding values
    # note that the value of clones will be != 0 for a comparison plot
    return coords_file[0], coords_file[1], coords_eigenvals, coords_pct, None,\
        None, clones

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
            or
            Category:ColumnToSearch==ValueWithinTheColumnToSearch=ValueToFill
    criteria: function that takes a value and returns true or false, default is
    to check if the inputed value is numeric or not.

    Output:
    data: Filled in mapping file data

    """
    out_data = deepcopy(data)

    # parsing the input values
    values = map(strip, values.split(';'))
    values_dict = {}
    for v in values:
        colname, vals = map(strip, v.split(':', 1))
        vals = map(strip, vals.split(','))
        assert len(vals)==1,  "You can only pass 1 replacement value: %s" % vals
        if colname not in values_dict:
            values_dict[colname] = []
        values_dict[colname].extend(vals)

    for key, v in values_dict.items():
        for value in v:
            # variable that is going to contain the name of the column for multiple
            # subtitutions
            column = None
            # variable to control if the values with in a column exist
            used_column_index = False

            try:
                header_index = headers.index(key)
            except ValueError:
                raise EmperorInputFilesError, ("The header %s does not exist in the "
                    "mapping file" % key)

            # for the special case of multiple entries
            if '==' in value and '=' in value:
                arrow_index = value.index('==')
                equal_index = value.rindex('=')
                assert ((arrow_index+2)!=equal_index and (arrow_index+1)!=equal_index), \
                    "Not properly formatted: %s" % value

                column = value[:arrow_index]
                column_value = value[arrow_index+2:equal_index]
                new_value = value[equal_index+1:]

                try:
                    column_index = headers.index(column)
                except ValueError:
                    raise EmperorInputFilesError, ("The header %s does not exist in the "
                        "mapping file" % column)

            # fill in the data
            fill_the_data = False
            for line in out_data:
                if criteria(line[header_index]) == False:
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
                raise EmperorInputFilesError, ("This value '%s' doesn't exist in '%s' or "
                "it wasn't used in for processing" % (column_value, column))

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

