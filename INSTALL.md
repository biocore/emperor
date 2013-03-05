Emperor Installation Notes
==========================

Emperor is a python package that relies in [QIIME][], [NumPy][] and [PyCogent][]. These packages must be installed prior running the `setup.py` script.

Global Installation
===================

To perform a global installation of Emperor, execute the following command from a terminal session:

    sudo python setup.py install

If you do not have sudo access add the Emperor scripts and libraries to the `PATH` and `PYTHONPATH` environment variables. To add these variables to your `.bash_profile` issue the following terminal commands:

    echo "export PATH=$HOME/emperor_bin/:$PATH" >> ~/.bash_profile
    echo "export PYTHONPATH=$HOME/emperor_lib/:PYTHONPATH" >> ~/.bash_profile
    python setup.py install --install-scripts=~/emperor_bin/ --install-purelib=~/emperor_lib/ --install-lib=~/emperor_lib/

To test for a correct installation, open a new terminal window and issue the following command to see the help of `make_emperor.py`:

    make_emperor.py -h

[QIIME]: www.qiime.org
[NumPy]: www.numpy.org
[PyCogent]: www.pycogent.org

