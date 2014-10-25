import willie
import time
import re

queue=[]
events={}
#
#full: tline = [86400, 82800, 79200, 75600, 72000, 68400, 64800, 61200, 57600, 54000, 50400, 46800, 43200, 39600, 36000, 32400, 28800, 25200, 21600, 18000, 14400, 10800, 7200, 3600]+\
tline = [24*3600, 18*3600, 12*3600, 9*3600, 6*3600, 4*3600, 3*3600, 2*3600, 3600]+\
[45*60 ,30*60 ,15*60, 5*60, 60, 0]#, 30, 0]#,15,0]#,10,5,0]
interval = 5
ok_channels=[]#['#bottorture', 'cactus'] #deprecated

class Event():
	def __init__(self, idn, name, desc, s_time, bot):
		self.name=name
		self.desc=desc
		self.time=s_time
		self.id=idn

		bot.memory['kd_queue']=self.rebuildqueue(bot.memory['kd_queue'])


	def rebuildqueue(self, queue):
		ctime=time.time()
		newq=[]
		for qitem in queue:
			if qitem[1]!=self.id:
				newq.append(qitem)
		for t in tline:
			if self.time-t >= ctime:
				newq.append((self.time-t, self.id))
		newq.sort(key = lambda t: t[0])
		return newq



	def __str__(self):
		return "Event "+str(self.id)+" | %s (%s) at %s [unixtime %.1f]" % (self.name, self.desc, timestr(self.time), self.time)


#########################################################################

def pack_events(events):
	elst=[]
	for e in events:
		elst+=list(map(str,(events[e].id,events[e].name,events[e].desc,events[e].time)))
	return '|'.join(elst)
		
def unpack_events(bot, pacstring):
	plst=pacstring.split('|')
	l = len(plst)
	if l%4:
		return {}
	events={}
	for i in range (0,l,4):
		eid=int(plst[i])
		events[eid]=Event(eid,plst[i+1],plst[i+2],float(plst[i+3]),bot)
	return events

def saveevents(bot):
	bot.config.kdown.events=pack_events(bot.memory['kd_events'])
	bot.config.save()

def timeleft(seconds):
	'''returns a string representation of the time left'''
	if seconds <= 0:
		return "0 seconds"
	days=seconds//86400;seconds-=86400*days
	hours=seconds//3600;seconds-=3600*hours
	mins=seconds//60;seconds-=60*mins
	s=\
('%d day(s) ' % days if days else '') +\
('%d hour(s) ' % hours if hours else '') +\
('%d minute(s) ' % mins if mins else '') +\
('%.2f second(s)' % seconds if seconds else '')
	return s.strip()


def timestr(unixtime=None, offset=0, fstring="%Y-%m-%d %H:%M:%S UTC%z"):
	'''returns a formatted string representing the unixtime argument in the <UTC+offset> timezone'''
	if not unixtime:
		unixtime=time.time()
	tt=time.gmtime(unixtime)
	return time.strftime(fstring,tt)


class ParsingError(Exception):
	pass

time_patterns = (
re.compile("[Uu](\d{4,5})-(\d{1,2})-(\d{1,2})-(\d{1,2})[:.](\d{1,2})[:.](\d{1,2})"), 
re.compile("[nN]\+?(?:(?:(?:(\d+):)?(\d+):)?(\d+):)?(\d+)"),
re.compile("[cCkK]?([-+])(?:(?:(?:(\d+):)?(\d+):)?(\d+):)?(\d+)"),
)

def parse_time( t_string, kd_time=None):
	'''Parses a time string, in the following formats:
	raw unixtime: 	 		%s	
	UTC: 		 		[uU]%Y-%m-%d-%H[:.]%M[:.]%S
	relative to now: 		[nN]\+?(((%d:)?%h:)?%m:)?%s
	relative to current kd time: 	[cCkK]?[-+](((%d:)?%h:)?%m:)?%s
	The last one depends on the kd_time argument, if it is none and time is given in that format, raises a ParsingError.
	'''
	t_string = t_string.strip()
	mutc, mrn, mrk = (p.match(t_string) for p in time_patterns)
	if mutc:
		ts = time.strptime(t_string.replace('.', ':')[1:], "%Y-%m-%d-%H:%M:%S")	
		secs=int(time.strftime('%s', ts))	#dirty hack to have the time-tuple interpreted as UTC no matter what the local timezone is
		return secs
	elif mrn:
		days,hrs,mins,secs = (0 if mrn.group(t) is None else int(mrn.group(t)) for t in range(1,5))
		return int(time.time()) + days*3600*24 + hrs*3600 + mins*60 + secs
	elif mrk:
		if kd_time is not None:
			sign = 1 if mrk.group(1)=='+' else -1
			days,hrs,mins,secs = (0 if mrk.group(t) is None else int(mrk.group(t)) for t in range(2,6))
			return int(kd_time) + sign * (days*3600*24 + hrs*3600 + mins*60 + secs)
			
		else:
			raise ParsingError('Time in rel-kd format, but kd_time not given!')
	elif t_string.isdigit():
		return int(t_string)
	else:
		raise  ParsingError('Unknown time format')


