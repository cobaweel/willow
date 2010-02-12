# This is the code for a real experiment conducted at George Mason
# University. The computerized part of the experiment consists of an
# several iterated trust games, and a very long survey. This is an
# example of how to do some rather complex subject matching
# algorithms.


from willow.willow import *
from willow.twig import *
import random,datetime

#DO_TRUST_GAMES = True
DO_TRUST_GAMES = False
#DO_LOTTERIES = True
DO_LOTTERIES = False
DO_SURVEY = True
#DO_SURVEY = False

SCALE1 = ["Never", "Once", "More than once", "Often", "Very often"]
SCALE2 = [ "Strongly disagree", "Somewhat disagree", 
           "Slightly disagree", "No opinion", "Slightly agree",
           "Somewhat agree", "Strongly agree"]
SCALE3 = [ "Strongly disagree", "Somewhat disagree", "No opinion", 
           "Somewhat agree", "Strongly agree"]
SCALE4 = [ "Very strongly disagree", "Strongly disagree", "Somewhat disagree", 
           "Slightly disagree", "No opinion", "Slightly agree",
           "Somewhat agree", "Strongly agree", "Very strongly agree"]
SCALE5 = ["1. Very inaccurate", "2. Moderately inaccurate",
          "3. Neither inaccurate nor accurate", "4. Moderately accurate",
          "5. Very accurate"]

