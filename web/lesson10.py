from willow.willow import *

def session(me):
  while True:
    msg = take({"tag": "serial"})
    add("<li>%s" % msg["byte"])

run(session)        
 
