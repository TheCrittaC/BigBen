import irclib
import urllib
import BeautifulSoup
import HTMLParser
import thread
import os
import sys
class nowplaying:
    def __init__(self):
        if not os.path.exists("modules/pubmsg/lastfmprofile"):
            open("modules/pubmsg/lastfmprofile", 'w').close()
        self.nickDict = dict()
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.getUsernames()
        
    def getUsernames(self):
        nickfile = open("modules/pubmsg/lastfmprofile", 'r')
        nicklist = nickfile.read().splitlines()
        for line in nicklist:
            self.nickDict[line.split()[0]] = line.split()[1]
        nickfile.close()

    #creates the file if it does not exist
    def getLastfm(self, username):
        try:
            url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + username + "&api_key=e18f4688abaae4639472aaed54fe58bf"
            page = urllib.urlopen(url)
            soup = BeautifulSoup.BeautifulSoup(page.read(), fromEncoding = 'utf-8')
            for node in soup.findAll('artist', limit=1):
                artist = ''.join(node.findAll(text=True))
            for node in soup.findAll('name', limit=1):
                name = ''.join(node.findAll(text=True))
            for node in soup.findAll('album', limit=1):
                album = ''.join(node.findAll(text=True))
            for node in soup.findAll('track', limit=1):
                attrs = dict(node.attrs)
                try:
                    attrs['nowplaying']
                    prepend = 'Now playing:'
                except:
                    prepend = 'Last played:'
            if len(artist) == 0:
                return "No tracks found for this user"
            return (HTMLParser.HTMLParser().unescape("{0} {1} - {2} on {3}".format(prepend, artist, name, album)))
            #gets the last track from the user's page
        except:
            return "No tracks found or user does not exist"
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        username = ""
        if message.startswith(".np"):
            messagenew = message[4:]
            if messagenew.startswith("set "):
                lastfmprofile = messagenew[4:]
                ircnick = event.source().split('!')[0]
                self.nickDict[ircnick] = lastfmprofile
                nickfile = open("modules/pubmsg/lastfmprofile", 'w')
                for key in self.nickDict:
                    writenick = '{0} {1}\n'.format(key, self.nickDict[key])
                    nickfile.write(writenick)
                connection.privmsg(event.target(), "Set last.fm username to " + lastfmprofile)
            elif len(message.split(' ')) == 1:
                try:
                    username = self.nickDict[source]
                except:
                    username = source
                thread.start_new_thread(connection.privmsg, (event.target(), self.getLastfm(username)))
            else:
                username = messagenew
                thread.start_new_thread(connection.privmsg, (event.target(), self.getLastfm(username)))
            
