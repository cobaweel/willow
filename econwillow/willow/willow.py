# Willow, a Python framework for experimental economics. Copyright (c)
# 2009, George Mason University. All rights reserved. Redistribution
# allowed under certain conditions; see file COPYING.txt

# WILLOW #############################################################
# This file is a library that you can use to write a server. You use
# such a server in combination with a client. The client is always a
# web browser displaying willow.html and running willow.js. None of
# this client-server business, however, is germane to the way you
# ought to think about writing a Willow application, though: you can
# write your application as though you were using a regular old GUI
# toolkit and there wasn't a client/server architecture or a network
# in the first place.

# The comments in this file are meant for people who have some
# experience with distributed systems and want to hack Willow
# itself. If you merely want to USE the Willow library to construct
# your own applications, read the manual instead.

import json, BaseHTTPServer, time, Queue, mimetypes, SocketServer
import threading, sys, csv, os, os.path, copy, re, stat


# LOGGING ############################################################

# This section provides the code that produces the output files, which
# go in the log/ directory.

# The file names for output files are constructed so as to work on all
# platforms. This means we use os.path.join to insert the right path
# separator, and we do not the ':' character, which has a special
# meaning on Windows (as in "C:\"). All output is unbuffered
# (bufsize=0) and synchronized on a single mutex. This code SHOULD be
# unicode-safe (important if we want to use it in, say, China), but I
# haven't tested that very much.

_log_fn = os.path.join("log",time.strftime("%Y-%m-%d-%H-%M-%S"))
_log_csv = csv.writer(open(_log_fn + ".csv","w",0))
_log_txt = open(_log_fn + ".txt", "w", 0)
_log_lock = threading.Lock()

tbl = []

def log(*msg):
  with _log_lock:
    _log_csv.writerow([int(1000*time.time())] + list(msg))
    tbl.append(msg)
  _trace("log",unicode(tuple(msg)))

def _trace(tag, *objs):
  with _log_lock:
    msg = "\n".join([ ("%s" % d) for d in objs ])
    out = ""
    for line in (msg + " ").splitlines():
      for i in range(0,len(line),70):
        out += "        " + line[i:i+70] + "\n"
    s = "%-4s %2d %s" % (tag, _me(), out[8:])
    lines = s.splitlines()
    if len(lines) > 10: lines = lines[:3] + ["..."]
    for line in lines: sys.stdout.write(line + "\n")
    _log_txt.write("%s\t%d\t%r\n" % (tag, _me(), msg))

def _trace_action(obj):
  tag = obj["action"]
  msg = "(%s)" % obj["selector"]
  if obj.get("timestamp", False):
    msg += " ...timestamp..."
  if obj.get("delay",0) != 0:
    msg += " ...%s..." % obj["delay"]
  if obj.get("css_class", "") != "":
    msg += " %s" % obj["css_class"]
  if obj.get("attribute", "") != "":
    msg += " %s=" % obj["attribute"]
  if obj.get("value", "") != "":
    msg += "%s" % obj["value"]
  if obj.get("content", "") != "":
    if len(str(obj["content"]))>50:
      msg += "\n"
    else:
      msg += " "
    msg += "%s" % obj["content"]
  _trace(tag, msg)


# TUPLE SPACE ########################################################

# The tuple space is for communication between session threads, and
# for asynchronous messages from the clients to the session
# threads. (Messages from the session threads to the clients go
# through a system of queues instead, which we will meet in the next
# session.) It allows you to write your program without shared state
# between threads, and thus without your having to worry about
# race conditions.

# Conceptually, the tuple space is a multiset of dictionaries, but
# Python doesn't have multisets, so we use a dictionary of
# dictionaries in which the keys are not really used for much of
# anything (they are simply sequentially assigned integers). All
# access to the tuple space is synchronized on a condition variable. A
# put() operation is a simple matter of inserting a value into the
# dictionary and waking up any threads that are blocking on take(). A
# deep copy is made of the inserted object to prevent a user from
# accidentally sharing data structures between threads by way of the
# tuple space; the whole point of the tuple space is to facilitate a
# shared-nothing archictecture in which the user need not be concerned
# with mutual exclusion! There are both blocking (take()) and
# nonblocking (grab()) functions for retrieving (and deleting)
# dictionaries from the space, and both of those invoke a simple
# linear search. To facilitate future extensions along the lines of
# the Metaweb Query Language (both faster-than-linear search if that
# turns out necessary and also more elaborate query constructs), I
# restrict keys in the dictionaries and in queries to be only strings.

_board_space   = {}
_board_counter = 0
_board_cv      = threading.Condition()

def put(item):
  with _board_cv:
    global _board_counter
    assert type(item) == dict
    assert all([ type(key) in [unicode, str] for key in item.keys() ])
    _trace("put", item)
    _board_counter += 1
    _board_space[_board_counter] = copy.deepcopy(item)
    _board_cv.notifyAll()

