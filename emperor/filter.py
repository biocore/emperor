# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division
from numpy import array


def filter_samples_from_coords(headers, coords,
                               valid_sample_ids, negate=False):
    """Filter samples from a pair of headers and coordinates

    Parameters
    ----------
    headers : array_like
         list of sample ids corresponding to the coordinates data
    coords : numpy.ndarray
         numpy array of float values
    valid_sample_ids : list, str
         list of sample ids to keep
    negate: bool, optional
         False means keep the samples in valid_sample_ids,
         True means remove the samples in valid_sample_ids

    Returns
    -------
    out_coord_ids : list, str
         Filtered list headers
    out_coords : list, np.array
         Filtered list of coordinates

    Raises
    ------
    ValueError
        If all the samples are filtered out
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
        raise ValueError("All samples have been filtered out")

    return out_coord_ids, array(out_coords)


def keep_samples_from_pcoa_data(headers, coords, sample_ids):
    """Controller function to filter coordinates data according to a list

    Parameters
    ----------
    headers : list, str
        list of sample identifiers, if used for jackknifed data, this
        should be a list of lists containing the sample identifiers
    coords : numpy.ndarray
        2-D numpy array with the float data in the coordinates, if used for
        jackknifed data, coords should be a list of 2-D numpy arrays
    sample_ids : list, str
        list of sample ids that should be kept

    Returns
    -------
    out_headers : list, str
        list of headers
    out_coords : list, np.array
        list of coordinates
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
        out_headers, out_coords = filter_samples_from_coords(headers,
                                                             coords,
                                                             sample_ids)
        return out_headers, out_coords
