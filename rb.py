from willow import willow
import random

def colors(fmt, n, k):
  sample = random.sample(range(n),k)
  return ",".join([ fmt % i for i in range(n) if not i in sample ])

cfg = willow.config("rb.cfg")

def session(number, net, board, log):
  net.add(number, open("rb.html"))
  board.get(("click", number, None))
  net.hold(number)
  net.hide(number, "#title")
  net.set(number, cfg['ab_incentive'],".ab_incentive")
  net.set(number, cfg['cd_incentive'],".cd_incentive")
  net.show(number, "#exp")
  score = 0
  net.set(number, "0.00", "#score")
  net.flush(number)
  for _ in range(cfg['rounds']):
    d = random.choice((1,2,3,4))
    c = 10 * d + random.choice((-2,-1,0,1,2))
    b = random.choice((1,2,3,4))
    a = 10 * b + random.choice((-2,-1,0,1,2))
    white = (colors("#A td:eq(%d)", 100, a)+","+
             colors("#B td:eq(%d)",  10, b)+","+
             colors("#C td:eq(%d)", 100, c)+","+
             colors("#D td:eq(%d)",  10, d))
    net.hold(number)
    net.hide(number, "#spin")
    net.pop(number, "on",".on")
    net.push(number, "on",white)
    net.flush(number)
    time = 5
    ab = "."
    cd = "."
    for t in range(1,6): board.put(("timer", number, 0), t)
    while time > 0:
      net.set(number, "%d seconds left" % time,"#time")
      _, _, arg = board.get(("click", number, None),
                            ("timer", number, 0))
      net.hold(number)
      if arg == "A":
        net.push(number, "on", "#A")
        net.pop(number, "on", "#B")
        ab = "A"
      elif arg == "B":
        net.push(number, "on", "#B")
        net.pop(number, "on", "#A")
        ab = "B"
      elif arg == "C":
        net.push(number, "on", "#C")
        net.pop(number, "on", "#D")
        cd = "C"
      elif arg == "D":
        net.push(number, "on", "#D")
        net.pop(number, "on", "#C")
        cd = "D"
      else:
        time -= 1
      net.flush(number)
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
    log.write(number,a,b,c,d,ab,cd,ab_score,cd_score,score)
    net.hold(number)
    net.set(number, "%.2f" % (score/100.0), "#score")
    net.set(number, "", "#time")
    net.pop(number, "on",".on")
    net.show(number, "#spin")
    net.flush(number)
    board.put(("timer", number, 0), 2)
    board.get(("timer", number, 0))


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
