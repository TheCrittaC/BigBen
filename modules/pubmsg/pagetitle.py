import irclib
import urllib
import urllib2
import BeautifulSoup
import HTMLParser
import thread
from re import sub
from re import search

class pagetitle:
    def __init__(self):
        silentChannelsFile = open("./modules/pubmsg/SILENTCHANNELS", 'r')
        self.silentChannels = silentChannelsFile.read().splitlines()
        silentChannelsFile.close()
        noFetchFile = open("./modules/pubmsg/NoTitle", 'r')
        self.noFetchRegexes = noFetchFile.read().splitlines()
        noFetchFile.close()

    def getContentType(self, url):
        headers = urllib2.urlopen(url)
        return headers.headers['content-type']

    def sayWebpageTitle(self, url, event, connection):
        if url == "":
            return
        if not self.getContentType(url).startswith("text/html"):
            return
        HTMLParserObject = HTMLParser.HTMLParser()
        headers = {'User-Agent' : 'Mozilla/5.0'}
        #our user agent prevents some 403 errors
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
        if ("http://" in message or "https://" in message 
            and not (message.startswith(".shorten"))):
            if not event.target() in self.silentChannels:
                messageList = message.split(' ')
                for element in messageList:
                    if element.startswith(("http://","https://"), ):
                        for regex in self.noFetchRegexes:
                            if search(regex, element):
                                element = ""
                        else:
                            thread.start_new_thread(self.sayWebpageTitle, (element,event, connection))
