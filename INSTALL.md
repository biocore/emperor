Emperor Installation Notes
==========================

Emperor is a python package that relies in [QCLI](https://pypi.python.org/pypi/qcli) and [NumPy](http://www.numpy.org). These packages must be installed prior running the `setup.py` script.

To download Emperor, use [this link](https://github.com/biocore/emperor/archive/master.zip) or use git to get the latest version of the repository:

    git clone git://github.com/biocore/emperor.git

Installation
============

By far the easiest way to install Emperor is running:

    pip install emperor

In other case, to perform a global installation of Emperor, execute the following command from a terminal session:

    python setup.py install

If you do not want to do a global installation, you will have to add the Emperor scripts and libraries to the `PATH` and `PYTHONPATH` environment variables. To add these variables to your `.bash_profile` issue the following terminal commands:

``` bash
echo "export PATH=$HOME/emperor_bin/:$PATH" >> ~/.bash_profile
echo "export PYTHONPATH=$HOME/emperor_lib/:$PYTHONPATH" >> ~/.bash_profile
python setup.py install --install-scripts=~/emperor_bin/ --install-purelib=~/emperor_lib/ --install-lib=~/emperor_lib/
```

To test for a correct installation, open a new terminal window and issue the following command to see the help of `make_emperor.py`:

    make_emperor.py -h
