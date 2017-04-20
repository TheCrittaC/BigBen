import irc
import ntplib
from time import ctime
from datetime import datetime
import thread
from time import sleep
from re import sub, search
import traceback

class bong:
    def getTime(self, ntpclient, ntpserver):
        response = ntpclient.request(ntpserver)
        return datetime.fromtimestamp(response.orig_time)
    def __init__(self, parent,  connection):
        ntpclient = ntplib.NTPClient()
        silentChannelsFile = open("./modules/static/NOBONGCHANNELS", 'r')
        self.silentChannels = silentChannelsFile.read().splitlines()
        silentChannelsFile.close()
        while 1:
            currentTime = self.getTime(ntpclient, "pool.ntp.org")
            currentHour = int(currentTime.strftime("%I"))
            #12-hour current hour
            currentMin = int(currentTime.strftime("%M"))
            currentSec = int(currentTime.strftime("%S"))
            secondsToSleep = 3600 - (currentMin * 60) - currentSec
            sleep(secondsToSleep)
            currentHour = currentHour + 1
            message = ""
            for i in range(currentHour):
                message += "BONG "
            for channel in parent.getChannels():
                if not channel in self.silentChannels:
                    connection.privmsg(channel, message)
            message = ""

        


        
