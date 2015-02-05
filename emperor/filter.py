#!/usr/bin/env python
# File created on 12 May 2013
from __future__ import division

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "0.9.51"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Release"

from numpy import array

def filter_samples_from_coords(headers, coords, valid_sample_ids, negate=False):
    """Filter samples from a pair of headers and coordinates

    headers: list of sample ids corresponding to the coordinates data
    coords: numpy array of float values
    valid_sample_ids: list of sample ids to keep
    negate: False means keep the samples in valid_sample_ids, True means remove
    the samples in valid_sample_ids

    Notes:
    Raises ValueError when all the samples are filtered out
    """
    out_coord_ids, out_coords = [], []

    # define the strategy to take for each of the iterations
    if negate:
        def keep_sample(s):
            return s not in valid_sample_ids
    else:
        def keep_sample(s):
            return s in valid_sample_ids

    for sample_id, coord in zip(headers, coords):
        if keep_sample(sample_id):
            out_coord_ids.append(sample_id)
            out_coords.append(array(coord))

    # do not allow empty sets as return values, raise an exception
    if len(out_coord_ids) < 1:
        raise ValueError, "All samples have been filtered out"

    return out_coord_ids, array(out_coords)

def keep_samples_from_pcoa_data(headers, coords, sample_ids):
    """Controller function to filter coordinates data according to a list

    headers: list of sample identifiers, if used for jackknifed data, this
    should be a list of lists containing the sample identifiers
    coords: 2-D numpy array with the float data in the coordinates, if used for
    jackknifed data, coords should be a list of 2-D numpy arrays
    sample_ids: list of sample ids that should be kept
    """

    # if the coords are a list then it means that the input jackknifed
    if type(coords) == list:
        out_coords, out_headers = [], []

        for single_headers, single_coords in zip(headers, coords):
            a, b = filter_samples_from_coords(single_headers, single_coords,
                sample_ids)

            out_headers.append(a)
            out_coords.append(b)

        return out_headers, out_coords
    else:
        return filter_samples_from_coords(headers, coords, sample_ids)
