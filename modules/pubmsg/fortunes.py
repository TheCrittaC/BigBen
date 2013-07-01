import random
class fortunes:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]

	if message.startswith(".fortune"):
		fortunestxt = open("modules/pubmsg/fortunes", 'r')
		fortuneslist = fortunestxt.read().splitlines()
		response = random.choice(fortuneslist)
		connection.privmsg(event.target(), response)

