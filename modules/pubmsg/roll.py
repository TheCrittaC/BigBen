import irclib
import random
class roll:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".roll"):
            splitRoll = message.split(' ')
            try:
                if len(splitRoll) == 3:
                    min = int(splitRoll[1])
                    max = int(splitRoll[2])
                elif len(splitRoll) == 2:
				min = 1
				max = int(splitRoll[1])
                elif len(splitRoll) == 1:
                    min = 1
                    max = 6
                response = random.randint(min, max) #gets the random number init
                connection.privmsg(event.target(), source + " rolled a " +str(response))
            except:
                connection.privmsg(event.target(), "Invalid number format.")
                    #prints the error init