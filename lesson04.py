from willow.willow import *

def session():
  if me() == 0:
    add("<h1>Monitor</h1>")
    while True:
      _, n = get(("HELLO", None))
      add("<p>Client %d logged in" % n)
  else:
    put(("HELLO", me()))
    add(me())
    
run(session)        

