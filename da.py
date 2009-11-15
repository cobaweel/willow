from willow import willow

# Read the configuration file
cfg = willow.config("da.cfg")
N = cfg["subjects"]
R = cfg["rounds"]
LENGTH = cfg["length"]

# The monitor client
def monitor(client, board, log):
  # Show the monitor interface
  client.add(open("da.html"))
  client.add("Monitor","h1")

  # Wait for all subjects to connect, then notify them all
  subjects = set()
  while not subjects == set(range(1,N+1)):
    _, new_subject = board.get(("login", None))
    client.add("Subject %d logged in.\n" % new_subject, "#status")
    subjects.add(new_subject)
  for n in range(N+1):
    board.put(("start",n))

  # Run R rounds of the double auction    
  for r in range(R):
    # Tell everyone the round starts now, and after LENGTH seconds,
    # tell everyone the round ends.
    for n in range(N+1):
      board.put(("status", n, "Round %d has begun.\n" % r))
      board.put(("end", n, r), LENGTH)
    while True:
      event, x, y = board.get(("order", None, None),
                              ("book", client.number, None),
                              ("status",client.number, None),
                              ("end", client.number, None))
      if event == "end":
        break
      elif event == "status":
        client.add(y,"#status")
      elif event == "order":
        for n in range(N+1):
          board.put(("book", n, "Subject %r has bid %d.\n" % (x,y)))
      elif event == "book":
        client.add(y,"#book")
    client.add("Round %d has ended.\n" % r, "#status")

# The subject clients        
def subject(client, board, log):
  # Notify the monitor that we have connected
  board.put(("login", client.number))

  # Show the subject interface, with bid or ask button as appropriate
  client.add(open("da.html"))
  client.add("Subject %d" % client.number,"h1")
  if client.number % 2:
    client.show("#bid")
  else:
    client.show("#ask")
    
  # Wait for the start signal
  board.get(("start",client.number))
  client.show("#input")

  # Run R rounds of the double auction
  for r in range(R):
    while True:
      event, _, y = board.get(("click", client.number, None),
                              ("status", client.number, None),
                              ("book", client.number, None),
                              ("end", client.number, None))
      if event == "click":
        client.data("#amount")
        _, _, amount = board.get(("data", client.number, None))
        try:
          amount = int(amount)
          board.put(("order", client.number, amount))
        except:
          pass
      elif event == "book" and y == "":
        client.set("","#book")          
      elif event == "book":
        client.add(y,"#book")
      elif event == "status":
        client.add(y,"#status")          
      elif event == "end":
        client.set("","#book")
        break
    client.add("Round %d has ended.\n" % r, "#status")

# The first client that connects becomes the monitor, the rest are
# subjects
def session(client, board, log):
  if client.number == 0:
    monitor(client, board, log)
  else:
    subject(client, board, log)

willow.run(session)        

# Willow, a Python framework for experimental economics
# Copyright (c) 2009, George Mason University
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the George Mason University nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission. THIS SOFTWARE
# IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
