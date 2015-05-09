r"""
Emperor 3D PCoA viewer (:mod:`emperor.core`)
============================================

This module provides an Object to interact and visualize an Emperor plot
from the IPython notebook.

.. currentmodule:: emperor.core

Classes
-------
.. autosummary::
    :toctree: generated/

    Emperor
"""
# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import division
#RESOURCES_URL = 'http://emperor.colorado.edu/master/make_emperor/emperor_output/emperor_required_resources'
class Emperor(object):
    def __init__(self, ordination, mapping_file_data, mapping_file_headers):
        self.ordination = ordination
        self.mapping_file_data = mapping_file_data
        self.mapping_file_headers = mapping_file_headers
        self.ids = [s[0] for s in mapping_file_data]
        self._html = None

    def __str__(self):
        if self._html is None:
            self._make_emperor()
        return self._html

    def _repr_html_(self):
        """Used to be displayed in the IPython notebook"""
        # we import here as IPython shouldn't be a dependency of Emperor
        # however if this method is called it will be from an IPython notebook
        # otherwise the developer is responsible for calling this method
        from IPython.display import display, HTML

        # this provides a string representation that's independent of the
        # filesystem, it will instead retrieve them from the official website
        #output = str(self).replace('emperor_required_resources',
        #                           RESOURCES_URL)
        output = str(self)
        return display(HTML(output), metadata=dict(isolated=True))


    def _make_emperor(self):
        """Private method to build an Emperor HTML string"""
        key_string = "var ids = %s;"%str(self.ids)
        coords_string = "var coords = %s;"%self.ordination.site.tolist()
        pct_var_string = "var pct_var = %s;"%self.ordination.proportion_explained.tolist()

        md_header_string = "var md_headers = %s;"%self.mapping_file_headers
        metadata_string = "var metadata = %s;"%self.mapping_file_data

        x = __file__
        from os.path import dirname, abspath, join
        x = join(dirname(abspath(__file__)), 'support_files')

    #<!-- Libraries the code depends on -->
    #<script src="../vendor/js/underscore-min.js"></script>
    #<script src="../vendor/js/jquery-1.7.1.min.js"></script>
    #<script src="../vendor/js/chroma.min.js"></script>
    #<script src="../vendor/js/three.min.js"></script>
    #<script src="../vendor/js/three.js-plugins/OrbitControls.js"></script>>

    #<!--Source files to test-->
    #<script src="model.js"></script>
    #<script src="view.js"></script>
    #<script src="sceneplotview3d.js"></script>
    #<script src="controller.js"></script>


        underscore = open("%s/vendor/js/underscore-min.js"%x).read()
        jquery = open("%s/vendor/js/jquery-1.7.1.min.js"%x).read()
        chroma = open("%s/vendor/js/chroma.min.js"%x).read()
        three = open("%s/vendor/js/three.min.js"%x).read()
        orbits = open("%s/vendor/js/three.js-plugins/OrbitControls.js"%x).read()

        model = open("%s/js/model.js"%x).read()
        view = open("%s/js/view.js"%x).read()
        sceneplot = open("%s/js/sceneplotview3d.js"%x).read()
        controller = open("%s/js/controller.js"%x).read()

        stuff = """
      $("<div id='plots' style='float:left; height:500px; width:500px'></div>").appendTo(document.getElementById('container'))
      var div = $('#plots');
      """
    

        # build the HTML string
        output = [EMPEROR2_HEADER_HTML_STRING,
                  underscore, jquery,
                  chroma, three, orbits, model, view, sceneplot, controller,
                  stuff,
                  key_string, coords_string,
                  pct_var_string, md_header_string, metadata_string,
                  EMPEROR2_MAIN_HTML_STRING,
                  EMPEROR2_FOOTER_HTML_STRING]

        # add the remote resources
        _emperor = '\n'.join(output)

        self._html = _emperor


EMPEROR2_HEADER_HTML_STRING = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Emperor test</title>
    <meta charset="utf-8">
    <style>
      body {
        margin: 0px;
        background-color: #000000;
        overflow: hidden;
      }
    </style>
  </head>
  <body>

    <script>
"""
EMPEROR2_HEADER_HTML_STRING = """
    <div id='container'>
    </div>
    <script>
"""

EMPEROR2_FOOTER_HTML_STRING = """
    </script>

  </body>
</html>
"""

EMPEROR2_FOOTER_HTML_STRING = """
    </script>

"""

EMPEROR2_MAIN_HTML_STRING = """
      var dm, ec;

      init();
      animate();

      function init() {
        // Initialize the DecompositionModel
        dm = new DecompositionModel(name, ids, coords, pct_var,
                                    md_headers, metadata);
        // Initialize the EmperorController
        ec = new EmperorController($('#plots').width(), $('#plots').height(), dm, 'plots');


        div.append(ec.renderer.domElement);

        window.addEventListener( 'resize', onWindowResize, false );

      }

      function onWindowResize() {
       ec.resize($('#plots').width(), $('#plots').height());
      }

      function animate() {
        requestAnimationFrame(animate);
        ec.render();
      }
