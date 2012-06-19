BigBen

written by Christopher T. Lemay
requires python-irclib
===============================


A simple IRC bot that will chime off the number of BONGs at the top of the hour.

USAGE: ./BigBenBot <network[:port]> <#channel1 #channel2> <nickname> <password> <ircname>

This will cause the bot to connect to the given network, assume the given
nickname and ircname, identify with nickserv using the given password, and join
the given channels.

At the top of the hour, the bot will chime off the same number of BONGs that Big
Ben does. Thus the bot is set to GMT. This happens in all channels that BigBen
is in.

The bot is set to check for a change in the hour once per second, in order to
greatly reduce CPU strain.

If the phrase ".time" is said in the channel, the bot will tell what time it is,
using the phrase "OI IT'S X BONG", where X is the number of BONGs said at the
top of the hour.
The same thing happens if the message ".time #channel" is messaged to the bot privately.

If the bot receives a private message of ".speak #channel TEXT_HERE", it will
echo the text back to the channel specified.

If kicked, the bot will reconnect after 10 seconds have passed.

BigBen is licensed under the terms of the GNU General Public license, version
2 or later, at the user's discretion.
