import irclib
class htmlconvert:
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".convert"):
            try:
                color = message.split(' ')[1]
                if color.startswith("#"):
                    first = str(int(color[1:3], 16))
                    for i in range (3 - len(first)):
                        first = "0" + first
                    second = str(int(color[3:5], 16))
                    for i in range (3 - len(second)):
                        second = "0" + second
                    third = str(int(color[5:7], 16)) #gets each color
                    for i in range (3 - len(third)):
                        third = "0" + third
                    connection.privmsg(event.target(), first + "-" + second + "-" + third)
                else:
                    first = hex(int(color[0:3]))[2:]
                    if len(first) == 1:
                        first = "0" + first
                    second = hex(int(color[4:7]))[2:]
                    if len(second) == 1:
                        second = "0" + second
                    third = hex(int(color[8:11]))[2:]
                    if len(third) == 1:
                        third = "0" + third
                    connection.privmsg(event.target(), "#" + first + second + third)
            except:
                connection.privmsg(event.target(), "Invalid syntax.")
