import urllib2
from xml.dom import minidom
import re
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
            connection.privmsg(event.target(), message)

    def getVideo(self, keyword):
        url = 'https://gdata.youtube.com/feeds/api/videos?q={0}&max-results=1&v=2'.format(keyword)
        xmldoc = minidom.parse(urllib2.urlopen(url))
        title = xmldoc.getElementsByTagName('title')
        url = xmldoc.getElementsByTagName('media:player')
        title = title[1].toxml()
        title = re.sub('<[^>]*>', '', title)
        url = url[0].attributes['url'].value
        url = re.sub('&feature.+', '', url)
        message = u"\u00031,00You\u000300,5Tube\u000300,1 {0} - {1}".format(title, url)
        return message
