import irclib
import urllib
import urllib2
import BeautifulSoup
import HTMLParser
import thread
from re import sub
from re import search
class youtube:
    def on_pubmsg(self, nick, connection, event):   
        message = event.arguments()[0]
        username= event.source().split('!')[0]
        try:
            arg1 = message.split('.yt ')[1]
        except IndexError:
            return 1
        if message.startswith(".yt"):
            arg1 = arg1.replace(" ", "+")
            message = self.getVideo(arg1)
            try:
                connection.privmsg(event.target(), message)
            except:
                connection.privmsg(event.target(), "Nothing found")
    def getContentType(self, url):
        headers = urllib2.urlopen(url)
        return headers.headers['content-type']
                
    def getVideo(self, keyword):
        url = 'https://www.youtube.com/results?search_query={0}'.format(keyword)
        headers = {'User-Agent' : 'Mozilla/5.0'}
        #our user agent prevents some 403 errors
        req = urllib2.Request(url, '', headers)
        if not self.getContentType(url).startswith("text/html"):
            return
        try:
            youtubePage = BeautifulSoup.BeautifulSoup(urllib2.urlopen(req).read())
        except:
            return
        try:
            relevantDiv = youtubePage.findAll("div", { "class" : "yt-lockup-content" })[0]
        except IndexError:
            message = "No video found."
            return message
        title = relevantDiv.h3.a['title']
        link = 'https://www.youtube.com/{0}'.format(relevantDiv.h3.a['href'])
        message = u"\u00031,00You\u000300,5Tube\u0003 {0} - {1}".format(title, link)
        return message
