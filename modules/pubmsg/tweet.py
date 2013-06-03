import irclib
import urllib
import BeautifulSoup
import HTMLParser
import thread
class tweet:
    def getTweets(self, username, number):
        try:
            url = "https://api.twitter.com/1/statuses/user_timeline.xml?screen_name=" + username + "&count=" + str(number)
            page = urllib.urlopen(url)
            soup = BeautifulSoup.BeautifulSoup(page.read())
            tweets = soup.findAll('text')
            if len(tweets) == 0:
                return "No tweets found on this page."
            else:
                return (HTMLParser.HTMLParser().unescape(tweets[-1].text)).encode('utf-8')
                #gets the nth tweet from the user's page
        except:
            return "Error retrieving that user's tweets. Perhaps the account is suspended?"
            # accounts for a 401 error
    
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".tweet"):
            if len(message.split(' ')) == 1:
                username = event.source().split('!')[0]
                    #uses nick as Twitter username
            else:
                username = message.split(' ')[1]
            try:
                thread.start_new_thread(connection.privmsg, (event.target(), self.getTweets(username, int(message.split(' ')[2]))))
                    #tries to get the nth tweet
            except Exception:
                thread.start_new_thread(connection.privmsg, (event.target(), self.getTweets(username, 1)))
                    #if n is not specified, we get the first tweet
