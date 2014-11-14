.. _make_emperor:

.. index:: make_emperor.py

*make_emperor.py* -- Create three dimensional PCoA plots
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Description:**

This script automates the creation  of three-dimensional PCoA plots to be visualized with Emperor using Google Chrome.


**Usage:** :file:`make_emperor.py [options]`

**Input Arguments:**

.. note::

	
	**[REQUIRED]**
		
	-i, `-`-input_coords
		Depending on the plot to be generated, can be one of the following: (1) Filepath of a coordinates file to create a PCoA plot. (2) Directory path to a folder containing coordinates files to create a jackknifed PCoA plot. (3) Directory path to a folder containing coordinates files to compare the coordinates there contained when --compare_plots is enabled (useful for procustes analysis plots). For directories: hidden files, sub-directories and files suffixed as '_procrustes_results.txt'
	-m, `-`-map_fp
		Path to a metadata mapping file
	
	**[OPTIONAL]**
		
	`-`-number_of_axes
		Number of axes to be incorporated in the plot. Only 3 will be displayed at any given time but this option modifies how many axes you can use for your visualization. Note that Emperor will only use the axes that explain more than 0.5% (this will be shown as 1% in the GUI)of the variability [default: 10]
	-a, `-`-custom_axes
		Comma-separated list of metadata categories to use as custom axes in the plot. For instance, if there is a time category and you would like to see the samples plotted on that axis instead of PC1, PC2, etc., you would pass time as the value of this option.  Note: if there is any non-numeric data in the metadata column, an error will be presented [default: None]
	`-`-add_unique_columns
		Add to the output categories of the mapping file the columns where all values are different. Note: if the result of one of the concatenated fields in --color_by is a column where all values are unique, the resulting column will get removed as well [default: False]
	`-`-add_vectors
		Comma-sparated category(ies) used to add connecting lines (vectors) between samples. The first category specifies the samples that will be connected by the vectors, whilst the second category (optionally) determines the order in which the samples will be connected. [default: [None, None]]
	-b, `-`-color_by
		Comma-separated list of metadata categories (column headers) to color by in the plots. The categories must match the name of a column header in the mapping file exactly. Multiple categories can be listed by comma separating them without spaces. The user can also combine columns in the mapping file by separating the categories by "&&" without spaces. [default=color by all categories except ones where all values are different, to disable this behaviour pass --add_unique_columns]
	`-`-biplot_fp
		Output filepath that will contain the coordinates where each taxonomic sphere is centered. [default: None]
	-c, `-`-compare_plots
		Passing a directory with the -i (--input_coords) option in combination with this flag results in a set of bars connecting the replicated samples across all the input files. [default=False]
	-e, `-`-ellipsoid_method
		Used only when plotting ellipsoids for jackknifed beta diversity (i.e. using a directory of coord files instead of a single coord file). Valid values are "IQR" (for inter-quartile ranges) and "sdev" (for standard deviation). [default=IQR]
	`-`-ignore_missing_samples
		This will overpass the error raised when the coordinates file contains samples that are not present in the mapping file. Be aware that this is very misleading as the PCoA is accounting for all the samples and removing some samples could lead to  erroneous/skewed interpretations.
	-n, `-`-n_taxa_to_keep
		Number of taxonomic groups from the "--taxa_fp" file to display. Passing "-1" will cause to display all the taxonomic groups, this option is only used when creating BiPlots. [default=10]
	-s, `-`-master_pcoa
		Used only when the input is a directory of coordinate files i. e. for jackknifed beta diversity plot or for a coordinate comparison plot (procrustes analysis). The coordinates in this file will be the center of each ellipsoid in the case of a jackknifed PCoA plot or the center where the connecting arrows originate from for a comparison plot. [default: arbitrarily selected file from the input directory for a jackknifed plot or None for a comparison plot in this case one file will be connected to the next one and so on]
	-t, `-`-taxa_fp
		Path to a summarized taxa file (i. e. the output of `summarize_taxa.py <./summarize_taxa.html>`_). This option is only used when creating BiPlots. [default=None]
	-x, `-`-missing_custom_axes_values
		Option to override the error shown when the catergory used in '--custom_axes' has non-numeric values in the mapping file. The basic format is custom_axis:new_value. For example, if you want to plot in time 0 all the samples that do not have a numeric value in the column Time. you would pass -x "Time:0". Additionally, you can pass this format custom_axis:other_column==value_in_other_column=new_value, with this format you can specify different values (new_value) to use in the substitution based on other column (other_column) value (value_in_other_column); see example above. This option could be used in all explicit axes.
	-o, `-`-output_dir
		Path to the output directory that will contain the PCoA plot. [default: emperor]
	`-`-number_of_segments
		The number of segments to generate any spheres, this includes the samples, the taxa (biplots), and the confidence intervals (jackknifing). Higher values will result in better quality but can make the plots less responsive, also it will make the resulting SVG images bigger. The value should be between 4 and 14. [default: 8]
	`-`-pct_variation_below_one
		Allow the percent variation explained by the axis to be below one. The default behaivor is to multiply by 100 all values if PC1 is < 1.0 [default: False]