def _find(pop, *patterns):
  for number, item in _board_space.iteritems():
    for pattern in patterns:
      assert all([ type(key) == str for key in pattern.keys() ])      
      if all([ k in item and item[k] == v for k,v in pattern.iteritems()]):
        if pop: _board_space.pop(number)
        return item
  return None

def take(*patterns):
  with _board_cv:
    _trace("take", *patterns)
    while True:
      item = _find(True, *patterns)
      if item != None: break
      _board_cv.wait()
    _trace("took", item)
    return item

def view(*patterns):
  with _board_cv:
    _trace("view", *patterns)
    while True:
      item = _find(False, *patterns)
      if item != None: break
      _board_cv.wait()
    _trace("veow", item)
    return item

def grab(*patterns):
  with _board_cv:
    _trace("grab", *patterns)
    item = _find(True, *patterns)
    _trace("grub", item)
    return item


# THREAD POOL EXTENSION TO THE PYTHON TCP SERVER #####################

# In order to get decent performance on Windows, we must improve a bit
# upon the standard Python TCP server. In particular, we replace
# SocketServer.ThreadingMixIn with a homebrew class. 

# If you want to use the original, you can try this instead:
# 
# class WillowPool(SocketServer.ThreadingMixIn): pass

class WillowPool:
  # By default, we create "non-daemon" threads. 
  daemon_threads = False

  # The pool is a queue of available worker threads
  pool = Queue.Queue()

  # A new worker thread creates a mailbox (i.e. length-1 queue) in
  # which to receive assignments. It then goes to sleep, but it wakes
  # up whenever it gets an assignment. When it gets an assignment, it
  # does the server thing, and then adds itself to the pool to
  # indicate that it is available again.
  class Worker(threading.Thread):
    def __init__(self, server):
      threading.Thread.__init__(self)
      self.server = server
      self.mailbox = Queue.Queue(1)

    def run(self):
      while True:
        (request, address) = self.mailbox.get()
        try:
          self.server.finish_request(request, address)
          self.server.close_request(request)
        except:
          self.server.handle_error(request, address)
          self.server.close_request(request)
        self.server.pool.put(self)

  # When a request comes in, we try to get a worker from the pool. If
  # there are none, we make a new one. Then we tell the worker to
  # work.
  def process_request(self, request, address):
    try:
      worker = self.pool.get_nowait()
    except Queue.Empty:
      worker = self.Worker(self)
      worker.daemon = self.daemon_threads
      worker.start()
    worker.mailbox.put((request, address))



# WEB SERVER #########################################################

# The Willow web server is built on Python's BaseHTTPServer. It uses a
# new thread for each request, which is slow on Windows. A thread pool
# would be useful improvement. GET requests are served from the file
# system, but POST requests are special and assumed to come from
# willow.js. They come in three flavors: a newly connected client
# POSTs to /new first, requesting a client ID. On this occasion, a
# queue is created and inserted into the _clients dictionary
# (synchronized on a condition variable) keyed by the new client ID,
# and a session thread is started. The queue is for communication
# between the web server threads and the session thread. Once the
# client ID is determined it is sent to the client, which can now make
# to other kinds of POST requests. The first is to URL /put, and this
# simply lets the client put something on the tuple space. (The client
# objects are JSON data structures, which map directly onto Python
# data structures and no further processing is required.) The second
# type of POST request from the client is a request for commands, and
# these commands the web server gets from the queue corresponding to
# the client, where they are put by the session thread corresponding
# to the client. If multiple commands are on the queue, they are all
# sent to the client at once. The commands are assumed to be
# dictionaries and because they are sent in JSON, so conversion from
# Python comes (again) nearly free.

class Client: 
  def __init__(self):
    self.queue = Queue.Queue()
    self.trace = []

  def send(self, msg):
    self.queue.put(msg)
    self.trace.append(msg)

  def replay(self):
    cancellation = Queue.Queue()
    self.queue.put(cancellation)
    cancellation.get()
    for msg in self.trace:
      self.queue.put(msg)

_clients = {}
_clients_cv = threading.Condition()

