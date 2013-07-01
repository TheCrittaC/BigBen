import irclib
import urllib
import json
import HTMLParser
import thread
import os
class google:
    def Gsearch(self, query, connection, event):
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + query
            search_response = urllib.urlopen(url)
            search_results = search_response.read()
            results = json.loads(search_results)
            data = results['responseData']
            hits = data['results']
            url_1 = hits[0]['url']
            title_1 = hits[0]["titleNoFormatting"]
            url_2 = hits[1]['url']
            title_2 = hits[1]['titleNoFormatting']
            connection.privmsg(event.target(), (u"{0} :: {1}").format(title_1, url_1))
            connection.privmsg(event.target(), (u"{0} :: {1}").format(title_2, url_2))
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        query = ""
        if message.startswith(".g"):
            query = message[3:]
            thread.start_new_thread(self.Gsearch(query, connection, event))