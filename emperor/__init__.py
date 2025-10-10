# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE.md, distributed with this software.
# ----------------------------------------------------------------------------

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version('emperor')  # noqa

from emperor.core import Emperor
from emperor._pandas import scatterplot
from emperor.util import nbinstall


__all__ = ['Emperor', 'scatterplot', 'biplots', 'format', 'filter', 'parse',
           'sort', 'util', 'nbinstall']
