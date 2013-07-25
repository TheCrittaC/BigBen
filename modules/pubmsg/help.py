import __init__

class help:
	def on_pubmsg(self, nick, connection, event):
		message = event.arguments()[0]
		source = event.source().split('!')[0]
		if message.startswith(".help"):
			try:
				message.split()[1]
			except IndexError:
				for module in __init__.__enabled__:
					connection.privmsg(source, self.findHelp(module))
	   		else:
				try:
					module = __init__.__commands__[message.split()[1]]
				except KeyError:
					connection.privmsg(event.target(), "'{0}' doesn't exist".format(message.split()[1]))
				else:
					connection.privmsg(event.target(), self.findHelp(module))

	def findHelp(self, module):
		try:
			man = __init__.__help__[module]
		except KeyError:
			man = "{0} - No help for this module".format(module)
		return man


