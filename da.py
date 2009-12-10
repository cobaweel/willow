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
