Emperor ChangeLog
=================

# Emperor 1.0.4-dev (changes since 1.0.4 go here)

### Bug Fixes

### New Features

### Miscellaneous

* Pin `notebook<7` for CI workflow.
* Update Python unit tests for new Pandas versions.
* Remove EOL Python version `3.7` from test matrix in CI workflow.
* Apply a workaround (`OPENSSL_CONF=/dev/null`) for running PhantomJS on `ubuntu-latest` in CI workflow.


# Emperor 1.0.4 (10 Jul 2023)
-----------------------------

### Bug Fixes

* Update remote URL to no longer use rawgit.
  ([#751](https://github.com/biocore/emperor/issues/751)).

### New Features

* Add `Toggle Visible` button to `Visibility` tab.

### Miscellaneous

* Pin Sphinx version to be less than 4.0.
* Jupyter templates no longer require jQuery to add the CSS headers.
* Limit jinja2 version for doc dependencies in setup.py. Allowed versions are: `>=2.9` and `<3.1`.
* Fix broken test suite with Pandas >=1.5 ([#810](https://github.com/biocore/emperor/issues/810)).

# Emperor 1.0.3 (14 Apr 2021)
-----------------------------

### Bug Fixes

* Fix a bug causing slight inaccuracies in how color gradients were drawn
  ([#788](https://github.com/biocore/emperor/issues/788)).

### New Features

* Added a new "info" attribute to display statistics
  and other pertinent information directly on emperor
  plot.

### Miscellaneous

* Fix wording in the README slightly; update a link to QIIME 2's documentation.


# Emperor 1.0.2 (20 Nov 2020)
-----------------------------

### Bug Fixes

* Fix a bug with `scatterplot`.

### New Features

* Add support for synchronized animations with Empress.

### Miscellaneous

* Add testing for Python 3.8 and drop support for Python 3.5.

# Emperor 1.0.1 (22 Jun 2020)
-----------------------------

### Bug Fixes
* Fix "incomplete" interpolation when using sequential / diverging color maps
  (e.g. `viridis`) and when not using the `Continuous values` option
  ([#760](https://github.com/biocore/emperor/issues/760))
* Make the order consistent between color assignment and sorting in the legend
  ([#761](https://github.com/biocore/emperor/issues/761))
* Update the Chroma.js version to v2.1.0 from v1.1.1; this resulted in some
  very slight precision differences in things like color interpolation
  ([#762](https://github.com/biocore/emperor/issues/762))
* Fix issue failing to correctly load axes settings.
* Fix issue where biplots and parallel plots would not work well together
  ([#747](https://github.com/biocore/emperor/issues/747)).

### New features

* Add sample selection support. Users can select samples by holding shift and
  dragging the mouse. Selected samples are copied to the users' clipboard
  ([#153](https://github.com/biocore/emperor/issues/153)).
* Add callback support for multiple grid events.

### Miscellaneous

* Updated THREE.js and plugins to the latest version (r116).

# Emperor 1.0.0 (13 Feb 2020)
-----------------------------

Introducing Emperor 1.0.0, an improved and new version of Emperor. Including
a stable Python API and JavaScript API.

Emperor 0.9.61 (11 Apr 2018)
----------------------------

* Maintenance release ([#631](https://github.com/biocore/emperor/issues/631)).

Emperor 0.9.60 (2 Nov 2016)
---------------------------

### Bug Fixes
* Fix problem where the taxonomic vectors weren't scaled properly when the scale coordinates button was toggled  ([#386](https://github.com/biocore/emperor/issues/373).
* Fix problem where `make_emperor.py` would attempt to parse `Icon?` files when a directory was passed via the `-i` option ([#323](https://github.com/biocore/emperor/issues/323)).
* Fix bug where Emperor would try to animate trajectories with a single timepoint i.e. a single unique value in the gradient category.
* Fix bug where the output saved to `--biplot_fp` would list the principal coordinate axes starting at zero instead of one ([#389](https://github.com/biocore/emperor/issues/389)).
* Remove misleading "QIIME version" from `index.html` ([#447](https://github.com/biocore/emperor/issues/447)).
* Fix problem where the speed slider in the *Animations* tab would not work correctly ([#546](https://github.com/biocore/emperor/pull/546)).
* Fix problem bug that would prevent users from using the *Visibility* and *Scaling* controllers ([#420](https://github.com/biocore/emperor/issues/420)).

### Miscellaneous

* Reorganized `emperor/support_files/` to separate Emperor's source code from third-party packages.
* Add code coverage support through [Coveralls](https://coveralls.io/r/biocore/emperor).
* Add [flake8](http://flake8.readthedocs.org/en/2.3.0/) to enforce the PEP-8 coding guidelines in every Travis build ([#342](https://github.com/biocore/emperor/issues/342)).
* Add an `all` target to get all the needed dependencies for emperor development (`pip install emperor[all]`).
* Update FileSaver.js to the latest development version and fixes a bug with large file downloads.
* Emperor's website can now be found by going to [http://emperor.microbio.me](http://emperor.microbio.me)

### New features

* Add a slider bar under the `Labels` tab to select different taxonomies for display.
* Biplots now include arrows, which represent taxa variances. These can be turned off using the `Taxa arrow visibility` checkbox.
* Add new tutorial on how to create animations ([#547](https://github.com/biocore/emperor/pull/547)).

Emperor 0.9.51 (5 Feb 2015)
---------------------------

* Improved error message when none of the samples match between coordinates and mapping file.
* Removed warning due to NumPy 1.9.x.
* Added support for NumPy 1.9.x.

Emperor 0.9.5 (14 Nov 2014)
---------------------------

* Add `make_emperor.py` script auto-generated documentation.
* Add numpydoc generated documentation setup.
* Emperor's documentation requires `sphinx-boostrap-theme` and `sphinx`.
* Add documentation about file formats.
* Updated to three.js revision 68.
* Fixed problem that removed unique/single-valued categories in the mapping file even if these were selected with `--color_by`.
* Added [chosen](http://harvesthq.github.io/chosen/) v1.1.0 for drop down menu.
* Replace MeshLambertMaterial for MeshPhongMaterial to get nicer coloring.
* Add options to select among different [colorbrewer](http://colorbrewer2.org) colormaps for continuous coloring.
* Discrete colors are provided by [colorbrewer](http://colorbrewer2.org).
* The rainbow colormap has disappeared from emperor, see [this paper](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=4118486) if you want to use that colormap.
* Remove discrete/continuous coloring checkbox and replace for the color-scheme drop down menu.
* Add option to select QIIME colors from the color-scheme drop down menu.
* Emperor now depends on scikit-bio 0.2.1.

Emperor 0.9.4 (10 Sept 2014)
----------------------------

* Category names are no longer trimmed to 25 characters in the user interface.
* Change the minimum percent required to display a plot to be greater than 0.01 instead of 0.5.
* The percent explained by each of the axes is now formatted as a floating point number with two digits in the mantissa.
* The `Key` tab now uses all the available space on screen.
* Improve mouse sensitivity to rotate, pan, zoom-in and zoom out in the 3D plot.
* Emperor is now hosted under the biocore GitHub organization.
* Add toggle visible button (`Invert Selected`) under the `Visibility` tab, this button will change hidden categories to visible and vice-versa.
* Supports both NumPy 1.7 and 1.8.
* Depends on scikit-bio 0.1.4.
* Emperor provides a Python object that is IPython aware (emperor.Emperor) that will display a usable plot from within the IPython notebook.
* Each of the categories in the Colors tab displays the # of samples. Also, the labels svg has this information.
* Emperor will multiply by 100 the percentages explained in the input file if PC1 is lower than 1. This behavior can be stopped using --pct_variation_below_one.

*Bug Fixes*

* Fixed problem where coordinate files with large values (greater than 100) would not be displayed on screen.
* Fixed problem that prevented the user from scrolling through the categories in the user interface.
* Clean-up the layout of the user interface so it's cleaner and consistent.
* Fix problem where long category names would alter the layout of the interface.
* Fix inability to write an 'E' character in the Filename field when exporting an svg.
* Fix problem where Emperor would generate invalid SVG files for the labels and the plot.
* Fix inability to reset an animation using the rewind button.
* Fix one-sample trajectories to not fail during rendering of the animation (these will get ignored).
* Fix sample identifiers that would fail when the animation started.
* Fix failure due to passing --missing_custom_axes_values and having a value for all rows in the column of interest. Now is ignored.

*New Features*

* Add animations tab to the main user interface.
* Add unit tests for the JavaScript library code.
* Support both classic and [scikit-bio](http://scikit-bio.org)'s coordinate formats.
* The legends file that emperor generates now has a non-monospace font and a line surrounding each colored square.

Emperor 0.9.3 (5 Dec 2013)
--------------------------

* `Use gradient colors` checkbox is now found under the `Colors` tab.
* Merge the `Options` and `View` tabs; additionally the global opacity slider and global scale slider were moved to their respective tabs.
* `Use gradient colors` checkbox now uses the standard blue -> red color gradient
* Add Emperor to the Python Package Index, now you can install Emperor running `pip install emperor`.
* Remove dependency on QIIME and PyCogent.
* Emperor now depends on qcli and Numpy.

*Bug Fixes*

* Add more meaningful error message for biplots when the contingency table passed included only one row.

Emperor 0.9.2 (24 Oct 2013)
---------------------------

*Bug Fixes*

* Fixes bug where files named `procrustes_results.txt` would not be ignored in a plot comparison.


Emperor 0.9.1 (21 Oct 2013)
---------------------------

*New features*

* Scientific notation is now taken into account in the GUI for scientific coloring.
* GUI is usable in mobile devices that support WebGL.
* User documentation: tutorial, installation instructions, GUI description, etc.
* Ability to make plot comparisons (very useful for procrustes analysis plots).
* The user can select the number of axes to be considered in the GUI and re-plot using lower axes; this is, for example: PC3 vs PC4 vs PC10.
* In missing_custom_axes_values you can reference other column within the mapping file to place the samples without numeric values at different points in the gradient.
* Parallel plots functionality.
* Separated out some options to the View menu.
* The "Colors" tab now has a selector, which allows to use the arrows to move between categories.
* Default coloring scheme is discrete.
* Add color pickers for the axes and axes labels.
* To take a screenshot (PNG) of your current visualization you can press `ctrl+p`.
* Export to SVG your visualization.
* Emperor now relies on QIIME 1.7.0.
* Added option `--number_of_segments` to control the quality of all spheres
* Labels for biplots now have a color picker.
* Add color pickers for connecting bars in coordinate comparison plots.
* Add option to select a master set of coordinates when making a comparison plot.
* Adds a feature to negate axes. With this feature you can negate the coordinates of each data point. As a result, the spheres and/or edges will be adjusted appropriately.
* Minor additions to the separator controller for the side bar.
* As of 308629f550ff3e108903d3bcf1ce76ce85f4cb96 Emperor is now released under a BSD license.


*Bug Fixes*

* Fixes recenter camera not working.
* Category names are sorted alphabetically.
* Category names with non-alphanumeric characters are colored correctly now.
* Biplots checkbox now accurately reflects status of biplot visiblity rather than opposite.
* Comparison bars checkbox now accurately reflects status of the visiblity rather than opposite.
* Scaling by percent explained now works with vectors and coordinate comparison plots.
* Fixed bug where only the first bars in coordinate comparison plots could be hidden.
* Improved documentation for saving and exporting images.
* Emperor now fails graciously when WebGL is not enabled and gives you a few suggestions on how to get it to work.



Emperor 0.9.0 (14 May 2013)
---------------------------

*New features*:

* Intuitive and modern graphical user interface.
* Simple workflow to modify the color of a sample/label from the user interface.
* Color the labels for the samples by a category in the mapping file.
* Scale the elements in the plot by the percentage explained from the user interface.
* Notify the user when values will be removed from the input files.
* Search for a sample name from the graphical user interface.
* Show a selector in the plot when double-clicking a sample name.
* Show and hide samples by a category in the mapping file.
* Change the opacity of spheres/ellipses from the graphical user interface.
* Change the size of a sphere from the graphical user interface.
* Biplots can be created with a custom axis.
* The color of the biplot spheres can now be changed from the user interface.
* Extensive script usage testing
* Addition of contextualized error messages.
* Reduced output size for datasets with rich mapping files.

*Performance improvements*:

* Improved performance and responsiveness from the graphical user interface.
* Superior graphics quality; elements are rendered in the graphics card not in the CPU.
* Enhanced performance to create the output files.
