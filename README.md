Emperor
=======

[![Join the chat at https://gitter.im/biocore/emperor](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/biocore/emperor?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/biocore/emperor.png?branch=master)](https://travis-ci.org/biocore/emperor) [![Coverage Status](https://coveralls.io/repos/biocore/emperor/badge.svg)](https://coveralls.io/r/biocore/emperor)

Emperor is a next-generation tool for the analysis and visualization of large microbial ecology datasets; amongst many features Emperor provides a modern user interface that will rapidly adjust to your daily workflow.

To start using Emperor, please refer to the [installation notes](INSTALL.md).

Before contributing code to Emperor, please familiarize yourself with the [contributing guidelines](CONTRIBUTING.md).

## Usage examples

The main interface to create Emperor visualizations is the `make_emperor.py` script, inputing a mapping file and a PCoA data file, will generate an Emperor graphical user interface to analyze and visualize your data.

If you have a QIIME compliant mapping file and a PCoA file, try the following command from a terminal session:

```bash
make_emperor.py -i unweighted_unifrac_pc.txt -m mapping_file.txt
```

That command will create a new directory called emperor, there you will find a file called `index.html` open it with Google Chrome to start visualizing and interacting with your data.

Similarly if you have a study expressed over a gradient, for example a study where you have multiple samples over time, you can use this metadata with your visualization using the `-a` option:

```bash
make_emperor.py -i unweighted_unifrac_pc_time.txt -m mapping_with_time.txt -a TIMEPOINT
```

Some build examples are bundled with every Emperor repository, you can begin exploring some sample data using **Google Chrome**:

- To see an example of a simple PCoA plot, see this [link](http://emperor.microbio.me/master/make_emperor/emperor_output/index.html).
- To see an example of a Jackknifed plot, see this [link](http://emperor.microbio.me/master/make_emperor/jackknifed_pcoa/index.html).
- To see an example of a PCoA Biplot, see this [link](http://emperor.microbio.me/master/make_emperor/biplot/index.html).
- To see an example of a PCoA plot with connecting lines between samples, see this [link](http://emperor.microbio.me/master/make_emperor/vectors/index.html).
- To see an example of a PCoA plot with connecting lines between samples and an explicit axis, see this [link](http://emperor.microbio.me/master/make_emperor/sorted_by_DOB/index.html).
