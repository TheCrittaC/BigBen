import irclib
import time
import csv
speakfile = "speak.txt"
class lastspoke:
    def __init__(self):
        speakFileFile = open("./modules/pubmsg/SPEAKFILE", 'r')
        self.speakFile = speakFileFile.readline()
        speakFileFile.close()
    def lastSpoke(self, channel, user, message):
        theTime = time.gmtime()#does things for GMT
        theDate = "{0}-{1}-{2}".format(theTime.tm_year, theTime.tm_mon, theTime.tm_mday)
        hour = str(theTime.tm_hour+1)
        minute = str(theTime.tm_min)
        if len(hour) == 1: hour = "0"+hour
        if len(minute) == 1: minute = "0"+minute
        theTime = "{0}:{1}".format(hour, minute)
        # [0] = time
        # [1] = channel
        # [2] = user
        # [3] = message
        # [4] = date
        try:
            infile = open(self.speakFile, 'rb')
        except:
            open(self.speakFile, "w").close()
        finally:
            infile = open(self.speakFile, 'rb')
        reader = csv.reader(infile, delimiter=',')
        reader = list(reader)
        infile.close()
        
        outfile = open(self.speakFile, 'wb')
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[2] != user:
                writer.writerow(row)
        writer.writerow([theTime,channel,user,message, theDate])
        outfile.close()

    def getLastSpoke(self, channel, user, connection):
        theDate = time.gmtime()
        with open(self.speakFile, 'rb') as infile:
            reader = csv.reader(infile, delimiter=',')
            for row in reader:
                if row[2].lower() == user.lower():
                    tDate = row[4].split('-')
                    sDate = ""
                    if int(tDate[0]) < theDate.tm_year or int(tDate[1]) < theDate.tm_mon or int(tDate[2]) < theDate.tm_mday:
                        year = str(tDate[0])
                        month = str(tDate[1])
                        day = str(tDate[2])
                        if len(month) == 1: month = "0"+month
                        if len(day) == 1: day = "0"+day
                        sDate = "{0}/{1}/{2}".format(year, month, day)
                    connection.privmsg(channel, u"{0}\u00036[\u000300{1}\u00036]\u00030\u00033 {2} \u00030\u00036<\u000300{3}\u00036>\u000300 {4}".format(sDate, row[0], row[1], row[2], row[3]) )
                    return 0
        connection.privmsg(channel, "I don't think I've seen {0}".format(user))
        
    def on_pubmsg(self, nick, connection, event):
        self.connection = connection
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        self.lastSpoke(event.target(), source, message)
        if message.startswith(".seen"):
            #try:
            user = message.split(' ')[1]
            self.getLastSpoke(event.target(), user, connection)
            #except:
             #   connection.privmsg(event.target(),"To use the seen command: .seen Username")
