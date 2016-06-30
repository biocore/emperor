#!/usr/bin/env python

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2011, The QIIME Project" 
__credits__ = ["Catherine Lozupone", "Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshik89@gmail.com"
__status__ = "Development"

from scipy.spatial import procrustes

from emperor.qiime_backports.parse import parse_mapping_file_to_dict

from numpy.ma.extras import apply_along_axis
from numpy.ma import MaskedArray
from numpy import (shape, vstack, zeros, sum as numpy_sum, sort as numpy_sort,
    nan as numpy_nan, array, median)

def is_valid_git_refname(refname):
    """check if a string is a valid branch-name/ref-name for git

    Input:
    refname: string to validate

    Output:
    True if 'refname' is a valid branch name in git. False if it fails to meet
    any of the criteria described in the man page for 'git check-ref-format',
    also see:

    http://www.kernel.org/pub/software/scm/git/docs/git-check-ref-format.html
    """
    if len(refname) == 0:
        return False

    # git imposes a few requirements to accept a string as a refname/branch-name

    # They can include slash / for hierarchical (directory) grouping, but no
    # slash-separated component can begin with a dot . or end with the sequence
    # .lock
    if (len([True for element in refname.split('/')\
            if element.startswith('.') or element.endswith('.lock')]) != 0):
        return False

    # They cannot have two consecutive dots .. anywhere
    if '..' in refname:
        return False

    # They cannot have ASCII control characters (i.e. bytes whose values are
    # lower than \040, or \177 DEL), space, tilde, caret ^, or colon : anywhere
    if len([True for refname_char in refname if ord(refname_char) < 40 or\
            ord(refname_char) == 177 ]) != 0:
        return False
    if ' ' in refname or '~' in refname or '^' in refname or ':' in refname:
        return False

    # They cannot have question-mark ?, asterisk *, or open bracket [ anywhere
    if '?' in refname or '*' in refname or '[' in refname:
        return False

    # They cannot begin or end with a slash / or contain multiple consecutive
    # slashes
    if refname.startswith('/') or refname.endswith('/') or '//' in refname:
        return False

    # They cannot end with a dot ..
    if refname.endswith('.'):
        return False

    # They cannot contain a sequence @{
    if '@{' in refname:
        return False

    # They cannot contain a \
    if '\\' in refname:
        return False

    return True

def is_valid_git_sha1(hash):
    """check if a string is a valid git sha1 string

    Input:
    hash: string to validate

    Output:
    True if the string has 40 characters and is an hexadecimal number, False
    otherwise.

    """

    if len(hash) != 40:
        return False
    try:
        value = int(hash, 16)
    except ValueError:
        return False

    return True

class MetadataMap():
    """This class represents a QIIME metadata mapping file.
    
    Public attributes:
        Comments - the comments associated with this metadata map (a list of
            strings)
    """

    @staticmethod
    def parseMetadataMap(lines):
        """Parses a QIIME metadata mapping file into a MetadataMap object.

        This static method is basically a factory that reads in the given
        metadata mapping file contents and returns a MetadataMap instance. This
        method is provided for convenience.

        Arguments:
            lines - a list of strings representing the file contents of a QIIME
                metadata mapping file
        """
        return MetadataMap(*parse_mapping_file_to_dict(lines))

    def __init__(self, sample_metadata, Comments):
        """Instantiates a MetadataMap object.

        Arguments:
            sample_metadata - the output of parse_mapping_file_to_dict(). It
                expects a python dict of dicts, where the top-level key is
                sample ID, and the inner dict maps category name to category
                value. This can be an empty dict altogether or the inner dict
                can be empty
            Comments - the output of parse_mapping_file_to_dict(). It expects a
                list of strings for the comments in the mapping file. Can be an
                empty list
        """
        self._metadata = sample_metadata
        self.Comments = Comments

    def __eq__(self, other):
        """Test this instance for equality with another.

        Note: This code was taken from http://stackoverflow.com/questions/
            390250/elegant-ways-to-support-equivalence-equality-in-python-
            classes.
        """
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Test this instance for inequality with another.

        Note: This code was taken from http://stackoverflow.com/questions/
            390250/elegant-ways-to-support-equivalence-equality-in-python-
            classes.
        """
        return not self.__eq__(other)

    def getSampleMetadata(self, sample_id):
        """Returns the metadata associated with a particular sample.

        The metadata will be returned as a dict mapping category name to
        category value.

        Arguments:
            sample_id - the sample ID (string) to retrieve metadata for
        """
        return self._metadata[sample_id]

    def getCategoryValue(self, sample_id, category):
        """Returns the category value associated with a sample's category.

        The returned category value will be a string.

        Arguments:
            sample_id - the sample ID (string) to retrieve category information
                for
            category - the category name whose value will be returned
        """
        return self._metadata[sample_id][category]

    def getCategoryValues(self, sample_ids, category):
        """Returns all the values of a given category.

        The return categories will be a list.

        Arguments:
            sample_ids - An ordered list of sample IDs (i.e., from a distance
                matrix)
            category - the category name whose values will be returned
        """
        return [self._metadata[sid][category] for sid in sample_ids]

    def isNumericCategory(self, category):
        """Returns True if the category is numeric and False otherwise.

        A category is numeric if all values within the category can be
        converted to a float.

        Arguments:
            category - the category that will be checked
        """
        category_values = self.getCategoryValues(self.SampleIds, category)

        is_numeric = True
        for category_value in category_values:
            try:
                float(category_value)
            except ValueError:
                is_numeric = False
        return is_numeric

    def hasUniqueCategoryValues(self, category):
        """Returns True if the category's values are all unique.

        Arguments:
            category - the category that will be checked for uniqueness
        """
        category_values = self.getCategoryValues(self.SampleIds, category)

        is_unique = False
        if len(set(category_values)) == len(self.SampleIds):
            is_unique = True
        return is_unique

    def hasSingleCategoryValue(self, category):
        """Returns True if the category's values are all the same.

        For example, the category 'Treatment' only has values 'Control' for the
        entire column.

        Arguments:
            category - the category that will be checked
        """
        category_values = self.getCategoryValues(self.SampleIds, category)

        single_value = False
        if len(set(category_values)) == 1:
            single_value = True
        return single_value

    @property
    def SampleIds(self):
        """Returns the IDs of all samples in the metadata map.

        The sample IDs are returned as a list of strings in alphabetical order.
        """
        return sorted(self._metadata.keys())

    @property
    def CategoryNames(self):
        """Returns the names of all categories in the metadata map.

        The category names are returned as a list of strings in alphabetical
        order.
        """
        return sorted(self.getSampleMetadata(self.SampleIds[0]).keys()) \
            if len(self.SampleIds) > 0 else []

    def filterSamples(self, sample_ids_to_keep, strict=True):
        """Remove samples that are not in ``sample_ids_to_keep``.

        If ``strict=True``, a ``ValueError`` will be raised if any of the
        sample IDs in ``sample_ids_to_keep`` cannot be found in the metadata
        map.
        """
        for sid in self.SampleIds:
            if sid not in sample_ids_to_keep:
                del self._metadata[sid]

        if strict:
            extra_samples = set(sample_ids_to_keep) - set(self.SampleIds)

            if extra_samples:
                raise ValueError("Could not find the following sample IDs in "
                                 "metadata map: %s" % ', '.join(extra_samples))

def summarize_pcoas(master_pcoa, support_pcoas, method='IQR', apply_procrustes=True):
    """returns the average PCoA vector values for the support pcoas

    Also returns the ranges as calculated with the specified method.
    The choices are:
        IQR: the Interquartile Range
        ideal fourths: Ideal fourths method as implemented in scipy
    """
    if apply_procrustes:
        # perform procrustes before averaging
        support_pcoas = [list(sp) for sp in support_pcoas]
        master_pcoa = list(master_pcoa)
        for i, pcoa in enumerate(support_pcoas):
            master_std, pcoa_std, m_squared = procrustes(master_pcoa[1],pcoa[1])
            support_pcoas[i][1] = pcoa_std
        master_pcoa[1] = master_std

    m_matrix = master_pcoa[1]
    m_eigvals = master_pcoa[2]
    m_names = master_pcoa[0]
    jn_flipped_matrices = []
    all_eigvals = []
    for rep in support_pcoas:
        matrix = rep[1]
        eigvals = rep[2]
        all_eigvals.append(eigvals)
        jn_flipped_matrices.append(_flip_vectors(matrix, m_matrix))
    matrix_average, matrix_low, matrix_high = _compute_jn_pcoa_avg_ranges(\
            jn_flipped_matrices, method)
    #compute average eigvals
    all_eigvals_stack = vstack(all_eigvals)
    eigval_sum = numpy_sum(all_eigvals_stack, axis=0)
    eigval_average = eigval_sum / float(len(all_eigvals))
    return matrix_average, matrix_low, matrix_high, eigval_average, m_names

def _flip_vectors(jn_matrix, m_matrix):
    """transforms PCA vectors so that signs are correct"""
    m_matrix_trans = m_matrix.transpose()
    jn_matrix_trans = jn_matrix.transpose()
    new_matrix= zeros(jn_matrix_trans.shape, float)
    for i, m_vector in enumerate(m_matrix_trans):
        jn_vector = jn_matrix_trans[i]
        disT = list(m_vector - jn_vector)
        disT = sum(map(abs, disT))
        jn_flip = jn_vector*[-1]
        disF = list(m_vector - jn_flip)
        disF = sum(map(abs, disF))
        if disT > disF:
            new_matrix[i] = jn_flip
        else:
            new_matrix[i] = jn_vector
    return new_matrix.transpose()

def _compute_jn_pcoa_avg_ranges(jn_flipped_matrices, method):
    """Computes PCoA average and ranges for jackknife plotting

    returns 1) an array of jn_averages
             2) an array of upper values of the ranges
            3) an array of lower values for the ranges

    method: the method by which to calculate the range
        IQR: Interquartile Range
        ideal fourths: Ideal fourths method as implemented in scipy
    """
    x,y = shape(jn_flipped_matrices[0])
    all_flat_matrices = [matrix.ravel() for matrix in jn_flipped_matrices]
    summary_matrix = vstack(all_flat_matrices)
    matrix_sum = numpy_sum(summary_matrix, axis=0)
    matrix_average = matrix_sum / float(len(jn_flipped_matrices))
    matrix_average = matrix_average.reshape(x,y)
    if method == 'IQR':
        result = matrix_IQR(summary_matrix)
        matrix_low = result[0].reshape(x,y)
        matrix_high = result[1].reshape(x,y)
    elif method == 'ideal_fourths':
        result = idealfourths(summary_matrix, axis=0)
        matrix_low = result[0].reshape(x,y)
        matrix_high = result[1].reshape(x,y)
    elif method == "sdev":
        # calculate std error for each sample in each dimension
        sdevs = zeros(shape=[x,y])
        for j in range(y):
            for i in range(x):
                vals = array([pcoa[i][j] for pcoa in jn_flipped_matrices])
                sdevs[i,j] = vals.std(ddof=1)
        matrix_low = -sdevs/2
        matrix_high = sdevs/2


    return matrix_average, matrix_low, matrix_high

def IQR(x):
    """calculates the interquartile range of x

    x can be a list or an array
    
    returns min_val and  max_val of the IQR"""

    x.sort()
    #split values into lower and upper portions at the median
    odd = len(x) % 2
    midpoint = int(len(x)/2)
    if odd:
        low_vals = x[:midpoint]
        high_vals = x[midpoint+1:]
    else: #if even
        low_vals = x[:midpoint]
        high_vals = x[midpoint:]
    #find the median of the low and high values
    min_val = median(low_vals)
    max_val = median(high_vals)
    return min_val, max_val


def matrix_IQR(x):
    """calculates the IQR for each column in an array
    """
    num_cols = x.shape[1]
    min_vals = zeros(num_cols)
    max_vals = zeros(num_cols)
    for i in range(x.shape[1]):
        col = x[:, i]
        min_vals[i], max_vals[i] = IQR(col)
    return min_vals, max_vals

def idealfourths(data, axis=None):
    """This function returns an estimate of the lower and upper quartiles of the data along
    the given axis, as computed with the ideal fourths. This function was taken
    from scipy.stats.mstat_extra.py (http://projects.scipy.org/scipy/browser/trunk/scipy/stats/mstats_extras.py?rev=6392)
    """
    def _idf(data):
        x = data.compressed()
        n = len(x)
        if n < 3:
            return [numpy_nan,numpy_nan]
        (j,h) = divmod(n/4. + 5/12.,1)
        qlo = (1-h)*x[j-1] + h*x[j]
        k = n - j
        qup = (1-h)*x[k] + h*x[k-1]
        return [qlo, qup]
    data = numpy_sort(data, axis=axis).view(MaskedArray)
    if (axis is None):
        return _idf(data)
    else:
        return apply_along_axis(_idf, axis, data)
