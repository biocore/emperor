#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import division

from os import makedirs
from os.path import join, isdir

from qcli.option_parsing import parse_command_line_parameters, make_option
from skbio.util import flatten

from emperor.qiime_backports.filter import filter_mapping_file
from emperor.qiime_backports.parse import (parse_mapping_file,
                                           mapping_file_to_dict,
                                           parse_otu_table, QiimeParseError)
from emperor.qiime_backports.util import MetadataMap
from emperor.biplots import preprocess_otu_table
from emperor.sort import sort_comparison_filenames
from emperor.filter import keep_samples_from_pcoa_data
from emperor.util import (copy_support_files, preprocess_mapping_file,
                          preprocess_coords_file,
                          fill_mapping_field_from_mapping_file,
                          EmperorInputFilesError, guess_coordinates_files)
from emperor.format import (format_taxa_to_js, format_vectors_to_js,
                            format_emperor_html_footer_string,
                            format_mapping_file_to_js,
                            format_pcoa_to_js,
                            format_comparison_bars_to_js,
                            EmperorLogicError,
                            format_emperor_autograph)
from emperor._format_strings import EMPEROR_HEADER_HTML_STRING
from emperor.parse import parse_coords
from emperor import __version__


script_info = {}

script_info['brief_description'] = "Create three dimensional PCoA plots"
script_info['script_description'] = ("This script automates the creation of "
                                     "three-dimensional PCoA plots to be "
                                     "visualized with Emperor using Google "
                                     "Chrome.")
