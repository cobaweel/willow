# Willow, a Python framework for experimental economics. Copyright (c)
# 2009, George Mason University All rights reserved.  Redistribution
# and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the George Mason University nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission. THIS
# SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from willow import *
import string

def button(id, text, selector="body", 
           pre="", post="", clss="", number=None, wait=False):
    id = str(id)
    text = str(text)
    add(("%s<input type='submit' id='%s' class='%s' value='%s'>%s" %
         (pre, id, clss, text, post)),
        selector, number)
    if wait:
        clack()
        get(("click", me(), id))

def table(tbl, selector="body", 
          pre="", post="", clss="", number=None):
    txt = pre
    txt += "<table border=1 class='%s'>" % clss
    for row in tbl:
        txt += "<tr>"
        for col in row:
            txt += "<td>%s</td>" % col
        txt += "</tr>"
    txt += "</table>"
    txt += post
    add(txt, selector, number)
        
def assemble(required = 0):
  if me() == 0:
    set("Monitor", "title")
    set("<h1>Willow Client Assembly")
    login_numbers = [0]
    if required == 0: button(0, 0)
    while True:
      _, client_number, arg = get(("click", 0, None),
                                ("__present", None, None))
      if client_number == 0:
        for n in range(2,len(login_numbers)+1):
          button(string.join(map(str,login_numbers[0:n])),
                 string.join(map(str,login_numbers[0:n]),", "),
                 pre="<br>")
        _, _, arg = get(("click",0,None))
        use = map(int, string.split(arg))
        for _ in login_numbers[1:]: put(("__use",use))
        set("<h1>0")
        return 0, use
      else:
        login_number = arg
        if (login_number in login_numbers) or (not login_number):
          login_number = 0
          while login_number in login_numbers: login_number += 1
        login_numbers += [login_number]
        login_numbers.sort()
        add("<br>%r (%d)" % (login_numbers, len(login_numbers)-1))
        put(("__number", client_number, login_number))
        if required > 0 and login_numbers == range(required+1):
          for _ in login_numbers[1:]: put(("__use", login_numbers))
          set("<h1>0")
          return 0, login_numbers
  else:
    if url().lstrip('/').isdigit():
      login_number = int(url().lstrip('/'))
      put(("__present", me(), login_number))
    else:
      set("<input id='__login' type='submit' value='Log in'>")
      get(("click", me(), "__login"))
      put(("__present", me(), None))
    _, _, login_number = get (("__number", me(), None))
    set("<h1>%d" % login_number, "body,title")
    _, use = get(("__use", None))
    if login_number in use:
      return login_number, use
    else:
      set("<h1>X")
      return None, use

def clack():
    while grab(("click", me(), None)): pass

def survey(title, number, numbers, questions, selector="body"):
  if number == 0:
    button("__survey_%s" % title, title, selector, wait=True)
    add("<p>&nbsp;</p>")
    clack()
    for n in numbers: add("<div class='__survey_%s_%d'><b>%d</b> </div>" %
                          (title, n, n), selector)
    get(("click", me(), "__survey_%s" % title))
    sync(number, numbers)
  else:
    sync(number, numbers)    
    results = []
    for n_question, (question, valid) in enumerate(questions):
      n_question += 1
      while grab(("click", me(), None), ("peek", me(), None)): pass
      if type(valid) == list:
        tuples = []
        set("<p>%s" % question, selector)
        for n_answer, answer in enumerate(valid):
          tag = "__%d_%d_%s" % (n_question, n_answer, title)
          tuples += [("click", me(), tag)]
          button(tag, answer, selector, pre="<br>")
        _, _, choice = get(*tuples)
        choice = int(choice.split("_")[3]) + 1
      else:
        tried = False
        while not tried or (valid and not valid(choice)):
          tag = "__%d_%s" % (n_question, title)
          set("<p>%s" % question, selector)
          add("<input type='text' id='%s' value=''>" % tag, selector)
          if tried:
            tweak("background-color: red;","style","#%s" % tag)
          button(tag + "_OK", "OK", selector, pre="<br>")
          get(("click", me(), tag+"_OK"))
          peek("#%s" % tag)
          _, _, choice = get(("peek", me(), None))
          tried = True
      add("<sup>%d</sup>%s " % (n_question, choice),
          ".__survey_%s_%d" % (title, number), number=0)
      log(title, number, n_question, choice)
      results += [choice]
    return results

def sync(number,numbers):
    if number == numbers[0]:
        for n in numbers[1:]: get(("__ping",n))
        for n in numbers[1:]: put(("__pong",n))
    else:
        put(("__ping",number))
        get(("__pong",number))
