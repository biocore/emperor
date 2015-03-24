# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from numpy import zeros
import re


def sort_taxa_table_by_pcoa_coords(coords_header, otu_table, otu_header):
    """Sort and match the samples in the otu table and in the coordinates data

    This function will sort the columns of an otu table as suggested by the
    sample ids in the coords_header

    Parameters
    ----------
    coords_header: list of str
        sample ids that are present in principal coordinates data
    otu_table: numpy array
        numpy array with the data for an otu table
    otu_header: list of str
        sample ids present in the otu table

    Returns
    -------
    sorted_otu_headers: list of str
        sample ids that were present in the coords_header list, the order in
        this table matches the order of the coordinates data
    sorted_otu_table: numpy array
        otu table data with columns belonging to the sample ids in the
        sorted_otu_headers list
    """

    sorted_otu_headers = []

    # the size of the otu table can be pre-allocated for better memory usage
    matching_headers = len(set(coords_header) & set(otu_header))
    sorted_otu_table = zeros([otu_table.shape[0], matching_headers])

    # iterate through the available sample ids in the coordinates file and work
    # only with the ones that are present in the coords and the otu table; the
    # order of the ids is important hence iterate through the original list
    for i, element in enumerate(coords_header):
        if element in otu_header:
            current_index = otu_header.index(element)
            sorted_otu_table[:, i] = otu_table[:, current_index]
            sorted_otu_headers.append(element)

    return sorted_otu_headers, sorted_otu_table


def sort_comparison_filenames(coord_fps):
    """Pass in a list of file names and sort them using the suffix

    Parameters
    ----------
    coord_fps: list of str
        The filenames with the format something_something_qX.txt where X is
        the index of the file.

    Returns
    -------
    list of str
        A sorted version of the list that was passed in where the strings are
        sorted according to the suffix they have, if the string doesn't have a
        suffix it will be added to the beginning of the list.
    """

    if coord_fps == []:
        return []

    def _get_suffix(fp):
        """Gets the number in the suffix for a string using a regex"""
        # any alphanumeric set of characters proceeded by a 'q', a number,
        # a dot & a txt extension at the end of the line. Take for example
        # bray_curtis_q1.txt or unifrac_q11.txt
        regex = re.compile(r'(\w+)_q([0-9]+).txt$')
        tmatch = re.search(regex, fp)

        try:
            number = tmatch.group(2)
        # if the regex doesn't match then put it at the beginning
        except (IndexError, AttributeError):
            number = -1

        return float(number)

    # the key function retrieves the suffix number for the function to sort
    # according to it's floating point representation i. e. the cast to float
    return sorted(coord_fps, key=_get_suffix)
