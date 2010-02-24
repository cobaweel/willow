AB=5
CD=3
ROUNDS=10
INTERVAL=5

from willow.willow import *
import random


def session():
  number = me()
  add(open("rb.html"))

  # Set the incentive labels based on treatment variables
  set(AB,".ab_incentive")
  set(CD,".cd_incentive")

  # Show the title screen and wait for the button
  show("#title")
  get(("click", number, None))

  # Hide the title screen and show the experiment screen
  hide("#title")
  show("#exp")

  # Run through a number of rounds
  score = 0
  set("0.00", "#score")
  for _ in range(ROUNDS):
    # Reset the screen to standard form
    hide("#spin")

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
    for t in range(1,6): put(("timer", number, 0), t)
    while time > 0:
      set("%d seconds left" % time,"#time")
      _, _, arg = get(("click", number, None),
                      ("timer", number, 0))
      add(arg)
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
        time -= 1
    ab_score = -1
    cd_score = -1
    if ab == "A":
      if random.randint(1,100) <= a:
        score += int(AB)
        ab_score = 1
      else:
        ab_score = 0
    if ab == "B":
      if random.randint(1,10) <= b:
        score += int(AB)
        ab_score = 1
      else:
        ab_score = 0
    if cd == "C":
      if random.randint(1,100) <= c:
        score += int(CD)
        cd_score = 1
      else:
        cd_score = 0
    if cd == "D":
      if random.randint(1,10) <= d:
        score += int(CD)
        cd_score = 1
      else:
        cd_score = 0
    log(number,a,b,c,d,ab,cd,ab_score,cd_score,score)
    set("%.2f" % (score/100.0), "#score")
    set("", "#time")
    pop("on",".on")
    show("#spin")
    put(("timer", number, 0), 2)
    get(("timer", number, 0))


run(session)
