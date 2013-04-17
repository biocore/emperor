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

from qiime.biplots import get_taxa_prevalence, get_taxa_coords

def extract_taxa_data(otu_coords, otu_table, lineages, prevalence, N):
    """Extrac the N most prevalent elements according to a prevalence vector

    Inputs:
    otu_coords: coordinates where specific taxa is centered
    otu_table: contingency table
    lineages: taxonomic assignments for each row in the otu_table
    prevalence: vector with prevalnce from 0 to 1 for each row of the otu_table
    as returned from qiime.biplots.get_taxa_prevalence
    N: number of most prevalent elements to retain

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
