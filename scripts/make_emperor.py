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

from os import listdir
from os.path import join, exists, isdir

from qiime.biplots import get_taxa, get_taxa_coords, get_taxa_prevalence
from qiime.filter import filter_mapping_file
from qiime.parse import (parse_mapping_file, parse_coords, mapping_file_to_dict,
    parse_otu_table)
from qiime.util import (parse_command_line_parameters, make_option, create_dir,
    MetadataMap)
from qiime.biplots import make_biplot_scores_output

from emperor.biplots import preprocess_otu_table
from emperor.util import (copy_support_files, preprocess_mapping_file,
    preprocess_coords_file, fill_mapping_field_from_mapping_file)
from emperor.format import (format_pcoa_to_js, format_mapping_file_to_js,
    format_taxa_to_js, format_emperor_html_footer_string,
    EMPEROR_HEADER_HTML_STRING)

script_info = {}
script_info['brief_description'] = "Create three dimensional PCoA plots"
script_info['script_description'] = "This script automates the creation  of "+\
    "three-dimensional PCoA plots to be visualized with Emperor using Google "+\
    "Chrome."
script_info['script_usage'] = [("Plot PCoA data","Visualize the a PCoA file "
    "colored using a corresponding mapping file: ","%prog -i "
    "unweighted_unifrac_pc.txt -m Fasting_Map.txt -o emperor_output"),
    ("Coloring by metadata mapping file", "Additionally, using the supplied "
    "mapping file and a specific category or any combination of the available "
    "categories. When using the -b option, the user can specify "
    "the coloring for multiple header names, where each header is separated by "
    "a comma. The user can also combine mapping headers and color by the "
    "combined headers that are created by inserting an '&&' between the input "
    "header names. Color by 'Treatment' and by the result of concatenating "
    "the 'DOB' category and the 'Treatment' category: ","%prog -i "
    "unweighted_unifrac_pc.txt -m Fasting_Map.txt -b 'Treatment&&DOB,Treatment'"
    " -o emperor_colored_by"),
    ("PCoA plot with an explicit axis", "Create a PCoA plot with an axis of "
    "the plot representing the 'DOB' of the samples. This option is useful when"
    " presenting a gradient from your metadata e. g. 'Time' or 'pH': ", "%prog "
    "-i unweighted_unifrac_pc.txt -m Fasting_Map.txt -a DOB -o pcoa_dob"),
    ("Jackknifed principal coordinates analysis plot", "Create a jackknifed "
    "PCoA plot (with confidence intervals for each sample) passing as the input"
    " a directory of coordinates files (where each file corresponds to a "
    "different OTU table) and use the standard deviation method to compute the "
    "dimensions of the ellipsoids surrounding each sample: ", "%prog -i "
    "unweighted_unifrac_pc -m Fasting_Map.txt -o jackknifed_pcoa -e sdev"),
    ("Jackknifed PCoA plot with a master coordinates file", "Passing a master "
    "coordinates file (--master_pcoa) will display the ellipsoids centered by "
    "the samples in this file: ", "%prog -i unweighted_unifrac_pc -s "
    "unweighted_unifrac_pc/pcoa_unweighted_unifrac_rarefaction_110_5.txt -m "
    "Fasting_Map.txt -o jackknifed_with_master"),
    ("BiPlots","To see which taxa are the ten more prevalent in the different "
    "areas of the PCoA plot, you need to pass a summarized taxa file i. e. the "
    "output of summarize_taxa.py. Note that if the the '--taxa_fp' has fewer "
    "than 10 taxa, the script will default to use all.","%prog -i unweighted_un"
    "ifrac_pc.txt -m Fasting_Map.txt -t otu_table_L3.txt -o biplot"),
    ("BiPlots with extra options","To see which are the three most prevalent "
    "taxa and save the coordinates where these taxa are centered, you can use "
    "the -n (number of taxa to keep) and the --biplot_fp (output biplot file "
    "path) options.", "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -t"
    " otu_table_L3.txt -o biplot_options -n 3 --biplot_fp biplot.txt")]
script_info['output_description']= "This script creates an output directory "+\
    "with an HTML formated file named 'emperor.html' and a complementary "+\
    "folder named 'emperor_required_resources'. Opening emperor.html with "+\
    "Google's Chrome web browser will display a three dimensional "+\
    "visualization of the processed PCoA data file and the corresponding "+\
    "metadata mapping file."
