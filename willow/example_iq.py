# This code was originally developed for administering a shortened
# form of the Raven Advanced Progressive Matrices, an IQ test. For
# copyright reasons, the JPG images used have been changed, but you
# can still use this as a template for how to do a test or survey
# where subjects are allowed to go back and forth between
# questions. The example requires exactly N_CLIENTS clients and a
# monitor. This is a neat example of how you can do a very simple
# system for monitoring results as they come in. The easiest way to
# test this is to run the python file and load 2frames.html in your
# browser. If you set N_CLIENTS to 6, you should use 6frames.html, and
# so on.

from willow.willow import *
from willow.branch import *
import time

N_CLIENTS  = 2                  # Number of clients required
N_IQ_ITEMS = 5                  # Number of IQ test items

def iq(me, numbers):
  answers = ["0"] * N_IQ_ITEMS  # Answers given so far
  current = 1                   # Current item being shown
  done = False                  # Has subject finished?

  let(N_IQ_ITEMS, "#total")     
  while not done:
    # Show the current item, and the current answer if any
    let(current, "#nr")
    poke("src","example_iq/%02d.jpg" % current, "img")
    pop("selected","button")
    push("selected","#%s" % answers[current-1])

    # When subject has completed all questions, give option to finish
    if not "0" in answers:
      hide("#going")
      show("#complete")

    # Process subject input
    msg = take_new({"tag": "click", "client": me})
    if msg["id"] == "prev":
      current = max(1, current-1)
    if msg["id"] == "next":
      current = min(N_IQ_ITEMS, current+1)
    if msg["id"] in ["1","2","3","4","5","6","7","8"]:
      global_nr =  current
      answers[current-1] = msg["id"]
      add("%s:%s " % (current,answers[current-1]),
          "li:eq(%s)" % (me-1), clients=0)
    if msg["id"] == "done":
      done = True

  # Write results to the log file
  for n in range(N_IQ_ITEMS):
    log("iq",me,n,answers[n])
      
def session(me, numbers):
  if me == 0: 
    # Monitor
    let("<h1>%s</h1><ol>" % time.ctime()) 
    for _ in range(N_CLIENTS): add("<li>","ol")
  else:
    # Subject
    let(open("example_iq/iq.html"))
    iq(me,numbers)
    let("")

assemble(session, range(N_CLIENTS + 1))

