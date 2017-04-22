import irc
import json
import ntplib
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import thread


class ChannelMessager(StreamListener):
    def setup(self, silentChannels, accounts, connection, parent):
        self.silentChannels = silentChannels
        self.accounts = accounts
        self.connection = connection
        self.parent = parent

    def on_data(self, data):
        tweet = json.loads(data)
        try:
            if tweet['created_at']:
                #we have a real tweet
                user = tweet['user']['screen_name']
                if not user in self.accounts:
                    return
                text = tweet['text']
                message = "@" + user + ": " + text
                for channel in self.parent.getChannels():
                    if not channel in self.silentChannels:
                        self.connection.privmsg(channel, message)
                        
        except:
            return
            
        return True
    def on_error(self, status_code):
        sleep(15)
        return False
    #wait 15 seconds before doing anything in case we are rate-limited


class monitortwitter:
    def monitor(self, parent, connection):
        ntpclient = ntplib.NTPClient()
        silentChannelsFile = open("./modules/static/NOTWEETCHANNELS", 'r')
        accountsToMonitorFile = open("./modules/static/TWITTERACCOUNTS", 'r')
        self.silentChannels = silentChannelsFile.read().splitlines()
        self.accounts = accountsToMonitorFile.read().splitlines()
        silentChannelsFile.close()
        accountsToMonitorFile.close()
        cm = ChannelMessager()
        cm.setup(self.silentChannels, self.accounts, connection, parent)
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
        auth = OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessKey, accessSecret)
        while True:
            stream = Stream(auth, cm, timeout=60)
            try:
                stream.userstream(_with='followings')
            except:
                print "Error, restarting stream"
            
    def __init__(self, parent,  connection):
        thread.start_new_thread(self.monitor, (parent, connection))


                
                
    
        
        
        
