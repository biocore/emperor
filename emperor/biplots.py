#!/usr/bin/env python
# File created on 14 Apr 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "0.9.51"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Release"

from numpy import argsort, array

from emperor.util import EmperorUnsupportedComputation
from emperor.sort import sort_taxa_table_by_pcoa_coords
from emperor.qiime_backports.biplots import (get_taxa_prevalence,
    get_taxa_coords, make_biplot_scores_output)

def extract_taxa_data(otu_coords, otu_table, lineages, prevalence, N=0):
    """Extrac the N most prevalent elements according to a prevalence vector

    Inputs:
    otu_coords: coordinates where specific taxa is centered
    otu_table: contingency table
    lineages: taxonomic assignments for each row in the otu_table
    prevalence: vector with prevalnce from 0 to 1 for each row of the otu_table
    as returned from qiime.biplots.get_taxa_prevalence
    N: number of most prevalent elements to retain, if zero is passed, will
    reatain all available

    Outputs:
    otu_coords: N most prevalent coords
    out_otu_table: N most prevalent rows of the otu_table
    out_otu_lineages: N most prevalent taxonomic assignments for each row of the
    otu_table
    out_prevalence: first N values of prevalence

    Based on qiime.biplots.remove_rare_taxa; though this function opperates on
    generic data that's not in dict forma and returns the appropriate result.
    """
    # If less than zero or greater than length of taxa, N = fix to max
    if N<=0 or N>len(prevalence):
        N = len(prevalence)

    # get the first N indices to keep from all of the taxa data
    indices = argsort(prevalence)
    indices = indices[::-1][:N]

    # remove the indices that are not needed and return them individually
    out_otu_coords = otu_coords[indices, :]
    out_otu_table = otu_table[indices, :]
    out_otu_lineages = [lineages[index] for index in indices]
    out_prevalence = prevalence[indices]

    return out_otu_coords, out_otu_table, out_otu_lineages, out_prevalence

def preprocess_otu_table(otu_sample_ids, otu_table, lineages,
                        coords_data, coords_headers, N=0):
    """Preprocess the OTU table to to generate the required data for the biplots

    Input:
    otu_sample_ids: sample identifiers for the otu_table
    otu_table: contingency table
    lineages: taxonomic assignments for the OTUs in the otu_table
    coords_data: principal coordinates data where the taxa will be mapped
    N: number of most prevalent taxa to keep, by default will use all

    Output:
    otu_coords: coordinates representing the N most prevalent taxa in otu_table
    otu_table: N most prevalent OTUs from the input otu_table
    otu_lineages: taxonomic assignments corresponding to the N most prevalent
    OTUs
    otu_prevalence: vector with the prevalence scores of the N highest values
    lines: coords where the N most prevalent taxa will be positioned in the
    biplot
    """

    # return empty values if any of the taxa data is empty
    if (otu_sample_ids == []) or (otu_table == array([])) or (lineages == []):
        return [], [], [], [], ''

    # this means there's only one or fewer rows in the contingency table
    if len(otu_table) <= 1 or len(lineages) <= 1:
        raise EmperorUnsupportedComputation, "Biplots are not supported for "+\
            "contingency tables with one or fewer rows"

    # if this element is a list take the first headers and coordinates
    # both of these will be the master coordinates, i. e. where data is centered
    if type(coords_data) == list and type(coords_headers) == list:
        coords_data = coords_data[0]
        coords_headers = coords_headers[0]

    # re-arrange the otu table so it matches the order of the samples in the
    # coordinates data & remove any sample that is not in the coordinates header
    otu_sample_ids, otu_table = sort_taxa_table_by_pcoa_coords(coords_headers,
        otu_table, otu_sample_ids)

    # retrieve the prevalence and the coords prior the filtering
    prevalence = get_taxa_prevalence(otu_table)
    bi_plot_coords = get_taxa_coords(otu_table, coords_data)

    o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence =\
        extract_taxa_data(bi_plot_coords, otu_table, lineages, prevalence, N)

    lines = '\n'.join(make_biplot_scores_output({'coord': o_otu_coords,
        'lineages': o_otu_lineages}))

    return o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence, lines
