import irclib
import urllib
import BeautifulSoup
class eat:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]

	if message.startswith(".eat"):
			message = message[5:]
			name = message
			message = message.replace(" ", "%20")
			url = "http://www.wikieat.org/people/" + message.title()
			page = urllib.urlopen(url)
			soup = str(BeautifulSoup.BeautifulSoup(page.read()))
			if "Nothing here yet" in soup:
			   	connection.privmsg(event.target(), "Found nothing")
			else:
				response = name.title() + " with food << wikiEat :: " + url
				connection.privmsg(event.target(), response)
				