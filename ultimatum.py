from willow import willow

def session(number, net, board, log):
  if number == 0:
    net.add(0, open("ultimatum0.html"))
    _, _, bid = board.get(("click", 0, None))
    bid = int(bid)
    board.put(("bid", bid))
    net.show(0, "#wait")
    net.add(0, bid, "#offer")
    _, accept = board.get(("accept", None))
    if accept:
      net.show(0, "#accept,#pay")
      net.add(0, 10-bid, "#payoff")
    else:
      net.show(0, "#reject,#pay")
      net.add(0, 0,"#payoff")
    log.write("bid", bid)
    log.write("reaction", accept)
  elif number == 1:
    net.add(1, open("ultimatum1.html"))
    _, bid = board.get(("bid", None))
    net.show(1, "#offer")
    net.add(1, bid, "#bid")
    _, _, response = board.get(("click", 1, None))
    if response == "accept":
      net.show(1, "#pay")
      net.add(1, 10-bid,"#payoff")
      board.put(("accept",  True))
    else:
      net.show(1, "#pay")
      net.add(1, 0, "#payoff")
      board.put(("accept",  False))
  else:
    net.add(number, "<h1>Experiment is full.</h1>")

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
