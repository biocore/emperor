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

from jinja2 import DictLoader
from jinja2.environment import Environment
from random import sample
from sys import argv
from string import ascii_letters
from random import choice

import numpy as np


def listify(a):
    return np.asarray(a, dtype='str').tolist()

# From http://stackoverflow.com/a/6196098
pages = ['../emperor/support_files/templates/main-template.html',
         'template.html']
env = Environment()
templates = {}
for name in pages:
    with open(name, 'rb') as f:
        templates[name] = f.read()
env.loader = DictLoader(templates)
template = env.get_template('template.html')

N = 10
if len(argv) > 1:
    N = int(argv[1])

categories = np.asarray(np.random.randint(1, 1000, N), str)

coords_ids = listify(np.arange(N))
coords = np.random.randn(N, 10).tolist()
pct_var = (1/np.exp(np.arange(10))).tolist()

md_headers = ['SampleID', 'DOB', 'Strings']
metadata = []
for _id in coords_ids:
    metadata.append([_id, ''.join(sample(categories, 1)), ''.join(choice(
        ascii_letters) for x in range(10))])

with open('new-emperor.html', 'w') as f:
    f.write(template.render(coords_ids=coords_ids, coords=coords,
                            pct_var=pct_var, md_headers=md_headers,
                            metadata=metadata, plot_id='testing',
                            base_url='../emperor/support_files'))
