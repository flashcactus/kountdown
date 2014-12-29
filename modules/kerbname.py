import random
import willie

def setup(bot):
	with open('kerbnamelist') as namelist:
		names = [[]]
		nind=0
		for l in namelist.readlines():
			if l[0] == '!':
				names.append([])
				nind += 1
				continue
			names[nind].append(l.strip())
		bot.memory['kerbnames_nlst'] = names

@willie.module.commands('kerbname', 'kerbal', 'kerman')
def kerbname(bot, trigger):
	'''generates a random name for a kerbal'''
	names = bot.memory['kerbnames_nlst']
	if random.random() <= 0.05:
		name = random.choice(names[0])
	else:
		name = random.choice(names[1])+random.choice(names[2])
	bot.reply(name + ' Kerman')

