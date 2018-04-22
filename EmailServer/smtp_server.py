#!/usr/bin/python

import os
import socket
import sys
from threading import Thread, Lock, Condition

name = 'HnSWave'
host = '0.0.0.0'
port = 25

ERROR = {
  'unrecognized': '500 Error: command not recognized',
  'syntax_helo': '501 Syntax: HELO yourhostname',
  'syntax_from': '501 Syntax: MAIL FROM: you@domain.com',
  'syntax_to': '501 Syntax: RCPT TO: sendto@domain.com',
  'syntax_data': '501 Syntax: DATA <CR><LF> message <CR><LF>.<CR><LF>',
  'order': '503 Error: need {} command',
  'duplicate_helo': '503 Error: duplicate HELO',
  'nested_mail': '503 Error: nested MAIL command',
  'sender': '555 {}: Sender address rejected',
  'recipient': '555 {}: Recipient address invalid',
  'timeout': '421 4.4.2 {} Error: timeout exceeded'
}

OK = {
  'INIT': '220 {} SMTP',
  'HELO': '250 {}',
  'MAIL': '250 OK',
  'RCPT': '250 OK',
  'DATA': '354 End data with <CR><LF>.<CR><LF>',
  'FIN': '250 OK: Delivered {} messages'
}

class ConnectionHandler(Thread):
  def __init__(self, thread_pool):
    Thread.__init__(self)
    self.pool = thread_pool
    self.TIMEOUT = 30
    self.s_pointer = 0
    self.states = ['INIT', 'HELO', 'MAIL', 'RCPT', 'DATA', 'FIN']
    self.client_name = ''
    self.from_mail = ''
    self.to_mails = []
    self.text_body = ''

  def handle(self):
    self.send_ok('INIT')
    self.socket.close()

  def parse_buffer(self, messages):
    args = messages.split('\r\n')
    head_msg = args[0]
    tail_msg = args[1:-1]
    self.parse(head_msg)
    for m in tail_msg:
      self.parse(m)

  def parse(self, message):
    args = message.split()

  def send_ok(self, state):
    if state in self.states:
      self.s_pointer = self.states.index(state)
      message = OK[state]
    else:
      self.s_pointer = len(self.states) - 1
      message = 'State not recognized'
    self.socket.send(message)
    self.socket.settimeout(self.TIMEOUT)

  def send_error(self, state):
    message = ERROR[state]
    self.socket.send(message)

  def run(self):
    while True:
      try:
        self.socket = self.pool.get_connection()
        self.handle()
      except socket.timeout:
        self.send_error('timeout')
        self.socket.close()

class ThreadPool:
  def __init__(self, number_threads):
    self.pool_lock = Lock()
    self.connection_available = Condition(self.pool_lock)
    self.request_available = Condition(self.pool_lock)
    self.conn_pool = []
    self.number_connections = 0
    self.max_conn = number_threads

  def connection_ready(self, socket):
    with self.pool_lock:
      while self.number_connections >= self.max_conn:
        self.connection_available.wait()
      self.conn_pool.append(socket)
      self.number_connections += 1
      self.request_available.notifyAll()

  def get_connection(self):
    with self.pool_lock:
      while self.number_connections == 0:
        self.request_available.wait()
      socket = self.conn_pool.pop()
      self.number_connections -= 1
      self.connection_available.notifyAll()
      return socket

def serverloop():
  pool = ThreadPool(32)
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((host, port))
  server_socket.listen(5)

  for _ in range(32):
    ConnectionHandler(pool).start()

  while True:
    (client_socket, address) = server_socket.accept()
    pool.connection_ready(client_socket)

print('Server coming up on %s:%i' % (host, port))

if __name__ == '__main__':
  try:
    serverloop()
  except KeyboardInterrupt:
    print 'Interrupted'
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
