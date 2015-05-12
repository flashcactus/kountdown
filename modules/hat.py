import willie
import math
import time

1/0

fedora_interval = 3600*2 #every 6 hours
hat_interval = 605 # 10min + ε
channels = ['#bottorture',]
thresh = 200

fedoraprice = 0
my_hats = {ch:0 for ch in channels}
my_fedoras = {ch:0 for ch in channels}
good_bots = {'hatbot', 'bothat'}
play_hats = False
bet_amount = dict()


@willie.module.commands('hatstart')
@willie.module.require_owner
def beginph(bot, trigger):
    global play_hats
    global bet_amount
    play_hats = True
    bet_amount = {ch:1 for ch in channels}
    if trigger.group(2):
        good_bots.add(trigger.group(2).strip())
    for channel in channels:
        bot.msg(channel, '.bet 1')

@willie.module.commands('hatstop')
def endph(bot, trigger):
    global play_hats
    play_hats = False

#-----periodic checks----

@willie.module.interval(fedora_interval)
def check_fedoras(bot):
    print('fedora',time.time())
    for channel in channels:
        bot.msg(channel, '.fedora count')
        bot.msg(channel, '.fedora price')

@willie.module.interval(hat_interval)
def free_hats(bot):
    print('hat',time.time())
    for channel in channels:
        bot.msg(channel, '.hat')

#-----value triggers----

@willie.module.rule('.*thinks Kountdown.s enlightenment is around ([0-9]+).*')
def setfedoras(bot, trigger):
    my_fedoras[trigger.sender] = int(trigger.group(1))

@willie.module.rule('.*Kountdown.*(?:hat count to|should be content with|hats for a total of)[^0-9]*([0-9]+).*')
@willie.module.rule('.*(Kountdown).*has won the lottery resulting in[^0-9]*([0-9]+).*')
def sethats(bot, trigger):
    didnthave = (fedoraprice > my_hats[trigger.sender])
    try:
        my_hats[trigger.sender] = int(trigger.group(1))
    except:
        my_hats[trigger.sender] += int(trigger.group(2))
    if (my_hats[trigger.sender] >= fedoraprice) and didnthave:
        bot.say('.fedora price')

@willie.module.rule('.*takes ([0-9]+) (fedoras|hats) from Kountdown and gives them ([0-9]+).*')
def fedora_adjust(bot, trigger):
    if trigger.group(2) == 'fedoras':
        my_fedoras[trigger.sender] -= int(trigger.group(1))
        my_hats[trigger.sender] += int(trigger.group(3))
    else:
        my_fedoras[trigger.sender] += int(trigger.group(3))
        my_hats[trigger.sender] -= int(trigger.group(1))

#-----fedora market-----

@willie.module.rule('.*the current fedora value is ([0-9]+).*')
def fedoradecision(bot, trigger):
    global fedoraprice
    fedoraprice = int(trigger.group(1))
    if fedoraprice <= thresh and my_hats[trigger.sender] >= fedoraprice:
        bot.say('.fedora buy ' + str(math.floor(my_hats[trigger.sender] / fedoraprice)))
    elif fedoraprice >= thresh and my_fedoras[trigger.sender] > 1:
        bot.say('.fedora sell ' + str(my_fedoras[trigger.sender] - 1))

#-----hat gambling------

@willie.module.rule('.*(raises|lowers) Kountdown.s hat count to ([0-9]+).*')
def playhats(bot, trigger):
    if play_hats and (trigger.sender in channels):
            time.sleep(4)
            if not play_hats:
                return
            if trigger.group(1) == 'raises':
                bet_amount[trigger.sender] = 1
            else:
                bet_amount[trigger.sender] *= 2
            bot.say('.bet '+str(bet_amount[trigger.sender]))

