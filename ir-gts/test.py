#!/usr/bin/python

from gbatonds import makends
from boxtoparty import makeparty

with open('Pokemon/Kirlia.3gpkm','r') as f:
    with open('Pokemon/Kirlia.pkm','w') as g:
        g.write(makeparty(makends(f.read())))
