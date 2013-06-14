make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -o emperor_output
make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -b 'Treatment&&DOB,Treatment' -o emperor_colored_by
make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -a DOB -o pcoa_dob
make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map_modified.txt -a DOB -o pcoa_dob_with_missing_custom_axes_values -x 'DOB:20060000'
make_emperor.py -i unweighted_unifrac_pc -m Fasting_Map.txt -o jackknifed_pcoa -e sdev
make_emperor.py -i unweighted_unifrac_pc -s unweighted_unifrac_pc/pcoa_unweighted_unifrac_rarefaction_110_5.txt -m Fasting_Map.txt -o jackknifed_with_master
make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -t otu_table_L3.txt -o biplot
make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -t otu_table_L3.txt -o biplot_options -n 3 --biplot_fp biplot.txt
make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt -o vectors --add_vectors Treatment
make_emperor.py -i unweighted_unifrac_pc.txt -m Fasting_Map.txt --add_vectors Treatment,DOB -a DOB -o sorted_by_DOB