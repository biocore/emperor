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

from qiime.util import qiime_system_call, create_dir

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

def process_mapping_file(data, header, valid_columns):
    """Remove non-valid and non-useful columns in the mapping file

    Inputs:
    data: full mapping file data
    header: column names of the metadata mapping file
    valid_columns: list of valid columns

    Outputs:
    data: contents of the mapping file data that meet all the criteria
    specified in the input arguments; a list of lists
    header: complementary to data, a list of the columns that met the criteria
    specified in the input arguments

    Removes any column that has data unique for each of the fields.
    """

    final_header = [header[0]]
    final_mapping_data = [[col[0]] for col in data]

    len_header = len(header)
    for i in range(1,len_header-1):
        # validating existence of column 
        if header[i] not in valid_columns:
            continue

        # validating that the column values are not unique per sample or the
        # same for all of them
        unique_columns = len(set([col[i] for col in data]))
        if unique_columns!=len_header and unique_columns!=1:
            final_header.append(header[i])
            [final_mapping_data[j].append(col[i]) for j,col in enumerate(data)]

    return final_mapping_data, final_header
