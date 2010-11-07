# This is a very simple one, used in an experiment at GMU that does
# not otherwise use Willow in order to conduct a quiz. When the quiz
# is over, the experimenters go around the room, look at the answers,
# and explain any that the subject got wrong. The subject then clicks
# a button and the screen changes color to indicate that they're
# ready, which is a surprisingly useful expedient.

from willow.willow import *
from willow.twig import *

TF = ["True", "False"]
QUIZ = [
  ("You can adjust the fertilizer levels on your fruit farm by clicking on it anywhere.",TF),
  ("All subjects can use the teleporters freely during the experimental session.",TF),
  ("Each round lasts for 9 minutes.",TF),
  ("The yield of your fruit farm is placed in your inventory automatically at the beginning of each round.",TF),
  ("Your fruit farm will allow you to produce all of the three goods available on Tiki island.",TF),
  ("The only way to meet subjects from the other villages of Tiki Island is to travel to the central pavilion.",TF),
  ("You can keep your seeds after the end of a round.",TF),
  ("To remove a dialog window which you do not want to use, one can hit the \"Ignore\" button in the bottom-righthand corner.",TF),
  ("You can transfer seeds to any avatar anywhere on the island.",TF),
  ("You can adjust the fertilizer levels on your fruit farm at any time.",TF)
]
ANSWERS=["False", "False", "True", "False", "False",
         "True", "False", "True", "False", "True"]

def session():
  add(open("example_quiz.html"),"head")
  let("<div class='survey'></div>")
  results = survey("QUIZ", me(), QUIZ)
  let("")
  table( [ ["<b>Question</b>",
            "<b>Your answer</b>",
            "<b>Correct answer</b>"] ] +
         [ [ QUIZ[i][0], QUIZ[i][1][results[i]-1],
             ANSWERS[i] ] for i in range(len(QUIZ)) ])
  add("<p>Wait for an experimenter to review your answers.</p>")
  button("x","Click here when review is completed.")
  clack()
  get(("click",me(),"x"))
  tweak("background:olive;","style","td")
  
run(session)
