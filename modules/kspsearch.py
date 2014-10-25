'''
Adds commands for searching/googling the KSP forums and mod sites

'''

from willie.module import commands, example
import willie.modules.search as search


@commands('kf','kforums','gf','sf','forumsearch','searchforums')
@example('.kf high contrast navball')
def gf(bot, trigger):
    """.kf, .gf, .sf: Google the KSP forums for the input"""
    query = trigger.group(2)
    if not query:
        return bot.reply('what do you want me to search for?')
    uri = search.google_search('site:forum.kerbalspaceprogram.com '+query)
    if uri:
        bot.reply(uri)
        bot.memory['last_seen_url'][trigger.sender] = uri
    elif uri is False:
        bot.reply("Problem getting data from Google.")
    else:
        bot.reply("No results found for '%s'." % query)

@commands('ks','kstuff','kerbalstuff')
@example('.ks ferram aerospace')
def kstuff(bot, trigger):
    '''.ks, .kstuff: Search Kerbal Stuff for the input'''
    query = trigger.group(2)
    if not query:
        return bot.reply('what do you want me to search for?')
    uri = search.google_search('site:kerbalstuff.com '+query)
    if uri:
        bot.reply(uri)
        bot.memory['last_seen_url'][trigger.sender] = uri
    elif uri is False:
        bot.reply("Problem getting search results.")
    else:
        bot.reply("No results found for '%s'." % query)


@commands('kwiki', 'kw', 'kws')
@example('.kw vall')
def kwiki(bot, trigger):
    '''.kw, .kws, .kwiki: Search the official wiki for the input'''
    query = trigger.group(2)
    if not query:
        return bot.reply('what do you want me to search for?')
    uri = search.google_search('site:wiki.kerbalspaceprogram.com '+query)
    if uri:
        bot.reply(uri)
        bot.memory['last_seen_url'][trigger.sender] = uri
    elif uri is False:
        bot.reply("Problem getting data from Google.")
    else:
        bot.reply("No results found for '%s'." % query)
