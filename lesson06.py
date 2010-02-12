from willow.willow import *

def session():
  if me() == 0:
    add("<h1>Monitor</h1>")
  else:
    add("<p>Client %d logged in" % me(), number=0)
    add(me())
    
run(session)        
