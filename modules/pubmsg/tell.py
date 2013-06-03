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
            destNick = message.lstrip(".tell ").split(' ')[0]
            self.tellDict[destNick] = sourceNick + ":" + message[6 + len(destNick):]

        elif event.source().split('!')[0] in self.tellDict:
            sourceNick = event.source().split('!')[0]
            thread.start_new_thread(connection.privmsg, (sourceNick, self.tellDict[sourceNick]))
            del self.tellDict[sourceNick]