script_info['required_options'] = [
    make_option('-i','--input_coords',type="existing_path",help='Path to a '
    'coordinates file to create a PCoA plot. Alternatively a path to a '
    'directory containing only coordinates files to create a jackknifed PCoA '
    'plot.'),
    make_option('-m','--map_fp',type="existing_filepath",help='path to a '
    'metadata mapping file')
]
script_info['optional_options'] = [
    make_option('-a', '--custom_axes', type='string', help='Comma-separated '
    'list of metadata categories to use as custom axes in the plot. For '
    'instance, if there is a time category and you would like to see the '
    'samples plotted on that axis instead of PC1, PC2, etc., you would pass '
    'time as the value of this option.  Note: if there is any non-numeric data '
    'in the metadata column, an error will be presented [default: %default]',
    default=None),
    make_option('--add_unique_columns',action="store_true",help='Add to the '
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
    make_option('--biplot_fp', help='Output filepath that will contain the '
    'coordinates where each taxonomic sphere is centered. [default: %default]',
    default=None, type='new_filepath'),
    make_option('-e', '--ellipsoid_method', help='Used only when plotting '
    'ellipsoids for jackknifed beta diversity (i.e. using a directory of coord '
    'files instead of a single coord file). Valid values are "IQR" (for '
    'inter-quartile ranges) and "sdev" (for standard deviation). '
    '[default=%default]', default='IQR', type='choice', choices=['IQR','sdev']),
     make_option('--ignore_missing_samples', help='This will overpass the error'
    ' raised when the coordinates file contains samples that are not present in'
    ' the mapping file. Be aware that this is very misleading as the PCoA is '
    'accounting for all the samples and removing some samples could lead to '
    ' erroneous/skewed interpretations.', action='store_true', default=False),
    make_option('-n', '--n_taxa_to_keep', help='Number of taxonomic groups from'
    ' the "--taxa_fp" file to display. Passing "-1" will cause to display all '
    'the taxonomic groups, this option is only used when creating BiPlots. '
    '[default=%default]', default=10, type='int'),
    make_option('-s', '--master_pcoa', help='Used only when plotting ellipsoids'
    ' for jackknifed beta diversity (i.e. using a directory of coord files'
    ' instead of a single coord file). The coordinates in this file will be the'
    ' center of each ellipisoid. [default: arbitrarily selected file from the '
    'input directory]', default=None, type='existing_filepath'),
    make_option('-t', '--taxa_fp', help='Path to a summarized taxa file (i. '
    'e. the output of summarize_taxa.py). This option is only used when '
    'creating BiPlots. [default=%default]', default=None, type=
    'existing_filepath'),
    make_option('-x', '--missing_custom_axes_values', help='Option to override '
    'the error shown when the \'--custom_axes\' categories, have non-numeric '
    'values in the mapping file. For example, if you wanted to see all the '
    'control samples that do not have a time gradient value in the mapping '
    'file at the time-point zero and the missing pH values at 7, you would have'
    ' to pass  \'-x Time:0 -x pH:7\'.', action='append', default=None),
    make_option('-o','--output_dir',type="new_dirpath", help='path to the '
    'output directory that will contain the PCoA plot.')
]
script_info['version'] = __version__


def main():
    option_parser, opts, args = parse_command_line_parameters(**script_info)
    input_coords = opts.input_coords
    map_fp = opts.map_fp
    output_dir = opts.output_dir
    color_by_column_names = opts.color_by
    add_unique_columns = opts.add_unique_columns
    custom_axes = opts.custom_axes
    ignore_missing_samples = opts.ignore_missing_samples
    missing_custom_axes_values = opts.missing_custom_axes_values
    jackknifing_method = opts.ellipsoid_method
    master_pcoa = opts.master_pcoa
    taxa_fp = opts.taxa_fp
    n_taxa_to_keep = opts.n_taxa_to_keep
    biplot_fp = opts.biplot_fp

    # append headernames that the script didn't find in the mapping file
    # according to different criteria to the following variables
    offending_fields = []
    non_numeric_categories = []

    # can't do averaged pcoa plots _and_ custom axes in the same plot
    if custom_axes!=None and len(custom_axes.split(','))>1 and\
        isdir(input_coords):
        option_parser.error(('Jackknifed plots are limited to one custom axis, '
            'currently trying to use: %s. Make sure you use only one.' %
            custom_axes))

    # before creating any output, check correct parsing of the main input files
    try:
        mapping_data, header, comments = parse_mapping_file(open(map_fp,'U'))
    except:
        option_parser.error(('The metadata mapping file \'%s\' does not seem '
            'to be formatted correctly, verify the formatting is QIIME '
            'compliant by using check_id_map.py') % map_fp)

    # dir means jackknifing type of processing
    if isdir(input_coords):
        offending_coords_fp = []
        coords_headers, coords_data, coords_eigenvalues, coords_pct=[],[],[],[]

        # iterate only over the non-hidden files
        coord_fps = [join(input_coords, f) for f in listdir(input_coords)
            if not f.startswith('.')]

        if not coord_fps:
            option_parser.error('The input path is empty; if passing a folder '
                'as the input, please make sure it contains coordinates files.')

        # the master pcoa must be the first in the list of coordinates
        if master_pcoa:
            if master_pcoa in coord_fps: # remove it if duplicated
                coord_fps.remove(master_pcoa)
            coord_fps = [master_pcoa] + coord_fps # prepend it to the list

        for fp in coord_fps:
            try:
                _coords_headers, _coords_data, _coords_eigenvalues,_coords_pct=\
                    parse_coords(open(fp,'U'))

                # pack all the data correspondingly
                coords_headers.append(_coords_headers)
                coords_data.append(_coords_data)
                coords_eigenvalues.append(_coords_eigenvalues)
                coords_pct.append(_coords_pct)
            except:
                offending_coords_fp.append(fp)

        # in case there were files that couldn't be parsed
        if offending_coords_fp:
            option_parser.error(('The following file(s): \'%s\' could not be '
                'parsed properly. Make sure the input folder only contains '
                'coordinates files.') % ', '.join(offending_coords_fp))

        # check all files contain the same sample identifiers by flattening the
        # list of available sample ids and returning the sample ids that are
        # in one of the sets of sample ids but not in the globablly shared ids
        non_shared_ids = set(sum([list(set(sum(coords_headers, []))^set(e))
            for e in coords_headers],[]))
        if non_shared_ids and len(coords_headers) > 1:
            option_parser.error(('The following sample identifier(s): \'%s\''
                'are not shared between all the files. The files used to '
                'make a jackknifed PCoA plot must share all the same sample '
                'identifiers') % ', '.join(list(non_shared_ids)))

        # flatten the list of lists into a 1-d list
        _coords_headers = list(set(sum(coords_headers, [])))

        # number of samples ids that are shared between coords and mapping files
        sids_intersection=list(set(zip(*mapping_data)[0])&set(_coords_headers))

        # used to perform different validations in the script, very similar for
        # the case where the input is not a directory
        number_intersected_sids = len(sids_intersection)
        required_number_of_sids = len(coords_headers[0])

    else:
        try:
            coords_headers, coords_data, coords_eigenvalues, coords_pct =\
                parse_coords(open(input_coords,'U'))
        except:
            option_parser.error(('The PCoA file \'%s\' does not seem to be a '
                'coordinates formatted file, verify by manuall inspecting '
                'the contents.') % input_coords)

        # number of samples ids that are shared between coords and mapping files
        sids_intersection = list(set(zip(*mapping_data)[0])&set(coords_headers))
        number_intersected_sids = len(sids_intersection)
        required_number_of_sids = len(coords_headers)

    if taxa_fp:
        try:
            # for summarized tables the "otu_ids" are really the "lineages"
            otu_sample_ids, lineages, otu_table, _ = parse_otu_table(open(
                taxa_fp, 'U'), count_map_f=float, remove_empty_rows=True)
        except ValueError, e:
            option_parser.error('There was a problem parsing the --taxa_fp: %s'%
                e.message)

        # make sure there are matching sample ids with the otu table
        if not len(list(set(sids_intersection)&set(otu_sample_ids))):
            option_parser.error('The sample identifiers in the OTU table must '
                'have at least one match with the data in the mapping file and '
                'with the coordinates file. Verify you are using input files '
                'that belong to the same dataset.')
    else:
        # empty lists indicate that there was no taxa file passed in
        otu_sample_ids, lineages, otu_table = [], [], []

    # sample ids must be shared between files
    if number_intersected_sids <= 0:
        option_parser.error('The sample identifiers in the coordinates file '
            'must have at least one match with the data contained in mapping '
            'file. Verify you are using a coordinates file and a mapping file '
            'that belong to the same dataset.')

    # the intersection of the sample ids in the coords and the sample ids in the
    # mapping file must at the very least include all ids in the coords file
    # Otherwise it isn't valid; unless --ignore_missing_samples is set True
    if number_intersected_sids != required_number_of_sids and\
        not ignore_missing_samples:
        option_parser.error('The metadata mapping file has fewer sample '
            'identifiers than the coordinates file. Verify you are using a '
            'mapping file that contains at least all the samples contained in '
            'the coordinates file(s). You can force the script to ignore these '
            ' samples by passing the \'--ignore_missing_samples\' flag.')

    # ignore samples that exist in the coords but not in the mapping file, note:
    # we're using sids_intersection so if --ignore_missing_samples is enabled we
    # account for unmapped coords, else the program will exit before this point
    header, mapping_data = filter_mapping_file(mapping_data, header,
        sids_intersection, include_repeat_cols=True)


    # catch the errors that could ocurr when filling the mapping file values
    if missing_custom_axes_values:
        try:
            # the fact that this uses parse_metadata_state_descriptions makes
            # the follwoing option '-x Category:7;PH:12' to work as well as the 
            # script-interface-documented '-x Category:7 -x PH:12' option
            mapping_data = fill_mapping_field_from_mapping_file(mapping_data,
                header, ';'.join(missing_custom_axes_values))
        except AssertionError, e:
            option_parser.error(e.message)
        except ValueError, e:
            option_parser.error(e.message)

    # extract a list of the custom axes provided and each element is numeric
    if custom_axes:
        custom_axes = custom_axes.strip().strip("'").strip('"').split(',')

        # the MetadataMap object makes some checks easier
        map_object = MetadataMap(mapping_file_to_dict(mapping_data, header), [])
        for axis in custom_axes:
            # append the field to the error queue that it belongs to
            if axis not in header:
                offending_fields.append(axis)
            if map_object.isNumericCategory(axis) == False:
                non_numeric_categories.append(axis)

    # check that all the required columns exist in the metadata mapping file
    if color_by_column_names:
        color_by_column_names = color_by_column_names.split(',')

        # check for all the mapping fields
        for col in color_by_column_names:
            if col not in header and '&&' not in col:
                offending_fields.append(col)
    else:
        # if the user didn't specify the header names display everything
        color_by_column_names = header[:]

    # terminate the program for the cases where a mapping field was not found
    # or when a mapping field didn't meet the criteria of being numeric
    if offending_fields:
        option_parser.error("Invalid field(s) '%s'; the valid field(s) are:"
            " '%s'" % (', '.join(offending_fields), ', '.join(header)))
    if non_numeric_categories:
        option_parser.error(('The following field(s): \'%s\' contains values '
            'that are not numeric, hence not suitable for \'--custom_axes\'. '
            'Try the \'--missing_custom_axes_values\' option to fix these '
            'values.' % ', '.join(non_numeric_categories)))

    # process the coordinates file first, preventing the case where the custom
    # axes is not in the coloring categories i. e. in the --colory_by categories
    coords_headers, coords_data, coords_eigenvalues, coords_pct, coords_low,\
        coords_high = preprocess_coords_file(coords_headers, coords_data,
        coords_eigenvalues, coords_pct, header, mapping_data, custom_axes,
        jackknifing_method=jackknifing_method)

    # process the otu table after processing the coordinates to get custom axes
    # (when available) or any other change that occurred to the coordinates
    otu_coords, otu_table, otu_lineages, otu_prevalence, lines =\
        preprocess_otu_table(otu_sample_ids, otu_table, lineages,
        coords_data, coords_headers, n_taxa_to_keep)

    # remove the columns in the mapping file that are not informative taking
    # into account the header names that were already authorized to be used
    # and take care of concatenating the fields for the && merged columns
    mapping_data, header = preprocess_mapping_file(mapping_data, header,
        color_by_column_names, unique=not add_unique_columns)

    # use the current working directory as default
    if opts.output_dir:
        create_dir(opts.output_dir,False)
        dir_path=opts.output_dir
    else:
        dir_path='./'

    fp_out = open(join(dir_path, 'index.html'),'w')
    fp_out.write(EMPEROR_HEADER_HTML_STRING)

    # write the html file
    fp_out.write(format_mapping_file_to_js(mapping_data, header, header))
    fp_out.write(format_pcoa_to_js(coords_headers, coords_data,
        coords_eigenvalues, coords_pct, custom_axes, coords_low, coords_high))
    fp_out.write(format_taxa_to_js(otu_coords, otu_lineages, otu_prevalence))
    fp_out.write(format_emperor_html_footer_string(taxa_fp != None,
        isdir(input_coords)))
    copy_support_files(dir_path)

    # write the bilot coords in the output file if a path is passed
    if biplot_fp:
        # make sure this file can be created
        try:
            fd = open(biplot_fp, 'w')
        except IOError:
            option_parser.error('There was a problem creating the file with'
                ' the coordinates for the biplots (%s).' % biplot_fp)
        fd.writelines(lines)
        fd.close()

if __name__ == "__main__":
    main()
