'''
Adds commands for searching/googling the KSP forums and mod sites

'''

from willie.module import commands, example
import willie.modules.search as search

def duck(query):
    #If the API gives us something, say it and stop
    result = search.duck_api(query)
    if result:
        return result
    #Otherwise, look it up on the HTMl version
    return search.duck_search(query)


@commands('kf','kforums','gf','sf','forumsearch','searchforums')
@example('.kf high contrast navball')
def gf(bot, trigger):
    """.kf, .gf, .sf: Search the KSP forums for the input"""
    query = trigger.group(2)
    if not query:
        return bot.reply('what do you want me to search for?')
    uri = duck('site:forum.kerbalspaceprogram.com '+query)
    if uri:
        bot.reply(uri)
        bot.memory['last_seen_url'][trigger.sender] = uri
    elif uri is False:
        bot.reply("Problem getting data from DDG.")
    else:
        bot.reply("No results found for '%s'." % query)

@commands('ks','kstuff','kerbalstuff')
@example('.ks ferram aerospace')
def kstuff(bot, trigger):
    '''.ks, .kstuff: Search Kerbal Stuff for the input'''
    query = trigger.group(2)
    if not query:
        return bot.reply('what do you want me to search for?')
    uri = duck('site:kerbalstuff.com '+query)
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
    uri = duck('site:wiki.kerbalspaceprogram.com '+query)
    if uri:
        bot.reply(uri)
        bot.memory['last_seen_url'][trigger.sender] = uri
    elif uri is False:
        bot.reply("Problem getting data from DDG.")
    else:
        bot.reply("No results found for '%s'." % query)
