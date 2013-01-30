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
from qiime.util import parse_command_line_parameters, make_option, create_dir
from qiime.parse import parse_mapping_file, parse_coords

from emperor.util import copy_support_files, process_mapping_file
from emperor.format import (format_pcoa_to_js, format_mapping_file_to_js,
    EMPEROR_FOOTER_HTML_STRING, EMPEROR_HEADER_HTML_STRING)

script_info = {}
script_info['brief_description'] = "Create three dimensional PCoA plots"
script_info['script_description'] = "This script automates the creation  of "+\
    "three-dimensional PCoA plots to be visualized with Emperor using Google "+\
    "Chrome."
script_info['script_usage'] = [("Plot PCoA data","Visualize the a PCoA file "
    "colored using a corresponding mapping file.","%prog -i "
    "unweighted_unifrac_pc.txt -m Fasting_Map.txt -o emperor_output")]
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
    make_option('-o','--output_dir',type="new_dirpath", help='path to the '
    'output directory that will contain the PCoA plot.'),
    make_option('--add_unique_columns',action="store_true",help='add to the '
    'output unique columns [default: %default]', default=False),
    make_option('-c','--add_columns',help='name of the columns to add. '
    'A list of column names separated by commas. Empty means all.'
    '[default: %default]', default=None)
]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    pcoa_fp = opts.pcoa_fp
    map_fp = opts.map_fp
    output_dir = opts.output_dir
    add_unique_columns = opts.add_unique_columns
    add_columns = opts.add_columns

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

    # use the current working directory as default
    if opts.output_dir:
        create_dir(opts.output_dir,False)
        dir_path=opts.output_dir
    else:
        dir_path='./'

    fp_out = open(join(dir_path, 'emperor.html'),'w')
    fp_out.write(EMPEROR_HEADER_HTML_STRING)

    # check that all the required columns exist in the metadata mapping file
    if add_columns:
        add_columns = add_columns.split(',')
        for col in add_columns:
            if col not in header:
                raise ValueError, "Column '%s' is not valid, valid ones are %s"\
                    % (col, header)
    else:
        add_columns = header

    # remove the columns in the mapping file that are not informative taking
    # into account the header names that were already authorized to be used
    if not add_unique_columns:
        mapping_data, header = process_mapping_file(mapping_data, header,
            add_columns)

    fp_out.write(format_mapping_file_to_js(mapping_data, header, add_columns))
    fp_out.write(format_pcoa_to_js(*parsed_coords)) # unpack the data
    fp_out.write(EMPEROR_FOOTER_HTML_STRING)
    copy_support_files(dir_path)

if __name__ == "__main__":
    main()