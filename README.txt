BigBen

written by Christopher T. Lemay
requires python-irclib
===============================


A simple IRC bot that will chime off the number of BONGs at the top of the hour.

USAGE: ./BigBen <network[:port]> <#channel1 #channel2> <nickname> <password> <ircname>

OR
./BigBen -c

The first set of commands will cause the bot to connect to the given network, assume the given
nickname and ircname, identify with nickserv using the given password, and join
the given channels.

The second command will read the options from a file.

At the top of the hour, the bot will chime off the same number of BONGs that Big
Ben does. Thus the bot is set to GMT. This happens in all channels that BigBen
is in.

The bot is set to check for a change in the hour once per second, in order to
greatly reduce CPU strain.

If the phrase ".time" is said in the channel, the bot will tell what time it is,
using the phrase "OI IT'S X BONG", where X is the number of BONGs said at the
top of the hour.
The same thing happens if the message ".time #channel" is messaged to the bot privately.
If the phrase ".ptime" is said in the channel, the bot will /notice the person
who said such a thing with the current time.

If the bot receives a private message of ".speak #channel TEXT_HERE", it will
echo the text back to the channel specified.

If ".ping" (or any other message starting with '.' and ending with 'ing') is said in any
channel, the bot will replace 'ing' with 'ong' and respond to that same channel.

If the phrase ".tweet USERNAME" is said in the channel, the bot will fetch the
most recent (non-reply) tweet from that user. If a number is specified after the
tweet, the nth non-reply tweet will be fetched.

If kicked, the bot will reconnect after 10 seconds have passed.

If a message in any channel starts with the bot's nick and ends with '??' (for example,
"BigBen, am I ever going to get married??"), the bot will give a random response from the
RESPONSES file.

If the message, minus the leading nick and trailing question mark, is in the
CUSTOMRESPONSES file before the "::" in its line, the message after the "::"
will be sent to the channel.

Nicks in the IGNORE file will be ignored. This is useful if there are other
bots in the channel that we don't want BigBen to get links from. This file
needs to end with a newline character.

Nicks in the NICKS file can privately message the bot ".update" to update the
responses files, the IGNORE file and the NICKS file. The NICKS file also
needs to end with a newline character.

There is a function to log the number of users in each channel. If enabled,
it will write the number of users in each channel to the given file. This updates with
each join and part, and every fifteen seconds.

If you would like to see the bot in action and/or talk with me and the bot, you
can join #BigBen on irc://irc.rizon.net.

BigBen is licensed under the terms of the GNU General Public license, version
2 or later, at the user's discretion.
