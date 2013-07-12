#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import os.path
import httplib
import urllib,json
import tweepy
import time
import pickle
import optparse
from lxml import etree
import random
import re

# Constant
PICKLE_FILE = '/dev-app/takawo_checker/auth.pickle'
TIMEZONE = 'JST-9'

# App config
CONSUMER = 'YOUR KEY'
CONSUMER_SECRET = 'YOUR SECRET'
ACCESS_TOKEN = 'TOKEN'
ACCESS_TOKEN_SECRET = 'TOKEN SECRET'

since_id = 353180500468305920

def initialize():
  auth = tweepy.OAuthHandler(CONSUMER, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  return tweepy.API(auth)

def tweet():
  logFile = open('checked_sabun.log', 'r+')
  api = initialize()

  query = u'#takawo杯'
  encoded_query = urllib.quote_plus(query.encode('utf-8'));

  lastlines = logFile.readlines()
  fileLineNum = len(lastlines)
  lastlines = lastlines[fileLineNum-1:fileLineNum]

  try:
    result_list = tweepy.Cursor(api.search, encoded_query, since=since_id )

    for resultpage in result_list.pages():
      for tweet in resultpage:
        url = "https://twitter.com/#!/" + str(tweet.author.id) + "/status/" + str(tweet.id)
        print url
        logFile.write( '@' + str(tweet.author.screen_name.encode('utf-8')) + " "  + tweet.text.encode('utf-8') + " " + url +"\n")
        print( tweet.author.name , url)

  except tweepy.error.TweepError, e:
    print "error response code: " + str(e.response.status)
    print "error messate: " + str(e.response.reason)

  logFile.close()

  

def main():
  parser = optparse.OptionParser('Usage: %prog [options]')
  parser.add_option('-i', '--initialize',
      action='store_true', dest='initialize',
      help='Start the OAuth session')

  (options, args) = parser.parse_args()
  if len(args) != 0:
    parser.error('too many arguments')

  if options.initialize:
    print initialize()
  else:
    tweet()

if __name__ == '__main__':
  main()