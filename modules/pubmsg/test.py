import irclib
#place all imports up here
class test:
#the name of your class
    def __init__(self):
        #anything that needs to be initialized goes here
    def on_pubmsg(self, nick, connection, event):
        #all things that happen when the event is called go here
        connection.privmsg(event.target(), "test")
        #this class just sends the string "test" to the channel the message was in
