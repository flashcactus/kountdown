import willie

@willie.module.rule('^\x01ACTION +[Ss]tare.*$')
#@willie.module.rule('^.*[KkCc]ountdown.*$')
def stare_back(bot,trigger):
	bot.msg(trigger.sender,"\x01ACTION stares at "+trigger.nick+"\x01")
