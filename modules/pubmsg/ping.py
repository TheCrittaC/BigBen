import irclib
class ping:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".") and message.endswith("ing"):
            if " " not in message and ".bing" not in message: # doesn't let the bot bong or respond to commands with a space in them
                response = message[:-3] #response starts as everything but the 'ing'
                response = response + "ong"
                response = response.lstrip('.')
                connection.privmsg(event.target(), response)
