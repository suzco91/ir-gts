#!/usr/bin/python

from gbatonds import makends
from boxtoparty import makeparty

with open('Pokemon/Manectric.3gpkm','r') as f:
    with open('Pokemon/Manectric.pkm','w') as g:
        g.write(makeparty(makends(f.read())))
