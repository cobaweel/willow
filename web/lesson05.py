from willow.willow import *

def session(me):
  add("<p>Please enter your name.")
  add("<input id='bid' type='text'>")
  add("<input id='go' type='submit'>")
  take({"tag": "click", "id": "go", "client": me})
  peek("#bid")
  msg = take({"tag": "peek", "id": "bid", "client": me})
  add("<p>Hello, %s." % msg["value"])

run(session)        
