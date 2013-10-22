#!/usr/bin/env python

from distutils.core import setup
from glob import glob

__author__ = "Yoshiki Vazquez Baeza"
__copyright__ = "Copyright 2013, The Emperor Project"
__credits__ = ["Antonio Gonzalez Pena", "Meg Pirrung", "Yoshiki Vazquez Baeza"]
__license__ = "BSD"
__version__ = "0.9.1-dev"
__maintainer__ = "Yoshiki Vazquez Baeza"
__email__ = "yoshiki89@gmail.com"
__status__ = "Development"

# without any of these emperor will not function correctly
required_python_modules = ['numpy', 'cogent', 'qiime']
unavailable_dependencies = []

for module in required_python_modules:
    try:
        exec 'import %s' % module
    except ImportError:
        unavailable_dependencies.append(module)

if unavailable_dependencies:
    print ('Cannot find the following python package(s): %s. Check your '
        'PYTHONPATH environment variable and/or site-packages folder.' %
        ', '.join(unavailable_dependencies))
    exit(1)

# slightly modified from the biom-format setup.py script
qiime_version = tuple(map(int, qiime.__version__.replace('-dev','').split('.'))) 
if qiime_version < (1, 7, 0):
    print ('The minimum required version of the QIIME libraries is 1.7.0 '
        'please update your version accordingly (your current version %s).' %
        qiime.__version__)
    exit(2)

long_description = """Emperor: a tool for visualizing high-throughput microbial community data
"""

setup(name='emperor',
        version=__version__,
        description='Emperor',
        author="Antonio Gonzalez Pena, Meg Pirrung & Yoshiki Vazquez Baeza",
        author_email=__email__,
        maintainer=__maintainer__,
        maintainer_email=__email__,
        url='http://github.com/qiime/emperor',
        packages=['emperor'],
        scripts=glob('scripts/*py'),
        package_data={'emperor':['support_files/js/*.js',
            'support_files/js/js/*.js', 'support_files/js/js/ctm/*.js',
            'support_files/js/js/ctm/license/*.txt',
            'support_files/js/js/postprocessing/*.js',
            'support_files/img/*.png', 'support_files/img/*.ico',
            'support_files/css/*.css', 'support_files/css/images/*.png',
            'support_files/emperor/css/*.css',
            'support_files/emperor/js/*.js',]},
        data_files={},
        long_description=long_description)

