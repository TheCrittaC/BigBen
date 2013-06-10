import irclib
from urllib import urlopen
import json
class weather:
    def __init__(self):
        self.key = "cloudBurst"
    def on_pubmsg(self, nick, connection, event):
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        if message.startswith(".weather"):
            try: 
                location = message[9:]
                content = json.load(urlopen("http://apidev.accuweather.com/locations/v1/search?q="
                                        + location + "&apikey=" + self.key))
                locationKey = content[0]["Key"]
                name = content[0]["LocalizedName"]
                country = content[0]["Country"]["LocalizedName"]
                weatherJSON = json.load(urlopen
                ("http://apidev.accuweather.com/currentconditions/v1/" +
                 locationKey + ".json?language=en&apikey=" + self.key))
                if country == "United States":
                    area = content[0]["AdministrativeArea"]["EnglishName"] + ", "
                #puts the state in if it is a US area
                else:
                    area = ""
                location = name + ", " + area + country
                weather = "Conditions: " + weatherJSON[0]["WeatherText"]
                temp = ("Temperature: " + str(weatherJSON[0]["Temperature"]["Metric"]["Value"]) + " C / " +
                    str(weatherJSON[0]["Temperature"]["Imperial"]["Value"]) + " F")
                connection.privmsg(event.target(), location + " :: " + weather + " :: " + temp)
            except:
                connection.privmsg(event.target(), "Invalid location.")
