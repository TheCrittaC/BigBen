import irclib
from urllib import urlopen
import json
import os
import time
class weather:
    def __init__(self):
        if not os.path.exists("modules/pubmsg/userlocations"):
            open("modules/pubmsg/userlocations", 'w').close()
        self.locationsDict = dict()
        keyFile = open("modules/pubmsg/weatherKey", 'r')
        self.key = keyFile.read().splitlines()[0]
        keyFile.close()
        self.getLocations()

    def dayofweek(self, day):
        if day == 0:
            return "Mon"
        elif day == 1:
            return "Tue"
        elif day == 2:
            return "Wed"
        elif day == 3:
            return "Thu"
        elif day == 4:
            return "Fri"
        elif day == 5:
            return "Sat"
        elif day == 6:
            return "Sun"
        else:
            return "Invalid argument."
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

    def forecast(self, info, day):
        today = info['forecast']['simpleforecast']['forecastday'][day]
        day = today['date']['weekday_short']
        conditions = today['conditions']
        highc = today['high']['celsius'] + " C"
        highf = today['high']['fahrenheit'] + " F"
        return "%s: %s %s / %s" % (day, conditions, highc, highf)

    def getForecast(self, location, connection, event):
        url = "http://api.wunderground.com/api/"
        try:
            info = "%s/%s/forecast/q/%s.json" % (url, self.key, location)
            content = json.load(urlopen(info))
            if content['response'].has_key('results'):
                realLocation = content['response']['results'][-1]['l'][3:]
                self.getForecast(realLocation, connection, event)
            else:
                conditions = "%s/%s/conditions/q/%s.json" % (url, self.key, location)
                areainfo = json.load(urlopen(conditions))
                area = areainfo['current_observation']['display_location']['full']
                dayZero = self.forecast(content, 0)
                dayOne = self.forecast(content, 1)
                dayTwo = self.forecast(content, 2)
                wunderground = "Weather Underground :: http://www.wunderground.com"
                forecastString = "%s: %s %s %s :: %s" % (area, dayZero, dayOne, dayTwo, wunderground)
                connection.privmsg(event.target(), forecastString)
        except:
            self.openForecast(location, connection, event)


                
    def getWeather(self, location, connection, event):
        url = "http://api.wunderground.com/api/"
        try:
            info = "%s/%s/conditions/q/%s.json" % (url, self.key, location)
            content = json.load(urlopen(info))
            if content['response'].has_key('results'):
                realLocation = content['response']['results'][-1]['l'][3:]
                self.getWeather(realLocation, connection, event)
            else:
                area = content['current_observation']['display_location']['full']
                weather = content['current_observation']['weather']
                tempf = str(content['current_observation']['temp_f'])
                tempc = str(content['current_observation']['temp_c'])
                temp = ("Temperature: " + tempc  + " C / " +
                    tempf + " F")
                connection.privmsg(event.target(), area + " :: " + weather + " :: " + temp +
                               " :: Weather Underground :: http://www.wunderground.com")
        except:
            self.openWeather(location, connection, event)

    def openForecast(self, location, connection, event):
        try:
            locationData  = json.load(urlopen(
                "http://api.openweathermap.org/data/2.1/find/name?q="
                + location))
            cityID = str(locationData['list'][0]['id'])
            city = locationData['list'][0]['name']
            country = locationData['list'][0]['sys']['country']
            location = city + ", " +  country
            content = json.load(urlopen(
                "http://api.openweathermap.org/data/2.5/forecast?id="
                + cityID))
            days = []
            weather = []
            highc = []
            highf = []
            for i in range(3):
                days.append(self.dayofweek(time.localtime().tm_wday + i))
                weather.append(content['list'][i]['weather'][0]['main'])
                kelvinTemp = int(content['list'][i]['main']['temp_max'])
                highc.append(self.kelvinToCelsius(kelvinTemp))
                highf.append(self.kelvinToFahrenheit(kelvinTemp))
            forecastString = location + ": "
            for i in range (3):
                appendMe = "%s: %s %s C / %s F " % (days[i], weather[i], highc[i], highf[i])
                forecastString = forecastString + appendMe
            connection.privmsg(event.target(), forecastString)
        except:
            connection.privmsg(event.target(), "Invalid location.")
            
                
            
    def openWeather(self, location, connection, event):
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

        if message == ".f" or message == ".f ":
            if not source in self.locationsDict:
                connection.privmsg(event.target(),
                "To register your location, say .register_location LOCATION")
            else:
                location = self.locationsDict[source]
                self.getForecast(location, connection, event)

        elif message.startswith(".f "):
            location = message[3:]
            self.openForecast(location, connection, event)
          
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
