from willow.willow import *

def session(me):
  if me == 0:
    add("<h1>Monitor</h1>")
  else:
    add("<p>Client %s logged in" % me, clients=0)
    add(me)
    
run(session)        
