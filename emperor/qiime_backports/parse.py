#!/usr/bin/env python
#file parse.py: parsers for map file, distance matrix file, env file

__author__ = "Rob Knight"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Rob Knight", "Greg Caporaso", "Justin Kuczynski",
                "Cathy Lozupone", "Antonio Gonzalez Pena", "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "1.7.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"


from numpy import asarray

class QiimeParseError(Exception):
    pass

def parse_mapping_file(lines, strip_quotes=True, suppress_stripping=False):
    """Parser for map file that relates samples to metadata.
    
    Format: header line with fields
            optionally other comment lines starting with #
            tab-delimited fields

    Result: list of lists of fields, incl. headers.
    """
    if hasattr(lines,"upper"):
        # Try opening if a string was passed
        try:
            lines = open(lines,'U')
        except IOError:
            raise QiimeParseError("A string was passed that doesn't refer "
                                  "to an accessible filepath.")
        
    if strip_quotes:
        if suppress_stripping:
            # remove quotes but not spaces
            strip_f = lambda x: x.replace('"','')
        else:
            # remove quotes and spaces
            strip_f = lambda x: x.replace('"','').strip()
    else:
        if suppress_stripping:
            # don't remove quotes or spaces
            strip_f = lambda x: x
        else:
            # remove spaces but not quotes
            strip_f = lambda x: x.strip()
    
    # Create lists to store the results
    mapping_data = []
    header = []
    comments = []
    
    # Begin iterating over lines
    for line in lines:
        line = strip_f(line)
        if not line or (suppress_stripping and not line.strip()):
            # skip blank lines when not stripping lines
            continue
        
        if line.startswith('#'):
            line = line[1:]
            if not header:
                header = line.strip().split('\t')
            else:
                comments.append(line)
        else:
            # Will add empty string to empty fields
            tmp_line = list(map(strip_f, line.split('\t')))
            if len(tmp_line)<len(header):
                tmp_line.extend(['']*(len(header)-len(tmp_line)))
            mapping_data.append(tmp_line)
    if not header:
        raise QiimeParseError("No header line was found in mapping file.")
    if not mapping_data:
        raise QiimeParseError("No data found in mapping file.")
    
    return mapping_data, header, comments

def mapping_file_to_dict(mapping_data, header):
    """processes mapping data in list of lists format into a 2 deep dict"""
    map_dict = {}
    for i in range(len(mapping_data)):
        sam = mapping_data[i]
        map_dict[sam[0]] = {}
        for j in range(len(header)):
            if j == 0: continue # sampleID field
            map_dict[sam[0]][header[j]] = sam[j]
    return map_dict

def parse_metadata_state_descriptions(state_string):
    """From string in format 'col1:good1,good2;col2:good1' return dict."""
    result = {}
    state_string = state_string.strip()
    if state_string:
        cols = [s.strip()  for s in state_string.split(';')]
        for c in cols:
            # split on the first colon to account for category names with colons
            colname, vals = [s.strip() for s in c.split(':', 1)]

            vals = [v.strip() for v in vals.split(',')]
            result[colname] = set(vals)
    return result

def parse_mapping_file_to_dict(*args, **kwargs):
    """Parser for map file that relates samples to metadata.
    
    input format: header line with fields
            optionally other comment lines starting with #
            tab-delimited fields

    calls parse_mapping_file, then processes the result into a 2d dict, assuming
    the first field is the sample id
    e.g.: {'sample1':{'age':'3','sex':'male'},'sample2':...

    returns the dict, and a list of comment lines
"""
    mapping_data, header, comments = parse_mapping_file(*args,**kwargs)
    return mapping_file_to_dict(mapping_data, header), comments

def process_otu_table_sample_ids(sample_id_fields):
    """ process the sample IDs line of an OTU table """
    if len(sample_id_fields) == 0:
            raise ValueError('Error parsing sample ID line in OTU table. '
                             'Fields are %s' % ' '.join(sample_id_fields))
            
    # Detect if a metadata column is included as the last column. This
    # field will be named either 'Consensus Lineage' or 'OTU Metadata',
    # but we don't care about case or spaces.
    last_column_header = sample_id_fields[-1].strip().replace(' ','').lower()
    if last_column_header in ['consensuslineage', 'otumetadata', 'taxonomy']:
        has_metadata = True
        sample_ids = sample_id_fields[:-1]
    else:
        has_metadata = False
        sample_ids = sample_id_fields
    
    # Return the list of sample IDs and boolean indicating if a metadata
    # column is included.
    return sample_ids, has_metadata