###################################################################

def setup(bot):
	ctime = time.time()
	bot.memory['kd_queue']=[]
	
	try:
		bot.memory['kd_evnctr']=int(bot.config.kdown.ev_ctr)
	except:
		bot.memory['kd_evnctr']=0
	
	#try:
	if True:
		print(bot.config.kdown.events)	
		events=unpack_events(bot, bot.config.kdown.events)
		bot.memory['kd_events']=events
		print(bot.memory['kd_events'])
		print()
		print(bot.memory['kd_queue'])
#	except Exception as e:
#		raise e
#		bot.memory['kd_events']={}
#	print(bot.memory['kd_events'])
	
	try:
		subscrl=bot.config.kdown.get_list('subscribers')
		bot.memory['kd_subscribers']=set()
		for sub in subscrl:
			bot.memory['kd_subscribers'].add(sub)
		print(subscrl,bot.memory['kd_subscribers'])
	except Exception as e:
		bot.memory['kd_subscribers']=set()

	admins=set(bot.config.core.get_list('admins'))
	admins.update(set(bot.config.kdown.get_list('admins')))
	admins.add(bot.config.core.owner)
	bot.memory['kd_admins']=admins
	print(bot.memory['kd_admins'])



##################################################################

@willie.module.commands('addevent','addevt','addkd','kdadd')
def addevt(bot,trigger):
	'''Add countdown event. 
Syntax: .addevent name|description|time. Refer to https://github.com/flashcactus/kountdown/wiki/Time-Format for valid time formats.
This command is currently available only to kd-admins.
'''
	if str(trigger.nick) not in bot.memory['kd_admins']:
		bot.say("admin-only command.")
		return
	if bot.memory.contains('kd_evnctr'):
		evnctr=int(bot.config.kdown.ev_ctr)
	else:
		evnctr=1
	cline=trigger.group(2).split('|')
	name=cline[0]
	desc=cline[1]
	try:
		s_time = parse_time(cline[2])
	except ParsingError:
		bot.reply("Wrong time format. See https://github.com/flashcactus/kountdown/wiki/Time-Format for valid formats.")
	bot.memory['kd_events'][evnctr]=Event(evnctr,name,desc,s_time,bot)
	bot.config.kdown.ev_ctr=evnctr+1
	saveevents(bot)
	bot.say('added:'+str(bot.memory['kd_events'][evnctr]))


@willie.module.commands('lsevents','lskd','kdls','lsevt')
def lsevents(bot,trigger):
	'''.lsevents, .lskd, .kdls, .lsevt: list pending Kountdown Events'''
	if not len(bot.memory['kd_events']):
		bot.reply("No scheduled events right now.")
	else:
		if str(trigger.nick) != str(trigger.sender):
			bot.reply("PMing the list to you!")
		events = sorted((bot.memory['kd_events'][event] for event in bot.memory['kd_events']), key=lambda evt:evt.time - time.time() )
		for evt in events:
			bot.msg(trigger.nick, "id:%3d | Name:%s | time: %s | unixtime:%.1f | %s left" % \
					( evt.id, evt.name, timestr(evt.time), evt.time, timeleft(evt.time - time.time()) )\
				)
			bot.msg(trigger.nick, "Description: %s " % evt.desc)

@willie.module.commands('rmkd','kdrm','rmevent','rmevt')
def rmevent(bot,trigger):
	'''Delete countdown by id. Available to kd-admins only.'''
	if str(trigger.nick) in bot.memory['kd_admins']:
		try:
			k=int(trigger.group(2))
			del bot.memory['kd_events'][k]
			bot.config.kdown.events=pack_events(bot.memory['kd_events'])
			bot.config.save()
			bot.say("event deleted.")
		except:
			pass
	else:
		print(trigger.nick)
		print(bot.memory['kd_admins'])
		bot.say("admin-only command.")


@willie.module.commands('subscribe')
def subscribe(bot,trigger):
	'''Subscribe yourself to countdowns. All announcements posted to channels also get private-mailed to subscribers. 
	Unsubscription is available with the .unsubscribe command.'''
	bot.memory['kd_subscribers'].add(str(trigger.nick))
	bot.config.kdown.subscribers=list(bot.memory['kd_subscribers'])
	bot.config.save()

@willie.module.commands('subschan')
def chansubscr(bot,trigger):
	'''.subschan [channel]: Subscribe a channel to countdowns. This command is only available to the ops of the channel in question and bot admins. If channel argument is not given, subscribes the channel the command is issued in.'''
	chan=trigger.group(2)
	chan=chan.strip() if chan else trigger.sender
	if str(trigger.nick) in bot.ops.get(chan, []) or str(trigger.nick) in bot.config.core.get_list('admins'):
		chan=chan.lower()
		if chan in bot.memory['kd_subscribers']:
			bot.say('This channel is already subscribed.')
			return
		bot.memory['kd_subscribers'].add(chan)
		bot.config.kdown.subscribers=list(bot.memory['kd_subscribers'])
		bot.config.save()
		bot.say('Done.')
	else:
		bot.say('nope')

