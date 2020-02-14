Emperor Installation Notes
==========================

Emperor is a Python package that powers a JavaScript-based user interface. The
Python library relies on several packages from the scientific Python stack.

To install the latest release version of Emperor, you can use `pip` or
`conda`:

```bash
    # with pip
    pip install emperor

    # with conda
    conda install -c bioconda emperor
```

Developers
==========

If you are planning to do development, we recommend that you clone the git
repository, create a new environment (using `conda` or `virtualenvs`) and then
use `pip install -e` to work on the source code without having to reinstall
when you make editions:

```bash
    # fork
    git clone git://github.com/YOUR-USERNAME/emperor.git

    # if you are using conda
    conda create -n emperor-dev scipy numpy pandas matplotlib jupyter

    # if you are using virtualenvs
    mkvirtualenv emperor-dev && workon emperor-dev

    # now install the repository
    cd emperor
    pip install -e '.[all]'
```
