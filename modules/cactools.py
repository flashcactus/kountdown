import willie
import time


def setup(bot):
	if not bot.config.kdown.cactrack_pwd:
		bot.config.kdown.cactrack_pwd = ''
		bot.config.save()
	bot.memory['cactrack_pwd'] = bot.config.kdown.cactrack_pwd.strip()
	bot.memory['cactrack_cdts'] = {}
	bot.memory['cactrack_cooldown'] = 120 #int(bot.config.kdown.reaction_cooldown)

##############-tracker-###############

@willie.module.commands('findcactus', 'whichcactus', 'cactus')
def findcactus(bot, trigger):
	'''.findcactus, .cactus, .whichcactus: Shows which nickname cactus currently has.'''
	if bot.memory.get('cactrack_name', False):
		bot.reply("To my knowledge, cactus is currently known as: " + bot.memory['cactrack_name'])
	else:
		bot.reply("Unfortunately I don't know what cactus calls himself at the moment.")


@willie.module.rule('.*[Pp]refix[Cc]actus')
def pcreact(bot, trigger): 
	ctime = time.time()
	timestamp = bot.memory['cactrack_cdts'].get(trigger.sender, 0)
	if (ctime - timestamp) >= bot.memory['cactrack_cooldown']: 
		if bot.memory.get('cactrack_name', False):
			bot.reply("To my knowledge, cactus is currently known as: " + bot.memory['cactrack_name'])
		else:
			bot.reply("Unfortunately I don't know what cactus calls himself at the moment.")
		bot.memory['cactrack_cdts'][trigger.sender] = time.time()
	else:
		bot.notice("nope", trigger.nick.strip()) #magic


@willie.module.commands('setcactus')
def setcactus(bot, trigger):
	'''used by cactus to provide info for the .findcactus command'''
	if trigger.group(2) and trigger.group(2).strip() == bot.memory['cactrack_pwd']:
		bot.memory['cactrack_name'] = trigger.nick.strip()
		bot.reply("ok!", notice=True)
	else:
		bot.reply("invalid or no password!")

###############-relay-################

@willie.module.rule('^(.*(?:[KkCc]ountdown|[KkCc][Aa][KkCc][tT](?:[Uu][Ss]|[Ii])|[Aa]rtichoke).*)$')
def redirect(bot,trigger):
	bot.msg(bot.config.core.owner, "!hilight! %s in %s : %s" % (trigger.nick, trigger.sender, trigger.group(1)))
	if bot.memory.get('cactrack_name', False):
		bot.msg( bot.memory['cactrack_name'],  "!hilight! %s in %s : %s" % (trigger.nick, trigger.sender, trigger.group(1)))



@willie.module.rule('(^.*$)')
def redirpc(bot,trigger):
	if(trigger.nick == trigger.sender) or (trigger.group(0)[0]=='.' and trigger.group(0)[:2]!='..'):
		bot.msg(bot.config.core.owner, "%s in %s : %s" % (trigger.nick, trigger.sender, trigger.group(1)))
		if bot.memory.get('cactrack_name', False):
			bot.msg( bot.memory['cactrack_name'],  "%s in %s : %s" % (trigger.nick, trigger.sender, trigger.group(1)))


