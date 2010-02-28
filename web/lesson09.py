from willow.willow import *

def session(me):
  if me == 0:
    add(open("lesson09_0.html"))
    msg = take({"tag": "click"})
    bid = int(msg["id"])
    put({"tag": "bid", "amount": bid})
    show("#wait")
    add(bid, "#offer")
    msg = take({"tag": "accept"})
    accept = msg["accepted"]
    if accept:
      show("#accept,#pay")
      add(10 - bid, "#payoff")
    else:
      show("#reject,#pay")
      add(0, "#payoff")
    log("bid", bid)
    log("reaction", accept)
  elif me == 1:
    add(open("lesson09_1.html"))
    msg = take({"tag":"bid"})
    bid = msg["amount"]
    show("#offer")
    add(bid, "#bid")
    msg = take({"tag": "click"})
    accept = msg["id"] 
    if accept == "accept":
      show("#pay")
      add(bid,"#payoff")
      put({"tag": "accept", "accepted": True})
    else:
      show("#pay")
      add(0, "#payoff")
      put({"tag": "accept", "accepted": False})
  else:
    add("<h1>Experiment is full.</h1>")

run(session)
