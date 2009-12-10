from willow import willow
import random

ROUNDS = 2
LIKERT = ["1. Very inaccurate",
          "2. Moderately inaccurate",
          "3. Neither inaccurate nor accurate",
          "4. Moderately accurate",
          "5. Very accurate"]

SURVEY = [
  ("""Describe yourself as you generally are now, not as you
      wish to be in the future. Describe yourself as you honestly see
      yourself, in relation to other people you know of the same sex as you
      are, and roughly your same age. So that you can describe yourself in
      an honest manner, your responses will be kept in absolute
      confidence.<p>Indicate for each statement whether it is 1. Very
      Inaccurate, 2. Moderately Inaccurate, 3. Neither Accurate Nor
      Inaccurate, 4. Moderately Accurate, or 5. Very Accurate as a
      description of you.""",["Proceed"]),
  ("I am the life of the party.",LIKERT),
  ("I feel little concern for others.",LIKERT),
  ("I am always prepared.",LIKERT),
  ("I get stressed out easily.",LIKERT),
  ("I have a rich vocabulary.",LIKERT),
  ("I don't talk a lot.",LIKERT),
  ("I am interested in people.",LIKERT),
  ("I leave my belongings around.",LIKERT),
  ("I am relaxed most of the time.",LIKERT),
  ("I have difficulty understanding abstract ideas.",LIKERT),
  ("I feel comfortable around people.",LIKERT),
  ("I insult people.",LIKERT),
  ("I pay attention to details.",LIKERT),
  ("I worry about things.",LIKERT),
  ("I have a vivid imagination.",LIKERT),
  ("I keep in the background.",LIKERT),
  ("I sympathize with others' feelings.",LIKERT),
  ("I make a mess of things.",LIKERT),
  ("I seldom feel blue.",LIKERT),
  ("I am not interested in abstract ideas.",LIKERT),
  ("I start conversations.",LIKERT),
  ("I am not interested in other people's problems.",LIKERT),
  ("I get chores done right away.",LIKERT),
  ("I am easily disturbed.",LIKERT),
  ("I have excellent ideas.",LIKERT),
  ("I have little to say.",LIKERT),
  ("I have a soft heart.",LIKERT),
  ("I often forget to put things back in their proper place.",LIKERT),
  ("I get upset easily.",LIKERT),
  ("I do not have a good imagination.",LIKERT),
  ("I talk to a lot of different people at parties.",LIKERT),
  ("I am not really interested in others.",LIKERT),
  ("I like order.",LIKERT),
  ("I change my mood a lot.",LIKERT),
  ("I am quick to understand things.",LIKERT),
  ("I don't like to draw attention to myself.",LIKERT),
  ("I take time out for others.",LIKERT),
  ("I shirk my duties.",LIKERT),
  ("I have frequent mood swings.",LIKERT),
  ("I use difficult words.",LIKERT),
  ("I don't mind being the center of attention.",LIKERT),
  ("I feel others' emotions.",LIKERT),
  ("I follow a schedule.",LIKERT),
  ("I get irritated easily.",LIKERT),
  ("I spend time reflecting on things.",LIKERT),
  ("I am quiet around strangers.",LIKERT),
  ("I make people feel at ease.",LIKERT),
  ("I am exacting in my work.",LIKERT),
  ("I often feel blue.",LIKERT),
  ("I am full of ideas.",LIKERT),
  ("Now proceed to the next section of the questionnaire.",["Proceed"]),
  ("What is your age in years?",None),
  ("What is your gender?",["Male","Female"]),
  ("What is the highest level of education that you have completed?",
   ["Less than high school","High school diploma or GED",
    "Bachelor's degree","Master's degree","Doctoral degree"]),
  ("What class are you in?",
   ["Freshman","Sophomore","Junior","Senior","MA student",
    "Pre-dissertation PhD student","Dissertation PhD student"]),
  ("In what range is your GPA?",
   ["0 to 2.0","2.1 to 2.5","2.6 to 3.0","3.1 to 3.5","3.6 to 4.0"]),
  ("If you took it, what was your SAT verbal score?"+
   " (Leave blank if you did not take it.)",None),
  ("If you took it, what was your SAT quantitative score?"+
   " (Leave blank if you did not take it.)",None),
  ("If you took it, what was your GRE verbal score?"+
   " (Leave blank if you did not take it.)",None),
  ("If you took it, what was your GRE quantitative score?"+
   " (Leave blank if you did not take it.)",None),
  ("If you took it, what was your GRE analytical score?"+
   " (Leave blank if you did not take it.)",None)
]


HEADER = """
<style type="text/css">
body { font-size: 24pt; }
input { font-size: 18pt;}
input.wide { width: 800px; }
</style>
"""

