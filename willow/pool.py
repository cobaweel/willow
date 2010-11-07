from SocketServer import ThreadingMixIn
from Queue import Queue
import threading, socket

class ThreadPoolMixIn(ThreadingMixIn):
    numThreads = 10
    allow_reuse_address = True

    def serve_forever(self):
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target = self.process_request_thread)
            t.setDaemon(1)
            t.start()

        while True:
            self.handle_request()
            
        self.server_close()

    
    def process_request_thread(self):
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())

    
    def handle_request(self):
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            self.requests.put((request, client_address))
