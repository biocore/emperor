#!/usr/bin/env python
# File created on 06 Jul 2012
from __future__ import division

__author__ = "Antonio Gonzalez Pena"
__copyright__ = "Copyright 2011, The Emperor Project"
__credits__ = ["Antonio Gonzalez Pena", "Yoshiki Vazquez Baeza"]
__license__ = "GPL"
__version__ = "0.0.0-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "antgonza@gmail.com"
__status__ = "Development"

from os.path import join, exists
from qiime.parse import parse_mapping_file, parse_coords
from qiime.util import parse_command_line_parameters, make_option, create_dir

from emperor.util import copy_support_files, preprocess_mapping_file
from emperor.format import (format_pcoa_to_js, format_mapping_file_to_js,
    EMPEROR_FOOTER_HTML_STRING, EMPEROR_HEADER_HTML_STRING)

script_info = {}
script_info['brief_description'] = "Create three dimensional PCoA plots"
script_info['script_description'] = "This script automates the creation  of "+\
    "three-dimensional PCoA plots to be visualized with Emperor using Google "+\
    "Chrome."
script_info['script_usage'] = [("Plot PCoA data","Visualize the a PCoA file "
    "colored using a corresponding mapping file.","%prog -i "
    "unweighted_unifrac_pc.txt -m Fasting_Map.txt -o emperor_output"),
    ("Coloring by metadata mapping file", "Additionally, using the supplied "
    "mapping file and a specific category or any combination of the available "
    "categories. When using the -b option, the user can specify "
    "the coloring for multiple header names, where each header is separated by "
    "a comma. The user can also combine mapping headers and color by the "
    "combined headers that are created by inserting an '&&' between the input "
    "header names. Color by 'Treatment' and by the result of concatenating "
    "the 'DOB' category and the 'Treatment' category","%prog -i "
    "unweighted_unifrac_pc.txt -m Fasting_Map.txt -b 'Treatment&&DOB,Treatment'"
    )]
script_info['output_description']= "This script creates an output directory "+\
    "with an HTML formated file named 'emperor.html' and a complementary "+\
    "folder named 'emperor_required_resources'. Opening emperor.html with "+\
    "Google's Chrome web browser will display a three dimensional "+\
    "visualization of the processed PCoA data file and the corresponding "+\
    "metadata mapping file."
script_info['required_options'] = [
    make_option('-i','--pcoa_fp',type="existing_filepath",help='path to a PCoA'
    ' file'),
    make_option('-m','--map_fp',type="existing_filepath",help='path to a '
    'metadata mapping file'),
]
script_info['optional_options'] = [
    make_option('--add_unique_columns',action="store_true",help='add to the '
    'output categories of the mapping file the columns where all values are '
    'different. Note: if the result of one of the concatenated fields in '
    '--color_by is a column where all values are unique, the resulting column '
    'will get removed as well [default: %default]', default=False),
    make_option('-b', '--color_by', dest='color_by', type='string', help=
    'Comma-separated list of metadata categories (column headers) to color by'
    ' in the plots. The categories must match the name of a column header in '
    'the mapping file exactly. Multiple categories can be listed by comma '
    'separating them without spaces. The user can also combine columns in'
    ' the mapping file by separating the categories by "&&" without spaces. '
    '[default=color by all categories]', default=''),
     make_option('--ignore_missing_samples', help='This will overpass the error'
    ' raised when the coordinates file contains samples that are not present in'
    ' the mapping file. Be aware that this is very misleading as the PCoA is '
    'accounting for all the samples and removing some samples could lead to '
    ' erroneous/skewed interpretations.', action='store_true', default=False),
    make_option('-o','--output_dir',type="new_dirpath", help='path to the '
    'output directory that will contain the PCoA plot.')
]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    pcoa_fp = opts.pcoa_fp
    map_fp = opts.map_fp
    output_dir = opts.output_dir
    color_by_column_names = opts.color_by
    add_unique_columns = opts.add_unique_columns
    ignore_missing_samples = opts.ignore_missing_samples

    # before creating any output, check correct parsing of the main input files
    try:
        parsed_coords = parse_coords(open(pcoa_fp,'U'))
    except:
        option_parser.error(('The PCoA file \'%s\' does not seem to be a '
            'coordinates formatted file, verify by manuall inspecting '
            'the contents.') % pcoa_fp)
    try:
        mapping_data, header, comments = parse_mapping_file(open(map_fp,'U'))
    except:
        option_parser.error(('The metadata mapping file \'%s\' does not seem '
            'to be formatted correctly, verify the formatting is QIIME '
            'compliant by using check_id_map.py') % map_fp)

    # number of samples ids that are shared between coords and mapping files
    sids_intersection = len(set(zip(*mapping_data)[0]) & set(parsed_coords[0]))

    # sample ids must be shared between files
    if sids_intersection <= 0:
        option_parser.error('The sample identifiers in the coordinates file '
            'must have at least one match with the data contained in mapping '
            'file. Verify you are using a coordinates file and a mapping file '
            'that belong to the same dataset.')

    # the intersection of the sample ids in the coords and the sample ids in the
    # mapping file must at the very least include all ids in the coords file
    # Otherwise it isn't valid; unless --ignore_missing_samples is set True
    if sids_intersection!=len(parsed_coords[0]) and not ignore_missing_samples:
        option_parser.error('The metadata mapping file has fewer sample '
            'identifiers than the coordinates file. Verify you are using a '
            'mapping file that contains at least all the samples contained in '
            'the coordinates file. You can force the script to ignore these '
            ' samples by passing the \'--ignore_missing_samples\' flag.')

    # use the current working directory as default
    if opts.output_dir:
        create_dir(opts.output_dir,False)
        dir_path=opts.output_dir
    else:
        dir_path='./'

    fp_out = open(join(dir_path, 'emperor.html'),'w')
    fp_out.write(EMPEROR_HEADER_HTML_STRING)

    # check that all the required columns exist in the metadata mapping file
    if color_by_column_names:
        offending_fields = []
        color_by_column_names = color_by_column_names.split(',')

        # check for all the mapping fields
        for col in color_by_column_names:
            if col not in header and '&&' not in col:
                offending_fields.append(col)

        # terminate the program
        if offending_fields:
            option_parser.error("Invalid field(s) '%s'; the valid field(s) are:"
                " '%s'" % (', '.join(offending_fields), ', '.join(header)))
    else:
        # if the user didn't specify the header names display everything
        color_by_column_names = header[:]

    # remove the columns in the mapping file that are not informative taking
    # into account the header names that were already authorized to be used
    # and take care of concatenating the fields for the && merged columns
    mapping_data, header = preprocess_mapping_file(mapping_data, header,
        color_by_column_names, unique=not add_unique_columns)

    # write the html file
    fp_out.write(format_mapping_file_to_js(mapping_data, header, header))
    fp_out.write(format_pcoa_to_js(*parsed_coords)) # unpack the data
    fp_out.write(EMPEROR_FOOTER_HTML_STRING)
    copy_support_files(dir_path)

if __name__ == "__main__":
    main()