def session(number, net, board, log):
  if number == 0:
    subjects = 0
    net.add(0, "<h1>Monitor console</h1>")
    net.add(0, "When enough subjects are logged in, click"+
               " <input type='submit' id='start' value='here'>.")
    while True:
      event, subject, _ = board.get(("click", 0, "start"),
                                    ("logon", None, None))
      if event == "click" and subjects > 0 and subjects % 2 == 0:
        break
      elif event == "click":
        net.add(0, "<li>Number of subjects must be positive and even.")
      else:
        net.add(0, "<li>Subject %d logged on." % subject)
        subjects += 1
    assert subjects > 0 and subjects % 2 == 0

    net.add(0,"<p>How many subjects showed up?<p>")
    subjects_options = []
    for i in range(2,subjects + 1,2):
      net.add(0,"<input type='submit' id='%d' value='%d'>" % (i,i))
      subjects_options += [("click",0,"%d" % i)]
    _,_,show_ups = board.get(*subjects_options)
    show_ups = int(show_ups)
    for i in range(show_ups+1,subjects+1): 
      net.set(i,HEADER+"Do not use this terminal.")
    subjects = show_ups

    net.add(0, "<h2>Task 1</h2>"+
               "<p><input type='submit' id='first' value='Click to start'>")
    board.get(("click",number,"first"))
    shuffle = random.sample(range(1,subjects+1), subjects)
    for subject in range(1,subjects+1):
      group = shuffle.index(subject) / 2
      role  = shuffle.index(subject) % 2
      net.add(0, "<li>Subject %d is in group %d role %d" % (subject,group,role))
      log.write("ASSIGN1",subject,group,role)
      board.put(("assign", subject, (group,role)))
    for _ in range(ROUNDS):
      for _ in range(subjects): board.get(("round-ping",))
      for _ in range(subjects): board.put(("round-pong",))
    for subject in range(1, subjects+1):
      board.get(("done",subject, "first"))

    net.add(0, "<h2>Task 2</h2>"+
               "<p><input type='submit' id='second' value='Click to start'>")
    board.get(("click",number,"second"))
    for subject in range(1,subjects+1):
      group = shuffle.index(subject) / 2
      role  = shuffle.index(subject) % 2
      if role == 1: group = (group + 1) % (subjects / 2)
      net.add(0, "<li>Subject %d is in group %d role %d" % (subject,group,role))
      log.write("ASSIGN2",subject,group,role)
      board.put(("assign", subject, (group,role)))
    for _ in range(ROUNDS):
      for _ in range(subjects): board.get(("round-ping",))
      for _ in range(subjects): board.put(("round-pong",))
    for subject in range(1, subjects+1):
      board.get(("done",subject,"second"))

    payoffs = ""
    payoffs += """<h2>Payoffs</h2><table border="1"><tr>
                  <td>Subject</td><td>Task 1</td>
                  <td>Task 2</td></tr>"""
    for subject in range(1, subjects+1):
      _,_,cash1,cash2 = board.get(("cash",subject, None,None))
      payoffs += ("<tr><td>%d</td><td>%d</td><td>%d</td></tr>" %
                  (subject, cash1, cash2))
    payoffs += "</table>"
    net.add(0,payoffs)

    net.add(0, "<h2>Task 3</h2>"+
               "<p><input type='submit' id='third' value='Click to start'>")
    board.get(("click",number,"third"))
    for subject in range(1,subjects+1):
      board.put(("third",subject,None))
    for subject in range(1,subjects+1):
      board.get(("done",subject,"third"))
    
  else:
    net.set(number, HEADER+"You are subject %d. Please wait..." % number)
    board.put(("logon", number, None))

    cash1 = 0
    _, _, (group,role) = board.get(("assign",number, None))
    for round in range(1,ROUNDS+1):
      while board.grab(("click", number, None)): pass
      net.set(number, HEADER+"<h2>Task 1 round %d of %d.</h2>" % (round,ROUNDS))
      net.add(0, "<li>Subject %d started round %d" % (number,round))
      net.add(number,"""
<li>If you choose blue and the other person chooses blue you earn $0.50.
<li>If you choose blue and the other person chooses green you earn $0.50.
<li>If you choose green and the other person chooses blue you earn $0.00.
<li>If you choose green and the other person chooses green you earn $0.75.
""")
      net.add(number, ("<p>Choose <input type='submit' id='G.%d' value='green'>"+
                       " or <input type='submit' id='B.%d' value='blue'>...")%
                          (round,round))

      _, _, choice = board.get(("click", number, "B.%d" % round),
                               ("click", number, "G.%d" % round))
      choice = choice[0]
      board.put(("choice", (group, role), choice))
      if choice == "G":
        net.add(number, "<p>You chose green.")
      elif choice == "B":
        net.add(number, "<p>You chose blue.")
      else:
        assert False, "IMPOSSIBLE"
      _, _, other  = board.get(("choice", (group, 1-role), None))
      if   choice == "B" and other == "B": now = 50
      elif choice == "B" and other == "G": now = 50
      elif choice == "G" and other == "B": now = 0
      elif choice == "G" and other == "G": now = 75
      cash1 += now
      net.add(number, ("""<p>In this round, you earned $%.2f.
                          <p>So far you have earned $%.2f in task 1.""" %
                         (now/100., cash1/100.)))
      log.write("CHOICE1",number,group,role,round,choice,other)
      log.write("CASH1",number,cash1)
      net.add(number,
              ("<p>Click to <input type='submit' id='1.%d' value='proceed'>"%
               round))
      board.get(("click",number,"1.%d"%round))
      net.set(number,HEADER+"Wait...")
      board.put(("round-ping",))
      board.get(("round-pong",))
    net.set(number,
            (HEADER+"Task 1 is over. You earned a total of $%.2f in task 1." %
             (cash1/100.0)))
    board.put(("done",number,"first"))

    cash2 = 0
    _, _, (group,role) = board.get(("assign",number, None))
    for round in range(1,ROUNDS+1):
      while board.grab(("click", number, None)): pass
      net.set(number, HEADER+"<h2>Task 2 round %d of %d.</h2>" % (round,ROUNDS))
      net.add(0, "<li>Subject %d started round %d" % (number,round))
      net.add(number,"""
<li>If you choose square and the other person chooses square you earn $0.25.
<li>If you choose square and the other person chooses circle you earn $1.50.
<li>If you choose circle and the other person chooses square you earn $0.00.
<li>If you choose circle and the other person chooses circle you earn $1.00.
""")
      net.add(number, ("<p>Choose <input type='submit' id='S.%d' value='square'>"+
                       " or <input type='submit' id='C.%d' value='circle'>...")%
                          (round,round))
      _, _, choice = board.get(("click", number, "S.%d" % round),
                               ("click", number, "C.%d" % round))
      choice = choice[0]
      board.put(("choice", (group, role), choice))
      if choice == "S":
        net.add(number, "<p>You chose square.")
      elif choice == "C":
        net.add(number, "<p>You chose circle.")
      _, _, other  = board.get(("choice", (group, 1-role), None))
      if   choice == "S" and other == "S": now = 25
      elif choice == "S" and other == "C": now = 150
      elif choice == "C" and other == "S": now = 0
      elif choice == "C" and other == "C": now = 100
      cash2 += now
      net.add(number, ("""<p>In this round, you earned $%.2f.
                          <p>So far you have earned $%.2f in task 2.""" %
                       (now/100., cash2/100.)))
      log.write("CHOICE2",number,group,role,round,choice,other)
      log.write("CASH2",number,cash2)
      net.add(number,
              ("<p>Click to <input type='submit' id='2.%d' value='proceed'>"%
               round))
      board.get(("click",number,"2.%d"%round))
      net.set(number,HEADER+"Wait...")
      board.put(("round-ping",))
      board.get(("round-pong",))
    net.set(number,(HEADER+"""Task 2 is over. You earned a total of $%.2f in task 1
                      and $%.2f in task 2."""%
                    (cash1/100.0,cash2/100.0)))
    board.put(("done",number,"second"))
    board.put(("cash",number,cash1,cash2))
    
    board.get(("third",number,None))
    for question in range(1,len(SURVEY)+1):
      net.add(0, "<li>Subject %d answering question %d" % (number,question))
      text, options = SURVEY[question-1]
      net.set(number, HEADER + "<p>%s<p>" % text)
      if options:
        clicks = []
        for option in options:
          option_id = "%s*%d" % (option,question)
          net.add(number,
                  ("<input type='submit' id='%s' value='%s' class='wide'><br>" % 
                   (option_id,option)))
          clicks += [("click",number,option_id)]
        _,_,answer = board.get(*clicks)
        log.write("SURVEY",number,question,answer)
      else:
        net.add(number,("""<input type='text' id='answer-%d' style='wide'>
                          <input type='submit' id='submit-%d' value='OK'>"""%
                        (question,question)))
        board.get(("click",number,"submit-%d" % question))
        net.data(number,"#answer-%d" % question)
        _,_,answer = board.get(("data",number,None))
        log.write("SURVEY",number,question,answer)
  net.add(0,"Task 3 is over.")
  net.set(number,HEADER+"Task 3 is over.")
  board.put(("done",number,"third"))

willow.run(session)
