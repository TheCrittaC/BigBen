import irclib
import urllib
import BeautifulSoup
import HTMLParser
import thread
class tz:
    def tz(self, location, connection, event):
		url = "http://api.worldweatheronline.com/free/v1/tz.ashx?q=" + location + "&format=xml&key=s8z5mpga43gb6th7nx7k5njq"
		page = urllib.urlopen(url)
		soup = BeautifulSoup.BeautifulSoup(page.read())
		for node in soup.findAll('query', limit=1):
			query = ''.join(node.findAll(text=True))
		for node in soup.findAll('localtime', limit=1):
			localtime = ''.join(node.findAll(text=True))
			localtime = localtime[-5:]
		try:
			connection.privmsg(event.target(), (u"Local time in {0}: {1}".format(query, localtime,))).encode('utf-8')
		except:
			return
		
    def on_pubmsg(self, nick, connection, event):
		message = event.arguments()[0]
		source = event.source().split('!')[0]
		location = ""
		if message.startswith(".tz"):
			location = message[4:]
			self.tz(location, connection, event)
