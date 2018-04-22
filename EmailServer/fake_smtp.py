#!/usr/bin/env python

import smtpd
import asyncore
import time

class FakeSMTPServer(smtpd.SMTPServer):
  def __init__(*args, **kwargs):
    print 'Running fake smtp server on port 25'
    smtpd.SMTPServer.__init__(*args, **kwargs)

  def process_message(*args, **kwargs):
    mail = open('mails/' + str(time.time()) + '.eml', 'w')
    print 'New mail from ' + args[2]
    mail.write(args[4])
    mail.close
    pass

if __name__ == '__main__':
  smtp_server = FakeSMTPServer(('0.0.0.0', 25), None)
  try:
    asyncore.loop()
  except KeyboardInterrupt:
    smtp_server.close()
