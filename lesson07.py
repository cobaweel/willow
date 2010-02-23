from willow.willow import *

def session():
  add("Hello, ")
  put(("PING",), delay=2)
  get(("PING",))
  add("world.")

run(session)        
 
