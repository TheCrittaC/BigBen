import irclib
import thread
class tell:
    def __init__(self):
        self.tellDict = dict()
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".tell"):
            sourceNick = event.source().split('!')[0]
            destNick = message[6:].split(' ')[0].upper()
            #we convert everything to uppercase so, for the purpose
            #of this bot, the nicks are case insensitive 
            if not destNick in self.tellDict:
                self.tellDict[destNick] = []
            self.tellDict[destNick].append(sourceNick + ":" + message[6 + len(destNick):])

        elif event.source().split('!')[0].upper() in self.tellDict:
            sourceNick = event.source().split('!')[0]
            for message in self.tellDict[sourceNick.upper()]:
                connection.privmsg(sourceNick, message)
            del self.tellDict[sourceNick.upper()]
