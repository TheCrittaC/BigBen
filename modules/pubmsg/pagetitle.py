import irclib
import urllib
import urllib2
import BeautifulSoup
import HTMLParser
import thread
from re import sub

class pagetitle:
    def __init__(self):
        silentChannelsFile = open("./modules/pubmsg/SILENTCHANNELS", 'r')
        self.silentChannels = silentChannelsFile.readlines()
        silentChannelsFile.close()

    def sayWebpageTitle(self, url, event, connection):
        HTMLParserObject = HTMLParser.HTMLParser()
        headers = {'User-Agent' : 'Mozilla/5.0'} #our user agent prevents some 403 errors
        req = urllib2.Request(url, '', headers)
        try:
            title = HTMLParserObject.unescape(BeautifulSoup.BeautifulSoup(urllib2.urlopen(req).read()).title.string)
        except Exception:
            title = HTMLParserObject.unescape(BeautifulSoup.BeautifulSoup(urllib.urlopen(url)).title.string)
        title = title.strip() #removes leading and trailing whitespace
        title = sub('[\n]', '', title) #removes any newlines that are in the title
        #retrieves page titles and parses special characters
        title = title.encode('utf-8')
        if not title == "":
            connection.privmsg(event.target(), "Title: " + title)
    
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if "http://" in message or "https://" in message:
            if not event.target() in self.silentChannels:
                messageList = message.split(' ')
                for element in messageList:
                    if element.startswith(("http://","https://"), ):
                        thread.start_new_thread(self.sayWebpageTitle, (element,event, connection))
