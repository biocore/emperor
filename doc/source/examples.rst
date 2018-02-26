.. _examples:

.. index:: examples

Examples
^^^^^^^^

Emperor provides a Python API (:ref:`emperor-python-docs`) intended to be used
to create interactive plots, which can be visualized in the context of
the `Jupyter notebook <http://jupyter.org>`_, or outside it.
Alternatively, if you are using `QIIME 2 <https://qiime2.org>`_, these same
capabilities are exposed through QIIME 2's interfaces (most notably the command
line interface and graphical user interface).

The main entry point for Emperor is the ``Emperor`` object, this
object relies on two pieces of information:

- **Sample metadata**: this data is represented as a Pandas ``DataFrame``
  object that describes a series of samples and any additional information that
  was measured for each of them. In the context of QIIME and QIIME 2, this is
  referred to as the *mapping file*.

- **Coordinates data**: this data is represented as a scikit-bio
  ``OrdinationResults`` object that describes the position of a series of
  samples in an `n`-dimensional space.

To try out the examples below, download a copy of the repository (`here
<https://github.com/biocore/emperor/archive/new-api.zip>`_), and navigate
inside the examples folder.

Plotting Principal Coordinates Analysis
---------------------------------------

In `this notebook
<http://nbviewer.jupyter.org/github/biocore/emperor/blob/new-api/examples/keyboard.ipynb>`_,
we explore the simplest use-case, visualizing a previously computed principal
coordinates analysis matrix. For this example, we processed the OTU table using
`Qiita <https://qiita.ucsd.edu/>`_ (to compute a distance matrix and ordinated
coordinates), so all we need to do is load the coordinates and metadata. To
plot data, we use the ``Emperor`` constructor.

Note that, we load the metadata mapping file in such a way that no data types
are inferred (this is to guarantee data integrity) however, so as long as your
data is in a Pandas ``DataFrame``, you can load it in any way you find the most
convenient.  Additionally, in the line where we call the ``Emperor``
constructor, we specify ``remote=True``, this allows us to share the notebook
via `nbviewer <http://nbviewer.jupyter.org>`_, and make the plot interactive
for anyone who accesses the notebook from their browser.

Distance Metric Browser
-----------------------

`This example
<http://nbviewer.jupyter.org/github/biocore/emperor/blob/new-api/examples/evident.ipynb>`_,
explores how `Jupyter <http://jupyter.org>`_'s interactive components can be
used together with Emperor, to create a distance metric browser.

There are a few important things to note from this example. First, we rely on a
few packages that are **not** Emperor dependencies, but are generally useful in
the context of microbiome data analysis (`scikit-learn
<http://scikit-learn.org>`_, `biom-format <http://biom-format.org>`_,
`qiime_default_reference <https://github.com/biocore/qiime-default-reference>`_
and `ipywidgets <http://ipywidgets.readthedocs.io>`_).


Sharing a Plot
==============

In the Jupyter Notebook
-----------------------

Emperor has the ability to display its interface inline inside a Jupyter
notebook. By **default**, plots are created such that if the notebook is shared
with someone else (using GitHub, nbviewer, or by sharing the notebook file),
the plots can be loaded without needing any additional dependencies (in the
examples above that's why we set ``remote=True``).  Remember, that in order to
do this, you will need to have access to an internet connection.  Alternatively
when there's no internet connection available, you can use the `nbinstall`
function, which will make the resources available from within your running
notebook server.

Outside the Jupyter Notebook
----------------------------

In certain circumstances it is more convenient to create plots independent of
the Jupyter notebook, to do this you would need to do the same thing as above
(load the metadata and coordinates), and then instead of displaying the plot
inline, you can use the Python API to create a folder with the plot and needed
resources. The following snippet uses the ``Emperor`` object but this time it
sets the ``remote`` parameter to the current directory i.e. ``remote='.'``
(like in UNIX, ``'.'`` refers to the current path)::

   from emperor import Emperor
   from os import makedirs
   from os.path import join
   from skbio import OrdinationResults

   import pandas as pd

   # this is just an example of how to load a metadata table and ordination
   metadata = pd.read_csv('mapping-file.txt', sep='\t', index_col='#SampleID')
   ordination = OrdinationResults.read('bray-curtis.txt')


   # the remote argument refers to where the support files will be located
   # relative to the plot itself i.e. index.html.
   emp = Emperor(ordination, metadata, remote='.')
   output_folder = 'plot' # new folder where data will be saved

   # create an output directory
   makedirs(output_folder, exist_ok=True)

   with open(join(output_folder, 'index.html'), 'w') as f:
       f.write(emp.make_emperor(standalone=True))
       emp.copy_support_files(output_folder)

To view the plot, open the ``index.html`` file inside the ``plot`` folder. This
will launch Emperor, but this time the interface will use the entire screen,
as opposed to just a cell (like in the notebooks above).
