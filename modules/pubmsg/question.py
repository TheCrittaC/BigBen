import irclib
import random
class question:
    def __init__(self):
        customResponsesFile = open("CUSTOMRESPONSES", "r")
        self.customResponses = customResponsesFile.readlines()
        customResponsesFile.close()
        messagesFile = open("RESPONSES", 'r')
        self.responses = messagesFile.readlines()
        messagesFile.close()

    def magicConch(self):
        lines = len(self.responses)
        lineNum = random.randint(0, lines - 1)
        return self.responses[lineNum - 1].rstrip('\n')
    
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        custom = 0
        if message.startswith(nick) and message.endswith("??"):
            for e in self.customResponses:
                if message.lstrip(nick).lstrip(",: ").rstrip(" ??") == e.split("::")[0]:
                    connection.privmsg(event.target(), e.split("::")[1])
                    custom = 1 # tells the bot we have a custom reply
            if custom == 0: # if we have not had a custom reply
                connection.privmsg(event.target(), self.magicConch())
            custom = 0 # resets the custom reply
