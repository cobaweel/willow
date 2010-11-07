class ThreadPoolMixIn:
  # By default, we create "non-daemon" threads. 
  daemon_threads = False

  # The pool is a queue of available worker threads
  pool = Queue.Queue()

  # A new worker thread takes note of the pool it belongs to, and
  # creates a mailbox (i.e. length-1 queue) in which to receive
  # assignments. It then goes to sleep, but it wakes up whenever it
  # gets an assignment. When it gets an assignment, it does its
  # servery thing, and then adds itself to the pool to indicate that
  # it is available again.
  class Worker(Thread):
    def _init_(self, pool):
      self.pool = pool
      self.assignment = Queue.Queue(1)

    def run(self):
      while True:
        (request, address) = self.assignment.get()
        try:
          self.finish_request(request, client_address)
          self.close_request(request)
        except:
          self.handle_error(request, client_address)
          self.close_request(request)
        self.pool.put(self)

  # When a request comes in, we try to get a worker from the pool. If
  # there are none, we make a new one. Then we tell the worker to
  # work.
  def process_request(self, request, address):
    try:
      worker = pool.get_nowait()
    except Empty:
      worker = Worker(pool)
      worker.daemon = daemon_threads
      worker.start()
    worker.assignment.put((request, thread))