SURVEY = [
 ("The next part of the experiment is a set of 5 surveys. Try to answer each item as best you can.", ["Proceed"]),
 # 1. Altruism 
 ("We will now start the 1st of 5 surveys.", ["Proceed"]),  
 ("I have helped a stranger with car troubles (i.e. pushed out of the snow)", SCALE1),                                                                            # 1
 ("I have given directions to a stranger.", SCALE1),                                                                                                              # 2
 ("I have made change for a stranger.", SCALE1),                                                                                                                  # 3
 ("I have given money to a charity.", SCALE1),                                                                                                                    # 4
 ("I have given money to a stranger who needed it (or asked me for it).", SCALE1),                                                                                # 5
 ("I have donated goods or clothes to a charity.", SCALE1),                                                                                                       # 6
 ("I have done volunteer work for a charity.", SCALE1),                                                                                                           # 7
 ("I have donated blood.", SCALE1),                                                                                                                               # 8
 ("I have helped carry a stranger's belongings (books, packages, etc.)", SCALE1),                                                                                 # 9
 ("I have delayed an elevator and held the door open for a stranger.", SCALE1),                                                                                   # 10
 ("I have allowed someone to go ahead of me in a line (at Xerox machine, in the supermarket).", SCALE1),                                                          # 11
 ("I have given a stranger a ride in my car.", SCALE1),                                                                                                           # 12
 ("I have pointed out a clerk's error (in a bank, at the supermarket) in undercharging mefor an item.", SCALE1),                                                  # 13
 ("I have let a neighbor whom I didn't know too well borrow an item of some value to me (e.g. a dish, tools, etc.).", SCALE1),                                    # 14
 ("I have bought 'charity' holidy cards deliberately because I knew it was a good cause.", SCALE1),                                                               # 15
 ("I have helped a classmate who I did not know that well with a homework assignment when my knowledge was greater than his or hers.", SCALE1),                   # 16
 ("I have before benig asked, voluntarily looked after a neighbor's pet or children without being paid for it.", SCALE1),                                         # 17
 ("I have offered to help a disabled or elderly stranger across a street.", SCALE1),                                                                              # 18
 ("I have offered my seat on a bus or train to a stranger who was standing.", SCALE1),                                                                            # 19
 ("I have helped an acquaintance to move households.", SCALE1),                                                                                                   # 20
 # 2. Machiavellianism
 ("We will now start the 2nd of 5 surveys.", ["Proceed"]),    
 ("Never tell anyone the real reason you did something unless it is useful to do so.", SCALE2),                                                                   # 1
 ("The best way to handle people is to tell them what they want to hear.", SCALE2),                                                                               # 2
 ("One should take action only when sure it is morally right.", SCALE2),                                                                                          # 3
 ("Most people are basically good and kind.", SCALE2),                                                                                                            # 4
 ("It is safest to assume that all people have a vicious streak and it will come out when they are given a chance.", SCALE2),                                     # 5
 ("Honesty is the best policy in all cases.", SCALE2),                                                                                                            # 6
 ("There is no excuse for lying to someone.", SCALE2),                                                                                                            # 7
 ("It is hard to get ahead without cutting corners here and there.", SCALE2),                                                                                     # 8
 ("All in all, it is better to be humble and honest than important and dishonest.", SCALE2),                                                                      # 9
 ("When you ask someone to do something for you, it is best to give the real reasons for wanting it rather than giving reasons that carry more weight.", SCALE2), # 10
 ("Most people whoget ahead int he world lead clean, moral lives.", SCALE2),                                                                                      # 11
 ("Anyone who completely trusts anyone else is asking for trouble.", SCALE2),                                                                                     # 12
 ("The biggest differences between most criminals and other people is that criminals are stupid enough to get caught.", SCALE2),                                  # 13
 ("Most men are brave.", SCALE2),                                                                                                                                 # 14
 ("It is wise to flatter important people.", SCALE2),                                                                                                             # 15
 # 3.
 ("We will now start the 3rd of 5 surveys.", ["Proceed"]),    
 ("I daydream and fantasize, with some regularity, about things that might happen to me.", SCALE3),                                                               # 1
 ("I often have tender, concerned feelings for other people less fortunate than me.", SCALE3),                                                                    # 2
 ("I sometimes find it difficult to see things from the \"other guy's\" point of view.", SCALE3),                                                                 # 3
 ("Sometimes I don't feel very sorry for other people when they are having problems.", SCALE3),                                                                   # 4
 ("I really get involved with the feelings of the characters in a novel.", SCALE3),                                                                               # 5
 ("In emergency situations, I feel apprehensive and ill-at-ease.", SCALE3),                                                                                       # 6
 ("I am usually objective when I watch a movie or play, and I don't often get completely caught up in it.", SCALE3),                                              # 7
 ("I try to look at everybody's side of a disagreement before I make a decision.", SCALE3),                                                                       # 8
 ("When I see someone being taken advantage of, I  feel kind of protective towards them.", SCALE3),                                                               # 9
 ("I sometimes feel helpless when I am in the middle of a very emotional situation.", SCALE3),                                                                    # 10
 ("I sometimes try to understand my friends better by imagining how things look from their perspective.", SCALE3),                                                # 11
 ("Becoming extremely involved in a good book or movie is somewhat rare for me.", SCALE3),                                                                        # 12
 ("When I see someone get hurt, I tend to remain calm.", SCALE3),                                                                                                 # 13
 ("Other people's misfortunes do not usually disturb me a great deal.", SCALE3),                                                                                  # 14
 ("If I'm sure I'm right about something, I don't waste much time listening to other people's arguments.", SCALE3),                                               # 15
 ("After seeing a play or movie, I have felt as though I were one of the characters.", SCALE3),                                                                   # 16
 ("Being in a tense emotional situation scares me.", SCALE3),                                                                                                     # 17
 ("When I see someone being treated unfairly, I sometimes don't feel very much pity for them.", SCALE3),                                                          # 18
 ("I am usually pretty effective in dealing with emergencies.", SCALE3),                                                                                          # 19
 ("I am often quite touched by things that I see happen.", SCALE3),                                                                                               # 20
 ("I believe that there are two sides to every question and try to look at them both.", SCALE3),                                                                  # 21
 ("I would describe myself as a pretty soft-hearted person.", SCALE3),                                                                                            # 22
 ("When I watch a good movie, I can very easily put myself in the place of the leading character.", SCALE3),                                                      # 23
 ("I tend to lose control during emergencies.", SCALE3),                                                                                                          # 24
 ("When I'm upset at someone, I usually try to \"put myself in his shoes\" for awhile.", SCALE3),                                                                 # 25
 ("When I am reading an interesting story or novel, I imagine how <i>I</i> would feel if the events in the story were happening to me.", SCALE3),                 # 26
 ("When I see someone who badly needs help in an emergency, I go to pieces.", SCALE3),                                                                            # 27
 ("Before criticizing somebody, I try to imagine how I would feel if I were in their place.", SCALE3),                                                            # 28
 # 4.
 ("We will now start the 4th of 5 surveys.", ["Proceed"]),    
 ("I very much enjoy and feel uplifted by happy endings.", SCALE4),                                                                                               # 1
 ("I cannot feel much sorrow for those who are responsible for their own misery.", SCALE4),                                                                       # 2
 ("I am moved deeply when I observe strangers who are struggling to survive.", SCALE4),                                                                           # 3
 ("I hardly ever cry when watching a very sad movie.", SCALE4),                                                                                                   # 4
 ("I can almostfeel the pain of elderly people who are weak and must struggle to move about.", SCALE4),                                                           # 5
 ("I cannot relate to the crying and sniffling at weddings.", SCALE4),                                                                                            # 6
 ("It would be extremely painful for me to have to convey very bad news to another.", SCALE4),                                                                    # 7
 ("I cannot easily empathize with the hopes and aspirations of strangers.", SCALE4),                                                                              # 8
 ("I don't get caught up easily in the emotions generated by a crowd.", SCALE4),                                                                                  # 9
 ("Unhappy movie endings haunt me for hours afterward.", SCALE4),                                                                                                 # 10
 ("It pains me to see young people in wheelchairs.", SCALE4),                                                                                                     # 11
 ("It is very exciting for me to watch children open presents.", SCALE4),                                                                                         # 12
 ("Helpless old people don't have much of an emotional effect on me.", SCALE4),                                                                                   # 13
 (" the sadness of a close one easiliy rubs off onme.", SCALE4),                                                                                                  # 14
 (" I don't get overly involved with friends' problems.", SCALE4),                                                                                                # 15
 (" It is difficult for me to strongly experience the feelings of characters in a book or a movie.", SCALE4),                                                     # 16
 (" It upsets me to see someone being mistreated.", SCALE4),                                                                                                      # 17
 (" I easily get carried away by the lyrics of love songs.", SCALE4),                                                                                             # 18
 (" I am not affected easily by the strong emotions of peolpe around me.", SCALE4),                                                                               # 19
 (" I have difficulty knowing what babies and children feel.", SCALE4),                                                                                           # 20
 (" It really hurts me to watch someone who is suffering from a terminal illness.", SCALE4),                                                                      # 21
 (" A crying child does not necessarily get my attention.", SCALE4),                                                                                              # 22
 (" Another's happiness can be very uplifting for me.", SCALE4),                                                                                                  # 23
 (" I have difficulty feeling ad reacting to the emotional expressions of foreigners.", SCALE4),                                                                  # 24
 (" I get a strong urge to help when I see someone in distress.", SCALE4),                                                                                        # 25
 (" I am rarely moved to tears while reading a book or watching a mavie.", SCALE4),                                                                               # 26
 (" I have little sympathy for people who cause their own serious illnesses (e.g., heart disease, diabetes, lung cancer).", SCALE4),                              # 27
 (" I would not watch an execution.", SCALE4),                                                                                                                    # 28
 (" I easily get excited when those around me are lively and happy.", SCALE4),                                                                                    # 29
 (" The unhappiness or distress of a stranger are not especially moving for me.", SCALE4),                                                                        # 30
 # 5. Big 5 personality inventory
 ("We will now start the 5th of 5 surveys.", ["Proceed"]),    
 ("I am the life of the party.", SCALE5),                                                                                                                         # 1
 ("I feel little concern for others.", SCALE5),                                                                                                                   # 2
 ("I am always prepared.", SCALE5),                                                                                                                               # 3
 ("I get stressed out easily.", SCALE5),                                                                                                                          # 4
 ("I have a rich vocabulary.", SCALE5),                                                                                                                           # 5
 ("I don't talk a lot.", SCALE5),                                                                                                                                 # 6
 ("I am interested in people.", SCALE5),                                                                                                                          # 7
 ("I leave my belongings around.", SCALE5),                                                                                                                       # 8
 ("I am relaxed most of the time.", SCALE5),                                                                                                                      # 9
 ("I have difficulty understanding abstract ideas.", SCALE5),                                                                                                     # 10
 ("I feel comfortable around people.", SCALE5),                                                                                                                   # 11
 ("I insult people.", SCALE5),                                                                                                                                    # 12
 ("I pay attention to details.", SCALE5),                                                                                                                         # 13
 ("I worry about things.", SCALE5),                                                                                                                               # 14
 ("I have a vivid imagination.", SCALE5),                                                                                                                         # 15
 ("I keep in the background.", SCALE5),                                                                                                                           # 16
 ("I sympathize with others' feelings.", SCALE5),                                                                                                                 # 17
 ("I make a mess of things.", SCALE5),                                                                                                                            # 18
 ("I seldom feel blue.", SCALE5),                                                                                                                                 # 19
 ("I am not interested in abstract ideas.", SCALE5),                                                                                                              # 20
 ("I start conversations.", SCALE5),                                                                                                                              # 21
 ("I am not interested in other people's problems.", SCALE5),                                                                                                     # 22
 ("I get chores done right away.", SCALE5),                                                                                                                       # 23
 ("I am easily disturbed.", SCALE5),                                                                                                                              # 24
 ("I have excellent ideas.", SCALE5),                                                                                                                             # 25
 ("I have little to say.", SCALE5),                                                                                                                               # 26
 ("I have a soft heart.", SCALE5),                                                                                                                                # 27
 ("I often forget to put things back in their proper place.", SCALE5),                                                                                            # 28
 ("I get upset easily.", SCALE5),                                                                                                                                 # 29
 ("I do not have a good imagination.", SCALE5),                                                                                                                   # 30
 ("I talk to a lot of different people at parties.", SCALE5),                                                                                                     # 31
 ("I am not really interested in others.", SCALE5),                                                                                                               # 32
 ("I like order.", SCALE5),                                                                                                                                       # 33
 ("I change my mood a lot.", SCALE5),                                                                                                                             # 34
 ("I am quick to understand things.", SCALE5),                                                                                                                    # 35
 ("I don't like to draw attention to myself.", SCALE5),                                                                                                           # 36
 ("I take time out for others.", SCALE5),                                                                                                                         # 37
 ("I shirk my duties.", SCALE5),                                                                                                                                  # 38
 ("I have frequent mood swings.", SCALE5),                                                                                                                        # 39
 ("I use difficult words.", SCALE5),                                                                                                                              # 40
 ("I don't mind being the center of attention.", SCALE5),                                                                                                         # 41
 ("I feel others' emotions.", SCALE5),                                                                                                                            # 42
 ("I follow a schedule.", SCALE5),                                                                                                                                # 43
 ("I get irritated easily.", SCALE5),                                                                                                                             # 44
 ("I spend time reflecting on things.", SCALE5),                                                                                                                  # 45
 ("I am quiet around strangers.", SCALE5),                                                                                                                        # 46
 ("I make people feel at ease.", SCALE5),                                                                                                                         # 47
 ("I am exacting in my work.", SCALE5),                                                                                                                           # 48
 ("I often feel blue.", SCALE5),                                                                                                                                  # 49
 ("I am full of ideas.", SCALE5),                                                                                                                                 # 50
]

