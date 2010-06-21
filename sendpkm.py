#!/usr/bin/python
from pokehaxlib import *
from pkmlib import encode
from sys import argv, exit
from string import uppercase, lowercase, digits
from random import sample
from time import sleep

#end='\x01\x00\x01\x01\xc5\x00\x01Z\x00\x00\x00\x00\xda\x07\x02\x15\x00\x08\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x87\x8d\x96\rG\x00\x07\x00\x0e\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\xb50g,\x0b\x00\x07\x01'
end=""
pop=uppercase+lowercase+digits

pathtopoke=None
if len(argv)==2:
  pathtopoke=argv[1]
  #print "Usuage: %s poop.pkm"%argv[0]
  #exit(0)
else:
  print "No arguments given, please enter path to .pkm or .bin file :"
  pathtopoke=raw_input()

pathtopoke = pathtopoke.strip()

if pathtopoke.lower().endswith(".pkm"):
  pkm=open(pathtopoke, "rb").read()
  print "Encoding!"
  bin=encode(pkm)
elif pathtopoke.lower().endswith(".bin"):
  bin=open(pathtopoke, "rb").read()
  print "Decoding!"
  pkm=decode(bin)
else:
  print "Please use either a .bin or a .pkm file with this sender."
  exit(1)
if len(pkm)<236: pkm+="\x00"*(236-len(pkm))
end+=pkm[8:10] #id
end+="\x03" if ord(pkm[64])&4 else chr((ord(pkm[64])&2)+1) #gender
end+=pkm[140] #level
end+="\x01\x00\x03\x00\x00\x00\x00\x00" #requesting bulba, either, any
end+="\x00"*20 #timestamps and pid
end+=pkm[0x68:0x78] #ot name
end+=pkm[0x0c:0x0e] #ot id
end+="\x00\x00" #country, city
end+="\x00"*4 #dunno what these are
bin+=end
alreadysent=False

initServ()
while True:
  sock, req=getReq()
  if len(req.getvars)==1:
    ans="".join(sample(pop, 32))
  elif req.action=="info":
    ans="\x01\x00"
  elif req.action=="setProfile":
    ans="\x00"*8
  elif req.action=="result":
    if alreadysent:
      ans=chr(4)+"\x00"
    else:
      ans=bin
  elif req.action=="get":
    ans=bin
  elif req.action=="return" or req.action=="delete":
    ans="\x01\x00"
    print "Saying 'Bye' to %s!"%pathtopoke
    alreadysent=True
  sendResp(sock, ans)
  if alreadysent:
    break
sleep(22)
