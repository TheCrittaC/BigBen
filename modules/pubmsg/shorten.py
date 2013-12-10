import irclib
import urllib
import BeautifulSoup
import re

class shorten:
    def __init__(self):
	self.messageList = []
	self.lastUrls = []

    def shortenURL(self, url):
	returnMessage = ""
	try:
		open_Url = urllib.urlopen("http://is.gd/create.php?format=simple&url=" + url)
		read_Content = str(BeautifulSoup.BeautifulSoup(open_Url.read()))
		returnMessage= "Shortened url: " + read_Content
	except:
		returnMessage = "Invalid url"
	return returnMessage

    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
	if message == ".shorten":
		if(len(self.lastUrls)>0):
			connection.privmsg(event.target(), self.shortenURL(self.lastUrls[0]))
	elif message.startswith(".shorten"):
		url = message[9:]
		connection.privmsg(event.target(), self.shortenURL(url))
	elif ("http://" in message or "https://" in message):
		self.lastUrls = re.findall(r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+',message)
