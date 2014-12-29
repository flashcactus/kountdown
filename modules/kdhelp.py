import willie
import help

@willie.module.rule('$nick' r'(?i)help(?:[?!]+)?$')
@willie.module.priority('low')
def kdhelp(bot, trigger):
	bot.notice('For more info about this particular bot visit the page at https://github.com/flashcactus/kountdown', trigger.nick.strip())
