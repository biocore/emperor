#!/usr/bin/env python
# File created on 25 Jan 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2011, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza", "Antonio Gonzalez Pena"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from os.path import abspath, dirname, join, exists

from copy import deepcopy
from qiime.format import format_mapping_file
from qiime.filter import filter_mapping_file
from qiime.parse import mapping_file_to_dict
from qiime.util import qiime_system_call, create_dir, MetadataMap

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
    # directory into another existing directory, hence the system call
    cmd = 'cp -R %s/* %s' % (get_emperor_support_files_dir(), abspath(file_path))
    cmd_o, cmd_e, cmd_r = qiime_system_call(cmd)

    if cmd_e:
        raise EmperorSupportFilesError, "Error found whilst trying to copy " +\
            "the support files:\n%s\n Could not execute: %s" % cmd_e, cmd

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
