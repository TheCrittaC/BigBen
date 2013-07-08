import urllib
import irclib
import BeautifulSoup
import ast
class imdb:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]

	if message.startswith(".imdb"):
		try:
			message = message[6:]
			url = "http://www.omdbapi.com/?t=" + message
			page = urllib.urlopen(url)
			soup = str(BeautifulSoup.BeautifulSoup(page.read()))

			a = ast.literal_eval(soup)["Title"]
			b = ast.literal_eval(soup)["Year"]
			c = ast.literal_eval(soup)["imdbRating"]
			d = ast.literal_eval(soup)["Genre"]
			e = ast.literal_eval(soup)["Plot"]
			f = ast.literal_eval(soup)["imdbID"]
			return_url = "www.imdb.com/title/" + f
			g = ast.literal_eval(soup)["Actors"]
			h = ast.literal_eval(soup)["Runtime"]

			response = "[Title: " + a + "] "
			response = response + "[Year: " + b + "] "
			response = response + "[Rating: " + c + "] "
			response = response + "[Runtime: " + h + "] "
			response = response + "[Genre: " + d + "] "
			response = response + "[Actors: " + g + "] "
			response = response + "[Plot: " + e + "] "

			connection.privmsg(event.target(), response)
			connection.privmsg(event.target(), return_url)

		except:
			connection.privmsg(event.target(), "Found nothing")
