import urllib
import irclib
class isup:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
	
	url = message[6:]

	if message.startswith(".isup") and 'http://' not in url and 'https://' not in url:
		url = 'http://' + url
		try:
			urllib.urlopen(url, proxies=None)
			connection.privmsg(event.target(), source + ": " + url + " seems to be up")
		except:
			connection.privmsg(event.target(), source + ": " + url + " seems to be down")
	
	elif message.startswith(".isup"):
		try:
			urllib.urlopen(url, proxies=None)
			connection.privmsg(event.target(), source + ": " + url + " seems to be up")
		except:
			connection.privmsg(event.target(), source + ": " + url + " seems to be down")
