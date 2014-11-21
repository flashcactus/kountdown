import willie
import random

citations = [
		'http://en.wikipedia.org/wiki/Cessna_Citation',
		'http://en.wikipedia.org/wiki/Chevrolet_Citation',
		'http://en.wikipedia.org/wiki/Edsel_Citation',
		'http://en.wikipedia.org/wiki/Citation_(horse)',
		'http://en.wikipedia.org/wiki/Gibson_Citation',
		'http://en.wikipedia.org/wiki/Citation_Boulevard',
		'http://en.wikipedia.org/wiki/Citation_(album)',
		'http://en.wikipedia.org/wiki/Unit_citation',
		'http://en.wikipedia.org/wiki/Case_citation',
		'http://en.wikipedia.org/wiki/Traffic_citation',
		'http://en.wikipedia.org/wiki/Citation',
	]
@willie.module.rule('(?:.*[^A-Za-z])?[Cc]itation needed')
#@willie.module.commands('citation', 'cite')
def citation(bot, trigger):
	bot.reply(random.choice(citations))
