from willow.willow import *
from willow.branch import *
import time

def session(client, clients):
  let(open("example02.html"))
  chatbox(client, clients, "chatbox", "chatbar", "chatbutton",
          label="(Subject %s) " % client)
  tick = ticker(client, clients, "ticker")
  
  let("Subject %s" % client, "h1")

  while True:
    msg = take({"tag": "click", "client":client, "id": "0"},
               {"tag": "click", "client":client, "id": "1"},
               {"tag": "click", "client":client, "id": "2"},
               {"tag": "click", "client":client, "id": "3"},
               {"tag": "click", "client":client, "id": "4"},
               {"tag": "click", "client":client, "id": "5"},
               {"tag": "click", "client":client, "id": "6"},
               {"tag": "click", "client":client, "id": "7"},
               {"tag": "click", "client":client, "id": "8"},
               {"tag": "click", "client":client, "id": "9"},
               {"tag": "click", "client":client, "id": "10"})
    bid = int(msg["id"])
    tick("Subject %s has bid %s" % (client,bid))
    
assemble(session,[0,1])
 
