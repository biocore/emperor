#!/usr/bin/env python
# File created on 20 Apr 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2011, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "1.6.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"


from numpy import zeros

def sort_taxa_table_by_pcoa_coords(coords_header, otu_table, otu_header):
    """Sort and match the samples in the otu table and in the coordinates data

    Inputs:
    coords_header: sample ids that are present in principal coordinates data
    otu_table: numpy array with the data for an otu table
    otu_header: sample ids present in the otu table

    Ouputs:
    sorted_otu_headers: sample ids that were present in the coords_header list,
    the order in this table matches the order of the coordinates data
    sorted_otu_table: otu table data with columns belonging to the sample ids in
    the sorted_otu_headers list

    This function will sort the columns of an otu table as suggested by the
    sample ids in the coords_header
    """

    sorted_otu_headers = []

    # the size of the otu table can be pre-allocated for better memory usage
    matching_headers = len(set(coords_header)&set(otu_header))
    sorted_otu_table = zeros([otu_table.shape[0], matching_headers])

    # iterate through the available sample ids in the coordinates file and work
    # only with the ones that are present in the coords and the otu table; the
    # order of the ids is important hence iterate through the original list
    for i, element in enumerate(coords_header):
        if element in otu_header:
            current_index = otu_header.index(element)
            sorted_otu_table[:,i] = otu_table[:,current_index]
            sorted_otu_headers.append(element)

    return sorted_otu_headers, sorted_otu_table
