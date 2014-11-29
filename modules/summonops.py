import time
import willie

def setup(bot):
	bot.memory['summonops_delay'] = {}
	try:
		bot.memory['summonops_interv'] = int(bot.config.summonops.approve_time)
	except:
		bot.memory['summonops_interv'] = 15

@willie.module.commands('ops','summonops')
def summon_ops(bot, trigger):
	"""
	.ops, .summonops: summons all channel ops by spitting out a line with their names in it. 
	THIS COMMAND SHOULD ONLY BE USED IN EMERGENCIES IF YOU DON'T WANT TO BE SMOTE FOR SPAMMING.
	"""
	chan = trigger.sender.strip()
	nick = trigger.nick.strip()
	if chan == nick:
		bot.say("This command is pointless in private.")	
		return
	ctime = time.time()
	dtuple = bot.memory['summonops_delay'].get(chan, (0, nick))
	if (ctime - dtuple[0]) <= bot.memory['summonops_interv']: # not a confirmation
		if dtuple[1] == nick:
			bot.reply("An other person must confirm this, not you.")
		else:
			ops = bot.ops.get(chan, [])
			bot.say("Hailing all ops! " + ", ".join(ops) + "! " + dtuple[1] + " and " + nick + " request your attention." )
	else:
		bot.reply("Are you sure? If this truly is an emergency, then another person on the channel must type this command within the next " + str(bot.memory['summonops_interv']) + " seconds." )
		bot.memory['summonops_delay'][chan] = (time.time(), nick)

