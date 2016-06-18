# ----------------------------------------------------------------------------
# Copyright (c) 2013--, emperor development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from __future__ import division


from sys import argv
from os.path import abspath
from datetime import datetime
from socket import gethostname

from emperor import __version__ as emperor_library_version


def format_emperor_autograph(metadata_fp, coords_fp, language='HTML'):
    """Create a signature with some meta-data of the Emperor package

    Parameters
    ----------
    metadata_fp : str
        Absolute file path to the metadata mapping file
    coords_fp : str
        Absolute file path to the coordinates file
    language : {'HTML', 'Python', 'C', 'Bash'}, optional
        Language to which it will be formatted as a multi-line comment

    Returns
    -------
    str
        String with information about the executed command

    Raises
    ------
    AssertionError
        If the file is not allowed.
    """

    # supported open and closing of multi-line comments for different languages
    _languages = {'HTML': ('<!--', '-->'), 'Python': ('"""', '"""'),
                  'C': ('/*', '*/'), 'Bash': ('<<COMMENT', 'COMMENT')}

    assert language in list(_languages.keys()), ('%s is not a supported '
                                                 'language' % language)

    autograph = []
    autograph.append(_languages[language][0])
    autograph.append("*Summary of Emperor's Information*")

    # add the day and time at which the command was called
    autograph.append(datetime.now().strftime('Command executed on %B %d, %Y at'
                                             ' %H:%M:%S'))

    # add library version and SHA-1 if available
    autograph.append('Emperor Version: %s' % emperor_library_version)
    autograph.append('HostName: %s' % gethostname())

    # full path to input files
    autograph.append('Metadata: %s' % abspath(metadata_fp))
    autograph.append('Coordinates: %s' % abspath(coords_fp))

    if any([True for element in argv if 'make_emperor.py' in element]):
        autograph.append('Command: %s' % ' '.join(argv))
    else:
        autograph.append('Command: Cannot find direct call to make_emperor.py')
    autograph.append(_languages[language][1])

    return '%s' % '\n'.join(autograph)
