from willow.willow import *
from willow.contrib import *
import random

def button(id, text, selector="body", number=None):
    html = ("<input class='small' type='submit' id='%s' value='%s'>" % 
            (id,text))
    add(html, selector, number)
def brbutton(id, text, selector="body", number=None):
    html = ("<br><input type='submit' class='wide' id='%s' value='%s'>" % 
            (id,text))
    add(html, selector, number)


def session():
  number = me()            # Client ID for this thread
  add(open("rt.html"),"head")

  
  # Log clients on
  clients = 0
  if number == 0:
    brbutton("start","start")
    initializing = True
    while initializing:
      event, subject, n = get(("click", 0, "start"),
                              ("logon", None, None))
      if event == "click":
        initializing = False
      else:
        clients += 1
        add("%d " % clients)
        put(("assign",subject,clients))
  else:
    brbutton("start","login")
    get(("click", me(), "start"))
    put(("logon", me(), None))
    _,_,new = get(("assign",me(),None))
    number = new
    set(number)

  # Nix superfluous clients

  if number == 0:
    options = []
    for i in range(0, clients+1):
      brbutton(i, "Use %d" % i)
      options += [("click", 0, "%d" % i)]
    _, _, use = get(*options)
    for client in range(1, int(use)+1):         put(("nix",client,False))
    for client in range(int(use)+1, clients+1): put(("nix",client,True))
    clients = int(use)
  else:
    _, _, nix = get(("nix",number,None))
    if nix:
      set("X")
      return

  def trust_0(senders, receivers):
    for _ in senders+receivers: put(("positions",senders,receivers))
    for _ in senders+receivers: get(("ping",))

  def trust_n(number, header):
    set(header)
    _, senders, receivers = get(("positions",None,None))      
    if number in senders:
      sender, receiver = number, receivers[senders.index(number)]
      set("<p>You have $10.<br>How much do you want to send?<p>")
      while grab(("click", number, None)): pass
      for i in range(0,11): button(i,"$%d"%i)
      _, _, send = get(("click", number, None))
      send = int(send)
      add("<p>Wait...")
      put(("send",receiver,send))
      _, _, back = get(("back",sender,None))
      add("""<p>You sent: $%d.
             <br>You kept: $10 &minus; $%d = $%d.
             <br>The receiver received: 3 &times; $%d = $%d.
             <br>The receiver returned: $%d.
             <br>You earned $%d + $%d = $%d.""" %
          (send,send,10-send,send,2*send,back,10-send,back,10-send+back))
      log("TRUST",sender,receiver,send,back)
    elif number in receivers:
      sender, receiver = senders[receivers.index(number)], number
      set("Wait...")
      _, _, send = get(("send", receiver, None))
      set("""<h2>%s</h2><p>The sender sent: $%d.
             <br>You received: 3 &times; $%d = $%d.
             <br>How much do you return?<p>""" % (header,send,send,2*send))
      while grab(("click", number, None)): pass
      for i in range(0,2*send+1): button(i,"$%d"%i)
      _, _, back = get(("click", number, None))
      back = int(back)
      put(("back",sender,back))
      add("""<p>You returned: $%d.
             <br>You earned: $%d &minus; $%d = $%d.""" %
          (back, 3*send, back, 3*send-back))
    while grab(("click", number, "ok")): pass
    brbutton("ok","Proceed...")
    get(("click",number,"ok"))
    set("Wait...")
    put(("ping",))

  if number == 0:
      trust_0([1],[2])
  else:
      trust_n(number,"Round 1")

run(session)
