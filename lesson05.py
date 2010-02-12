from willow.willow import *

def session():
  add("<p>Please enter your name.")
  add("<input id='bid' type='text'>")
  add("<input id='submit' type='submit'>")
  _, _, _ = get(("click", me(), "submit"))
  peek("#bid")
  _, _, name = get(("peek", me(), None))
  add("<p>Hello, %s." % name)

run(session)        
 
