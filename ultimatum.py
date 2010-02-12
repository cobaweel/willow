from willow.willow import *

def session():
  if me() == 0:
    add(open("ultimatum0.html"))
    _, _, bid = get(("click", 0, None))
    bid = int(bid)
    put(("bid", bid))
    show("#wait")
    add(bid, "#offer")
    _, accept = get(("accept", None))
    if accept:
      show("#accept,#pay")
      add(10 - bid, "#payoff")
    else:
      show("#reject,#pay")
      add(0, "#payoff")
    log("bid", bid)
    log("reaction", accept)
  elif me() == 1:
    add(open("ultimatum1.html"))
    _, bid = get(("bid", None))
    show("#offer")
    add(bid, "#bid")
    _, _, response = get(("click", 1, None))
    if response == "accept":
      show("#pay")
      add(10-bid,"#payoff")
      put(("accept",  True))
    else:
      show("#pay")
      add(0, "#payoff")
      put(("accept",  False))
  else:
    add("<h1>Experiment is full.</h1>")

run(session)
