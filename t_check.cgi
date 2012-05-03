#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import cgi

import httplib
from xml.dom.minidom import parseString

if 'QUERY_STRING' in os.environ:
    query = cgi.parse_qs(os.environ['QUERY_STRING'])
else:
    query = {}


# Yahoo!API config
appId = 'API KEY'
session = httplib.HTTPConnection('jlp.yahooapis.jp')

if len(query)>0:
    analiseStr = str(query['str'][0])
else:
    analiseStr = " "
#analiseStr = "魚鶏nだTeamよ"

#replace small space to all size space
analiseStr = analiseStr.replace(" ","　")

f = open('checked.log')
databaseFile = f.readlines()
f.close()

# set thresould if you want
thresould = 17
foundNum = 0

strArr =[]
scrArr =[]


def detect(line,dstr):
    detector = line.lower()
    isFind = detector.find( str(dstr.lower()) )
    if isFind>=0:
        return line
    else:
        return 0
        

def request(reqstStr):
    isFoundNearTweet = False
    
    fanaliseStr = reqstStr
    session.request('GET', '/KeyphraseService/V1/extract?appid='+appId+'&sentence='+fanaliseStr)
    response = session.getresponse().read()
    
    print  " " + fanaliseStr +"<br/>" +"<br/>"

    data = parseString( response )
    for item in data.getElementsByTagName('Keyphrase'):
        xmlTag = item.toxml()
        xmlData=xmlTag.replace('<Keyphrase>','').replace('</Keyphrase>','')
        strArr.append(xmlData)

        
    for item in data.getElementsByTagName('Score'):
        xmlTag = item.toxml()
        xmlData=xmlTag.replace('<Score>','').replace('</Score>','')
        scrArr.append(xmlData)

    # loop for detect lines
    if len(strArr) > 0:
        for item in range( len(strArr) ):
            if int( int(scrArr[item]) )>thresould:
                oncePrint = True
                print "key word: " + strArr[item].encode('utf-8') +" point: " + scrArr[item].encode('utf-8') + "<br/>" + "<br/>"
                for line in databaseFile:
                    dStr = detect( line, strArr[item].encode('utf-8') )
                    if not( dStr == 0 ):
                        isFoundNearTweet = True
                        if oncePrint:
                            print "似ているかもしれないダジャレ： " + "<br/>"
                            oncePrint = False
                        print dStr + "<br/>" + "<br/>"

                        
    if not( isFoundNearTweet ):
        print "見つからなかったよ" +"<br/>" +"<br/>"
    # else:
    #     print "キーワードが見つからなかったよ" +"<br/>" +"<br/>"
        

def main():
    
    if len(analiseStr)<=0:
        print "　"
    else:
        request( analiseStr )
    
    #print "</html>\n"

if __name__ == '__main__':
    main()
  
