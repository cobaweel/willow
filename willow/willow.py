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

import json, BaseHTTPServer, time, Queue, mimetypes, SocketServer
import threading, sys, csv, os, os.path

__all__ = ('log', 'put', 'get', 'tweak', 'grab', 'me', 'hold', 'flush',
           'add', 'set', 'push', 'pop', 'hide', 'show', 'peek', 'run',
           'config', 'url')

# The user may write records to a CSV file, which is automatically
# named based on the time the library is loaded, using the thread-safe
# log() function.  The library may write records to a trace file,
# which is automatically named based on the time the library is
# loaded, using the thread-safe trace() function.

log_fn1  = os.path.join("log",time.strftime("%Y-%m-%d-%H-%M-%S.csv"))
log_fd1  = open(log_fn1,"w")
log_csv  = csv.writer(log_fd1)
log_lock = threading.Lock()
log_fn2  = os.path.join("log",time.strftime("%Y-%m-%d-%H-%M-%S.txt"))
log_fd2  = open(log_fn2,"w")

def log(*msg):
  log_lock.acquire()
  log_csv.writerow([str(int(time.time()))] + list(msg))
  log_fd1.flush()
  log_fd2.write("%s  \t%r\n" % ("LOG", msg))
  log_fd2.flush()
  log_lock.release()

def trace(tag, obj, d=False):
  assert type(tag) == str
  def de(s): 
    if type(s) == unicode:
      return str(s)
    else:
      return s
  if type(obj) == tuple and d:
    obj = tuple(map(de,obj))
  msg = str(obj) + " "
  out = ""
  for line in msg.splitlines():
    for i in range(0,len(line),70):
      out += "         " + line[i:i+70] + "\n"
  log_lock.acquire()
  sys.stderr.write(("%s %d" % (tag, me())).ljust(9) + out[9:])
  log_fd2.write("%s\t%d\t%r\n" % (tag, me(), obj))
  log_lock.release()


# A tuple space is exposed to the user for communication between
# threads. Tuples can be inserted with put (with an optional delay),
# and removed with get (blocking) or grab (nonblocking, returns None
# on failure). Both get() and grab() accept a list of patterns and
# will only remove tuples that match the pattern, with None used as a
# wildcard. The JavaScript UI engine can also post tuples.

board_space   = dict()
board_counter = 0
board_cv      = threading.Condition()

def find(*queries):
  for key, candidate in board_space.iteritems():
    for query in queries:
      assert type(query)==tuple, "the board can only contain tuples"
      if ( len(query) == len(candidate) and
           all(map( (lambda q,c: q in (None,c)) , query, candidate )) ):
          return key
  return None

def put(item, delay=0):
  assert type(item)==tuple, "the board can only contain tuples"
  if delay < 0:
    raise Exception, "time travel not yet implemented" 
  elif delay > 0:
    name = threading.current_thread().name
    def thunk():
      threading.current_thread().name = name
      put(item)
    threading.Timer(delay, thunk).start()
  else:
    board_cv.acquire()
    global board_counter
    board_counter += 1
    board_space[board_counter] = item
    board_cv.notifyAll()
    board_cv.release()
    trace("PUT",item,True)

def get(*queries):
  trace("GET",queries)
  board_cv.acquire()
  key = find(*queries)
  while not key:
    board_cv.wait()
    key = find(*queries)
  found = board_space.pop(key)
  board_cv.release()
  trace("GOT",found,True)
  return found

def grab(*queries):
  trace("GRAB",queries)
  board_cv.acquire()
  key = find(*queries)
  if key:
    found = board_space.pop(key)
  else:
    found = None
  board_cv.release()
  trace("GRUB",found,True)
  return found


# Each client has two identifiers: (1) a "uuid" assigned by the
# JavaScript part of Willow based on the time and a pseudorandom
# number; and (2) a sequential assigned client ID "number", also used
# as the thread name for the associated thread, and retrievable with
# the me() function. The user only ever uses the number; the UUID is
# needed purely to avoid Byzantine Generals. We maintain two
# dictionaries, indexed by the two identifiers, that hold _Client
# objects. These objects hold the queues used to buffer communication
# between the clients and their associated session threads.

class _Client(): pass
clients_by_uuid   = dict()
clients_by_number = dict()
clients_lock      = threading.Lock()

