#BigBen IRC Bot

####written by [Christopher T. Lemay](http://www.thecrittac.us)
####requires python-irc and beautifulsoup

###A simple IRC bot that will chime off the number of BONGs at the top of the hour, among other things.

USAGE: ./BigBen

The first set of commands will cause the bot to connect to the given network, assume the given
nickname and ircname, identify with nickserv using the given password, and join
the given channels.

The second command will read the options from a file.

At the top of the hour, the bot will chime off the same number of BONGs that Big
Ben does. Thus the bot is set to GMT. This happens in all channels that BigBen
is in. This is done with the `bong` static module.


Many of these commands can be changed in the COMMANDS file in order to cut down on possible spam.

Nicks in the IGNORE file will be ignored. This is useful if there are other
bots in the channel that we don't want BigBen to get links from or interact with. This file
needs to end with a newline character.


The next commands listed are provided as modules for the bot. See `modules/pubmsg/test.py`
for an example module. If you would like to write a module, but are stuck, please join #BigBen
on irc.rizon.net.

If ".ping" (or any other message starting with '.' and ending with 'ing') is said in any
channel, the bot will replace 'ing' with 'ong' and respond to that same channel. This is
provided with the `ping.py` module. 

If a URL is posted in the channel, the bot will fetch its title and send it to the
channel, unless it contains a regex in the `NoTitle` file. This is provided by the
`pagetitle.py` file.

If the phrase ".tweet USERNAME" is said in the channel, the bot will fetch the
most recent tweet from that user. If a number is specified after the tweet, the
nth tweet will be fetched. This is provided with the `tweet.py` module.

If the phrase ".urban TERM (optional definition number)" is said in the channel,
the bot will fetch a definition for that term from Urban Dictionary. If a number
is not specified, the bot will fetch the first definition for that term. This is
provided with the `urban.py` module.

If the phrase ".tell NICK MESSAGE" is said in the channel, the bot will /query
the message to the given nick when that nick joins any channel the bot is in or
sends a message to any channel the bot is in. This provided with the `tell.py`
module.

If the phrase ".4chan BOARD SEARCH_TERM" is said in the channel, the bot will
search the given board on 4chan for threads that have the search term in the
original post. For example, ".4chan g desktop thread" would search /g/ for
threads that have "desktop thread" in the original post. In addition, if a
link is posted to a 4chan post, the post's content will be put in the channel.
This is provided with the `fourchan.py` module. 

If the phrase ".convert" is said in the channel with an HTML color code in
hexidecimal as an argument, it will be converted to decimal. Similarly, if
it is in decimal (e.g. 255-255-255), the bot will convert it to hexidecimal
and message it to the channel. This is provided with the `htmlconvert.py` module.

If a message in any channel starts with the bot's nick and ends with '??' (for example,
"BigBen, am I ever going to get married??"), the bot will give a random response from the
RESPONSES file. This is provided with the `question.py` module.

If the message, minus the leading nick and trailing question mark, is in the
CUSTOMRESPONSES file before the "::" in its line, the message after the "::"
will be sent to the channel. This is also provided with the `question.py` module.

The `stock.py` module retrieves a stock quote for the specified stock symbol.
This uses the Google Finance API. For example, .stock F would retrieve a stock
quote for Ford Motor Company, which has the stock symbol F.

The `weather.py` module takes a location as an argument and returns weather for
that location, using the Weather Underground API. If the weather is not
available from there, it uses the OpenWeatherMap API. The command is
".weather LOCATION"

The bot also supports modifying previous messages with a sed-like syntax. For
example:

`<TheCrittaC> aabb`
`<TheCrittaC> :s/a/b`
`<BigBen> TheCrittaC: babb`
`<TheCrittaC> :s/a/b/g`
`<BigBen> TheCrittaC: bbbb`

This is provided with the `sed.py` module.

The `nowplaying.py` module lets the bot access a user's most recently played
song on last.fm. If no arguments are specified, the user's nick is used as
the last.fm username. A user can set their username with the command
`.np set USERNAME`. A user can see what another user is playing by using the
command `.np USERNAME`.

Static modules are always running. They are not event-driven.

The `fourchanmonitor.py` module monitors 4chan for updated threads that match
a given regular expression. This is configurable via the `ThreadMonitor` file.
When a new thread is found, it is sent to the given thread along with the first
fifty characters of the original post. Currently this probably does not work.

The `bong.py` module is the bonging module. It uses NTP to get the time, then 
sends a message on the hour change. For example, if the hour were to change from
2 to 3, then the bot would say "BONG BONG BONG" to each channel that it is in. 
Channels can be excluded by putting them in the `modules/static/NOBONGCHANNELS`
file, one per line.

Some modules are not documented here, instead of documenting them, there is
interactive help in the bot. Simply say .help to get a notification from the
bot of the enabled modules and their usage.

If you would like to see the bot in action and/or talk with me and the bot, you
can join #BigBen on [Rizon](irc://irc.rizon.net).

BigBen is licensed under the terms of the GNU General Public license, version
2 or later, at the user's discretion.
