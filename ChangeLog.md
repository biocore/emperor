Emperor 0.9.1 (changes since Emperor 0.9.0 go here)
===================================================

*New features*

* Scientific notation is now taken into account in the GUI for scientific coloring.
* GUI is usable in mobile devices that support WebGL.
* Ability to make plot comparisons (very useful for procrustes analysis plots).
* The user can select the number of axes to be considered in the GUI and re-plot using lower axes; this is, for example: PC3 vs PC4 vs PC10.
* In missing_custom_axes_values you can reference other column within the mapping file to place the samples without numeric values at different points in the gradient.
* Parallel plots functionality
* Separated out some options to the View menu

*Bug Fixes*

* Fixes recenter camera not working.
* Category names are sorted alphabetically.
* Category names with non-alphanumeric characters are colored correctly now.
* Biplots checkbox now accurately reflects status of biplot visiblity rather than opposite.

Emperor 0.9.0 (14 May 2013)
===========================

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
