from willow.willow import *

def session():
  if me() == 0:
    add("<h1>About to send some greetings...</h1>")
    add("<p>Please enter your name.</p>")
    add("<input id='bid' type='text' />")
    add("<input id='submit' type='submit' />")
    _, _, _ = get(("click", 0, "submit"))
    peek("#bid")
    add("<p>Greetings have been sent!</p><hr>")
  else:
    add("<h1>Waiting for some greetings...</h1>")
    _, _, name = get(("poke", 0, None))
    log("name", name)
    add("<p>Greetings from %s.</p><hr>" % name)

run(session)        
 
