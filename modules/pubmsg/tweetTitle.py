import irc
import urllib
import json
import thread
import oauth2 as oauth
import HTMLParser
import re
class tweetTitle:
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
        
    def getTweet(self, tweetId):
        url = "https://api.twitter.com/1.1/statuses/show.json?id=" + str(tweetId)
        response, data = self.client.request(url)
        tweetData = json.loads(data)
        return tweetData

    def on_pubmsg(self, nick, connection, event):
        message = event.arguments[0]
        source = event.source.split('!')[0]
        for tweetURL in (re.findall('http[s:/]+.twitter.com.[a-zA-Z]+.status.[0-9]*', message)):
            #get all the tweet URLs
            tweetId = re.search('[0-9]+', tweetURL).group()
            tweet = self.getTweet(tweetId)
            try:
                accountName = tweet['user']['name']
                tweetText = tweet['text']
                connection.privmsg(event.target, accountName + ": " + tweetText)
            except KeyError:
                connection.privmsg(event.target, "Unable to find tweet.")
                