script_info['script_usage'] = [
    ("Plot PCoA data",

     "Visualize the a PCoA file colored using a corresponding mapping file: ",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -o emperor_output"
     ),

    ("Plot data generated from non-phylogenetic distance matrices",

     "Visualize a PCoA file where the data was computed with a "
     "non-phylogenetic distance metric (Euclidian, Bray-Curtis, etc.)",

     "%prog -i euclidian_pc.txt -m Fasting_Map.txt -o euclidian"
     ),

    ("Coloring by metadata mapping file",

     "Additionally, using the supplied mapping file and a specific category "
     "or any combination of the available categories. When using the -b "
     "option, the user can specify the coloring for multiple header names, "
     "where each header is separated by a comma. The user can also combine "
     "mapping headers and color by the combined headers that are created by "
     "inserting an '&&' between the input header names. Color by 'Treatment' "
     "and by the result of concatenating the 'DOB' category and the "
     "'Treatment' category: ",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -b "
     "'Treatment&&DOB,Treatment' -o emperor_colored_by"
     ),

    ("PCoA plot with an explicit axis",

     "Create a PCoA plot with an axis of the plot representing the 'DOB' of "
     "the samples. This option is useful when presenting a gradient from your "
     "metadata e. g. 'Time' or 'pH': ",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -a DOB -o "
     "pcoa_dob"
     ),

    ("PCoA plot with an explicit axis and using --missing_custom_axes_values",

     "Create a PCoA plot with an axis of the plot representing the 'DOB' of "
     "the samples and define the position over the gradient of those samples "
     "missing a numeric value; in this case we are going to plot the samples "
     "in the value 20060000. You can select for each explicit axis which "
     "value you want to use for the missing values: ",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map_modified.txt -a DOB "
     "-o pcoa_dob_with_missing_custom_axes_values -x 'DOB:20060000'"
     ),

    ("PCoA plot with an explicit axis and using --missing_custom_axes_values "
     "but setting different values based on another column",

     "Create a PCoA plot with an axis of the plot representing the 'DOB' of "
     "the samples and defining the position over the gradient of those "
     "samples missing a numeric value but using as reference another column "
     "of the mapping file. In this case we are going to plot the samples that "
     "are Control on the Treatment column on 20080220 and on 20080240 those "
     "that are Fast:",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map_modified.txt -a DOB "
     "-o pcoa_dob_with_missing_custom_axes_with_multiple_values -x "
     "'DOB:Treatment==Control=20080220' -x 'DOB:Treatment==Fast=20080240'"
     ),

    ("Jackknifed principal coordinates analysis plot",

     "Create a jackknifed PCoA plot (with confidence intervals for each "
     "sample) passing as the input a directory of coordinates files (where "
     "each file corresponds to a different OTU table) and use the standard "
     "deviation method to compute the dimensions of the ellipsoids "
     "surrounding each sample: ",

     "%prog -i unweighted_unifrac_pc -m Fasting_Map.txt -o "
     "jackknifed_pcoa -e sdev"
     ),

    ("Jackknifed PCoA plot with a master coordinates file",

     "Passing a master coordinates file (--master_pcoa) will display the "
     "ellipsoids centered by the samples in this file: ",

     "%prog -i unweighted_unifrac_pc -s "
     "unweighted_unifrac_pc/pcoa_unweighted_unifrac_rarefaction_110_5.txt -m "
     "Fasting_Map.txt -o jackknifed_with_master"
     ),

    ("BiPlots",

     "Create a distance biplot to visualize where samples and taxa are in "
     "PCoA space.  The cosine of the angle between taxanomic vectors "
     "approximates the correlation of those two taxa. The length of each of "
     "the taxonomic vectors approximates the variance of each taxa throughout "
     "all of the samples.  The direction of the taxanomic vector explains the "
     "variance of all of the samples along that direction. "
     "To see which taxa are the ten more prevalent in the different "
     "areas of the PCoA plot, you need to pass a summarized taxa file i.e. "
     "the output of summarize_taxa.py. Note that if the the '--taxa_fp' has "
     "fewer than 10 taxa, the script will default to use all.",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -t "
     "otu_table_L3.txt -o biplot"
     ),

    ("BiPlots with extra options",

     "To see which are the three most prevalent taxa and save the coordinates "
     "where these taxa are centered, you can use the -n (number of taxa to "
     "keep) and the --biplot_fp (output biplot file path) options.",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -t "
     "otu_table_L3.txt -o biplot_options -n 3 --biplot_fp biplot.txt"
     ),

    ("Drawing connecting lines between samples",

     "Tao draw lines betwen samples within a category use the '--add_vectors' "
     "option. For example to connect the lines by the 'Treatment' category.",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -o vectors "
     "--add_vectors Treatment"
     ),

    ("Drawing connecting lines between samples with an explicit axis",

     "To draw lines between samples within a category of the mapping file and "
     "have them sorted by a category that's explicitly represented in the 3D "
     "plot use the '--add_vectors' and the '-a' option.",

     "%prog -i unweighted_unifrac_pc.txt -m Fasting_Map.txt --add_vectors "
     "Treatment,DOB -a DOB -o sorted_by_DOB"
     ),

    ("Compare two coordinate files",

     "To draw replicates of the same samples like for a procustes plot.",

     "%prog -i compare -m Fasting_Map.txt --compare_plots -o comparison"
     )]

script_info['output_description'] = \
    ("This script creates an output directory with an HTML formated file "
     "named 'index.html' and a complementary folder named "
     "'emperor_required_resources'. Opening index.html with Google's Chrome "
     "web browser will display a three dimensional visualization of the "
     "processed PCoA data file and the corresponding metadata mapping file.")
script_info['required_options'] = [
    make_option('-i', '--input_coords', type="existing_path",
                help=("Depending on the plot to be generated, can be one of "
                      "the following: (1) Filepath of a coordinates file to "
                      "create a PCoA plot. (2) Directory path to a folder "
                      "containing coordinates files to create a jackknifed "
                      "PCoA plot. (3) Directory path to a folder containing "
                      "coordinates files to compare the coordinates there "
                      "contained when --compare_plots is enabled (useful for "
                      "procustes analysis plots). For directories: hidden "
                      "files, sub-directories, 'Icon?' and files suffixed by "
                      "'_procrustes_results.txt' will be ignored.")),
    make_option('-m', '--map_fp', type="existing_filepath",
                help='path to a metadata mapping file')
]