def msg(part, round):
  if part == 1:
    m = ("In this part of the experiment, "
         "you are partnered with a different random person in each round.")
  elif part == 3 and (round % 2) == 1:
    m = ("In this round you are partnered "
         "with the same person as in the <b>next</b> round.")
  elif part == 3 and (round % 2) == 0:
    m = ("In this round you are partnered "
         "with the same person as in the <b>previous</b> round.")
  return [
"""
<h1>Part %d Round %d of 10</h1><p>%s<p>You are <b>decision maker
1</b>. <p>You have <b>10</b> franks. How many franks do you want to send
to <b>decision maker 2</b>?
""" % (part, round, m),
"""
<p>You sent <b>%d</b> franks to <b>decision maker 2</b>. <b>Decision
maker 2</b> has received
3&nbsp;&times;&nbsp;<b>%d</b>&nbsp;=&nbsp;<b>%d</b> franks. You must
now wait for <b>decision maker 2</b> to make their decision....
""",
"""
<p><b>Decision maker 2</b> has sent you <b>%d</b> franks. You had
<b>%d</b> franks leftover that you did not send to <b>decision maker
2</b> in the first place. Therefore, you have earned a total of
<b>%d</b> franks in this round.
""",
"""
<h1>Part %d Round %d of 10</h1><p>%s<p>You are <b>decision maker
2</b>. <p>You must now wait for <b>decision maker 1</b> to make their
decision.
""" % (part, round,m),
"""
<p><b>Decision maker 1</b> has sent you <b>%d</b> franks. You have
received 3&nbsp;&times;&nbsp;%d&nbsp;=&nbsp;<b>%d</b> franks. How many
franks do you want to return to <b>decision maker 1</b>?
""",
"""
<p>You received <b>%d</b> franks, of which you have returned <b>%d</b>
franks to <b>decision maker 1</b>. Therefore, you have earned
<b>%d</b> franks in this round.
"""
]

