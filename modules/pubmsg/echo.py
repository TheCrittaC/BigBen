import irclib
class echo:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".echo "):
            connection.privmsg(event.target(), message[6:])
