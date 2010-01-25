from willow.willow import *
from willow.contrib import *
import random

def button(id, text, selector="body", number=None):
    html = ("<br><input class='wide' type='submit' id='%s' value='%s'>" % 
            (id,text))
    add(html, selector, number)

def smallbutton(id, text, selector="body", number=None):
    html = ("<input class='small' type='submit' id='%s' value='%s'>" % 
            (id,text))
    add(html, selector, number)


def session():
  number = me()            # Client ID for this thread
  
  #
  # Get clients to connect
  #
  add(open("rt.html"),"head")

  if number == 0:
    clients = 0         # Number of clients connected
    subjects = 0        # Number of clients in use after nixing
    button("start","Click when clients are all logged on.")
    add("<br>")
    while True:
      event, subject, _ = get(("click", 0, "start"),
                              ("logon", None, None))
      if event == "click":
        break
      elif event == "logon":
        clients += 1
  else:
    add("%d " % number, number=(0,number))
    put(("logon", None, None))


  #
  # Use an even number of clients based on subject turn-out
  #

  if number == 0:
    options = []
    for i in range(0, 2 * (clients / 2) + 1, 2):
      button(i, "Click if %d subjects showed up" % i)
      options += [("click", 0, "%d" % i)]
    _, _, show_ups = get(*options)
    subjects = int(show_ups)
    for client in range(1, subjects+1): put(("nix",client,False))
    for client in range(subjects+1, clients+1): put(("nix",client,True))
  else:
    _, _, nix = get(("nix",number,None))
    if nix:
      set("X")
      return

  def trust(senders, receivers):
    if number in senders:
      n = senders.index(number)
      sender = number
      receiver = receivers[n]
      set("You have $10.<br>How much do you want to send?<p>")
      while grab(("click", number, None)): pass
      for i in range(0,11): smallbutton(i,"$%d"%i)
      _, _, send = get(("click", number, None))
      send = int(send)
      add("<p>Wait...")
      put(("send",n,send))
      _, _, back = get(("back",n,None))
      add("""<p>You sent: $%d.
             <br>You kept: $10 &minus; $%d = $%d.
             <br>The receiver received: 2 &times; $%d = $%d.
             <br>The receiver returned: $%d.
             <br>You earned $%d + $%d = $%d.""" %
          (send,send,10-send,send,2*send,back,10-send,back,10-send+back))
    elif number in receivers:
      n = receivers.index(number)
      receiver = number
      sender = senders[n]
      set("Wait...")
      _, _, send = get(("send", n, None))
      set("""<p>The sender sent: $%d.
             <br>You received: 2 &times; $%d = $%d.
             <br>How much do you return?<p>""" % (send,send,2*send))
      while grab(("click", number, None)): pass
      for i in range(0,2*send+1): smallbutton(i,"$%d"%i)
      _, _, back = get(("click", number, None))
      back = int(back)
      put(("back",n,back))
      add("""<p>You returned: $%d.
             <br>You earned: $%d &minus; $%d = $%d.""" %
          (back, 2*send, back, 2*send-back))
    if number > 0:
      while grab(("click", number, "ok")): pass
      button("ok","Proceed...")
      get(("click",number,"ok"))

  for _ in range(3):
    trust([1],[2])


run(session)
