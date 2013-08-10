import irclib
import json
from urllib import urlopen
import BeautifulSoup
import HTMLParser
import thread
from re import sub, search
class fourchan:
    def __init__(self):
        threadCountFile = open("./modules/pubmsg/THREADCOUNT", 'r')
        self.threadCount = int(threadCountFile.readline())
        threadCountFile.close()
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if "boards.4chan.org" in message:
            messageList = message.split(' ')
            for element in messageList:
                if element.startswith(("http://boards.4chan.org", "https://boards.4chan.org", "boards.4chan.org"), ):
                    thread = element.split("#p")[0]
                    try:
                        content = json.load(urlopen("%s.json" % thread))
                    except:
                        break
                    if "#p" in element:
                        postnumber = element.split("#p")[1]
                    else:
                        postnumber = element.split('/')[-1]
                    content = content["posts"]
                    postnumber = int(postnumber)
                    for i in range(len(content)):
                        target = int(content[i]["no"])
                        if target == postnumber:
                            comment = content[i]["com"]
                            comment = (HTMLParser.HTMLParser().unescape(comment)).encode('utf-8')
                            comment = sub('<[^<]+?>', ' ', comment)
                            try:
                                name = content[i]["name"]
                            except:
                                name = ""
                            now = content[i]["now"]
                            try:
                                trip = " " + content[i]["trip"]
                            except:
                                trip = ""
                            connection.privmsg(event.target(),
                                               "{0}{1} :: {2} :: {3} :: {4}".format(
                                                   name, trip, now, postnumber, comment).encode('utf-8'))

        if message.startswith(".4chan"):
            search_term = search('\.4chan\s(\w*)\s(.*)', message)
            try:
                board = search_term.group(1)
                search_term = search_term.group(2)
            except:
                connection.privmsg(event.target(), "Incorrect syntax: .4chan board search_term")
                return 0
            try:
                content = json.load(urlopen("http://boards.4chan.org/%s/catalog.json" % board))
                content
            except ValueError:
                connection.privmsg(event.target(), "Error opening catalog")
                return 0
            found_thread = 0
            output = []
            try:
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
                        if (search('(?i)%s' % search_term, comment)
                            or search('(?i)%s' % search_term, subject)):
                            found_thread += 1
                            output.append("[Replies: %d] [Images: %d] http://boards.4chan.org/%s/res/%s - " % (athread["replies"], athread["images"], board, athread["no"]) + sub(r"(<([^>]+)>)", " ", athread["com"])[:50] )
                connection.privmsg(event.target(), "Found %d threads containing keyword '%s':" % (found_thread, search_term))
                output = output[:self.threadCount] #The amount to show
                for athread in output:
                    athread = (HTMLParser.HTMLParser().unescape(athread)).encode('utf-8')
                    connection.privmsg(event.target(), athread)
            except:
                connection.privmsg(event.target(), "Invalid search syntax.")
