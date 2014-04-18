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

			#yay variables
			a = parser.unescape(ast.literal_eval(soup)["Title"])
			b = parser.unescape(ast.literal_eval(soup)["Year"])
			c = parser.unescape(ast.literal_eval(soup)["tomatoMeter"])
			d = parser.unescape(ast.literal_eval(soup)["tomatoRating"])
			e = parser.unescape(ast.literal_eval(soup)["tomatoFresh"])
			f = parser.unescape(ast.literal_eval(soup)["tomatoRotten"])
			g = parser.unescape(ast.literal_eval(soup)["tomatoConsensus"])
			h = parser.unescape(ast.literal_eval(soup)["Website"])
			i = parser.unescape(ast.literal_eval(soup)["Runtime"])


			#Remade the code to make it easier to read and change if need be
			response = "[Title: " + a + "] "
			response = response + "[Year: " + b + "] "
			response = response + "[Runtime: " + i + "] "
			response = response + "[TomatoMeter: " + c + "] "
			response = response + "[TomatoRating: " + d + "] "
			response = response + "[TomatoFresh: " + e + "] "
			response = response + "[TomatoRotten: " + f + "] "
			response = response + "[TomatoConsensus: " + g + "] "
			connection.privmsg(event.target(), response)
			#the following statement is to check if the website exists and if it does then print the website name otherwise do nothing

			if h != "N/A":
				connection.privmsg(event.target(), h)

		except:
			connection.privmsg(event.target(), "Found nothing")
