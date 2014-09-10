#!/usr/bin/env python
from __future__ import division
__author__ = "Rob Knight"
__copyright__ = "Copyright 2011, The QIIME Project" 
__credits__ = ["Rob Knight", "Justin Kuczynski", "Antonio Gonzalez Pena",
               "Daniel McDonald", "Jai Ram Rideout"]
#remember to add yourself if you make changes
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

def format_mapping_file(headers, mapping_data, comments=None):
    """ returns a large formatted string representing the entire mapping file

    each input is a list, and all data should be strings, not e.g. ints
    * headers defines column labels, and SampleID should not include a '#'
    * mapping_data is a list of lists, each sublist is a row in the mapping file
    each mapping_data sublist must be the same length as headers - use ''
    for absent data
    * if included, commments will be inserted above the header line
    comments should not include a # - that will be appended in this formatter
    """
    result = [] # each elem is a string representing a line

    result.append('#' + '\t'.join(headers))

    if comments != None:
        for comment in comments:
            result.append('#' + comment)

    for mapping_line in mapping_data:
        if not (len(mapping_line) == len(headers)):
            raise RuntimeError('error formatting mapping file, does each '+\
             'sample have the same length of data as the headers?')
        result.append('\t'.join(mapping_line))

    str_result = '\n'.join(result)
    return str_result
