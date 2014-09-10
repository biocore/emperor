#!/usr/bin/env python

from __future__ import division

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.9.4"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Release"

from skbio.math.stats.ordination import OrdinationResults
from skbio.core.exception import FileFormatError

from emperor.qiime_backports.parse import parse_coords as qiime_parse_coords


def parse_coords(lines):
    """Parse skbio's ordination results file into  coords, labels, eigvals,
        pct_explained.

    Returns:
    - list of sample labels in order
    - array of coords (rows = samples, cols = axes in descending order)
    - list of eigenvalues
    - list of percent variance explained

    For the file format check
    skbio.math.stats.ordination.OrdinationResults.from_file

    Strategy: read the file using skbio's parser and return the objects
              we want
    """
    try:
        pcoa_results = OrdinationResults.from_file(lines)
        return (pcoa_results.site_ids, pcoa_results.site, pcoa_results.eigvals,
                pcoa_results.proportion_explained)
    except FileFormatError:
        if type(lines) == file:
            lines.seek(0)
        return qiime_parse_coords(lines)