"""

# from emperor.format import (format_mapping_file_to_js, format_pcoa_to_js,
#                             format_taxa_to_js, format_vectors_to_js,
#                             format_comparison_bars_to_js,
#                             format_emperor_html_footer_string)
# from emperor._format_strings import EMPEROR_HEADER_HTML_STRING

# # we are going to use this remote location to load external resources
# RESOURCES_URL = 'http://emperor.colorado.edu/master/make_emperor/emperor_outpu\
# t/emperor_required_resources'


# class Emperor(object):
#     """Display principal coordinates analysis plots

#     Use this object to interactively display a PCoA plot using the Emperor
#     GUI. IPython provides a rich display system that will let you display a
#     plot inline, without the need of creating a temprorary file or having to
#     write to disk.

#     Parameters
#     ----------
#     ordination: skbio.maths.stats.ordination.OrdinationResults
#         Object containing the computed values for an ordination method in
#         scikit-bio.
#     mapping_file_data: list of list objects
#         Metadata mapping file used to color the plot.
#     mapping_file_headers: list of str objects
#         List of strings representing the header names of the
#         `mapping_file_data`. All names should be unique.

#     Examples
#     --------
#     Create an Emperor object and display it from the IPython notebook:

#     >>> data = [['PC.354', 'Control', '20061218', 'Control_mouse_I.D._354'],
#     ... ['PC.355', 'Control', '20061218', 'Control_mouse_I.D._355'],
#     ... ['PC.356', 'Control', '20061126', 'Control_mouse_I.D._356'],
#     ... ['PC.481', 'Control', '20070314', 'Control_mouse_I.D._481'],
#     ... ['PC.593', 'Control', '20071210', 'Control_mouse_I.D._593'],
#     ... ['PC.607', 'Fast', '20071112', 'Fasting_mouse_I.D._607'],
#     ... ['PC.634', 'Fast', '20080116', 'Fasting_mouse_I.D._634'],
#     ... ['PC.635', 'Fast', '20080116', 'Fasting_mouse_I.D._635'],
#     ... ['PC.636', 'Fast', '20080116', 'Fasting_mouse_I.D._636']]
#     >>> headers = ['SampleID', 'Treatment', 'DOB', 'Description']
#     >>> ordination = OrdinationResults.read('unweighted_unifrac_pc.txt')

#     Now import the Emperor object and display it using IPython, note that this
#     call will have no effect under an interactive Python session:

#     >>> from emperor import Emperor
#     >>> Emperor(ordination, data, headers)

#     Notes
#     -----
#     This object currently does not support the full range of actions that the
#     GUI does support and should be considered experimental at the moment.

#     References
#     ----------
#     .. [1] EMPeror: a tool for visualizing high-throughput microbial community
#        data Vazquez-Baeza Y, Pirrung M, Gonzalez A, Knight R.  Gigascience.
#        2013 Nov 26;2(1):16.

#     """
#     def __init__(self, ordination, mapping_file_data, mapping_file_headers):
#         self.ordination = ordination
#         self.mapping_file_data = mapping_file_data
#         self.mapping_file_headers = mapping_file_headers
#         self.ids = [s[0] for s in mapping_file_data]
#         self._html = None

#     def __str__(self):
#         if self._html is None:
#             self._make_emperor()
#         return self._html

#     def _repr_html_(self):
#         """Used to be displayed in the IPython notebook"""

#         # we import here as IPython shouldn't be a dependency of Emperor
#         # however if this method is called it will be from an IPython notebook
#         # otherwise the developer is responsible for calling this method
#         from IPython.display import display, HTML

#         # this provides a string representation that's independent of the
#         # filesystem, it will instead retrieve them from the official website
#         output = str(self).replace('emperor_required_resources',
#                                    RESOURCES_URL)

#         # thanks to the IPython devs for helping me figure this one out
#         return display(HTML(output), metadata=dict(isolated=True))

#     def _make_emperor(self):
#         """Private method to build an Emperor HTML string"""
#         pcoa_string = format_pcoa_to_js(self.ids,
#                                         self.ordination.site,
#                                         self.ordination.proportion_explained)

#         # we pass the mapping file headers twice so nothing is filtered out
#         mf_string = format_mapping_file_to_js(self.mapping_file_data,
#                                               self.mapping_file_headers,
#                                               self.mapping_file_headers)

#         # A lot of this is going to be empty because we don't really need any
#         # of it
#         footer = format_emperor_html_footer_string(False, False, False, False)
#         taxa = format_taxa_to_js([], [], [])
#         bars = format_comparison_bars_to_js([], [], 0)
#         vectors = format_vectors_to_js([], [], [], [], None)

#         # build the HTML string
#         output = [EMPEROR_HEADER_HTML_STRING, mf_string, pcoa_string, taxa,
#                   bars, vectors, footer]

#         # add the remote resources
#         _emperor = '\n'.join(output)

#         self._html = _emperor