def session():
  # Load the style sheet
  set(open("rts.html"), "head")

  # Log in terminals and give them numbers
  number, numbers = assemble(12)

  # Function to play one trust game
  def trust(msg, name, dm1, dm2):
    if name in dm1:
      partner = dm2[dm1.index(name)]
      set(msg[0])
      for ii in range(11):
        button(ii, ii)
      clack()
      _, _, ii = get(("click", me(), None))
      ii = int(ii)
      put(("ii", partner, ii))
      add(msg[1] % (ii, ii, 3*ii))
      _, _, rr = get(("rr", name, None))
      add(msg[2] % (rr, 10-ii, 10-ii+rr))
      score = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2][ii]
      log("dm1", number, ii, rr)
    elif name in dm2:
      partner = dm1[dm2.index(name)]
      set(msg[3])
      _, _, ii = get(("ii", name, None))
      add(msg[4] % (ii, ii, 3*ii))
      for rr in range(3*ii+1):
        button(rr, rr)
      clack()
      _, _, rr = get(("click", me(), None))
      rr=int(rr)
      add(msg[5] % (3*ii, rr, 3*ii-rr))
      if rr < ii:
        score = -2
      elif rr == ii:
        score = 0
      else:
        score = 2
      put(("rr", partner, rr))
      log("dm2", number, ii, rr)
    button("Proceed", "Proceed", wait=True)
    set("Wait...")
    sync(number, numbers[1:])
    return score

  # Function to play one lottery
  def lotteries():
    for n in [6, 7, 8, 9, 10, 11, 12]:
      sync(number, numbers)      
      if number > 0:
        set("<p>Set X. You will earn 1.5X with p=%d/12 and 0 otherwise." % n)
        for i in range(10):
          button(i,i)
        clack()
        _, _, x = get(("click", me(), None))
        x = int(x)
        die1, die2 = random.randint(1,6), random.randint(1,6)
        add("<p><img src='rt%d.png'><img src='rt%d.png'>" % (die1, die2))
        if die1+die2 >= n:
          pay = 1.5 * x
        else:
          pay = 0
        add("<p>You earn $%.02f" % pay)
        button("Proceed", "Proceed", wait=True)
        set("Wait...")

  # Do parts 1-4 twice
  for _ in range(2):
    # Part 1
    if DO_TRUST_GAMES:
      if number == 0: button(1, 1, wait=True)
      sync(number,numbers)
      names = list("123456abcdef")
      if number == 0:
        random.shuffle(names)
        for n in numbers:
          put(("name", n, names[n-1]))
        scores = [0] * 12
        for n in numbers:
          _, scores[n-1] = get(("score", None))
      else:
        _, _, name = get(("name", number, None))
        score = 0
        score += trust(msg(1,1),  name, "135ace", "246bdf")
        score += trust(msg(1,2),  name, "124abd", "356cef")
        score += trust(msg(1,3),  name, "123abc", "465dfe")
        score += trust(msg(1,4),  name, "123abc", "546edf")
        score += trust(msg(1,5),  name, "124abd", "635fce")
        score += trust(msg(1,6),  name, "bdf246", "135ace")
        score += trust(msg(1,7),  name, "cef356", "124abd")
        score += trust(msg(1,8),  name, "dfe465", "123abc")
        score += trust(msg(1,9),  name, "edf546", "123abc")
        score += trust(msg(1,10), name, "fce635", "124abe")
        put(("score", score))

    # Part 2
    if DO_LOTTERIES:
      if number == 0: button(2, 2, wait=True)
      lotteries()

    # Part 3
    if DO_TRUST_GAMES:
      if number == 0: button(3, 3, wait=True)
      sync(number,numbers)
      if number == 0:
        ranking = zip(*sorted(zip(scores, range(1,13)), reverse=True))[1]
        names = ["123456abcdef"[ranking.index(i)] for i in range(1,13)]
        for n in numbers:
          put(("name", n, names[n-1]))
      else:
        _, _, name = get(("name", number, None))
        set(name)      
        trust(msg(3,1), name, "135ace", "246bdf")
        trust(msg(3,2), name, "135ace", "246bdf")
        trust(msg(3,3), name, "123456", "abcdef")
        trust(msg(3,4), name, "123456", "abcdef")
        trust(msg(3,5), name, "fedcba", "563412")
        trust(msg(3,6), name, "fedcba", "563412")
        trust(msg(3,7), name, "123abc", "456def")
        trust(msg(3,8), name, "123abc", "456def")

    # Part 4
    if DO_LOTTERIES:
      if number == 0: button(4, 4, wait=True)
      lotteries()

   # Now run the surveys
  if DO_SURVEY:
    if number == 0:
      add("<div class='survey' />")
    else:
      set("<div class='survey' />")
    survey("SURVEY", number, numbers, SURVEY, ".survey")

  # Clear the screen
  if number > 0:      
    set(number)
      
run(session)
