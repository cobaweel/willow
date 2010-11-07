from willow.willow import *

def session(me):
  if me == 0:
    add("<h1>Monitor</h1>")
    while True:
      msg = take({"tag": "HELLO"})
      add("<p>Client %s logged in" % msg["number"])
  else:
    add(me)
    put({"tag": "HELLO", "number": me})
    
run(session)        

