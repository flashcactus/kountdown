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
	"Replies with a smartypants link whenever someone requests a citation"
	bot.reply(random.choice(citations))


@willie.module.rule('^\x01ACTION +[Ss]tare.*$')
#@willie.module.rule('^.*[KkCc]ountdown.*$')
def stare_back(bot,trigger):
        bot.msg(trigger.sender,"\x01ACTION stares at "+trigger.nick+"\x01")

