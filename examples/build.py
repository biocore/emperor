#!/usr/bin/env python
from __future__ import division

ts = """I think--I think when it's all over,
It just comes back in flashes, you know?
It's like a kaleidoscope of memories.
It just all comes back. But he never does.
I think part of me knew the second I saw him that this would happen.
It's not really anything he said or anything he did,
It was the feeling that came along with it.
And the crazy thing is I don't know if I'm ever gonna feel that way again.
But I don't know if I should.
I knew his world moved too fast and burned too bright.
But I just thought, how can the devil be pulling you toward someone who looks so much like an angel when he smiles at you?
Maybe he knew that when he saw me.
I guess I just lost my balance.
I think that the worst part of it all wasn't losing him.
It was losing me.

Once upon a time a few mistakes ago
I was in your sights, you got me alone
You found me, you found me, you found me
I guess you didn't care, and I guess I liked that
And when I fell hard you took a step back
Without me, without me, without me

And he's long gone when he's next to me
And I realize the blame is on me

'Cause I knew you were trouble when you walked in
So shame on me now
Flew me to places I'd never been
'Til you put me down, oh
I knew you were trouble when you walked in
So shame on me now
Flew me to places I'd never been
Now I'm lying on the cold hard ground
Oh, oh, trouble, trouble, trouble
Oh, oh, trouble, trouble, trouble

No apologies. He'll never see you cry,
Pretends he doesn't know that he's the reason why.
You're drowning, you're drowning, you're drowning.
Now I heard you moved on from whispers on the street
A new notch in your belt is all I'll ever be
And now I see, now I see, now I see

He was long gone when he met me
And I realize the joke is on me, yeah!

I knew you were trouble when you walked in
So shame on me now
Flew me to places I'd never been
'Til you put me down, oh
I knew you were trouble when you walked in
So shame on me now
Flew me to places I'd never been
Now I'm lying on the cold hard ground
Oh, oh, trouble, trouble, trouble
Oh, oh, trouble, trouble, trouble

And the saddest fear comes creeping in
That you never loved me or her, or anyone, or anything, yeah

I knew you were trouble when you walked in
So shame on me now
Flew me to places I'd never been
'Til you put me down, oh
I knew you were trouble when you walked in (you were right there, you were right there)
So shame on me now
Flew me to places I'd never been
Now I'm lying on the cold hard ground
Oh, oh, trouble, trouble, trouble
Oh, oh, trouble, trouble, trouble

I knew you were trouble when you walked in
Trouble, trouble, trouble
I knew you were trouble when you walked in
Trouble, trouble, trouble
"""
ts = ts.split()

from jinja2 import Template
from random import sample
from sys import argv

import numpy as np


def listify(a):
    return np.asarray(a, dtype='str').tolist()

with open('new-emperor.html', 'w') as f, open('template.html') as temp:
    template = Template(temp.read())

    N = 10
    if len(argv) > 1:
        N = int(argv[1])

    coords_ids = listify(np.arange(N))
    coords = listify(np.random.randn(N, 10))
    pct_var = listify(1/np.exp(np.arange(10)))

    md_headers = ['SampleID', 'DOB']
    metadata = []
    for _id in coords_ids:
        metadata.append([_id, ' '.join(sample(ts, 3))])

    f.write(template.render(coords_ids=coords_ids, coords=coords,
                            pct_var=pct_var, md_headers=md_headers,
                            metadata=metadata))
