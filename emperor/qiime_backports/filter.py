#!/usr/bin/env python
# File created on 18 May 2010
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Greg Caporaso", "Will Van Treuren", "Daniel McDonald",
               "Jai Ram Rideout", "Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from emperor.qiime_backports.format import format_mapping_file
from emperor.qiime_backports.parse import (parse_metadata_state_descriptions,
    parse_mapping_file)

def filter_mapping_file_by_metadata_states(mapping_f,valid_states_str):
    sample_ids_to_keep = sample_ids_from_metadata_description(mapping_f,valid_states_str)
    mapping_f.seek(0)
    return filter_mapping_file_from_mapping_f(mapping_f,sample_ids_to_keep)

def sample_ids_from_metadata_description(mapping_f,valid_states_str):
    """ Given a description of metadata, return the corresponding sample ids
    """
    map_data, map_header, map_comments = parse_mapping_file(mapping_f)
    valid_states = parse_metadata_state_descriptions(valid_states_str)
    sample_ids = get_sample_ids(map_data, map_header, valid_states)

    if len(sample_ids)<1:
        raise ValueError("All samples have been filtered out for the criteria"
                         " described in the valid states")

    return sample_ids

def filter_mapping_file_from_mapping_f(mapping_f,sample_ids_to_keep,negate=False):
    """ Filter rows from a metadata mapping file """
    mapping_data, header, comments = parse_mapping_file(mapping_f)
    filtered_mapping_data = []
    sample_ids_to_keep = {}.fromkeys(sample_ids_to_keep)
    
    for mapping_datum in mapping_data:
        hit = mapping_datum[0] in sample_ids_to_keep
        if hit and not negate:
            filtered_mapping_data.append(mapping_datum)
        elif not hit and negate:
            filtered_mapping_data.append(mapping_datum)
        else:
            pass
    return format_mapping_file(header,filtered_mapping_data)

def get_sample_ids(map_data, map_header, states):
    """Takes col states in {col:[vals]} format.

    If val starts with !, exclude rather than include.
    
    Combines cols with and, states with or.

    For example, Study:Dog,Hand will return rows where Study is Dog or Hand;
    Study:Dog,Hand;BodySite:Palm,Stool will return rows where Study is Dog
    or Hand _and_ BodySite is Palm or Stool; Study:*,!Dog;BodySite:*,!Stool
    will return all rows except the ones where the Study is Dog or the BodySite
    is Stool.
    """
    
    name_to_col = dict([(s,map_header.index(s)) for s in states])
    good_ids = []
    for row in map_data:    #remember to exclude header
        include = True
        for s, vals in states.items():
            curr_state = row[name_to_col[s]]
            include = include and (curr_state in vals or '*' in vals) \
                and not '!'+curr_state in vals
        if include:        
            good_ids.append(row[0])
    return good_ids

def filter_mapping_file(map_data, map_header, good_sample_ids, 
               include_repeat_cols=False, column_rename_ids=None):
    """Filters map according to several criteria.

    - keep only sample ids in good_sample_ids
    - drop cols that are different in every sample (except id)
    - drop cols that are the same in every sample
    """
    # keeping samples
    to_keep = []
    to_keep.extend([i for i in map_data if i[0] in good_sample_ids])
    
    # keeping columns
    headers = []
    to_keep = list(zip(*to_keep))
    headers.append(map_header[0])
    result = [to_keep[0]]
    
    if column_rename_ids:
        # reduce in 1 as we are not using the first colum (SampleID)
        column_rename_ids = column_rename_ids-1
        for i,l in enumerate(to_keep[1:-1]):
            if i==column_rename_ids:
                if len(set(l))!=len(result[0]):
                     raise ValueError("The column to rename the samples is not unique.")
                result.append(result[0])
                result[0] = l
                headers.append('SampleID_was_' + map_header[i+1])
            elif include_repeat_cols or len(set(l))>1:
                headers.append(map_header[i+1])
                result.append(l)
    else:
        for i,l in enumerate(to_keep[1:-1]):
            if include_repeat_cols or len(set(l))>1:
                headers.append(map_header[i+1])
                result.append(l)
    headers.append(map_header[-1])
    result.append(to_keep[-1])
    
    result = list(map(list, zip(*result)))
    
    return headers, result
