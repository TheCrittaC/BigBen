import irclib
import json
from urllib import urlopen
import BeautifulSoup
import HTMLParser
import thread
from time import sleep
from re import sub, search
import traceback

class fourchanmonitor:
    def __init__(self, connection):
        self.connection = connection
        monitorFile = open("./modules/static/ThreadMonitor", 'r')
        monitorList = monitorFile.read().splitlines()
        monitorFile.close()
        for item in monitorList:
            splitInfo = item.split(' :: ')
            channel = splitInfo[0]
            board = splitInfo[1]
            regex = splitInfo[2]
            updateInterval = int(splitInfo[3])
            thread.start_new_thread(self.watchThreads,
                                    (channel, board, regex,
                                     updateInterval, self.connection))
            
    def watchThreads(self, channel, board, regex,
                     updateInterval, connection):
        oldPostNum = 0
        postNum = 0
        while 1:
            try:
                content = json.load(urlopen("http://boards.4chan.org/%s/catalog.json" % board))
                for i in range(len(content)):
                    for athread in content[i]["threads"]:
                        comment = ""
                        subject = ""
                        try:
                            comment = athread["com"]
                        except KeyError:
                            break
                        try:
                            subject = athread["sub"]
                        except KeyError:
                            pass
                        if (search('(?i)%s' % regex, comment)
                            or search('(?i)%s' % regex, subject)
                            and int(athread["no"]) > postNum):
                            oldPostNum = postNum
                            postNum = int(athread["no"])
                            output = ("Found new thread matching %s - http://boards.4chan.org/%s/res/%s - %s"
                                          % (regex, board, athread["no"], athread["com"][:50]))
                            output = (HTMLParser.HTMLParser().unescape(output)).encode('utf-8')
                            if oldPostNum != 0:
                                connection.privmsg(channel, output)
                            break
                    if oldPostNum != postNum:
                        break
                    
            except:
                print "Error with parsing."
            sleep(updateInterval)
