import irclib
import urllib
import json
import HTMLParser
import thread
import os
import urllib
class google:
    def __init__(self):
        if not os.path.exists("modules/pubmsg/bad_googlers"):
            open("modules/pubmsg/bad_googlers", 'w').close()
            #creates bad googlers file if it does not exist
        badGooglersFile = open("modules/pubmsg/bad_googlers", 'r')
        self.badGooglers = badGooglersFile.read().splitlines()
        
    def Gsearch(self, query, connection, event):
            parser = HTMLParser.HTMLParser()
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + query
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = json.loads(search_results)
            data = results['responseData']
            hits = data['results']
            try:
                url_1 = parser.unescape(hits[0]['url'])
                title_1 = parser.unescape(hits[0]["titleNoFormatting"])
                connection.privmsg(event.target(), (u"{0} :: {1}").format(title_1, urllib.unquote(url_1)).encode('utf-8'))
            except:
                connection.privmsg(event.target(), ("Error: No results found"))
            try:
                url_2 = parser.unescape(hits[1]['url'])
                title_2 = parser.unescape(hits[1]['titleNoFormatting'])
                connection.privmsg(event.target(), (u"{0} :: {1}").format(title_2, urllib.unquote(url_2)).encode('utf-8'))
            except:
                return
            
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        query = ""
        if message.startswith(".g") and source not in self.badGooglers:
            query = message[3:]
            self.Gsearch(query, connection, event)
