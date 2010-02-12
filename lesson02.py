from willow.willow import *

def session():
  if me() == 0:
      add("Hello monitor %d at URL %s" % (me(), url()))
  else:
      add("Hello subject %d at URL %s" % (me(), url()))

run(session)        
