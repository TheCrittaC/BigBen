import irclib
from urllib import urlopen
import thread
import json
class urban:
    def urban(self, term, number):
        try:
            url = "http://api.urbandictionary.com/v0/define?term=" + term
            content = json.load(urlopen(url))
            if len(content['list']) == 0:
                return "No definitions found for " + term + "."
            elif len(content['list']) < number:
                return "There are only " + str(len(content['list'])) + " definitions available."
            else:
                return content['list'][number]['definition'][:512]
        except Exception:
            return "Error retrieving definition for the term " + term + "."
            
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".urban"):
            if len(message.split(' ')) == 2:
                term = message.split(' ')[1]
                defnum = 1
                thread.start_new_thread(connection.privmsg, (event.target(), self.urban(term, defnum - 1)))
                #accounts for the special case of the term being a number
            else:
                try:
                    try:
                        defnum = int(message.split(' ')[-1])
                    except:
                        defnum = 1
                    term = message.replace(".urban ", "").replace(" " + str(defnum), "")
                    thread.start_new_thread(connection.privmsg, (event.target(), self.urban(term, defnum - 1)))
                except Exception:
                    thread.start_new_thread(connection.privmsg, (event.target(), "Usage: .urban word (definition number)"))
