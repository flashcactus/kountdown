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
                'http://en.wikipedia.org/wiki/Cetacean',
                'http://en.wikipedia.org/wiki/List_of_cetaceans',
	]
@willie.module.rule('(?:.*[^A-Za-z])?[Cc]itation needed')
@willie.module.commands('citation', 'cite')
def citation(bot, trigger):
	"Replies with a smartypants link whenever someone requests a citation"
	bot.reply(random.choice(citations))


@willie.module.rule('(?i)^(?:\x01ACTION)? *(?:stares|glares|pokes).*$')
#@willie.module.rule('^.*[KkCc]ountdown.*$')
def stare_back(bot, trigger):
        bot.msg(trigger.sender,"\x01ACTION glares at "+trigger.nick+"\x01")

@willie.module.rule('(?i)^(?:\x01ACTION)? *(?:slaps|zaps|kicks|hits|smacks|chokes|stabs|suffocates|burns).*$')
def slap_back(bot, trigger):
	bot.msg(trigger.sender,"\x01ACTION zaps "+trigger.nick+"\x01")

@willie.module.rule('(?i).*(?:good bot|.*bot ?snack).*$')
def snack(bot, trigger):
	bot.reply('Thank you! Glad to be of service.')

@willie.module.rule('(?i).*(?:bad bot|bot ?smack).*$')
def bbf(bot, trigger):
    bot.say(':[')

@willie.module.rule('(?i).*(?:needs? a hug|hug me).*$')
def hug(bot,trigger):
    bot.msg(trigger.sender,"\x01ACTION hugs "+trigger.nick+"\x01")
