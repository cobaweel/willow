from willow.willow import *

def session(me):
  add("Hello, ")

  def ping():
    put({"tag":"PING", "client": me})
  background(ping, 3)
  
  take({"tag":"PING", "client": me})
  add("world.")

run(session)        
 
