import urllib
import irclib
import BeautifulSoup
import ast
import HTMLParser
class rt:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]

	if message.startswith(".rt"):
		try:
			message = message[4:]
			url = "http://www.omdbapi.com/?t=" + message + "&tomatoes=true"
			page = urllib.urlopen(url)
			soup = str(BeautifulSoup.BeautifulSoup(page.read()))
			parser = HTMLParser.HTMLParser()

			a = parser.unescape(ast.literal_eval(soup)["Title"])
			b = parser.unescape(ast.literal_eval(soup)["Year"])
			c = parser.unescape(ast.literal_eval(soup)["tomatoMeter"])
			d = parser.unescape(ast.literal_eval(soup)["tomatoRating"])
			e = parser.unescape(ast.literal_eval(soup)["tomatoFresh"])
			f = parser.unescape(ast.literal_eval(soup)["tomatoRotten"])
			g = parser.unescape(ast.literal_eval(soup)["tomatoConsensus"])
			h = parser.unescape(ast.literal_eval(soup)["Website"])
			response = "[Title: " + a + "] [Year: " + b + "] [TomatoMeter: " + c + "] [TomatoRating: " + d + "] " + "[TomatoFresh: " + e + "] " + "[TomatoRotten: " + f + "] " + "[TomatoConcensus: " + g + "] " + h
			connection.privmsg(event.target(), response)

		except:
			connection.privmsg(event.target(), "Found nothing")