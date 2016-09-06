#!/usr/bin/env python
#file make_3d_plots.py

__author__ = "Dan Knights"
__copyright__ = "Copyright 2011, The QIIME Project" 
__credits__ = ["Dan Knights", "Justin Kuczynski"] #remember to add yourself
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Dan Knights"
__email__ = "daniel.knights@colorado.edu"
__status__ = "Development"

from emperor.qiime_backports.parse import parse_otu_table
from numpy import array, apply_along_axis, dot,delete, argsort
import numpy as np

def get_taxa_coords(tax_counts,sample_coords):
    """Returns the PCoA coords of each taxon based on the coords of the samples."""
    # normalize taxa counts along each row/sample (i.e. to get relative abundance)
    tax_counts = apply_along_axis(lambda x: x/float(sum(x)), 0, tax_counts)
    # normalize taxa counts along each column/taxa (i.e. to make PCoA score contributions sum to 1)
    tax_ratios = apply_along_axis(lambda x: x/float(sum(x)), 1, tax_counts)
    return(dot(tax_ratios,sample_coords))

def get_taxa_prevalence(tax_counts):
    """Returns the each lineage's portion of the total count 
    
    takes an otu_table (rows = otus), normalizes samples to equal counts,
    and returns each otu's relative representation in this normalized otu table,
    scaled such that the rarest otu is 0, most prominent is 1
    """
    tax_ratios = apply_along_axis(lambda x: x/float(sum(x)), 0, tax_counts)
    lineage_sums = apply_along_axis(lambda x: sum(x), 1, tax_ratios)
    total_count = sum(lineage_sums)
    prevalence = lineage_sums / float(total_count)
    # scale prevalence from 0 to 1
    prevalence = (prevalence - min(prevalence)) / (max(prevalence) - min(prevalence))
    return prevalence

def make_biplot_scores_output(taxa):
    """Create convenient output format of taxon biplot coordinates

       taxa is a dict containing 'lineages' and a coord matrix 'coord'

       output is a list of lines, each containing coords for one taxon
    """
    output = []
    ndims = len(taxa['coord'][1])
    header = '#Taxon\t' + '\t'.join(['pc%d' %(i+1) for i in range(ndims)])
    output.append(header)
    for i, taxon in enumerate(taxa['lineages']):
        line = taxon + '\t'
        line += '\t'.join(map(str, taxa['coord'][i]))
        output.append(line)
    return output
