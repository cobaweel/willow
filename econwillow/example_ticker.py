# This shows off how to do a broadcast message "ticker" that runs in
# the background. You can embed the ticker() function in your own
# code, or modify it. Because it runs in the background, you can
# easily add the chatbox to existing code without modifying the rest
# of it.

from willow.willow import *
from willow.branch import *
import time
  
# This function runs a ticker. You must have an HTML element for the
# ticker and feed a CSS selectors pointing to it into the function as
# an argument. You can also set the timestamp format for the messages.
def ticker(client,clients,tickerbox,label_time="[%H:%M] "):
  tag = "ticker %s %s" % (clients,tickerbox)
  def f():
    while True:
      msg = take({"tag": tag, "client": client})
      if msg["tag"] == tag:
        add(msg["msg"], "#%s" % tickerbox)
  background(f)
  def g(msg):
    msg = "%s%s<br>" % (time.strftime(label_time), msg)
    for c in clients:
      put({"tag": tag, "client":c, "msg": msg})
  return g

# This shows how to use the ticker() function
def session(client, clients):
  let(open("example_ticker.html"))

  tick = ticker(client, clients, "ticker")
  let("Subject %s" % client, "h1")
  while True:
    msg = take({"tag": "click", "client": client, "id": "0"},
               {"tag": "click", "client": client, "id": "1"},
               {"tag": "click", "client": client, "id": "2"},
               {"tag": "click", "client": client, "id": "3"},
               {"tag": "click", "client": client, "id": "4"},
               {"tag": "click", "client": client, "id": "5"},
               {"tag": "click", "client": client, "id": "6"},
               {"tag": "click", "client": client, "id": "7"},
               {"tag": "click", "client": client, "id": "8"},
               {"tag": "click", "client": client, "id": "9"},
               {"tag": "click", "client": client, "id": "10"})
    bid = int(msg["id"])
    tick("Subject %s has bid %s" % (client, bid))
    
assemble(session, [0,1])
