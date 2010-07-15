#!/usr/bin/python

from pokehaxlib import *
from pkmlib import encode, decode
from sys import argv, exit
from platform import system
import os.path

def sendpkm():
    token = 'c9KcX1Cry3QKS2Ai7yxL6QiQGeBGeQKR'

    print 'Note: you must exit the GTS before sending a pkm'
    print 'Enter the path or drag the pkm file here'

    path = raw_input().strip()
    path = os.path.normpath(path)
    if system() != 'Windows':
        path = path.replace('\\', '')

    if path.lower().endswith('.pkm'):
        with open(path, 'rb') as f:
            pkm = f.read()
        print 'Encoding!'
        bin = encode(pkm)
    elif path.lower().endswith('.bin'):
        with open(path, 'rb') as f:
            bin = f.read()
        print 'Decoding!'
        pkm = decode(bin)
    else:
        print 'Filename must end in either .bin or .pkm'
        return

    # Adding GTS data to end of file
    if len(pkm) != 236:
        print 'Invalid filesize. Note: Only party (i.e. not PC-boxed)',
        print 'Pokemon can be sent'
        return
    bin += pkm[0x08:0x0a] # id
    if ord(pkm[0x40]) & 0x04: bin += '\x03' # Gender
    else: bin += chr((ord(pkm[0x40]) & 2) + 1)
    bin += pkm[0x8c] # Level
    bin += '\x01\x00\x03\x00\x00\x00\x00\x00' # Requesting bulba, either, any
    bin += '\x00' * 20 # Timestamps and PID
    bin += pkm[0x68:0x78] # OT Name
    bin += pkm[0x0c:0x0e] # OT ID
    bin += '\xDB\x02' # Country, City
    bin += '\x46\x00\x07\x02' # Sprite, Exchanged (?), Version, Lang

    sent = False
    delete = False
    print 'Ready to send; you can now enter the GTS...'
    while not sent:
        sock, req = getReq()
        a = req.action
        if len(req.getvars) == 1:
            sendResp(sock, token)
        elif a == 'info':
            sendResp(sock, '\x01\x00')
            print 'Connection Established.'
        elif a == 'setProfile': sendResp(sock, '\x00' * 8)
        elif a == 'post': sendResp(sock, '\x0c\x00')
        elif a == 'search': sendResp(sock, '')
        elif a == 'result': sendResp(sock, bin)
        elif a == 'delete':
            sendResp(sock, '\x01\x00')
            sent = True

    print 'Pokemon sent successfully.',
