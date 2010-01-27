from willow.willow import *
from willow.contrib import *
import random

ROUNDS = 10
T12    = True
T3     = True

def button(id, text, selector="body", number=None):
    html = "<br><input type='submit' id='%s' value='%s'>" % (id,text)
    add(html, selector, number)


def session():
  #
  # Get clients to connect. They will be assigned subject numbers in
  # the order the log-on buttons are clicked, which may be different
  # from me(), although the monitor retains number 0 for both..
  #

  if me() == 0:
    clients = 0         # Number of clients connected
    subjects = 0        # Number of clients in use after nixing
    subject = 0         # Monitor is always subject 0
    add(open("cc0.html"),"head")
    button("start","Click when clients are all logged on.")
    while True:
      event, subject, _ = get(("click", 0, "start"),
                              ("logon", None, None))
      if event == "click":
        break
      elif event == "logon":
        clients += 1
        put(("rename",subject,clients))
  else:
    add(open("cc.html"),"head")
    button("logon","Log on")
    get(("click", me(),"logon"))
    put(("logon", me(), None))
    _, _, subject = get(("rename",me(),None))
    set("%d" % subject)
    add("%d " % subject, number=0)


  #
  # Now we are going to "nix" some subset of the logged on clients,
  # based on how many subjects actually showed up for our session. The
  # rest will have their session threads terminated and their screens
  # marked "X".
  #

  if me() == 0:
    options = []
    for i in range(0, 2 * (clients / 2) + 1, 2):
      button(i, "Click if %d subjects showed up" % i)
      options += [("click", 0, "%d" % i)]
    _, _, show_ups = get(*options)
    subjects = int(show_ups)
    for client in range(1, subjects+1): put(("nix",client,False))
    for client in range(subjects+1, clients+1): put(("nix",client,True))
  else:
    _, _, nix = get(("nix",subject,None))
    if nix:
      set("X")
      return

  #
  # At this point, the monitor thread is aware of the number of
  # clients and the number of subjects (i.e. active clients), and each
  # active client is aware of its subject number. Now we can start the
  # experiment.
  #


  #
  # Task 1
  #
  if T12:
    if me() == 0:
      # Wait for button click
      button("first","Start task 1")
      get(("click",me(),"first"))

      # Assign groups and roles to all subjects
      shuffle = random.sample(range(1,subjects+1), subjects)
      for subject in range(1,subjects+1):
        group = shuffle.index(subject) / 2
        role  = shuffle.index(subject) % 2
        add("<li>Subject %d is in group %d role %d" % (subject,group,role))
        log("ASSIGN1",subject,group,role)
        put(("assign", subject, (group,role)))

      # Synchronize the rounds
      for _ in range(1,ROUNDS+1):
        for _ in range(subjects): get(("ping",))
        for _ in range(subjects): put(("pong",))
      for _ in range(subjects): get(("ping",))

    else:
      # Retrieve group/role assignment
      _, _, (group,role) = get(("assign",subject, None))

      # Play rounds
      cash1 = 0
      for round in range(1,ROUNDS+1):
        while grab(("click", me(), None)): pass
        add("<li>Subject %d started round %d" % (subject,round), number=0)      
        set("""<h1>Task 1 round %d of %d.</h1><li>If you choose blue and
        the other person chooses blue you earn $0.50.<li>If you choose
        blue and the other person chooses green you earn $0.50.<li>If
        you choose green and the other person chooses blue you earn
        $0.00.  <li>If you choose green and the other person chooses
        green you earn $0.75.<p>Choose <input type='submit' id='G.%d'
        value='green'> or <input type='submit' id='B.%d'
        value='blue'>...""" % (round,ROUNDS,round,round))
        _, _, choice = get(("click", me(), "B.%d" % round),
                           ("click", me(), "G.%d" % round))
        choice = choice[0]
        put(("choice", (group, role), choice))
        if choice == "G":
          add("<p>You chose green.")
        elif choice == "B":
          add("<p>You chose blue.")
        _, _, other  = get(("choice", (group, 1-role), None))
        if   choice == "B" and other == "B": now = 50
        elif choice == "B" and other == "G": now = 50
        elif choice == "G" and other == "B": now = 0
        elif choice == "G" and other == "G": now = 75
        cash1 += now
        add(("""<p>In this round, you earned $%.2f.<p>So far you have
        earned $%.2f in task 1.""" % (now/100., cash1/100.)))
        log("CHOICE1", subject, group, role, round, choice, other)
        log("CASH1", subject, cash1)
        button("1.%d" % round, "Click to proceed")
        get(("click", me(), "1.%d" % round))
        set("Wait...")
        put(("ping", ))
        get(("pong", ))
      put(("ping", ))
      set(("Task 1 is over. You earned a total of $%.2f in task 1." %
           (cash1/100.0)))


    #
    # Task 2
    #

    if me() == 0:
      # Wait for button click to start task 2
      button("second", "Start task 2")
      get(("click", me(), "second"))

      # Assign groups and roles to all subjects
      for subject in range(1, subjects+1):
        group = shuffle.index(subject) / 2
        role  = shuffle.index(subject) % 2
        if role == 1: group = (group + 1) % (subjects / 2)
        add("<li>Subject %d is in group %d role %d" % (subject, group, role))
        log("ASSIGN2", subject, group, role)
        put(("assign", subject, (group, role)))

      # Synchronize the rounds
      for _ in range(ROUNDS):
        for _ in range(subjects): get(("ping", ))
        for _ in range(subjects): put(("pong", ))
      for _ in range(subjects): get(("ping", ))

    else:
      # Retrieve group/role assignment
      _, _, (group,role) = get(("assign",subject, None))

      # Play rounds
      cash2 = 0
      for round in range(1,ROUNDS+1):
        while grab(("click", me(), None)): pass
        add("<li>Subject %d started round %d" % (subject,round), number=0)
        set("""<h1>Task 2 round %d of %d.</h1><li>If you choose square
        and the other person chooses square you earn $0.25.<li>If you
        choose square and the other person chooses circle you earn
        $1.50.  <li>If you choose circle and the other person chooses
        square you earn $0.00.  <li>If you choose circle and the other
        person chooses circle you earn $1.00.<p>Choose <input
        type='submit' id='S.%d' value='square'> or <input type='submit'
        id='C.%d' value='circle'>...""" % (round, ROUNDS, round, round))
        _, _, choice = get(("click", me(), "S.%d" % round),
                           ("click", me(), "C.%d" % round))
        choice = choice[0]
        put(("choice", (group, role), choice))
        if choice == "S":
          add("<p>You chose square.")
        elif choice == "C":
          add("<p>You chose circle.")
        _, _, other  = get(("choice", (group, 1-role), None))
        if   choice == "S" and other == "S": now = 25
        elif choice == "S" and other == "C": now = 150
        elif choice == "C" and other == "S": now = 0
        elif choice == "C" and other == "C": now = 100
        cash2 += now
        add(("""<p>In this round, you earned $%.2f. <p>So far you have
        earned $%.2f in task 2.""" % (now/100., cash2/100.)))
        log("CHOICE2", subject, group, role, round, choice, other)
        log("CASH2", subject, cash2)
        button("2.%d" % round, "Click to proceed")
        get(("click", me(), "2.%d"%round))
        set("Wait...")
        put(("ping", ))
        get(("pong", ))
      put(("ping", ))
      set(("Task 2 is over. You earned a total of $%.2f in task 1 "
           "and $%.2f in task 2." %
           (cash1/100.0, cash2/100.0)))


    #
    # Compile pay table
    #

    if me() == 0:
      payoffs = ('<table border="1"><tr>'
                 '<td>Subject</td><td>Task 1</td>'
                 '<td>Task 2</td></tr>')
      for subject in range(1, subjects + 1):
        _, _, cash1, cash2 = get(("cash",subject, None, None))
        payoffs += ("<tr><td>%d</td><td>%d</td><td>%d</td></tr>" %
                    (subject, cash1, cash2))
      payoffs += "</table>"
      add(payoffs)
    else:
      put(("cash", subject, cash1, cash2))

  
  # 
  # Task 3 (the survey)
  #

  # This part is done by a generic table-driven routine, which could
  # be re-used later.

  def validate(lb,ub):
    def validator(n):
      try:
        n = float(n)
      except ValueError:
        return True
      return n >= lb and n <= ub
    return validator

  LIKERT = ["1. Very inaccurate",
            "2. Moderately inaccurate",
            "3. Neither inaccurate nor accurate",
            "4. Moderately accurate",
            "5. Very accurate"]

  SURVEY = [
    ("""Describe yourself as you generally are now, not as you wish to be in
        the future. Describe yourself as you honestly see yourself, in
        relation to other people you know of the same sex as you are,
        and roughly your same age. So that you can describe yourself
        in an honest manner, your responses will be kept in absolute
        confidence.<p>Indicate for each statement whether it is
        1. Very Inaccurate, 2. Moderately Inaccurate, 3. Neither
        Accurate Nor Inaccurate, 4. Moderately Accurate, or 5. Very
        Accurate as a description of you.""", ["Proceed"], None), # 0
    ("I am the life of the party.", LIKERT, None), # 1
    ("I feel little concern for others.", LIKERT, None), # 2
    ("I am always prepared.", LIKERT, None), # 3
    ("I get stressed out easily.", LIKERT, None), # 4
    ("I have a rich vocabulary.", LIKERT, None), # 5
    ("I don't talk a lot.", LIKERT, None), # 6
    ("I am interested in people.", LIKERT, None), # 7
    ("I leave my belongings around.", LIKERT, None), # 8
    ("I am relaxed most of the time.", LIKERT, None), # 9
    ("I have difficulty understanding abstract ideas.", LIKERT, None), # 10
    ("I feel comfortable around people.", LIKERT, None), # 11
    ("I insult people.", LIKERT, None), # 12
    ("I pay attention to details.", LIKERT, None), # 13
    ("I worry about things.", LIKERT, None), # 14
    ("I have a vivid imagination.", LIKERT, None), # 15
    ("I keep in the background.", LIKERT, None), # 16
    ("I sympathize with others' feelings.", LIKERT, None), # 17
    ("I make a mess of things.", LIKERT, None), # 18
    ("I seldom feel blue.", LIKERT, None), # 19
    ("I am not interested in abstract ideas.", LIKERT, None), # 20
    ("I start conversations.", LIKERT, None), # 21
    ("I am not interested in other people's problems.", LIKERT, None), # 22
    ("I get chores done right away.", LIKERT, None), # 23
    ("I am easily disturbed.", LIKERT, None), # 24
    ("I have excellent ideas.", LIKERT, None), # 25
    ("I have little to say.", LIKERT, None), # 26
    ("I have a soft heart.", LIKERT, None), # 27
    ("I often forget to put things back in their proper place.", LIKERT, None), # 28
    ("I get upset easily.", LIKERT, None), # 29
    ("I do not have a good imagination.", LIKERT, None), # 30
    ("I talk to a lot of different people at parties.", LIKERT, None), # 31
    ("I am not really interested in others.", LIKERT, None), # 32
    ("I like order.", LIKERT, None), # 33
    ("I change my mood a lot.", LIKERT, None), # 34
    ("I am quick to understand things.", LIKERT, None), # 35
    ("I don't like to draw attention to myself.", LIKERT, None), # 36
    ("I take time out for others.", LIKERT, None), # 37
    ("I shirk my duties.", LIKERT, None), # 38
    ("I have frequent mood swings.", LIKERT, None), # 39
    ("I use difficult words.", LIKERT, None), # 40
    ("I don't mind being the center of attention.", LIKERT, None), # 41
    ("I feel others' emotions.", LIKERT, None), # 42
    ("I follow a schedule.", LIKERT, None), # 43
    ("I get irritated easily.", LIKERT, None), # 44
    ("I spend time reflecting on things.", LIKERT, None), # 45
    ("I am quiet around strangers.", LIKERT, None), # 46
    ("I make people feel at ease.", LIKERT, None), # 47
    ("I am exacting in my work.", LIKERT, None), # 48
    ("I often feel blue.", LIKERT, None), # 49
    ("I am full of ideas.", LIKERT, None), # 50
    ("Now proceed to the next section of the questionnaire.", ["Proceed"], None), # 51
    ("What is your age in years?",None, None),
    ("What is your gender?", ["Male", "Female"], None),
    ("""What is the highest level of education that you have completed or
     are currently enrolled in? For example, if you are currently in
     college, then choose Bachelor's degree.""",
     ["Less than high school", "High school diploma or GED",
      "Bachelor degree", "Master degree", "Doctoral degree"], None),
    ("What class are you in?",
     ["Freshman", "Sophomore", "Junior", "Senior", "MA student",
      "Pre-dissertation PhD student", "Dissertation PhD student"], None),
    ("""In what range is your college GPA? If you are not currently in
    college (e.g., if you are a graduate student, None), then please put
    down your GPA from when you were in college.""",   
     ["0 to 2.0", "2.1 to 2.5", "2.6 to 3.0", "3.1 to 3.5", "3.6 to 4.0"], None),
    ("If you took it, what was your SAT verbal score?"+
     " If you can't remember exactly, try to remember approximately."+
     " (Leave blank if you did not take it.)",None, validate(200,800)),
    ("If you took it, what was your SAT quantitative score?"+
     " If you can't remember exactly, try to remember approximately."+   
     " (Leave blank if you did not take it.)",None, validate(200,800)),
    ("If you took it, what was your GRE verbal score?"+
     " If you can't remember exactly, try to remember approximately."+   
     " (Leave blank if you did not take it.)",None, validate(200,800)),
    ("If you took it, what was your GRE quantitative score?"+
     " If you can't remember exactly, try to remember approximately."+   
     " (Leave blank if you did not take it.)",None, validate(200,800)),
    ("If you took it, what was your GRE analytical score?"+
     " If you can't remember exactly, try to remember approximately."+   
     " (Leave blank if you did not take it.)",None, validate(0,6))
  ]

  if T3:
    if me() == 0:
      button("third","Start task 3")
      get(("click",me(),"third"))
      for subject in range(1, subjects+1):
        put(("third", subject, None))
      for subject in range(1, subjects+1):
        get(("done", subject, "third"))
    else:
      get(("third", subject, None))
      for question in range(1, len(SURVEY) + 1):
        add("<li>Subject %d answering question %d" %
            (subject, question), number=0)
        text, options, validation = SURVEY[question-1]
        valid = False
        retrying = False
        while not valid:
          set("<p>%s<p>" % text)
          if options:
            clicks = []
            for option in options:
              option_id = "%s*%d" % (option, question)
              add(("<input type='submit' id='%s' value='%s' class='wide'><br>" % 
                   (option_id,option)))
              clicks += [("click", me(), option_id)]
            _,_,answer = get(*clicks)
            valid = True
          else:
            add(("<input type='text' id='answer-%d' style='wide'>"
                 "<input type='submit' id='submit-%d' value='OK'>"%
                 (question,question)))
            if retrying: push("red","input")
            get(("click",me(),"submit-%d" % question))
            peek("#answer-%d" % question)
            _,_,answer = get(("poke",me(),None))
            if validation:
              valid = validation(answer)
            else:
              valid = True
            if not valid: 
              retrying = True
        log("SURVEY", subject, question, answer)
      set("Task 3 is over.")
      put(("done", subject, "third"))

  #
  # Task 4 (Hey-Orme pie charts task)
  #

  # The pie charts are generated by cc.do, a stata program, from
  # cc.csv. The file cc.csv contains the same data as is contained in
  # the following constants, and hence the numbers match the pie
  # charts... But this is not automated!

  LEFT = [(0, 0, 360, 0),
          (315, 0, 0, 45),
          (0, 90, 180, 90),
          (135, 135, 90, 0),
          (0, 360, 0, 0),
          (225, 0, 0, 135),
          (45, 225, 90, 0),
          (90, 0, 45, 225),
          (135, 180, 0, 45),
          (180, 90, 90, 0),
          (45, 315, 0, 0),
          (45, 270, 45, 0),
          (0, 0, 315, 45),
          (0, 360, 0, 0),
          (45, 225, 0, 90),
          (0, 135, 90, 135),
          (45, 0, 90, 225),
          (180, 180, 0, 0),
          (45, 0, 315, 0),
          (180, 0, 45, 135)]

  RIGHT = [(45 , 0 , 90 , 225 ),
           (270 , 90 , 0 , 0 ),
           (0 , 45 , 315 , 0 ),
           (180 , 45 , 135 , 0 ),
           (180 , 45 , 0 , 135 ),
           (180 , 0 , 180 , 0 ),
           (90 , 90 , 180 , 0 ),
           (45 , 0 , 315 , 0 ),
           (45 , 315 , 0 , 0 ),
           (135 , 225 , 0 , 0 ),
           (135 , 180 , 0 , 45 ),
           (135 , 45 , 180 , 0 ),
           (0 , 45 , 225 , 90 ),
           (45 , 180 , 135 , 0 ),
           (135 , 0 , 0 , 225 ),
           (0 , 90 , 225 , 45 ),
           (0 , 0 , 270 , 90 ),
           (315 , 0 , 0 , 45 ),
           (90 , 0 , 135 , 135 ),
           (135 , 0 , 225 , 0 )]

  if me() == 0:
    button("fourth","Start task 4")
    get(("click",me(),"fourth"))
    for subject in range(1, subjects+1):
      put(("fourth", subject, None))
    summaries = ""
    for subject in range(1, subjects+1):
      _, _, sum = get(("summary", subject, None))
      summaries += sum
    add(summaries)
  else:
    add(open("cc.html"),"head")
    get(("fourth", subject, None))
    n_pies = len(LEFT)
    choices = dict()
    for pie in range(1, n_pies+1):
      left = LEFT[pie-1]
      right = RIGHT[pie-1]

      def maybe_certain(p):
          if p == 360:
              return "(certain)"
          else:
              return ""

      msg = "<table class='big'><tr><td>"

      msg += ("<h2>Left</h2>If this lottery were played 1000 times, "
               "on average the payoff would be $%.2f.<br>"
               "<img src='cc%02dl.png'><br>" %
               (left[1]*10.0/360.0+left[2]*20.0/360.0+left[3]*30.0/360.0,pie))
      if left[0] > 0: 
        msg += ("<span class='p1'>Chance of winning $0: %d out of 8 %s</span><br>"%
                 (left[0]/45,maybe_certain(left[0])))
      if left[1] > 0: 
        msg += ("<span class='p2'>Chance of winning $10: %d out of 8 %s</span><br>"%
                 (left[1]/45,maybe_certain(left[1])))
      if left[2] > 0: 
        msg += ("<span class='p3'>Chance of winning $20: %d out of 8 %s</span><br>"%
                 (left[2]/45,maybe_certain(left[2])))
      if left[3] > 0: 
        msg += ("<span class='p4'>Chance of winning $30: %d out of 8 %s</span><br>"%
                 (left[3]/45,maybe_certain(left[3])))

      msg += "</td><td>"

      msg += ("<h2>Right</h2>If this lottery were played 1000 times, "
               "on average the payoff would be $%.2f.<br>"
               "<img src='cc%02dr.png'><br>" %
               (right[1]*10.0/360.0+right[2]*20.0/360.0+right[3]*30.0/360.0,pie))
      if right[0] > 0: 
        msg += ("<span class='p1'>Chance of winning $0: %d out of 8 %s</span><br>"%
                 (right[0]/45,maybe_certain(right[0])))
      if right[1] > 0: 
        msg += ("<span class='p2'>Chance of winning $10: %d out of 8 %s</span><br>"%
                 (right[1]/45,maybe_certain(right[1])))
      if right[2] > 0: 
        msg += ("<span class='p3'>Chance of winning $20: %d out of 8 %s</span><br>"%
                 (right[2]/45,maybe_certain(right[2])))
      if right[3] > 0: 
        msg += ("<span class='p4'>Chance of winning $30: %d out of 8 %s</span><br>"%
                 (right[3]/45,maybe_certain(right[3])))

      msg += """</td></tr></table>
                 <center>
                  Which do you prefer?<br>
                  <input type='submit' id='L.%d' value='Left'>
                  <input type='submit' id='N.%d' value=\"Don't care\">
                  <input type='submit' id='R.%d' value='Right'>
                 </center>""" % (pie,pie,pie)

      set(msg)

      _, _, decision = get(("click",me(),"L.%d" % pie),
                           ("click",me(),"N.%d" % pie),
                           ("click",me(),"R.%d" % pie))

      choices[pie] = decision[0]
      log("PIE", subject, pie, decision[0])        

    summary = ("""
    <h2>Summary for participant %d</h2>
    <table class='small'>
    <tr>
     <td>&nbsp;</td><td colspan='4'>Left lottery</td>
     <td>&nbsp;</td><td colspan='4'>Right lottery</td>
     <td colspan='2'>Your choice</td>
    </tr>
    <tr>
     <td>Pair</td><td>$0</td><td>$10</td><td>$20</td><td>$3</td>
     <td>Pair</td><td>$0</td><td>$10</td><td>$20</td><td>$3</td>
     <td>Pair</td><td>Your choice</td>
    </tr>
    """ % subject)
    for pie in range(1, n_pies+1):
      left = LEFT[pie-1]
      right = RIGHT[pie-1]
      if choices[pie] == 'L':
        choice = "Left"
      elif choices[pie] == 'N':
        choice = "Don't care"
      elif choices[pie] == 'R':
        choice = "Right"
      summary += ("""<tr> <td>%d</td><td class="p1">%d/8</td><td
      class="p2">%d/8</td><td class="p3">%d/8</td><td
      class="p4">%d/8</td> <td>%d </td><td class="p1">%d/8</td><td
      class="p2">%d/8</td><td class="p3">%d/8</td><td
      class="p4">%d/8</td> <td>%d</td><td>%s</td></tr>
      """ % (pie,
             left[0]/45,
             left[1]/45,
             left[2]/45,
             left[3]/45,
             pie,
             right[0]/45,
             right[1]/45,
             right[2]/45,
             right[3]/45,
             pie,
             choice))
    summary += "</table>"
    set(summary)
    add('<li>Subject %d done' % subject, number=0)
    put(('summary',subject,summary))

run(session)