def _new_client(session, uuid, url):
  clients_lock.acquire()
  number     = len(clients_by_number)
  t          = threading.Thread(target=session, name=("%d" % number))
  c          = _Client()
  c.queue    = Queue.Queue()
  c.flushing = True
  c.number   = number
  c.url      = url
  c.holding  = []
  clients_by_uuid[uuid]     = c
  clients_by_number[number] = c
  t.daemon   = True
  t.start()
  clients_lock.release()
  return c

def me():
  name = threading.current_thread().name
  try:
    number = int(name)
  except ValueError:
    raise Exception, "must be called from a session thread"
  return int(threading.current_thread().name)

def url():
  return clients_by_number[me()].url


# The user can stop immediate processing of UI actions and redirect
# them onto a queue with hold(), then flush the queue and turn
# immediate processing back on with flush(). This is optional, but may
# come in handy if performance is lacking. By default, these operate
# on the client associated with the current thread, but a different
# client or even a list of client numbers, can be provided
# instead.

def hold(number=None):
  if number == None: number = me()
  if type(number) == int: number = [number]
  for n in number:
    assert type(n) == int
    clients_by_number[n].flushing = False

def flush(number=None):
  if number == None: number = me()  
  if type(number) == int: number = [number]
  for n in number:
    assert type(n) == int
    client = clients_by_number[n]
    client.queue.put(client.holding)
    client.holding = []
    client.flushing = True


# A number of UI actions are available to the user. Each of these
# pushes a JSON object onto one or more client queues, which will be
# sent to the client when a POST request come into the web server. By
# default, these operate on the client associated with the current
# thread, but a different client number, or even a list of client
# numbers, can be provided instead. If the 'argument' is a file
# descriptor open for reading, the contents of the file will be
# passed.

def action(action, number, selector, arg1, arg2):
  if number == None: number = me()
  if type(number) == int: number = [number]
  for n in number:
    assert type(n) == int
    try: arg1 = arg1.read()
    except AttributeError: pass
    client = clients_by_number[n]
    client.holding += [{"action":   "%s" % action,
                        "selector": "%s" % selector,
                        "arg1": "%s" % arg1,
                        "arg2": "%s" % arg2}]
    if client.flushing:
      flush(n)

def add(arg1, selector="body", number=None):
  action("add", number, selector, arg1, "")

def set(arg1, selector="body", number=None):
  action("set", number, selector, arg1, "")

def tweak(arg1, arg2, selector, number=None):
  action("tweak", number, selector, arg1, arg2)

def push(arg1, selector="body", number=None):
  action("push", number, selector, arg1, "")

def pop(arg1, selector="body", number=None):
  action("pop", number, selector, arg1, "")

def hide(selector="body", number=None):
  action("hide", number, selector, "", "")

def show(selector="body", number=None):
  action("show", number, selector, "", "")

def peek(selector="body", number=None):
  action("peek", number, selector, "", "")


# A worse-is-better configuration API in one line

def config(fn): return json.load(open(fn))


# Run a web server. GET requests are simply served from the directory
# that willow.py is in, or if they are not present there, from the
# current directory. POST requests are where the magic happens.


WEBROOT = os.path.dirname(__file__)
def run(session, port=8000):
  class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def log_message(self, fmt, *arg): pass
    def do_GET(self):
      path = os.path.basename(self.path)
      if path in os.listdir(os.curdir):
        fn = os.curdir + self.path
      elif path in os.listdir(WEBROOT):
        fn = WEBROOT + self.path
      else:
        fn = WEBROOT + "/index.html"
      self.send_response(200)
      self.send_header("Content-type", mimetypes.guess_type(fn))
      self.end_headers()
      self.wfile.write(open(fn).read())
        
    def do_POST(self):
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      request_str = self.rfile.read(int(self.headers["Content-length"]))
      request_obj = json.loads(request_str)
      try:
        client = clients_by_uuid[request_obj["id"]]
      except KeyError:
        client = _new_client(session, request_obj["id"], request_obj["url"])
      threading.current_thread().name = str(client.number)
      if request_obj["action"] == "update":
        reply_obj = client.queue.get()
        while not client.queue.empty():
          reply_obj += client.queue.get()
        reply_str = json.dumps(reply_obj)
        for obj in reply_obj:
          trace(obj["action"].upper(),
                "%s ==> %s %s" % (obj["arg1"].strip(),
                                  obj["selector"].strip(),
                                  (obj["arg2"] or "").strip()))
        self.wfile.write(reply_str)
      else:
        put((request_obj["action"], client.number, request_obj["arg1"]))

  class MyHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

  MyHTTPServer(('', port), MyRequestHandler).serve_forever()

