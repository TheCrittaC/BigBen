import irclib
import urllib
import BeautifulSoup
import HTMLParser
import thread
class urban:
    def urban(self, term, number):
        try:
            url = "http://www.urbandictionary.com/define.php?term=" + term
            page = urllib.urlopen(url)
            soup = BeautifulSoup.BeautifulSoup(page.read())
            definitions = soup.findAll("div", {"class": "definition"})
            if len(definitions) == 0:
                return "No definitions found on this page."
            elif len(definitions) < number:
                return "There are only " + str(len(definitions)) + " definitions on this page."
            else:
                return (HTMLParser.HTMLParser().unescape(definitions[number -1].text)).encode('utf-8')
        except Exception:
            return "Error retrieving definition for the term " + term + "."
            
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".urban"):
            if len(message.split(' ')) == 2:
                term = message.split(' ')[1]
                defnum = 1
                thread.start_new_thread(connection.privmsg, (event.target(), self.urban(term, defnum)))
                #accounts for the special case of the term being a number
            else:
                try:
                    try:
                        defnum = int(message.split(' ')[-1])
                    except:
                        defnum = 1
                    term = message.replace(".urban ", "").replace(" " + str(defnum), "")
                    thread.start_new_thread(connection.privmsg, (event.target(), self.urban(term, defnum)))
                except Exception:
                    thread.start_new_thread(connection.privmsg, (event.target(), "Usage: .urban word (definition number)"))
