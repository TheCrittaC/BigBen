import irclib
import random
class quote:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]

	# Retrieve stored quote
	if message.startswith(".quote"):
		words = message.split()
		targetQuotes = []
		if len(words) == 2:
			quotesFile = open("modules/pubmsg/quotes", 'r')
			quotesList = quotesFile.read().splitlines()
			for quoteLine in quotesList:
				if quoteLine.startswith(words[1]):
					quoteArray = quoteLine.split(",")
					targetQuotes.append("<" + quoteArray[0] + "> " + quoteArray[1])
			if len(targetQuotes) > 0:
				response = random.choice(targetQuotes)
			else:
				response = "No quotes found."
		if len(words) > 2:
			quotesFile = open("modules/pubmsg/quotes", 'a')
			newQuote = words[1] + ","
			words.pop(0)
			words.pop(0)
			actualQuote = ' '.join(words)
			newQuote = newQuote + actualQuote
			quotesFile.write(newQuote + "\n")
			response = "Quote has been added forever."
		else:
			targetQuotes = "Invalid input."
		connection.privmsg(event.target(), response)