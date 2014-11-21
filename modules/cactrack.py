import willie



def setup(bot):
	if not bot.config.kdown.cactrack_pwd:
		bot.config.kdown.cactrack_pwd = ''
		bot.config.save()
	bot.memory['cactrack_pwd'] = bot.config.kdown.cactrack_pwd.strip()

@willie.module.commands('findcactus', 'whichcactus', 'cactus')
def findcactus(bot, trigger):
	if bot.memory.get('cactrack_name', False):
		bot.reply("To my knowledge, cactus is currently known as: " + bot.memory['cactrack_name'])
	else:
		bot.reply("I don't know, sorry.")

@willie.module.commands('setcactus')
def setcactus(bot, trigger):
	if trigger.group(2) and trigger.group(2).strip() == bot.memory['cactrack_pwd']:
		bot.memory['cactrack_name'] = trigger.nick.strip()
		bot.say("ok!")
	else:
		bot.say("invalid or no password!")