def parse_classic_otu_table(lines,count_map_f=int, remove_empty_rows=False):
    """parses a classic otu table (sample ID x OTU ID map)

    Returns tuple: sample_ids, otu_ids, matrix of OTUs(rows) x samples(cols),
    and lineages from infile.
    """
    otu_table = []
    otu_ids = []
    metadata = []
    sample_ids = []
    # iterate over lines in the OTU table -- keep track of line number 
    # to support legacy (Qiime 1.2.0 and earlier) OTU tables
    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            if (i==1 or i==0) and line.startswith('#OTU ID') and not sample_ids:
                # we've got a legacy OTU table
                try:
                    sample_ids, has_metadata = process_otu_table_sample_ids(
                     line.strip().split('\t')[1:])
                except ValueError:
                    raise ValueError("Error parsing sample IDs in OTU table. "
                                     "Appears to be a legacy OTU table. Sample"
                                     " ID line:\n %s" % line)
            elif not line.startswith('#'):
                if not sample_ids:
                    # current line is the first non-space, non-comment line 
                    # in OTU table, so contains the sample IDs
                    try:
                        sample_ids, has_metadata = process_otu_table_sample_ids(
                         line.strip().split('\t')[1:])
                    except ValueError:
                        raise ValueError("Error parsing sample IDs in OTU "
                                         "table. Sample ID line:\n %s" % line)
                else:
                    # current line is OTU line in OTU table
                    fields = line.split('\t')
                    
                    if has_metadata:
                        # if there is OTU metadata the last column gets appended
                        # to the metadata list
                        # added in a try/except to handle OTU tables containing
                        # floating numbers
                        try:
                            valid_fields = asarray(fields[1:-1], dtype=count_map_f)
                        except ValueError:
                            valid_fields = asarray(fields[1:-1], dtype=float)
                        # validate that there are no empty rows
                        if remove_empty_rows and (valid_fields>=0).all() and \
                           sum(valid_fields)==0.0:
                            continue
                        metadata.append([f.strip() for f in fields[-1].split(';')])
                    else:
                        # otherwise all columns are appended to otu_table
                        # added in a try/except to handle OTU tables containing
                        # floating numbers
                        try:
                            valid_fields = asarray(fields[1:], dtype=count_map_f)
                        except ValueError:
                            valid_fields = asarray(fields[1:], dtype=float)
                        # validate that there are no empty rows
                        if remove_empty_rows and (valid_fields>=0.0).all() and \
                           sum(valid_fields)==0.0:
                            continue
                    otu_table.append(valid_fields)
                    # grab the OTU ID    
                    otu_id = fields[0].strip()
                    otu_ids.append(otu_id)
                        
    return sample_ids, otu_ids, asarray(otu_table), metadata
parse_otu_table = parse_classic_otu_table

def parse_coords(lines):
    """Parse unifrac coord file into coords, labels, eigvals, pct_explained.

    Returns:
    - list of sample labels in order
    - array of coords (rows = samples, cols = axes in descending order)
    - list of eigenvalues
    - list of percent variance explained

    File format is tab-delimited with following contents:
    - header line (starts 'pc vector number')
    - one-per-line per-sample coords
    - two blank lines
    - eigvals
    - % variation explained

    Strategy: just read the file into memory, find the lines we want
    """

    lines = list(lines)

    # make sure these and the other checks below are true as they are what
    # differentiate coordinates files from distance matrix files
    if not lines[0].startswith('pc vector number'):
        raise QiimeParseError("The line with the vector number was not found"
            ", this information is required in coordinates files")

    lines = [l.strip() for l in lines[1:]] # discard first line, which is a label
    lines = [_f for _f in lines if _f] # remove any blank lines

    # check on this information post removal of blank lines
    if not lines[-2].startswith('eigvals'):
        raise QiimeParseError("The line containing the eigenvalues was not "
            "found, this information is required in coordinates files")
    if not lines[-1].startswith('% variation'):
        raise QiimeParseError("The line with the percent of variation explained"
            " was not found, this information is required in coordinates files")

    #now last 2 lines are eigvals and % variation, so read them
    eigvals = asarray(lines[-2].split('\t')[1:], dtype=float)
    pct_var = asarray(lines[-1].split('\t')[1:], dtype=float)

    #finally, dump the rest of the lines into a table
    header, result = [], []
    for line in lines[:-2]:
        fields = [f.strip() for f in line.split('\t')]
        header.append(fields[0])
        result.append([float(f) for f in fields[1:]])

    return header, asarray(result), eigvals, pct_var