@willie.module.commands('unsubschan')
def chanunsub(bot,trigger):
	'''.unsubschan [channel]: unubscribe a channel from countdowns. See .help subschan for details.'''
	chan=trigger.group(2)
	chan=chan.strip() if chan else trigger.sender
	if str(trigger.nick) in bot.ops.get(chan, []) or str(trigger.nick) in bot.config.core.get_list('admins'):
		chan=chan.lower()
		try:
			bot.memory['kd_subscribers'].remove(chan)
		except KeyError:
			bot.say('This channel wasn\'t subscribed.')
			return
		bot.config.kdown.subscribers=list(bot.memory['kd_subscribers'])
		bot.config.save()
		bot.say('Done.')
	else:
		bot.say('nope')

@willie.module.commands('unsubscribe')
def unsubscribe(bot,trigger):
	'''Unsubscribe yourself from countdowns. See .help subscribe for more info.'''
	bot.memory['kd_subscribers'].discard(str(trigger.nick))
	bot.config.kdown.subscribers=list(bot.memory['kd_subscribers'])
	bot.config.save()
	
@willie.module.commands('lssubscr')
def lssubscr(bot,trigger):
	'''sends you a list of all subscribers. Available to admins only.'''
	if str(trigger.nick) in bot.memory['kd_admins']:
		bot.msg(trigger.nick, str(bot.memory['kd_subscribers']))

@willie.module.commands('editevent', 'chevent', 'chevt', 'chkd')
def chevent(bot,trigger):
	'''
	.editevent, .chevent, .chevt, .chkd: Edit an event.
	Syntax: .editevent <event_id> (t[ime]|n[ame]|d[esc]) <value>. 
	 
	      The time must be in one of the formats defined  on the following page:
	      https://github.com/flashcactus/kountdown/wiki/Time-Format
	      Name&desc must not contain the pipe character (bug cactus if you really want it).
	      You could get the event id and current values via the .lsevents command.
	'''
	cmnd = trigger.group(2).split(None, 2)
	if len(cmnd)<3 or cmnd[1] not in ['n','t','d','name','time','desc'] or not cmnd[0].isdigit():
		bot.say("invalid command format. see .help chevt for details.")
	elif int(cmnd[0]) not in bot.memory['kd_events']:
		bot.say("I don't know of an active event with id %s." % cmnd[0])
	elif cmnd[1][0]=='t':
		try:
			newtime=parse_time(cmnd[2], kd_time=bot.memory['kd_events'][int(cmnd[0])].time)
		except:
			bot.say("invalid time format. Use unixtime with decimals")
			return
		bot.memory['kd_events'][int(cmnd[0])].time=newtime
		bot.memory['kd_queue']=bot.memory['kd_events'][int(cmnd[0])].rebuildqueue(bot.memory['kd_queue'])
		saveevents(bot)
		print('queue:\n')
		print(bot.memory['kd_queue'])

		bot.say('time changed successfully.')
	else:
		if '|' in cmnd[2]:
			bot.say("the pipe character is not permitted right now. Poke cactus if you really want it to be.")
		else:
			if cmnd[1][0]=='n':
				bot.memory['kd_events'][int(cmnd[0])].name=cmnd[2]
				bot.say('name changed successfully')
			elif cmnd[1][0]=='d':
				bot.memory['kd_events'][int(cmnd[0])].desc=cmnd[2]
				bot.say('description changed successfully')
			else:
				bot.say("Something went wrong. Very wrong.")




ctmutex = False #CheckTime Mutex
##########################################################

@willie.module.interval(interval)
def check_time(bot):
	global ctmutex
	ctime=time.time()
	if ctmutex:
		return
	else:
		ctmutex=True
	try:
		if bot.memory['kd_queue'][0][0] <= ctime:
			#print(bot.memory['kd_queue'])
			print(ctime, bot.memory['kd_queue'][0])
			try:
				evt=bot.memory['kd_events'][bot.memory['kd_queue'][0][1]]
			except KeyError: #nonexistant event
				print("nonexistant event!")
				bot.memory['kd_queue'].pop(0)
				ctmutex=False
				return
			tmlefts=timeleft(int(evt.time - bot.memory['kd_queue'][0][0]))
			if(evt.time <= ctime):		#event has happened already
				del bot.memory['kd_events'][bot.memory['kd_queue'][0][1]]
				bot.config.kdown.events=pack_events(bot.memory['kd_events'])
				bot.config.save()
			else:
				for chan in ok_channels+list(bot.memory['kd_subscribers']):
					bot.msg( chan, '<<  !  >>  No more than %s left until %s' % (tmlefts, str(evt)) )
			bot.memory['kd_queue'].pop(0)
	except IndexError as e:
		pass
	except Exception as e:
		ctmutex=False
		raise e
	finally:
		ctmutex=False


########################################################################
