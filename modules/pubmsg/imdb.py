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
			response = "[Title: " + a + "] [Year: " + b + "] [Rating: " + c + "] [Genre: " + d + "] " + "[Description: " + e + "] " + return_url
			connection.privmsg(event.target(), response)

		except:
			connection.privmsg(event.target(), "Found nothing")