script_info['optional_options'] = [
    make_option('--number_of_axes', type=int,
                help=("Number of axes to be incorporated in the plot. Only 3 "
                      "will be displayed at any given time but this option "
                      "modifies how many axes you can use for your "
                      "visualization. Note that Emperor will only use the "
                      "axes that explain more than 0.5% (this will be shown "
                      "as 1% in the GUI)of the variability [default: "
                      "%default]"),
                default=10),
    make_option('-a', '--custom_axes', type='string',
                help=("Comma-separated list of metadata categories to use as "
                      "custom axes in the plot. For instance, if there is a "
                      "time category and you would like to see the samples "
                      "plotted on that axis instead of PC1, PC2, etc., you "
                      "would pass time as the value of this option.  Note: if "
                      "there is any non-numeric data in the metadata column, "
                      "an error will be presented [default: %default]"),
                default=None),
    make_option('--add_unique_columns', action="store_true",
                help=('Add to the output categories of the mapping file the '
                      'columns where all values are different. Note: if the '
                      'result of one of the concatenated fields in --color_by '
                      'is a column where all values are unique, the resulting '
                      'column will get removed as well [default: %default]'),
                default=False),
    make_option('--add_vectors', type='string', dest='add_vectors',
                help=('Comma-sparated category(ies) used to add connecting '
                      'lines (vectors) between samples. The first category '
                      'specifies the samples that will be connected by the '
                      'vectors, whilst the second category (optionally) '
                      'determines the order in which the samples will be '
                      'connected. [default: %default]'), default=[None, None]),
    make_option('-b', '--color_by', dest='color_by', type='string',
                help=('Comma-separated list of metadata categories (column '
                      'headers) to color by in the plots. The categories must '
                      'match the name of a column header in the mapping file '
                      'exactly. Multiple categories can be listed by comma '
                      'separating them without spaces. The user can also '
                      'combine columns in the mapping file by separating the '
                      'categories by "&&" without spaces. [default=color by '
                      'all categories except ones where all values are '
                      'different, to disable this behaviour pass '
                      '--add_unique_columns]'),
                default=None),
    make_option('--biplot_fp', type='new_filepath',
                help=('Output filepath that will contain the coordinates '
                      'where each taxonomic sphere is centered. [default: '
                      '%default]'),
                default=None),
    make_option('-c', '--compare_plots', dest='compare_plots',
                action='store_true', default=False,
                help=('Passing a directory with the -i (--input_coords) '
                      'option in combination with this flag results in a set '
                      'of bars connecting the replicated samples across all '
                      'the input files. [default=%default]')),
    make_option('-e', '--ellipsoid_method',
                help=('Used only when plotting ellipsoids for jackknifed beta '
                      'diversity (i.e. using a directory of coord files '
                      'instead of a single coord file). Valid values are '
                      '"IQR" (for inter-quartile ranges) and "sdev" (for '
                      'standard deviation). [default=%default]'),
                default='IQR', type='choice', choices=['IQR', 'sdev']),
    make_option('--ignore_missing_samples', action='store_true', default=False,
                help=('This will overpass the error raised when the '
                      'coordinates file contains samples that are not present '
                      'in the mapping file. Be aware that this is very '
                      'misleading as the PCoA is accounting for all the '
                      'samples and removing some samples could lead to '
                      'erroneous/skewed interpretations.')),
    make_option('-n', '--n_taxa_to_keep', default=10, type='int',
                help=('Number of taxonomic groups from the "--taxa_fp" file '
                      'to display. Passing "-1" will cause to display all the '
                      'taxonomic groups, this option is only used when '
                      'creating BiPlots. [default=%default]')),
    make_option('-s', '--master_pcoa',
                help=('Used only when the input is a directory of coordinate '
                      'files i. e. for jackknifed beta diversity plot or '
                      'for a coordinate comparison plot (procrustes '
                      'analysis). The coordinates in this file will be the '
                      'center of each ellipsoid in the case of a jackknifed '
                      'PCoA plot or the center where the connecting arrows '
                      'originate from for a comparison plot. [default: '
                      'arbitrarily selected file from the input directory for '
                      'a jackknifed plot or None for a comparison plot in '
                      'this case one file will be connected to the next one '
                      'and so on]'), default=None, type='existing_filepath'),
    make_option('-t', '--taxa_fp', default=None, type='existing_filepath',
                help=('Path to a summarized taxa file (i.e. the output of '
                      'summarize_taxa.py). This option is only used when '
                      'creating BiPlots. [default=%default]')),
    make_option('-x', '--missing_custom_axes_values',
                help=('Option to override the error shown when the catergory '
                      'used in \'--custom_axes\' has non-numeric values in '
                      'the mapping file. The basic format is '
                      'custom_axis:new_value. For example, if you want to '
                      'plot in time 0 all the samples that do not have a '
                      'numeric value in the column Time. you would pass -x '
                      '"Time:0". Additionally, you can pass this format '
                      'custom_axis:other_col==value_in_other_col=new_value, '
                      'with this format you can specify different values '
                      '(new_value) to use in the substitution based on other '
                      'column (other_column) value (value_in_other_column); '
                      'see example above. This option could be used in all '
                      'explicit axes.'), action='append', default=None),
    make_option('-o', '--output_dir', type="new_dirpath", default='emperor',
                help=('path to the output directory that will contain the '
                      'PCoA plot. [default: %default]')),
    make_option('--number_of_segments', type="int", default=8,
                help=('The number of segments to generate any spheres, this '
                      'includes the samples, the taxa (biplots), and the '
                      'confidence intervals (jackknifing). Higher values will '
                      'result in better quality but can make the plots less '
                      'responsive, also it will make the resulting SVG images '
                      'bigger. The value should be between 4 and 14. '
                      '[default: %default]')),
    make_option('--pct_variation_below_one', action="store_true",
                help=('Allow the percent variation explained by the axis to '
                      'be below one. The default behaivor is to multiply by '
                      '100 all values if PC1 is < 1.0 [default: %default]'),
                default=False),
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
    add_vectors = opts.add_vectors
    verbose_output = opts.verbose
    number_of_axes = opts.number_of_axes
    compare_plots = opts.compare_plots
    number_of_segments = opts.number_of_segments
    pct_variation_below_one = opts.pct_variation_below_one

    # add some metadata to the output
    emperor_autograph = format_emperor_autograph(map_fp, input_coords, 'HTML')

    # verifying that the number of axes requested is greater than 3
    if number_of_axes < 3:
        option_parser.error(('You need to plot at least 3 axes.'))

    # verifying that the number of segments is between the desired range
    if not (4 <= number_of_segments <= 14):
        option_parser.error(('number_of_segments should be between 4 and 14.'))

    # append headernames that the script didn't find in the mapping file
    # according to different criteria to the following variables
    offending_fields = []
    non_numeric_categories = []

    serial_comparison = True

    # can't do averaged pcoa plots _and_ custom axes in the same plot
    if custom_axes is not None and isdir(input_coords):
        if custom_axes.count(',') > 0:
            option_parser.error(('Jackknifed plots are limited to one custom '
                                 'axis, currently trying to use: %s. Make '
                                 'sure you use only one.' % custom_axes))

    # make sure the flag is not misunderstood from the command line interface
    if not isdir(input_coords) and compare_plots:
        option_parser.error("Cannot use the '--compare_plots' flag unless the "
                            "input path is a directory.")

    # before creating any output, check correct parsing of the main input files
    try:
        mapping_data, header, comments = parse_mapping_file(open(map_fp, 'U'))

    except Exception:
        option_parser.error(("The metadata mapping file '%s' does not seem "
                             "to be formatted correctly, verify the "
                             "formatting is QIIME compliant by using "
                             "validate_mapping_file.py") % map_fp)
    else:
        # use this set variable to make presence/absensce checks faster
        lookup_header = set(header)
        mapping_ids = {row[0] for row in mapping_data}

    # dir means jackknifing or coordinate comparison type of processing
    if isdir(input_coords):
        offending_coords_fp = []
        coords_headers = []
        coords_data = []
        coords_eigenvalues = []
        coords_pct = []

        coord_fps = guess_coordinates_files(input_coords)

        # QIIME generates folders of transformed coordinates for the specific
        # purpose of connecting all coordinates to a set of origin coordinates.
        # The name of this file is suffixed as _transformed_reference.txt
        trans_suf = '_transformed_reference.txt'
        transformed = [f for f in coord_fps if f.endswith(trans_suf)]

        # this could happen and we rather avoid this problem
        if len(coord_fps) == 0:

            option_parser.error('Could not use any of the files in the input '
                                'directory.')

        # the master pcoa must be the first in the list of coordinates; however
        # if the visualization is not a jackknifed plot this gets ignored
        if master_pcoa and not compare_plots:
            if master_pcoa in coord_fps:  # remove it if duplicated
                coord_fps.remove(master_pcoa)
            coord_fps = [master_pcoa] + coord_fps  # prepend it to the list
        # passing a master file means that the comparison is not serial
        elif master_pcoa and compare_plots:
            serial_comparison = False

            # guarantee that the master is the first and is not repeated
            if master_pcoa in coord_fps:
                coord_fps.remove(master_pcoa)
                sorted_filenames = sort_comparison_filenames(coord_fps)
                coord_fps = [master_pcoa] + sorted_filenames

        elif master_pcoa is None and len(transformed):
            master_pcoa = transformed[0]
            serial_comparison = False

            # Note: the following steps are to guarantee consistency.
            # remove the master from the list and re-add it as a first element
            # the rest of the files must be sorted alphabetically so the result
            # will be: ['unifrac_transformed_reference.txt',
            # 'unifrac_transformed_q1.txt', 'unifrac_transformed_q2.txt'] etc
            coord_fps.remove(master_pcoa)
            coord_fps = [master_pcoa] + sort_comparison_filenames(coord_fps)

        for fp in coord_fps:
            try:
                parsed = parse_coords(open(fp, 'U'))
            except (ValueError, QiimeParseError):
                offending_coords_fp.append(fp)

                # do not add any of the data and move along
                continue
            else:
                # pack all the data correspondingly only if it was correctly
                # parsed
                coords_headers.append(parsed[0])
                coords_data.append(parsed[1])
                coords_eigenvalues.append(parsed[2])
                coords_pct.append(parsed[3])

        # in case there were files that couldn't be parsed
        if offending_coords_fp:
            errout = ', '.join(offending_coords_fp)
            option_parser.error(("The following file(s): '%s' could not be "
                                 "parsed properly. Make sure the input folder "
                                 "only contains coordinates files.") % errout)

        # check all files contain the same sample identifiers by flattening the
        # list of available sample ids and returning the sample ids that are
        # in one of the sets of sample ids but not in the globablly shared ids
        _coords_headers = set(flatten(coords_headers))
        _per_file_missing = [_coords_headers - set(e) for e in coords_headers]
        non_shared_ids = set(flatten(_per_file_missing))
        if non_shared_ids:
            errout = ', '.join(non_shared_ids)
            option_parser.error(("The following sample identifier(s): '%s' "
                                 "are not shared between all the files. The "
                                 "files used to make a jackknifed PCoA plot "
                                 "or coordinate comparison plot (procustes "
                                 "plot) must share all the same sample "
                                 "identifiers between each other.") % errout)

        # number of samples ids that are shared between coords and mapping
        # files
        sids_intersection = mapping_ids.intersection(_coords_headers)

        # sample ids that are not mapped but are in the coords
        sids_difference = _coords_headers.difference(mapping_ids)

        # used to perform different validations in the script, very similar for
        # the case where the input is not a directory
        number_intersected_sids = len(sids_intersection)
        required_number_of_sids = len(coords_headers[0])

    else:
        try:
            parsed = parse_coords(open(input_coords, 'U'))
        # this exception was noticed when there were letters in the coords file
        # other exeptions should be catched here; code will be updated then
        except (ValueError, QiimeParseError):
            option_parser.error(("The PCoA file '%s' does not seem to be a "
                                 "coordinates formatted file, verify by "
                                 "manually inspecting the contents.") %
                                input_coords)
        else:
            coords_headers = parsed[0]
            coords_data = parsed[1]
            coords_eigenvalues = parsed[2]
            coords_pct = parsed[3]

        # number of samples ids that are shared between coords and mapping
        # files
        sids_intersection = mapping_ids.intersection(coords_headers)

        # sample ids that are not mapped but are in the coords
        sids_difference = set(coords_headers).difference(mapping_ids)

        number_intersected_sids = len(sids_intersection)
        required_number_of_sids = len(coords_headers)

    if taxa_fp:
        try:
            # This should really use BIOM's Table.from_tsv
            # for summarized tables the "otu_ids" are really the "lineages"
            parsed = parse_otu_table(open(taxa_fp, 'U'), count_map_f=float,
                                     remove_empty_rows=True)
        except ValueError, e:
            option_parser.error(("There was a problem parsing the --taxa_fp: "
                                 "%s" % e.message))
        else:
            otu_sample_ids = parsed[0]
            lineages = parsed[1]
            otu_table = parsed[2]

        # make sure there are matching sample ids with the otu table
        if not sids_intersection.issuperset(otu_sample_ids):
            option_parser.error("The sample identifiers in the OTU table must "
                                "have at least one match with the data in the "
                                "mapping file and with the coordinates file. "
                                "Verify you are using input files that belong "
                                "to the same dataset.")
        if len(lineages) <= 1:
            option_parser.error("Contingency tables with one or fewer rows "
                                "are not supported, please try passing a "
                                "contingency table with more than one row.")
    else:
        # empty lists indicate that there was no taxa file passed in
        otu_sample_ids, lineages, otu_table = [], [], []

    # sample ids must be shared between files
    if number_intersected_sids <= 0:
        option_parser.error('None of your sample identifiers match between the'
                            ' mapping file and the coordinates file. Verify '
                            'you are using a coordinates file and a mapping '
                            'file that belong to the same dataset.')

    # the intersection of the sample ids in the coords and the sample ids in
    # the mapping file must at the very least include all ids in the coords
    # file Otherwise it isn't valid; unless --ignore_missing_samples is set
    # True
    if number_intersected_sids != required_number_of_sids:
        if ignore_missing_samples:
            # keep only the samples that are mapped in the mapping file
            coords_headers, coords_data = keep_samples_from_pcoa_data(
                coords_headers, coords_data, sids_intersection)
        else:
            message = ("The metadata mapping file has fewer sample "
                       "identifiers than the coordinates file. Verify you are "
                       "using a mapping file that contains at least all the "
                       "samples contained in the coordinates file(s). You can "
                       "force the script to ignore these samples by passing "
                       "the '--ignore_missing_samples' flag.")

            if verbose_output:
                missing_ids = ', '.join(sids_difference)
                message += ' Offending sample identifier(s): %s.' % missing_ids

            option_parser.error(message)

    # ignore samples that exist in the coords but not in the mapping file,
    # note: we're using sids_intersection so if --ignore_missing_samples is
    # enabled we account for unmapped coords, else the program will exit before
    # this point
    header, mapping_data = filter_mapping_file(mapping_data, header,
                                               sids_intersection,
                                               include_repeat_cols=True)

    # catch the errors that could occur when filling the mapping file values
    if missing_custom_axes_values:
        # the fact that this uses parse_metadata_state_descriptions makes the
        # following option '-x Category:7;PH:12' to work as well as the
        # script-interface-documented '-x Category:7 -x PH:12' option
        for val in missing_custom_axes_values:
            if ':' not in val:
                option_parser.error("Not valid missing value for custom "
                                    "axes: %s" % val)
        _mcav = ';'.join(missing_custom_axes_values)
        try:
            mapping_data = fill_mapping_field_from_mapping_file(mapping_data,
                                                                header, _mcav)
        except AssertionError, e:
            option_parser.error(e.message)
        except EmperorInputFilesError, e:
            option_parser.error(e.message)

    # check that all the required columns exist in the metadata mapping file
    if color_by_column_names:
        color_by_column_names = color_by_column_names.split(',')

        # check for all the mapping fields
        for col in color_by_column_names:
            # for concatenated columns check each individual field
            parts = col.split('&&')
            offending_fields.extend(p for p in parts if p not in lookup_header)
    else:
        # if the user didn't specify the header names display everything
        color_by_column_names = [None]

    # extract a list of the custom axes provided and each element is numeric
    if custom_axes:
        custom_axes = custom_axes.strip().strip("'").strip('"').split(',')

        # the MetadataMap object makes some checks easier
        map_object = MetadataMap(mapping_file_to_dict(mapping_data, header),
                                 [])
        for axis in custom_axes:
            # append the field to the error queue that it belongs to
            if axis not in lookup_header:
                offending_fields.append(axis)
                break
            # make sure this value is in the mapping file
            elif axis not in color_by_column_names:
                color_by_column_names.append(axis)
        # perform only if the for loop does not call break
        else:
            # make sure all these axes are numeric
            for axis in custom_axes:
                if not map_object.isNumericCategory(axis):
                    non_numeric_categories.append(axis)

    # make multiple checks for the add_vectors option
    if add_vectors != [None, None]:
        add_vectors = add_vectors.split(',')
        # check there are at the most two categories specified for this option
        if len(add_vectors) > 2:
            option_parser.error("The '--add_vectors' option can accept up to "
                                "two different fields from the mapping file; "
                                "currently trying to use %d (%s)." %
                                (len(add_vectors), ', '.join(add_vectors)))
        # make sure the field(s) exist
        for col in add_vectors:
            # concatenated fields are allowed now so check for each field
            if '&&' in col:
                for _col in col.split('&&'):
                    if _col not in lookup_header:
                        offending_fields.append(col)
                        break
                # only execute this block of code if all checked fields exist
                else:
                    # make sure that if it's going to be used for vector
                    # creation it gets used for coloring and map postprocessing
                    if col not in color_by_column_names:
                        color_by_column_names.append(col)
            # if it's a column without concatenations
            elif col not in lookup_header:
                offending_fields.append(col)
                break
            else:
                # check this vector value is in the color by category
                if col not in color_by_column_names:
                    color_by_column_names.append(col)
        # perform only if the for loop does not call break
        else:
            # check that the second category is all with numeric values
            if len(add_vectors) == 2:
                map_object = MetadataMap(mapping_file_to_dict(mapping_data,
                                                              header),
                                         [])
                # if it has non-numeric values add it to the list of offenders
                if not map_object.isNumericCategory(add_vectors[1]):
                    msg = add_vectors[1] + '(used in --add_vectors)'
                    non_numeric_categories.append(msg)
            else:
                add_vectors.append(None)

    # terminate the program for the cases where a mapping field was not found
    # or when a mapping field didn't meet the criteria of being numeric
    if offending_fields:
        option_parser.error("Invalid field(s) '%s'; the valid field(s) are: "
                            "'%s'" % (', '.join(offending_fields),
                                      ', '.join(header)))
    if non_numeric_categories:
        option_parser.error(("The following field(s): '%s' contain values "
                             "that are not numeric, hence not suitable for "
                             "'--custom_axes' nor for '--add_vectors'. Try "
                             "the '--missing_custom_axes_values' option to "
                             "fix these values." %
                             ', '.join(non_numeric_categories)))

    # process the coordinates file first, preventing the case where the custom
    # axes is not in the coloring categories i. e. in the --colory_by
    # categories
    preprocessed_coords = preprocess_coords_file(coords_headers, coords_data,
                                                 coords_eigenvalues,
                                                 coords_pct, header,
                                                 mapping_data, custom_axes,
                                                 jackknifing_method,
                                                 compare_plots,
                                                 pct_variation_below_one)
    coords_headers = preprocessed_coords[0]
    coords_data = preprocessed_coords[1]
    coords_eigenvalues = preprocessed_coords[2]
    coords_pct = preprocessed_coords[3]
    coords_low = preprocessed_coords[4]
    coords_high = preprocessed_coords[5]
    clones = preprocessed_coords[6]

    # process the otu table after processing the coordinates to get custom axes
    # (when available) or any other change that occurred to the coordinates
    preprocessed_otu_table = preprocess_otu_table(otu_sample_ids, otu_table,
                                                  lineages, coords_data,
                                                  coords_headers,
                                                  n_taxa_to_keep)
    otu_coords = preprocessed_otu_table[0]
    otu_table = preprocessed_otu_table[1]
    otu_lineages = preprocessed_otu_table[2]
    otu_prevalence = preprocessed_otu_table[3]
    lines = preprocessed_otu_table[4]

    # remove the columns in the mapping file that are not informative taking
    # into account the header names that were already authorized to be used
    # and take care of concatenating the fields for the && merged columns
    mapping_data, header = preprocess_mapping_file(mapping_data, header,
                                                   color_by_column_names,
                                                   not add_unique_columns,
                                                   clones=clones)

    # create the output directory before creating any other output
    if not isdir(opts.output_dir):
        makedirs(opts.output_dir)

    fp_out = open(join(output_dir, 'index.html'), 'w')
    fp_out.write(emperor_autograph+'\n')
    fp_out.write(EMPEROR_HEADER_HTML_STRING)

    # write the html file
    fp_out.write(format_mapping_file_to_js(mapping_data, header, header))

    # certain percents being explained cannot be displayed in the GUI
    try:
        fp_out.write(format_pcoa_to_js(coords_headers, coords_data,
                                       coords_pct, custom_axes, coords_low,
                                       coords_high,
                                       number_of_axes=number_of_axes,
                                       number_of_segments=number_of_segments))
    except EmperorLogicError, e:
        option_parser.error(e.message)

    fp_out.write(format_taxa_to_js(otu_coords, otu_lineages, otu_prevalence))
    fp_out.write(format_vectors_to_js(mapping_data, header, coords_data,
                                      coords_headers, add_vectors[0],
                                      add_vectors[1]))
    fp_out.write(format_comparison_bars_to_js(coords_data, coords_headers,
                                              clones, serial_comparison))
    has_taxa = taxa_fp is not None
    has_input_coords = isdir(input_coords) and not compare_plots
    has_add_vectors = add_vectors != [None, None]
    has_clones = clones > 0
    fp_out.write(format_emperor_html_footer_string(has_taxa, has_input_coords,
                                                   has_add_vectors,
                                                   has_clones))
    fp_out.close()
    copy_support_files(output_dir)

    # write the biplot coords in the output file if a path is passed
    if biplot_fp and taxa_fp:
        if biplot_fp.endswith('/') or isdir(biplot_fp):
            option_parser.error("Do not specify a path to a new (path ending "
                                "in a slash) or existing directory for "
                                "biplot_fp. The output file will be a "
                                "tab-delimited text file.")

        # make sure this file can be created
        try:
            fd = open(biplot_fp, 'w')
        except IOError:
            option_parser.error("There was a problem creating the file with "
                                "the coordinates for the biplots (%s)."
                                % biplot_fp)
        else:
            fd.writelines(lines)
            fd.close()


if __name__ == "__main__":
    main()