def run(session, port=8000):
  webroot = os.path.dirname(__file__) or os.curdir
  class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def log_message(self, fmt, *arg):      pass
    
    def do_GET(self):
      fns = [ os.path.join(os.curdir, self.path[1:]),
              os.path.join(os.path.dirname(__file__), self.path[1:]),
              os.path.join(os.path.dirname(__file__), "willow.html") ]
      for fn in fns:
        if os.path.isfile(fn):
          mime = mimetypes.guess_type(fn)
          if type(mime) == tuple: mime = mime[0]
          if re.search(".js$", fn):  mime = "text/javascript"
          if re.search(".css$", fn): mime = "text/css"
          self.send_response(200)
          self.send_header("Content-type", mime)
          self.end_headers()
          self.wfile.write(open(fn).read())
          return
        
    def do_POST(self):
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      request_sz = int(self.headers["Content-length"])
      request_str = self.rfile.read(request_sz) + " "
      request_obj = json.loads(request_str)
      
      if self.path == "/new":
        with _clients_cv:
          if request_obj < 0:
            client = 0
            while client in _clients:
              client += 1
          else:
            client = request_obj
          self.wfile.write(client)
          if not client in _clients:
            _clients[client] = Client()
            thread = threading.Thread(target=session,
                                      args=(client,),
                                      name=str(client))
            thread.daemon = True
            thread.start()
          else:
            _iam(client)
            _trace("bork", " *** CLIENT %s RESTARTED *** " % client)
            _clients[client].replay()
          
      if self.path == "/put":
        _iam(request_obj.get("client",-1))
        put(request_obj)
        
      if self.path == "/do":
        client = request_obj
        _iam(client)
        queue = _clients[client].queue
        actions = []
        try:
            while actions == [] or not queue.empty():
              action = queue.get()
              if isinstance(action,Queue.Queue): 
                action.put(0)
                raise Exception
              _trace_action(action)
              actions.append(action)
            self.wfile.write(json.dumps(actions))
        except Exception:
          pass

  class Server(WillowPool, BaseHTTPServer.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

  _iam(-1)
  _trace("run", "Willow is running on port %s" % port)
  Server(('', port), Handler).serve_forever()

def _me():
  return int(threading.current_thread().name)

def _iam(n):
  threading.current_thread().name = str(n)



# IO #################################################################

# This is where the bulk of the Willow API is: functions that do
# nothing but send a command to the client, which then processes the
# command in Javascript somehow. Documentation is in the manual. The
# one interesting point is that each session thread has one integer's
# worth of thread-local storage: the client ID of its corresponding
# client. That way, the user can call add(foo) rather than having to
# type add(foo,me) all the time.

def _action(object, clients):
  if clients == None: clients = _me()
  if type(clients) == int: clients = [clients]
  if "content" in object and type(object["content"]) == file:
    object["content"] = object["content"].read()
  if "content" in object: object["content"] = str(object["content"])
  if "value" in object: object["value"] = str(object["value"])
  for client in clients: 
    _clients[client].send(object)

def add(content, selector="body", clients=None, timestamp=False, delay=0):
  _action({ 'action': 'add', 'content': content,
            'selector': selector,
            "timestamp": timestamp, "delay": delay }, clients)

def let(content, selector="body", clients=None, timestamp=False, delay=0):
  _action({ 'action': 'let', 'content': content,
            'selector': selector,
            "timestamp": timestamp, "delay": delay }, clients)

def poke(attribute, value, selector="body", clients=None,
         timestamp=False, delay=0):
  _action({ 'action': 'poke', 'attribute': attribute, 'value': value,
            'selector': selector,
            "timestamp": timestamp, "delay": delay }, clients)

def hide(selector="body", clients=None, timestamp=False, delay=0):
  _action({ 'action': 'hide',
            'selector': selector,
            "timestamp": timestamp, "delay": delay }, clients)

def show(selector="body", clients=None, timestamp=False, delay=0):
  _action({ 'action': 'show',
            'selector': selector,
            "timestamp": timestamp, "delay": delay }, clients)

def push(css_class, selector="body", clients=None,
         timestamp=False, delay=0):
  _action({ 'action': 'push', 'css_class': css_class,
            'selector': selector,
            "timestamp": timestamp, "delay": delay }, clients)

def pop(css_class, selector="body", clients=None,
        timestamp=False, delay=0):
  _action({ 'action': 'pop', 'css_class': css_class,
            'selector': selector,
            "timestamp": timestamp, "delay": delay }, clients)

_ticket_lock = threading.Lock()
_ticket = [0]
def peek(selector="body", clients=None):
  with _ticket_lock:
    _ticket[0] += 1
    ticket = _ticket[0]
  _action({ 'action': 'peek', 'selector': selector,
            'ticket': ticket,
            "timestamp": False, "delay": 0 }, clients)
  msg = take({"tag":"peek","ticket":ticket})
  return msg['value']
  


# THREADING ##########################################################

# The background() function allows the user to start a new
# thread. This adjusts the thread-local stored client ID so that you
# can still call add() etc from inside the new thread and they will
# know which client to operate on. It also takes an optional delay, so
# you can use this to schedule events. Otherwise, it's just your basic
# forking operation.

def background(function, delay=0):
  name = threading.current_thread().name
  def thunk():
    threading.current_thread().name = name
    function()
  threading.Timer(delay, thunk).start()  

def sleep(delay):
  time.sleep(delay)
