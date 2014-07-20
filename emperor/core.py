r"""
Emperor 3D PCoA viewer
======================

This module provides an Object to interact and visualize an Emperor plot
from the IPython notebook.

Classes
-------
.. autosummary::
    Emperor

"""
from __future__ import division

from emperor.format import (format_mapping_file_to_js, format_pcoa_to_js,
                            format_taxa_to_js, format_vectors_to_js,
                            format_comparison_bars_to_js,
                            EMPEROR_HEADER_HTML_STRING,
                            format_emperor_html_footer_string)

# we are going to use this remote location to load external resources
RESOURCES_URL = 'http://emperor.colorado.edu/master/make_emperor/emperor_outpu\
t/emperor_required_resources'

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "0.9.3-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

class Emperor(object):
    """Display principal coordinates analysis plots

    Use this object to interactively display a PCoA plot using the Emperor
    GUI. IPython provides a rich display system that will let you display a
    plot inline, without the need of creating a temprorary file or having to
    write to disk.

    Parameters
    ----------
    """
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
        output = str(self).replace('emperor_required_resources',
                                   RESOURCES_URL)
        return display(HTML(output), metadata=dict(isolated=True))

    def _make_emperor(self):
        """Private method to build an Emperor HTML string"""
        pcoa_string = format_pcoa_to_js(self.ids,
                                        self.ordination.site,
                                        self.ordination.eigvals,
                                        self.ordination.proportion_explained)

        # we pass the mapping file headers twice so nothing is filtered out
        mf_string = format_mapping_file_to_js(self.mapping_file_data,
                                              self.mapping_file_headers,
                                              self.mapping_file_headers)

        # A lot of this is going to be empty because we don't really need any
        # of it
        footer = format_emperor_html_footer_string(False, False, False, False)
        taxa = format_taxa_to_js([], [], [])
        bars = format_comparison_bars_to_js([], [], 0)
        vectors = format_vectors_to_js([], [], [], [], None)

        # build the HTML string
        output = [EMPEROR_HEADER_HTML_STRING, mf_string, pcoa_string, taxa,
                  bars, vectors, footer]

        # add the remote resources
        _emperor = '\n'.join(output)

        self._html = _emperor

