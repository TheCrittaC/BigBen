import irclib
from urllib import urlopen
import json
import os
import traceback
class weather:
    def __init__(self):
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

    def kelvinToFahrenheit(self, kelvin):
        return str((kelvin - 273.15) * 1.8 + 32)

    def kelvinToCelsius(self, kelvin):
        return str(kelvin - 273.15)

    def getWeather(self, location, connection, event):
        try:
            content = json.load(urlopen(
                "http://api.openweathermap.org/data/2.1/find/name?q=" + location))
            city = content['list'][0]['name']
            country = content['list'][0]['sys']['country']
            weather = content['list'][0]['weather'][0]['main']
            location = city + ", " +  country
            kelvinTemp = int(content['list'][0]['main']['temp'])
            temp = ("Temperature: " + self.kelvinToCelsius(kelvinTemp)  + " C / " +
                    self.kelvinToFahrenheit(kelvinTemp) + " F")
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
