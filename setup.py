#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

__version__ = "1.0.0"
__maintainer__ = "Emperor development team"
__email__ = "yoshiki89@gmail.com"

# based on the text found in github.com/qiime/pynast
classes = """
    Development Status :: 5 - Production/Stable
    License :: OSI Approved :: BSD License
    Topic :: Software Development :: Libraries :: Application Frameworks
    Topic :: Software Development :: User Interfaces
    Programming Language :: Python
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""

classifiers = [s.strip() for s in classes.split('\n') if s]

with open('README.md') as f:
    long_description = f.read()

base = ["numpy >= 1.7", "scipy >= 0.17.0", "click", "pandas",
        "scikit-bio >= 0.4.1", "jinja2 >= 2.9", "future"]
doc = ["Sphinx", "sphinx-bootstrap-theme"]
test = ["pep8", "flake8", "nose"]
all_deps = base + doc + test

setup(
    name='emperor',
    version=__version__,
    description='Emperor',
    author="Antonio Gonzalez Pena, Meg Pirrung & Yoshiki Vazquez Baeza",
    author_email=__email__,
    maintainer=__maintainer__,
    maintainer_email=__email__,
    url='http://github.com/biocore/emperor',
    packages=find_packages(),
    package_data={
        'emperor': ['support_files/vendor/js/three.js-plugins/*.js',
                    'support_files/vendor/js/*.js',
                    'support_files/vendor/css/*.css',
                    'support_files/vendor/css/*.png',
                    'support_files/vendor/css/images/*.png',
                    'support_files/vendor/css/font/*.eot',
                    'support_files/vendor/css/font/*.ttf',
                    'support_files/vendor/css/font/*.woff',
                    'support_files/vendor/css/font/*.woff2',
                    'support_files/img/*.png',
                    'support_files/img/*.ico',
                    'support_files/css/*.css',
                    'support_files/js/*.js',
                    'support_files/templates/*.html']},
    data_files={},
    install_requires=base,
    extras_require={'doc': doc, 'test': test, 'all': all_deps},
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='BSD-3-Clause',
    classifiers=classifiers)
