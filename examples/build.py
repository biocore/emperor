#!/usr/bin/env python
"""
build.py: create an emperor plot with N random data samples by default N=10 but
you can change this value when calling from the command line, for example
to generate a plot with 111 samples do:

    ./build.py 111

Note that you will need jinja2 installed, and to execute the program from
within the examples folder.
"""
from __future__ import division

from random import sample, choice
from sys import argv
from string import ascii_letters

import numpy as np, pandas as pd
from emperor import Emperor
from emperor.util import get_emperor_support_files_dir
from skbio import OrdinationResults


def listify(a):
    return np.asarray(a, dtype='str').tolist()

N = 10
if len(argv) > 1:
    N = int(argv[1])

categories = np.asarray(np.random.randint(1, 1000, N), str)

coords_ids = listify(np.arange(N))
coords = (np.random.randn(N, 10) * 1000).tolist()
pct_var = pd.Series(1/np.exp(np.arange(10)))
pct_var = pct_var / pct_var.sum()


md_headers = ['SampleID', 'DOB', 'Strings']
metadata = []
for _id in coords_ids:
    metadata.append([_id, ''.join(sample(set(categories), 1)), ''.join(choice(
        ascii_letters) for x in range(10))])

samples = pd.DataFrame(index=coords_ids, data=coords)

mf = pd.DataFrame(data=metadata, columns=md_headers)
mf.set_index('SampleID', inplace=True)

minerals = ['rhodium', 'platinum', 'gold', 'ruthenium']
mf['subject'] = np.random.randint(low=0, high=len(minerals), size=N)

mf['subject'] = mf['subject'].apply(lambda x: minerals[x])

res = OrdinationResults(short_method_name='PC', long_method_name='Principal '
                        'Coordinates Analysis', eigvals=pct_var,
                        samples=samples, proportion_explained=pct_var)


viz = Emperor(res, mf, remote=get_emperor_support_files_dir())

with open('new-emperor.html', 'w') as f:
    f.write(viz.make_emperor(standalone=True))
