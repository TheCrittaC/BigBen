import irclib
import urllib
import BeautifulSoup
class shorten:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
	if message.startswith(".shorten"):
		try:
			url = "http://is.gd/create.php?format=simple&url=" + message[9:]
			open_Url = urllib.urlopen(url)
			read_Content = str(BeautifulSoup.BeautifulSoup(open_Url.read()))
			connection.privmsg(event.target(), "Shortened url: " + read_Content)
		except:
			connection.privmsg(event.target(), "Invalid url")