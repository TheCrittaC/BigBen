import irclib
import urllib2
import json
import thread
import oauth2 as oauth
import HTMLParser
class stock:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="
                
    def getQuote(self, symbol):
        url = self.prefix + symbol
        u = urllib2.urlopen(url) 
        content = u.read() 
        quote = json.loads(content[3:])[0]
        if not quote:
            return "Error getting quote for " + symbol + "."
        stockSymbol = quote['t']
        last = quote['l']
        change = quote['c']
        percent = quote['cp']
        if change.startswith("+"):
            percent = "+" + percent
        quoteString = (u"{0} : {1} ({2} {3}%)".format(stockSymbol, last, change, percent))
        return quoteString

        
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".stock"):
            if len(message.split(' ')) == 1:
                symbol = event.source().split('!')[0]
                    #uses nick as Twitter username
            else:
                symbol = message.split(' ')[1]
            try:
                thread.start_new_thread(connection.privmsg, (event.target(), self.getQuote(symbol)))
                    #tries to get the nth tweet
            except Exception:
                print (traceback.format_exc())
                thread.start_new_thread(connection.privmsg, (event.target(), "Error getting quote for " + symbol + "."))
                    #if n is not specified, we get the first tweet
