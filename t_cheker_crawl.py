#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import os.path
from lxml import etree
import httplib
import urllib,json

logFile = open('checked_sabun.log', 'r+')
d = urllib.urlopen("http://search.twitter.com/search.json?q=%23takawo杯&rpp=100&since_id=108550900326469633&page=7")

lastlines = logFile.readlines()
fileLineNum = len(lastlines)
lastlines = lastlines[fileLineNum-1:fileLineNum]

r = d.read()
l = json.loads(r)
#print l
for s in l["results"]:
    url = "https://twitter.com/#!/" + str(s["from_user"]) + "/status/" + str(s["id"])
    print s["from_user"],s["text"], s["id"]
    #print('@' + str(s["from_user"].encode('utf-8')) + " "  + str(s["text"].encode('utf-8')) + " " + url +"\n")
    
    logFile.write( '@' + str(s["from_user"].encode('utf-8')) + " "  + str(s["text"].encode('utf-8')) + " " + url +"\n")

logFile.close()
    