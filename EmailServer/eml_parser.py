#!/usr/bin/python

import os

email_files = []

def init():
  get_list_of_email_files()
  parse_email_files()

def get_list_of_email_files():
  global email_files
  email_files = os.listdir('example_emails')

def parse_email_files():
  for email in email_files:
    parse_eml_data(file_get_contents('example_emails/' + email))

def parse_eml_data(data):
  try:
    p = data.index('\r\n\r\n')
    rawHeaders = data[:p]
    rawBody = data[p+4:]
  except ValueError:
    try:
      p = data.index('\n\n')
      rawHeaders = data[:p]
      rawBody = data[p+2:]
    except ValueError:
      rawHeaders = data
      rawBody = ''

  print rawHeaders
  print rawBody

def file_get_contents(filename):
  with open(filename) as f:
    return f.read()

if __name__ == '__main__':
  init()
