from willow.willow import *
from willow.twig import *
import random,datetime

ROUNDS = 0                # How many rounds of CG and PD
PIES = 1                  # How many pies of RP
T3 = True                 # Survey on/off
T4 = True                 # Pie charts on/off

def session():
  number, numbers = assemble()
  if number == None: return

  # Assignment ###############################################################
  if number == 0:
    set("<h2>"+datetime.datetime.now().ctime())
    add("<h2>Assignment")
    subjects = numbers[1:]
    n_subjects = len(subjects)
    permutation = random.sample(subjects, n_subjects)
    assignments = [["Subject","Role","Group 1","Group 2"]]
    for i, subject in enumerate(permutation):
      role = i % 2
      group_1 = i/2
      group_2 = (group_1 + role) % (n_subjects / 2)
      put(("assign", subject, role, group_1, group_2))
      log("assign", subject, role, group_1, group_2)
      assignments += [[subject, role, group_1, group_2]]
    table(assignments)
  else:
    add(open("cc.html"),"head")
    _, _, role, group_1, group_2 = get(("assign", number, None, None, None))
    cash1 = 0
    cash2 = 0
  
  # CG ######################################################################
  if number == 0:
    add("<h2>CG game")
    button('CG','CG', pre="<br>")
    get(("click",0,'CG'))
    for round in range(1,ROUNDS+1):
      add("<br>Round %d: " % round)
      for _ in subjects: put(("ping",))
      for _ in subjects: get(("pong",))
  else:
    for round in range(1,ROUNDS+1):
      get(("ping",))
      set("""<h2>Task 1 round %d of %d.</h2><li>If you choose <b>blue</b> and
      the other person chooses <b>blue</b> you earn <b>$0.50</b>.<li>If you
      choose <b>blue</b> and the other person chooses <b>green</b> you earn
      <b>$0.50</b>.<li>If you choose <b>green</b> and the other person
      chooses <b>blue</b> you earn <b>$0.00</b>.  <li>If you choose <b>green</b> and
      the other person chooses <b>green</b> you earn <b>$0.75</b>.<p>Choose
      <input type='submit' id='G' value='green'> or <input
      type='submit' id='B' value='blue'>...""" % (round,ROUNDS))
      clack()
      _, _, choice = get(("click", me(), None))
      put(("choice", group_1, role, choice))
      if choice == "G":
        add("<p>You chose <b>green</b>.")
      elif choice == "B":
        add("<p>You chose <b>blue</b>.")
      _, _, _, other  = get(("choice", group_1, 1-role, None))
      if   choice == "B" and other == "B": now = 50
      elif choice == "B" and other == "G": now = 50
      elif choice == "G" and other == "B": now = 0
      elif choice == "G" and other == "G": now = 75
      cash1 += now
      add(("<p>In this round, you earned <b>$%.2f</b>."
           "<p>So far you have earned <b>$%.2f</b> in task 1." %
           (now/100., cash1/100.)))
      log("CG", number, round, choice, other)
      button("P", "Click to proceed",pre="<br>")
      clack()
      get(("click", me(), "P"))
      add(" %d " % number, number=0); set("Wait...")
      put(("pong", ))
    set(("Task 1 is over. You earned a total of <b>$%.2f</b> in task 1." %
         (cash1/100.0)))

  # PD ######################################################################
  if number == 0:
    add("<h2>PD game")
    button('PD','PD', pre="<br>")
    get(("click",0,'PD'))
    for round in range(1,ROUNDS+1):
      add("<br>Round %d: " % round)
      for _ in subjects: put(("ping",))
      for _ in subjects: get(("pong",))
  else:
    for round in range(1,ROUNDS+1):
      get(("ping",))
      set("""<h2>Task 2 round %d of %d.</h2><li>If you choose <b>square</b>
      and the other person chooses <b>square</b> you earn <b>$0.25</b>.<li>If you
      choose <b>square</b> and the other person chooses <b>circle</b> you earn
      <b>$1.50</b>.  <li>If you choose <b>circle</b> and the other person chooses
      <b>square</b> you earn <b>$0.00</b>.  <li>If you choose <b>circle</b> and the other
      person chooses <b>circle</b> you earn <b>$1.00</b>.<p>Choose <input
      type='submit' id='S' value='square'> or <input type='submit'
      id='C' value='circle'>...""" % (round, ROUNDS))
      clack()
      _, _, choice = get(("click", me(), None))
      put(("choice", group_2, role, choice))
      if choice == "S":
        add("<p>You chose <b>square</b>.")
      elif choice == "C":
        add("<p>You chose <b>circle</b>.")
      _, _, _, other  = get(("choice", group_2, 1-role, None))
      if   choice == "S" and other == "S": now = 25
      elif choice == "S" and other == "C": now = 150
      elif choice == "C" and other == "S": now = 0
      elif choice == "C" and other == "C": now = 100
      cash2 += now
      add(("<p>In this round, you earned <b>$%.2f</b>."
           "<p>So far you have earned <b>$%.2f</b> in task 2.""" %
           (now/100., cash2/100.)))
      log("PD", number, round, choice, other)
      button("P", "Click to proceed", pre="<br>")
      clack()
      get(("click", me(), "P"))
      add(" %d " % number, number=0); set("Wait...")
      put(("pong", ))
    set(("Task 2 is over. You earned a total of <b>$%.2f</b> in task 1 "
         "and <b>$%.2f</b> in task 2." %
         (cash1/100.0, cash2/100.0)))

  # Payoffs table ############################################################
  if number == 0:
    add("<h2>Payoffs table for CG and PD")
    payoffs = [["Subject","CG","PD"]]
    for subject in subjects:
      _, _, cash1, cash2 = get(("cash",subject, None, None))
      payoffs += [[subject, "$%.02f" % (cash1/100.), "$%.02f" % (cash2/100.)]]
    table(payoffs)
  else:
    put(("cash", number, cash1, cash2))

  # Survey ###################################################################
  LIKERT = ["1. Very inaccurate",
            "2. Moderately inaccurate",
            "3. Neither inaccurate nor accurate",
            "4. Moderately accurate",
            "5. Very accurate"]

  def validate(lb,ub):
    def validator(n):
      try:
        n = float(n)
      except ValueError:
        return True
      return n >= lb and n <= ub
    return validator

  SURVEY = [
    ("""<h2>Survey</h2>
        Describe yourself as you generally are now, not as you wish to be in
        the future. Describe yourself as you honestly see yourself, in
        relation to other people you know of the same sex as you are,
        and roughly your same age. So that you can describe yourself
        in an honest manner, your responses will be kept in absolute
        confidence.<p>Indicate for each statement whether it is
        1. Very Inaccurate, 2. Moderately Inaccurate, 3. Neither
        Accurate Nor Inaccurate, 4. Moderately Accurate, or 5. Very
        Accurate as a description of you.""", ["Proceed"]),
     ("I am the life of the party.", LIKERT),                             # 1
     ("I feel little concern for others.", LIKERT),                       # 2
     ("I am always prepared.", LIKERT),                                   # 3
     ("I get stressed out easily.", LIKERT),                              # 4
     ("I have a rich vocabulary.", LIKERT),                               # 5
     ("I don't talk a lot.", LIKERT),                                     # 6
     ("I am interested in people.", LIKERT),                              # 7
     ("I leave my belongings around.", LIKERT),                           # 8
     ("I am relaxed most of the time.", LIKERT),                          # 9
     ("I have difficulty understanding abstract ideas.", LIKERT),         # 10
     ("I feel comfortable around people.", LIKERT),                       # 11
     ("I insult people.", LIKERT),                                        # 12
     ("I pay attention to details.", LIKERT),                             # 13
     ("I worry about things.", LIKERT),                                   # 14
     ("I have a vivid imagination.", LIKERT),                             # 15
     ("I keep in the background.", LIKERT),                               # 16
     ("I sympathize with others' feelings.", LIKERT),                     # 17
     ("I make a mess of things.", LIKERT),                                # 18
     ("I seldom feel blue.", LIKERT),                                     # 19
     ("I am not interested in abstract ideas.", LIKERT),                  # 20
     ("I start conversations.", LIKERT),                                  # 21
     ("I am not interested in other people's problems.", LIKERT),         # 22
     ("I get chores done right away.", LIKERT),                           # 23
     ("I am easily disturbed.", LIKERT),                                  # 24
     ("I have excellent ideas.", LIKERT),                                 # 25
     ("I have little to say.", LIKERT),                                   # 26
     ("I have a soft heart.", LIKERT),                                    # 27
     ("I often forget to put things back in their proper place.", LIKERT),# 28
     ("I get upset easily.", LIKERT),                                     # 29
     ("I do not have a good imagination.", LIKERT),                       # 30
     ("I talk to a lot of different people at parties.", LIKERT),         # 31
     ("I am not really interested in others.", LIKERT),                   # 32
     ("I like order.", LIKERT),                                           # 33
     ("I change my mood a lot.", LIKERT),                                 # 34
     ("I am quick to understand things.", LIKERT),                        # 35
     ("I don't like to draw attention to myself.", LIKERT),               # 36
     ("I take time out for others.", LIKERT),                             # 37
     ("I shirk my duties.", LIKERT),                                      # 38
     ("I have frequent mood swings.", LIKERT),                            # 39
     ("I use difficult words.", LIKERT),                                  # 40
     ("I don't mind being the center of attention.", LIKERT),             # 41
     ("I feel others' emotions.", LIKERT),                                # 42
     ("I follow a schedule.", LIKERT),                                    # 43
     ("I get irritated easily.", LIKERT),                                 # 44
     ("I spend time reflecting on things.", LIKERT),                      # 45
     ("I am quiet around strangers.", LIKERT),                            # 46
     ("I make people feel at ease.", LIKERT),                             # 47
     ("I am exacting in my work.", LIKERT),                               # 48
     ("I often feel blue.", LIKERT),                                      # 49
     ("I am full of ideas.", LIKERT),                                     # 50
     ("Now proceed to the next section of the questionnaire.", ["Proceed"]),
     ("What is your age in years?",validate(18,120)),
     ("What is your gender?", ["Male", "Female"]),
     ("What is the highest level of education that you have completed or"
      "are currently enrolled in? For example, if you are currently in"
      "college, then choose Bachelor's degree.",
      ["Less than high school", "High school diploma or GED",
       "Bachelor degree", "Master degree", "Doctoral degree"]),
     ("What class are you in?",
      ["Freshman", "Sophomore", "Junior", "Senior", "MA student",
       "Pre-dissertation PhD student", "Dissertation PhD student"]),
     ("""In what range is your college GPA? If you are not currently in
     college (e.g., if you are a graduate student), then please put
     down your GPA from when you were in college.""",   
      ["0 to 2.0", "2.1 to 2.5", "2.6 to 3.0", "3.1 to 3.5", "3.6 to 4.0"]),
    ("The <b>SAT</b> has at least 2 sections:"
     "<br><b>verbal</b> (critical reading) and <b>quantitative</b> (math)."
     "<br>If you took it, what was your SAT <b>verbal</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."
     "<br>(Leave blank if you did not take it.)",validate(200,800)),
    ("The <b>SAT</b> has at least 2 sections:"
     "<br><b>verbal</b> (critical reading) and <b>quantitative</b> (math)."
     "<br>If you took it, what was your SAT <b>quantitative</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."   
     "<br>(Leave blank if you did not take it.)",validate(200,800)),
    ("The <b>ACT</b> has 4 sections:"
     "<br><b>English</b>, <b>math</b>, <b>reading</b>, and <b>science</b>."
     "<br>If you took it, what was your ACT <b>English</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."   
     "<br>(Leave blank if you did not take it.)",validate(1,36)),
    ("The <b>ACT</b> has 4 sections:"
     "<br><b>English</b>, <b>math</b>, <b>reading</b>, and <b>science</b>."
     "<br>If you took it, what was your ACT <b>math</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."   
     "<br>(Leave blank if you did not take it.)",validate(1,36)),
    ("The <b>ACT</b> has 4 sections:"
     "<br><b>English</b>, <b>math</b>, <b>reading</b>, and <b>science</b>."
     "<br>If you took it, what was your ACT <b>reading</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."   
     "<br>(Leave blank if you did not take it.)",validate(1,36)),
    ("The <b>ACT</b> has 4 sections:"
     "<br><b>English</b>, <b>math</b>, <b>reading</b>, and <b>science</b>."
     "<br>If you took it, what was your ACT <b>science</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."   
     "<br>(Leave blank if you did not take it.)",validate(1,36)),
    ("The <b>GRE</b> has at least 2 sections:"
     "<br><b>verbal</b> and <b>quantitative</b>."
     "<br>If you took it, what was your GRE <b>verbal</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."   
     "<br>(Leave blank if you did not take it.)",validate(200,800)),
    ("The <b>GRE</b> has at least 2 sections:"
     "<br><b>verbal</b> and <b>quantitative</b>."
     "<br>If you took it, what was your GRE <b>quantitative</b> score?"
     "<br>If you can't remember exactly, try to remember approximately."   
     "<br>(Leave blank if you did not take it.)",validate(200,800))
  ]

  if T3:
    if number == 0:
      add("<h2>Survey")
      button('S','S', pre="<br>")
      get(("click",0,'S'))
      add("<div class='survey'></div>")
      for _ in subjects: put(("ping",))
      for _ in subjects: get(("pong",))
    else:
      get(("ping",))
      set("<div class='survey'></div>")
      survey("SURVEY", number, SURVEY, ".survey")
      set("Wait...")
      put(("pong",))

  # Pie charts ###############################################################
  # The pie charts are generated by cc.do, a stata program, from
  # cc.csv. The file cc.csv contains the same data as is contained in
  # the following constants, and hence the numbers match the pie
  # charts... But this is not automated!

  LEFT = [(0, 0, 360, 0), (315, 0, 0, 45), (0, 90, 180, 90), (135,
          135, 90, 0), (0, 360, 0, 0), (225, 0, 0, 135), (45, 225, 90,
          0), (90, 0, 45, 225), (135, 180, 0, 45), (180, 90, 90, 0),
          (45, 315, 0, 0), (45, 270, 45, 0), (0, 0, 315, 45), (0, 360,
          0, 0), (45, 225, 0, 90), (0, 135, 90, 135), (45, 0, 90,
          225), (180, 180, 0, 0), (45, 0, 315, 0), (180, 0, 45, 135)]

  RIGHT = [(45, 0, 90, 225), (270, 90, 0, 0), (0, 45, 315, 0),
           (180, 45, 135, 0), (180, 45, 0, 135), (180, 0, 180, 0),
           (90, 90, 180, 0), (45, 0, 315, 0), (45, 315, 0, 0),
           (135, 225, 0, 0), (135, 180, 0, 45), (135, 45, 180, 0),
           (0, 45, 225, 90), (45, 180, 135, 0), (135, 0, 0, 225),
           (0, 90, 225, 45), (0, 0, 270, 90), (315, 0, 0, 45), (90,
           0, 135, 135), (135, 0, 225, 0)]


  if T4:
    if number == 0:
      add("<h2>RP task")
      button("RP", "RP", pre="<br>")
      get(("click",0,"RP"))
      for pie in range(1, PIES+1):
        add("<br>Pie %d: " % pie)
        for _ in subjects: put(("ping",))
        for _ in subjects: get(("pong",))
    else:
      choices = dict()
      for pie in range(1, PIES+1):
        get(("ping",))
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
                    <input type='submit' id='L' value='Left'>
                    <input type='submit' id='N' value=\"Don't care\">
                    <input type='submit' id='R' value='Right'>
                   </center>"""

        set(msg)

        clack()
        _, _, decision = get(("click",me(),None))
        choices[pie] = decision
        log("PIE", number, pie, decision)
        add(" %d " % number, number=0); set("Wait...")
        put(("pong",))

  # Pie chart summaries ######################################################
  if T4:
    if number == 0:
      summaries = ""
      for subject in subjects:
        _, _, summary = get(("summary", subject, None))
        summaries += summary
      add(summaries)
    else:      
      summary = ("""
      <h2>Summary for participant %d</h2>
      <table border=1>
      <tr>
       <td>&nbsp;</td><td colspan='4'>Left lottery</td>
       <td>&nbsp;</td><td colspan='4'>Right lottery</td>
       <td>&nbsp;</td><td>Your choice</td>
      </tr>
      <tr>
       <td>Pair</td><td>$0</td><td>$10</td><td>$20</td><td>$3</td>
       <td>Pair</td><td>$0</td><td>$10</td><td>$20</td><td>$3</td>
       <td>Pair</td><td>Your choice</td>
      </tr>
      """ % number)
      for pie in range(1, PIES+1):
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
      put(('summary',number,summary))
      

   

run(session)
