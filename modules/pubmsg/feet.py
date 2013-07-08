import irclib
import urllib
import BeautifulSoup
class feet:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]

	if message.startswith(".feet"):
			message = message[6:]
			name = message
			message = message.replace(" ", "_")
			url = "http://www.wikifeet.com/" + message.title()
			page = urllib.urlopen(url)
			if page.getcode() == 200:
				soup = str(BeautifulSoup.BeautifulSoup(page.read()))
				response = name.title() + "'s feet << wikiFeet :: " + url
				connection.privmsg(event.target(), response)
			else:
				connection.privmsg(event.target(), "Found nothing")