from willow.willow import *

def session(me):
  add("<p>Please enter your name.")
  add("<input id='name' type='text'>")
  add("<input id='go' type='submit'>")
  take({"tag": "click", "id": "go", "client": me})
  name = peek("#name")
  add("<p>Hello, %s." % name)

run(session)        
