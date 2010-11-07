from willow.willow import *

def session(me):
  if me == 0:
      add("Hello monitor %s" % me)
  else:
      add("Hello subject %s" % me)

run(session)        