**Output:**

This script creates an output directory with an HTML formated file named 'index.html' and a complementary folder named 'emperor_required_resources'. Opening index.html with Google's Chrome web browser will display a three dimensional visualization of the processed PCoA data file and the corresponding metadata mapping file.


**Plot PCoA data:**

Visualize the a PCoA file colored using a corresponding mapping file: 

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -o emperor_output

**Plot data generated from non-phylogenetic distance matrices:**

Visualize a PCoA file where the data was computed with a non-phylogenetic distance metric (Euclidian, Bray-Curtis, etc.)

::

	make_emperor.py -i euclidian_pc.txt -m Fasting_Map.txt -o euclidian

**Coloring by metadata mapping file:**

Additionally, using the supplied mapping file and a specific category or any combination of the available categories. When using the -b option, the user can specify the coloring for multiple header names, where each header is separated by a comma. The user can also combine mapping headers and color by the combined headers that are created by inserting an '&&' between the input header names. Color by 'Treatment' and by the result of concatenating the 'DOB' category and the 'Treatment' category: 

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -b 'Treatment&&DOB,Treatment' -o emperor_colored_by

**PCoA plot with an explicit axis:**

Create a PCoA plot with an axis of the plot representing the 'DOB' of the samples. This option is useful when presenting a gradient from your metadata e. g. 'Time' or 'pH': 

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -a DOB -o pcoa_dob

**PCoA plot with an explicit axis and using --missing_custom_axes_values:**

Create a PCoA plot with an axis of the plot representing the 'DOB' of the samples and define the position over the gradient of those samples missing a numeric value; in this case we are going to plot the samples in the value 20060000. You can select for each explicit axis which value you want to use for the missing values: 

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map_modified.txt -a DOB -o pcoa_dob_with_missing_custom_axes_values -x 'DOB:20060000'

**PCoA plot with an explicit axis and using --missing_custom_axes_values but setting different values based on another column:**

Create a PCoA plot with an axis of the plot representing the 'DOB' of the samples and defining the position over the gradient of those samples missing a numeric value but using as reference another column of the mapping file. In this case we are going to plot the samples that are Control on the Treatment column on 20080220 and on 20080240 those that are Fast:

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map_modified.txt -a DOB -o pcoa_dob_with_missing_custom_axes_with_multiple_values -x 'DOB:Treatment==Control=20080220' -x 'DOB:Treatment==Fast=20080240'

**Jackknifed principal coordinates analysis plot:**

Create a jackknifed PCoA plot (with confidence intervals for each sample) passing as the input a directory of coordinates files (where each file corresponds to a different OTU table) and use the standard deviation method to compute the dimensions of the ellipsoids surrounding each sample: 

::

	make_emperor.py -i unweighted_unifrac_pc -m Fasting_Map.txt -o jackknifed_pcoa -e sdev

**Jackknifed PCoA plot with a master coordinates file:**

Passing a master coordinates file (--master_pcoa) will display the ellipsoids centered by the samples in this file: 

::

	make_emperor.py -i unweighted_unifrac_pc -s unweighted_unifrac_pc/pcoa_unweighted_unifrac_rarefaction_110_5.txt -m Fasting_Map.txt -o jackknifed_with_master

**BiPlots:**

To see which taxa are the ten more prevalent in the different areas of the PCoA plot, you need to pass a summarized taxa file i. e. the output of `summarize_taxa.py <./summarize_taxa.html>`_. Note that if the the '--taxa_fp' has fewer than 10 taxa, the script will default to use all.

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -t otu_table_L3.txt -o biplot

**BiPlots with extra options:**

To see which are the three most prevalent taxa and save the coordinates where these taxa are centered, you can use the -n (number of taxa to keep) and the --biplot_fp (output biplot file path) options.

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -t otu_table_L3.txt -o biplot_options -n 3 --biplot_fp biplot.txt

**Drawing connecting lines between samples:**

To draw lines betwen samples within a category use the '--add_vectors' option. For example to connect the lines by the 'Treatment' category.

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -o vectors --add_vectors Treatment

**Drawing connecting lines between samples with an explicit axis:**

To draw lines between samples within a category of the mapping file and have them sorted by a category that's explicitly represented in the 3D plot use the '--add_vectors' and the '-a' option.

::

	make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt --add_vectors Treatment,DOB -a DOB -o sorted_by_DOB

**Compare two coordinate files:**

To draw replicates of the same samples like for a procustes plot.

::

	make_emperor.py -i compare -m Fasting_Map.txt --compare_plots -o comparison


