import irclib
from urllib import urlopen
import json
import os
class weather:
    def __init__(self):
        self.key = "cloudBurst"
        if not os.path.exists("modules/pubmsg/userlocations"):
            open("modules/pubmsg/userlocations", 'w').close()
        self.locationsDict = dict()
        self.getLocations()

    def getLocations(self):
        locationsfile = open("modules/pubmsg/userlocations", 'r')
        locationslist = locationsfile.read().splitlines()
        for line in locationslist:
            self.locationsDict[line.split(" = ")[0]] = line.split(" = ")[1]
        locationsfile.close()

    def getWeather(self, location, connection, event):
        try:
            content = json.load(urlopen("http://apidev.accuweather.com/locations/v1/search?q="
                                + location + "&apikey=" + self.key))
            locationKey = content[0]["Key"]
            name = content[0]["LocalizedName"]
            country = content[0]["Country"]["LocalizedName"]
            weatherJSON = json.load(urlopen
                    ("http://apidev.accuweather.com/currentconditions/v1/" +
                locationKey + ".json?language=en&apikey=" + self.key))
            if country == "United States" or country == "Canada":
                area = content[0]["AdministrativeArea"]["EnglishName"] + ", "
            else:
                area = ""
            location = name + ", " + area + country
            weather = "Conditions: " + weatherJSON[0]["WeatherText"]
            temp = ("Temperature: " + str(weatherJSON[0]["Temperature"]["Metric"]["Value"]) + " C / " +
            str(weatherJSON[0]["Temperature"]["Imperial"]["Value"]) + " F")
            connection.privmsg(event.target(), location + " :: " + weather + " :: " + temp)
        except:
            connection.privmsg(event.target(), "Invalid location.")
       
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message == ".w" or message == ".w ":
            if not source in self.locationsDict:
                connection.privmsg(event.target(),
                "To register your location, say .register_location LOCATION")
            else:
                location = self.locationsDict[source]
                self.getWeather(location, connection, event)
                
        elif message.startswith(".w "):
            location = message[3:]
            self.getWeather(location, connection, event)
          
        elif message.startswith(".register_location "):
            ircnick = source
            location = message[19:]
            self.locationsDict[ircnick] = location
            locationsfile = open("modules/pubmsg/userlocations", 'w')
            for key in self.locationsDict:
                writenick = '{0} = {1}\n'.format(key, self.locationsDict[key])
                locationsfile.write(writenick)
            locationsfile.close()
            connection.privmsg(event.target(), "Set location to " +
                               location)
