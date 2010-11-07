from willow import *
import random

# === assemble(session, clients=[], port=8000)
#
# This function is a replacement for run(). If clients is not
# specified, it will display buttons on client 0 as clients 1, 2,
# ... log on, which show subsets of the clients that have logged on so
# far. You can click one of these buttons at any time, and at that
# point, the function session() will be run once for each client IN
# THE SUBSET, with its client ID as the first number and the list of
# all client IDs IN THE SUBSET as its second argument. Clients that
# have connected but that are not in the subset will get a big X on
# their screens. The second way of using assemble() is to specify an
# explicit argument for clients=, some list of integers that indicates
# which clients you want. Once those client numbers have logged on,
# the session function is started once for every such client, and
# again any clients not in the set get a big X.
def assemble(session, clients=[], port=8000):
  def wrapper(me):
    let(me,"title")
    if me == 0:
      pool = [0]
      while True:
        if pool == clients:
          subset = pool
          break
        let("")
        for i in range(len(pool)):
          subset = pool[0:i+1]
          button_label = ""
          for i in range(max(subset+clients)+1):
            if i in subset:
              button_label += "%s " % i
            else:
              button_label += "_ "
          button_id = " ".join(map(str,subset))
          if clients == []:
            add("<button id='%s'>%s</button><br>" %
                (button_id, button_label))
          else:
            add("<p><tt>%s</tt>" % button_label)
        msg = take({"tag": "login"},
                   {"tag": "click"})
        if msg["tag"] == "click":
          subset = map(int, msg["id"].split())
          break
        client = msg["client"]
        pool.append(client)
        pool.sort()
      for i in pool:
        if i == 0:
          pass
        elif i in subset:
          put({"tag":"ping","pool":pool, "client":i})
        else:
          put({"tag":"ping","pool":None, "client":i})          
    else:
      let("<h1 style='font-size:3000%%'>%s</h1>" % me)
      put({"tag":"login","client": me})
      msg = take({"tag":"ping","client":me})
      pool = msg["pool"]
    if pool:
      let("<h1 style='color:green; font-size:3000%%'>%s</h1>" % me)
      session(me,pool)
    else:
      let("<h1 style='color:red; font-size:3000%%'>X</h1>")
  run(wrapper, port=port)

def sync(client,clients):
    if client == clients[0]:
      for n in clients[1:]: take({"tag":"syncping","client":n})
      for n in clients[1:]: put({"tag":"syncpong","client":n})
    else:
      put({"tag":"syncping","client":client})
      take({"tag":"syncpong","client":client})

def take_new(arg):
  while grab(arg): pass
  return take(arg)

# === Examples ===
#
# There is much additional useful code in the example_*.py files,
# which illustrate various ways to use Willow.
