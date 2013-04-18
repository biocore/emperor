#!/usr/bin/env python
# File created on 14 Apr 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2011, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

from numpy import argsort

from qiime.biplots import (get_taxa_prevalence, get_taxa_coords,
    make_biplot_scores_output)

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
                        coords_data, N=0, sample_ids=None):
    """Preprocess the OTU table to to generate the required data for the biplots

    Input:
    otu_sample_ids: sample identifiers for the otu_table
    otu_table: contingency table
    lineages: taxonomic assignments for the OTUs in the otu_table
    coords_data: principal coordinates data where the taxa will be mapped
    N: number of most prevalent taxa to keep, by default will use all
    sample_ids: sample identifiers to keep from the OTU table, if None is passed
    then all sample ids will be used

    Output:
    otu_coords: coordinates representing the N most prevalent taxa in otu_table
    otu_table: N most prevalent OTUs from the input otu_table
    otu_lineages: taxonomic assignments corresponding to the N most prevalent
    OTUs
    otu_prevalence: vector with the prevalence scores of the N highest values
    lines: coords where the N most prevalent taxa will be positioned in the
    biplot
    """

    # keep only the sample ids as suggested by the input argument
    if sample_ids:
        indices = [otu_sample_ids.index(sample_id) for sample_id in sample_ids]
        otu_table = otu_table[:,indices]

    # retrieve the prevalence and the coords prior the filtering
    prevalence = get_taxa_prevalence(otu_table)
    bi_plot_coords = get_taxa_coords(otu_table, coords_data)

    o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence =\
        extract_taxa_data(coords_data, otu_table, lineages, prevalence, N)

    lines = '\n'.join(make_biplot_scores_output({'coord': o_otu_coords,
        'lineages': o_otu_lineages}))

    return o_otu_coords, o_otu_table, o_otu_lineages, o_prevalence, lines
