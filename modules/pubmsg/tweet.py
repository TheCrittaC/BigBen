import irc
import urllib
import json
import thread
import oauth2 as oauth
import HTMLParser
class tweet:
    def __init__(self):
        keyFile = open("modules/pubmsg/TwitterKeys", 'r')
        keyList = keyFile.read().splitlines()
        keyFile.close()
        for entry in keyList:
            if entry.startswith('#'):
                keyList.remove(entry)
        consumerKey = keyList[0]
        consumerSecret = keyList[1]
        accessKey = keyList[2]
        accessSecret = keyList[3]
        consumer = oauth.Consumer(key = consumerKey, secret = consumerSecret)
        accessToken = oauth.Token(key = accessKey, secret = accessSecret)
        self.client = oauth.Client(consumer, accessToken)
        
    def getTweets(self, username, number):
        try:
            url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&count=" + str(number) + "&exclude_replies=true"
            response, data = self.client.request(url)
            tweetData = json.loads(data)[-1]
            if not tweetData['text']:
                return "No tweets found on this page."
            tweet = tweetData['text']
            tweet = tweet.replace('\r', ' ').replace('\n', ' ')
            name = tweetData['user']['name']
            handle = tweetData['user']['screen_name']
            time = tweetData['created_at'][:10]
            tweet = (u"{0} :: @{1} :: {2} :: {3}".format(name, handle, time, tweet))
            return HTMLParser.HTMLParser().unescape(tweet).encode('utf-8')
                #gets the nth tweet from the user's page
        except:
            return "Error retrieving that user's tweets. Perhaps the account is suspended?"
            # accounts for a 401 error
        
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments[0]
        source = event.source.split('!')[0]
        if message.startswith(".tweet"):
            if len(message.split(' ')) == 1:
                username = event.source.split('!')[0]
                    #uses nick as Twitter username
            else:
                username = message.split(' ')[1]
            try:
                thread.start_new_thread(connection.privmsg, (event.target, self.getTweets(username, int(message.split(' ')[2]))))
                    #tries to get the nth tweet
            except Exception:
                thread.start_new_thread(connection.privmsg, (event.target, self.getTweets(username, 1)))
                    #if n is not specified, we get the first tweet
