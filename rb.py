from willow import willow
import random

def colors(fmt, n, k):
  sample = random.sample(range(n),k)
  return ",".join([ fmt % i for i in range(n) if not i in sample ])

cfg = willow.config("rb.cfg")

def session(client, board, log):
  client.add(open("rb.html"))
  board.get(("click", client.number, None))
  client.hold()
  client.hide("#title")
  client.set(cfg['ab_incentive'],".ab_incentive")
  client.set(cfg['cd_incentive'],".cd_incentive")
  client.show("#exp")
  score = 0
  client.set("0.00", "#score")
  client.flush()
  for _ in range(cfg['rounds']):
    d = random.choice((1,2,3,4))
    c = 10 * d + random.choice((-2,-1,0,1,2))
    b = random.choice((1,2,3,4))
    a = 10 * b + random.choice((-2,-1,0,1,2))
    white = (colors("#A td:eq(%d)", 100, a)+","+
             colors("#B td:eq(%d)",  10, b)+","+
             colors("#C td:eq(%d)", 100, c)+","+
             colors("#D td:eq(%d)",  10, d))
    client.hold()
    client.hide("#spin")
    client.pop("on",".on")
    client.push("on",white)
    client.flush()
    time = 5
    ab = "."
    cd = "."
    for t in range(1,6): board.put(("timer", client.number, 0), t)
    while time > 0:
      client.set("%d seconds left" % time,"#time")
      _, _, arg = board.get(("click", client.number, None),
                            ("timer", client.number, 0))
      client.hold()
      if arg == "A":
        client.push("on", "#A")
        client.pop("on", "#B")
        ab = "A"
      elif arg == "B":
        client.push("on", "#B")
        client.pop("on", "#A")
        ab = "B"
      elif arg == "C":
        client.push("on", "#C")
        client.pop("on", "#D")
        cd = "C"
      elif arg == "D":
        client.push("on", "#D")
        client.pop("on", "#C")
        cd = "D"
      else:
        time -= 1
      client.flush()
    ab_score = -1
    cd_score = -1
    if ab == "A":
      if random.randint(1,100) <= a:
        score += int(cfg['ab_incentive'])
        ab_score = 1
      else:
        ab_score = 0
    if ab == "B":
      if random.randint(1,10) <= b:
        score += int(cfg['ab_incentive'])
        ab_score = 1
      else:
        ab_score = 0
    if cd == "C":
      if random.randint(1,100) <= c:
        score += int(cfg['cd_incentive'])
        cd_score = 1
      else:
        cd_score = 0
    if cd == "D":
      if random.randint(1,10) <= d:
        score += int(cfg['cd_incentive'])
        cd_score = 1
      else:
        cd_score = 0
    log.write(client.number,a,b,c,d,ab,cd,ab_score,cd_score,score)
    client.hold()
    client.set("%.2f" % (score/100.0), "#score")
    client.set("", "#time")
    client.pop("on",".on")
    client.show("#spin")
    client.flush()
    board.put(("timer", client.number, 0), 2)
    board.get(("timer", client.number, 0))


willow.run(session,8000)


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
