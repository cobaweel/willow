# This shows off how to do a chatbox that runs in the background. You
# can embed the chatbox() function in your own code, or modify
# it. Because it runs in the background, you can easily add the
# chatbox to existing code without modifying the rest of it.

from willow.willow import *
from willow.branch import *
import time

# This function runs a chatbox. You must have an HTML element for the
# chatbox itself, one for the input box, and one for a button, and
# feed CSS selectors for all three of these into the function as
# arguments. You can also set the format for the chat messages.
def chatbox(client,clients,chatbox,chatbar,chatbutton,
            label_time="[%H:%M] ",label=""):
  # First, we generate a unique tag for our messages. This makes it
  # possible to have multiple chatboxes at once that do not interfere
  # with each other.
  tag = "chatbox %s %s %s %s" % (clients,chatbox,chatbar,chatbutton)

  # The function f() will be run in the background, so that the
  # chatbox can work in parallel with whatever else is going on.
  def f():
    while True:
      msg = take({"tag": "click", "id": chatbutton, "client": client},
                 {"tag": tag,  "client": client})
      if msg["tag"] == "click" and msg["id"] == chatbutton:
        txt = "%s%s%s<br>" % ( time.strftime(label_time), 
                               label, 
                               peek("#%s" % chatbar) )
        poke("value", "", "#%s" % chatbar)
        for c in clients:
          put({"tag": tag, "client":c, "msg": txt})
      if msg["tag"] == tag:
        add(msg["msg"], "#%s" % chatbox)
  background(f)

# This shows how to use the chatbox() function
def session(client, clients):
  let(open("example_chat.html"))
  let(client, "h1")

  chatbox(client, clients, "chatbox", "chatbar", "chatbutton",
          label="(Subject %s) " % client)

  # You can do other things while the chatbox is running...
  while True: 
      sleep(1)
    
assemble(session, [0,1])
