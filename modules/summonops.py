
import willie


@willie.module.commands('ops','summonops')
def summon_ops(bot, trigger):
	"""
	.ops, .summonops: summons all channel ops by spitting out a line with their names in it. 
	THIS COMMAND SHOULD ONLY BE USED IN EMERGENCIES IF YOU DON'T WANT TO BE SMOTE FOR SPAMMING.
	"""
	chan = trigger.sender.strip()
	ops = bot.ops.get(chan, [])
	bot.say("Hailing all ops! " + ", ".join(ops) + "! " + trigger.nick.strip() + " requests your attention." )

