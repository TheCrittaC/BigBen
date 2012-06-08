BigBen
======

A simple IRC bot that will chime off the number of BONGs at the top of the hour.

USAGE: ./BigBenBot <network[:port]> <#channel> <nickname> <password> <ircname>

This will cause the bot to connect to the given network, assume the given
nickname and ircname, identify with nickserv using the given password, and join
the given channel.

At the top of the hour, the bot will chime off the same number of BONGs that Big
Ben does. Thus the bot is set to GMT.

The bot is set to check for a change in the hour once per second, in order to
greatly reduce CPU strain.

If the phrase ".time" is said in the channel, the bot will tell what time it is,
using the phrase "OI IT'S X BONG", where X is the number of BONGs said at the
top of the hour.
The same thing happens if the message ".time" is messaged to the bot privately.

If kicked, the bot will reconnect after 10 seconds have passed.