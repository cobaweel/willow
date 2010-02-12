from willow import willow

# Read the configuration file
cfg = willow.config("da.cfg")
N = cfg["subjects"]

def session(number, net, board, log):
  net.add(number, open("da.html"))  
  if number > 0:
    net.set(number, "Subject %d" % number, "title")
    board.put(("on",))
  else:
    net.set(0, "Monitor", "title")
    for _ in range(1, N+1): board.get(("on",))
    for n in range(1, N+1): net.show(n, "." + cfg["roles"][n])
    for r in range(1, cfg["rounds"]+1):
      net.add(range(N+1), "Round %d has begun.\n" % r, "#msg")
      board.put(("end", 0, 0), cfg["length"])
      while True:
        event, subject, amount = board.get(("click", None, None),
                                           ("end", 0, 0))
        if event == "end":
          break
        elif event == "click":
          net.data(subject, "#amount")
          _, _, amount = board.get(("data", subject, None))
          amount = int(amount)
          net.add(range(N+1), "%d has bid %d.\n" % (subject, amount), "#msg")
      net.add(range(N+1), "Round %d has ended.\n" % r, "#msg")

willow.run(session)        
