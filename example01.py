# Willow, a Python framework for experimental economics. Copyright (c)
# 2009, George Mason University. All rights reserved. Redistribution
# allowed under certain conditions; see file COPYING.txt

AB=5
CD=3
ROUNDS=10
INTERVAL=5

from willow.willow import *
import random


def session(number):
  add(open("example01.html"))

  # Set the incentive labels based on treatment variables
  let(AB,".ab_incentive")
  let(CD,".cd_incentive")

  # Show the title screen and wait for the button
  show("#title")
  take({"tag":"click"})

  # Hide the title screen and show the experiment screen
  hide("#title")
  show("#exp")

  # Run through a number of rounds
  score = 0
  let("0.00", "#score")
  for _ in range(ROUNDS):
    # Determine how many balls in boxes a,b,c,d will be white
    d = random.choice((1,2,3,4))
    c = 10 * d + random.choice((-2,-1,0,1,2))
    b = random.choice((1,2,3,4))
    a = 10 * b + random.choice((-2,-1,0,1,2))

    # Randomly color the balls
    def colors(fmt, n, k):
      sample = random.sample(range(n),k)
      return ",".join([ fmt % i for i in range(n) if not i in sample ])
    white = (colors("#A td:eq(%d)", 100, a)+","+
             colors("#B td:eq(%d)",  10, b)+","+
             colors("#C td:eq(%d)", 100, c)+","+
             colors("#D td:eq(%d)",  10, d))
    pop("on",".on")
    push("on",white)

    # Now, the subject has INTERVAL seconds to make selections
    time = INTERVAL
    ab = "."
    cd = "."
    def timeout():
      put({"tag":"timer", "client":number})
    background(timeout, 5)
    for dt in range(0,5):
      let(5-dt, "#time", delay=dt)
    while True:
      msg = take({"tag": "click", "client": number},
                 {"tag": "timer", "client": number})
      if msg["tag"] == "click":
        arg = msg["id"]
        if arg == "A":
          push("on", "#A")
          pop("on", "#B")
          ab = "A"
        elif arg == "B":
          push("on", "#B")
          pop("on", "#A")
          ab = "B"
        elif arg == "C":
          push("on", "#C")
          pop("on", "#D")
          cd = "C"
        elif arg == "D":
          push("on", "#D")
          pop("on", "#C")
          cd = "D"
      else:
        break;

    # Compute earnings
    if ab == "A":
      if random.randint(1,100) <= a:
        score += int(AB)
    if ab == "B":
      if random.randint(1,10) <= b:
        score += int(AB)
    if cd == "C":
      if random.randint(1,100) <= c:
        score += int(CD)
    if cd == "D":
      if random.randint(1,10) <= d:
        score += int(CD)

    # Log what happened
    log(number,a,b,c,d,ab,cd)

    let("%.2f" % (score/100.0), "#score")
    let("", "#time")
    pop("on",".on")
    sleep(2)
      
run(session)
