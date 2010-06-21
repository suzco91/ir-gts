#!/usr/bin/python

# A script that acts as the GTS, for sending and receiving pokemon between a
# retail cart and a PC. Credit goes to LordLandon and his sendpkm script, as
# well as the description of the GTS protocol from
# http://projectpokemon.org/wiki/GTS_protocol

from pokehaxlib import *
from getpkm import getpkm
from sendpkm import sendpkm
from platform import system
from os import getuid
from sys import argv, exit
from subprocess import call
from time import sleep

s = system()
if s == 'Darwin' or s == 'Linux':
    if getuid() != 0:
        args = ['sudo']
        args.extend(argv)
        call(args)
        exit(0)

token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR' # pulled from the actual GTS server

initServ()
sleep(1)

done = False
while not done:
    print 'Choose an option:'
    print 's - send pkm to game', 'r - receive pkm from game', 'q - quit'
    option = raw_input().strip().lower()

    if option.startswith('s'): sendpkm()
    elif option.startswith('r'): getpkm()
    elif option.startswith('q'):
        print 'Quitting program'
        done = True
    else: print 'Invalid option, try again'
