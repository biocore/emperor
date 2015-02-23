Emperor documentation
=====================

This guide contains instructions for building the Emperor documentation, as
well as guidelines for contributing to the documentation.

**Note:** If you're only interested in viewing the Emperor documentation,
visit [http://biocore.github.io/emperor/](http://biocore.github.io/emperor/).

Building the documentation
--------------------------

To build the documentation, you'll need the following Python packages
installed:

- [Sphinx](http://sphinx-doc.org/) >= 1.2.2
- [sphinx-bootstrap-theme](https://pypi.python.org/pypi/sphinx-bootstrap-theme/)

An easy way to install the dependencies is via pip:

    pip install Sphinx sphinx-bootstrap-theme

Finally, you will need to install Emperor.

**Important:** The documentation will be built for whatever version of
Emperor is *currently installed* on your system (i.e., the version imported
by ```import emperor```). This may not match the code located in this repository.
You will need to either install this version of Emperor somewhere (e.g., in
a virtualenv) or point your ```PYTHONPATH``` environment variable to this code,
*before* building the documentation.

To build the documentation, assuming you are at the top-level Emperor
directory:

    cd doc
    make html

The built HTML documentation will be at ```build/html/index.html```.

Contributing to the documentation
---------------------------------

If you would like to contribute to the documentation, whether by adding
something entirely new or by modifying existing documentation, please first
review our [Emperor contribution guide](../CONTRIBUTING.md).

Before submitting your changes, ensure that the documentation builds without
any errors or warnings, and that there are no broken links:

    make clean
    make html
    make linkcheck

### Troubleshooting

If things aren't working correctly, try running ```make clean``` and then
rebuild the docs. If things still aren't working, try building the docs
*without* your changes, and see if there are any Sphinx errors or warnings.
Make note of these, and then see what new errors or warnings are generated when
you add your changes again.
