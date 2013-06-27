import irclib
import random
class decide:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
		
	if message.startswith(".decide"):
		try:
			choices = message[8:].split(' or ')
			choices = [a for a in choices if a != 'or']
			response = random.choice(choices)
			connection.privmsg(event.target(), source + ": " + str(response))
		except:
			connection.privmsg(event.target(), "Invalid choices")
			
	if message.startswith(".flip"):
		try:
			choices = ['Heads', 'Tails']
			try:
					amount = int(message[6:])
					#connection.privmsg(event.targer(), amount)
					heads, tails = 0, 0
					for i in range(amount):
							if random.choice(choices) == 'Heads':
									heads += 1
							else:
									tails += 1
					response = 'Heads: {} Tails: {}'.format(heads, tails)
			except ValueError:
				response = random.choice(choices)
			connection.privmsg(event.target(), source + ": " + str(response))
		except:
			connection.privmsg(event.target(), "Invalid choices")