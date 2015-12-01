import irclib
from re import sub, search
pastmessages = []
class sed:
    def tokenise(self, d, s):
        l = []
        pos = s.find(d)
        while pos >= 0:
            i = 0
            while pos-i-1 >= 0 and s[pos-i-1] == '\\':
                i += 1
            if i % 2 == 0:
                l.append(s[:pos])
                s = s[pos+1:]
                pos = 0
            else:
                s = s[:pos-1] + s[pos:]
            pos = s.find(d, pos)
        l.append(s)
        return l
    
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if len(pastmessages) > 249:
            pastmessages.pop(0)
        if source != nick and not (message.startswith(":s/")):
            pastmessages.append((event.target(), source, message))
            #we don't add bot's messages or :s/ replies
        if message.startswith(":s/"):
            try:
                delimiter = message[2]
            except IndexError:
                connection.privmsg(event.target(), "Incorrect Syntax")
                return 1
            terms = self.tokenise(delimiter, message[3:])
            try:
                find = terms[0]
                replace = terms[1]
            except:
                connection.privmsg(event.target(), "Incorrect Syntax")
                return 1
            if "\\" in replace:
                connection.privmsg(event.target(), 
                                   "You don't get to send control characters.")
                return 1
            global_match = 1
            try:
                terms[2]
            except:
                pass
            else:
                for flag in terms[2]:
                    if flag == 'g' or flag == 'G':
                        global_match = 0
                    elif flag == 'i' or flag =='I':
                        find = '(?i){0}'.format(find)
            for i in range(len(pastmessages)-1,-1,-1):
                try:
                    if search(find, pastmessages[i][2]) and search(event.target(),pastmessages[i][0]):
                        fix_message = pastmessages[i]
                        break
                except Exception, err:
                    connection.privmsg(event.target(), str(err).capitalize())
                    return 1
            try:
                fix_message
            except NameError:
                connection.privmsg(event.target(), "No Match Found")
            else:
                find = r'{0}'.format(find)
                try:
                    newText = sub(find, replace, fix_message[2], global_match)
                except Exception, err:
                    connection.privmsg(event.target(), str(err).capitalize())
                    return 1
                else:
                    connection.privmsg(event.target(), fix_message[1] + ": " + newText)
