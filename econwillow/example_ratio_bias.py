# This is an example of an individual choice paradigm. There is no
# interaction, but the user interface is comparatively sophisticated.
# The subject is shown sets of circles, each circle white or red. The
# sets come in pairs, one of 10 circles and on of 100, with
# approximately but not quite the same *proportion* of red circles in
# each of the two sets in a pair. The subject is to select the set
# with highest proportion of red circles. (This is incentivized by
# drawing a circle from the chosen set at random and paying the
# subject if it is red.) The literature on this shows that subjects
# are more likely to incorrectly pick the large field when the small
# field is optimal than vice versa. To further complicate matters,
# there are actually two of these tasks on the screen, both of which
# the subject can solve, and the experimenter can vary the incentives
# for both.

AB = 5                          # Incentive for left task
CD = 3                          # Incentive for right task
ROUNDS=10                       # Number of iterations
INTERVAL=5                      # How much time to solve each (in seconds)

from willow.willow import *
import random

def session(number):
  add(open("example_ratio_bias/0.html"))

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
