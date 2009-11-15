import json, BaseHTTPServer, SimpleHTTPServer, time, Queue, mimetypes
import SocketServer, threading, sys, cgi, re, csv, os, os.path

WEBROOT = os.path.dirname(__file__)

class Board():
  """A Board is a thread-safe tuple space. You can post tuples on it,
  and remove tuples from it, with or without wildcard matching and
  with or without blocking."""

  def __init__(self, log):
    self.space = dict()
    self.counter = 0
    self.cv = threading.Condition()
    self.log = log

  def __find(self, *queries):
    for key, candidate in self.space.iteritems():
      for query in queries:
        assert type(query)==tuple, "Type mismatch."
        if (len(query) == len(candidate) and
            all(map((lambda q,c: q in set([None,c])), query, candidate))):
          return key
    return None

  def put(self, item, delay=0):
    """To add a tuple (x,y,z) to a board b, just call b.put(x,y,z)."""
    assert type(item)==tuple and type(delay)==int, "Type mismatch."
    if delay > 0:
      def thunk(): self.put(item)
      threading.Timer(delay, thunk).start()
    else:
      self.cv.acquire()
      self.counter += 1
      self.space[self.counter] = item
      self.cv.notifyAll()
      self.cv.release()
      self.log.trace("PUT",item)

  def get(self, *queries):
    """To remove e.g. a tuple that matches either (x,y) or (p,q), you
    call b.gets((x,y),(p,q)). You can still use wildcards."""
    assert type(queries)==tuple, "Type mismatch."    
    self.log.trace("GET",queries)
    self.cv.acquire()
    key = self.__find(*queries)
    while not key:
      self.cv.wait()
      key = self.__find(*queries)
    found = self.space.pop(key)
    self.cv.release()
    self.log.trace("GOT",found)
    return found

class Client():
  """A Client object corresponds to an instance of willow.html being
  viewed remotely."""

  number = -1
  """Number of the client."""

  ip = ""
  """IP address of the client."""

  def __init__(self, number, ip, log):
    self.number = number                # Number identifying client
    self.ip = ip                        # IP address of client    
    self.queue = Queue.Queue()          # Queue for AJAX messages
    self.flushing = True
    self.holding = []
    self.log = log

  def __action(self, action, selector, argument=None):
    try: argument = argument.read()
    except AttributeError: pass
    self.holding += [{"action":   "%s" % action,
                      "selector": "%s" % selector,
                      "argument": "%s" % argument}]
    if self.flushing:
      self.flush()

  def hold(self):
    self.flushing = False

  def flush(self):
    self.log.trace("FLUSH", self.holding)
    self.queue.put(self.holding)
    self.holding = []
    self.flushing = True

  def add(self, argument, selector="#base"):
    """Add some HTML to each element referenced by the selector."""
    self.__action("add", selector, argument)

  def set(self, argument, selector="#base"):
    """Set the contents of each element referenced by the selector."""
    self.__action("set", selector, argument)

  def push(self, argument, selector="#base"):
    """Push a class on each element referenced by the selector."""
    self.__action("push", selector, argument)

  def pop(self, argument, selector="#base"):
    """Pop a class from each element referenced by the selector."""
    self.__action("pop", selector, argument)

  def hide(self, selector="#base"):
    """Hide each element referenced by the selector."""
    self.__action("hide", selector)

  def show(self, selector="#base"):
    """Show each element referenced by the selector. This works both
    on elements previously hidden using the client.hide() method and
    on items automatically hidden because they are of class 'hidden'."""
    self.__action("show", selector)

  def data(self, selector="#base"):
    """Request that the 'value' attribute of each element referenced
    by the selector be posted on the board."""
    self.__action("data", selector)

class Log():
  """A Log object can be used to record log messages into a log file,
  which is in CSV format and automatically gets a name based on the
  date and time the session starts."""
  def __init__(self):
    self.fn = time.strftime("log/%Y-%m-%d-%H-%M-%S.csv")
    self.fd = open(self.fn,"w")
    self.csv = csv.writer(self.fd)
    self.fn2 = time.strftime("log/%Y-%m-%d-%H-%M-%S.txt")
    self.fd2 = open(self.fn2,"w")
    self.lock = threading.Lock()

  def write(self, *msg):
    """Write a record into the CSV log file, with the UNIX timestamp
    as the first field, and *msg as the subsequent fields."""
    self.lock.acquire()
    self.csv.writerow([str(int(time.time()))] + list(msg))
    sys.stderr.write("%s  \t%r\n" % ("LOG", msg))
    self.fd2.write("%s  \t%r\n" % ("LOG", msg))
    self.lock.release()

  def trace(self, tag, obj):
    """Show a trace message on stderr and in the trace file. For
    internal use by the willow library."""
    msg = str(obj)
    self.lock.acquire()
    sys.stderr.write("%s  \t%s\n" % (tag,msg[0:65]))
    for i in range(65,len(msg),65):
      sys.stderr.write("\t%s\n" % msg[i:i+65])
    self.fd2.write("%s  \t%r\n" % (tag, obj))
    self.lock.release()

def run(session, port=8000):
  """Run a web server using given session function on given TCP
  port. Use port numbers over 1024 to avoid the need for
  administrative privileges on the server machine. The session
  function must accept two arguments: the first is a Client object,
  and the second is a Board object. The Client object is different for
  each session thread; the Board object is the same for each session
  thread."""

  log = Log()
  clients = {}
  clients_lock = threading.Lock()
  board = Board(log)

  class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def log_message(self, fmt, *arg): pass
    def do_GET(self):
      path = os.path.basename(self.path)
      fn = None
      if path in ['','/']: fn = WEBROOT +"/index.html"
      if path in os.listdir(os.curdir): fn = os.curdir + self.path
      if path in os.listdir(WEBROOT): fn = WEBROOT + self.path
      if fn:
        self.send_response(200)
        self.send_header("Content-type", mimetypes.guess_type(fn))
        self.end_headers()
        self.wfile.write(open(fn).read())
      else:
        self.send_response(404)
        self.end_headers()
        self.wfile.write("<h1>File %r not found</h1>" % path)
        
    def do_POST(self):
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      request_str = self.rfile.read(int(self.headers["Content-length"]))
      request_obj = json.loads(request_str)
      log.trace("RECV", request_obj)
      request_id = request_obj["id"]
      try:
        client = clients[request_id]
      except KeyError:
        clients_lock.acquire()
        number = len(clients)
        ip, _ = self.client_address
        client = Client(number, ip, log)
        clients[request_id] = client
        clients_lock.release()
        t = threading.Thread(target=session, args=(client,board, log))
        t.daemon = True
        t.start()                
      if request_obj["action"] == "update":
        reply_obj = client.queue.get()
        while not client.queue.empty():
          reply_obj += client.queue.get()
        reply_str = json.dumps(reply_obj)
        log.trace("SEND", reply_obj)
        self.wfile.write(reply_str)
      else:
        board.put((request_obj["action"], client.number, request_obj["argument"]))

  class MyHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

  MyHTTPServer(('', port), MyRequestHandler).serve_forever()

def sleep(x):
  """Sleep x seconds, where x can be a floating point value."""
  time.sleep(x)
  
def escape(s):
  """Turn s into a string safe for inclusion in HTML;
  e.g. escape('<>')=='&lt;&gt;'.""" 
  return cgi.escape(s)

def config(fn):
  """Reads a configuration file in JSON format."""
  return json.load(open(fn))

# Willow, a Python framework for experimental economics
# Copyright (c) 2009, George Mason University
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the George Mason University nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission. THIS SOFTWARE
# IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
