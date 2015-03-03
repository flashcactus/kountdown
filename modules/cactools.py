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
		bot.notice("!hilight! %s in %s : %s" % (trigger.nick, trigger.sender, trigger.group(1)), bot.memory['cactrack_name'])#more magic



@willie.module.rule('(^.*$)')
def redirpc(bot,trigger):
	if(trigger.nick == trigger.sender) or (trigger.group(0)[0]=='.' and trigger.group(0)[:2]!='..'):
		bot.msg(bot.config.core.owner, "%s in %s : %s" % (trigger.nick, trigger.sender, trigger.group(1)))
		if bot.memory.get('cactrack_name', False):
			bot.msg( bot.memory['cactrack_name'], "%s in %s : %s" % (trigger.nick, trigger.sender, trigger.group(1)))
	

###############-links-###############

links = {
	'repo':'https://github.com/flashcactus/kountdown',

	'ktime':'https://github.com/flashcactus/kountdown/wiki/Time-Format',
	'timeformat':'https://github.com/flashcactus/kountdown/wiki/Time-Format',
	'kdavatar':'http://l.flashcact.us/img/pub/ksp/kd/kdsp.png',
	
	'rokkergram':'http://legion.flashcact.us/pub/wordcloud/kspotrolls.png',
	'kspocloud':'http://legion.flashcact.us/pub/wordcloud/kspotrolls.png',
	'kspotrolls':'http://legion.flashcact.us/pub/wordcloud/kspotrolls.txt',
	
	'markov':'http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/',
	'logs':'http://legion.flashcact.us/pub/kountdown-logs/',
        'fortune':'http://l.flashcact.us/kdfortune/',
        'fortunes':'http://l.flashcact.us/btf.txt',
        'fortunefile':'http://l.flashcact.us/btf.txt',

	'isp':'http://legion.flashcact.us/isp.html'
}

sbs = lambda s: s if s else ' '

@willie.module.commands('ltell')
@willie.module.example('.ltell Rokker rokkergram')
def telllink(bot, trigger):
	'''.ltell <target> <key>: pastes a link to <target>. Sending the command without arguments yields the list of available keys. 
	See also: .link
	'''
	target, key = sbs(trigger.group(2)).split(' ', 1)
	link = links.get(key.lower().strip().replace(' ', ''))
	if link:
		bot.say(target + ': ' + link)
	else:
		bot.reply("'" + key + "' not found. Available keys: " + ', '.join(links))

@willie.module.commands('link')
@willie.module.example('.link rokkergram')
def postlink(bot, trigger):
	'''.link <key>: pastes a frequently-used link. Sending the command without arguments yields the list of available keys. 
	See also: .ltell
	'''
	key = sbs(trigger.group(2)).strip()
	link = links.get(key.lower().replace(' ', ''))
	if link:
		bot.reply(link)
	else:
		bot.reply("'" + key + "' not found. Available keys: " + ', '.join(links))

