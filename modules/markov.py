import willie
import random
import re
import sys
import sqlite3
import codecs
import threading
import time

#------sql.py-------

class Sql:
    WORD_COL_NAME_PREFIX = 'word'
    COUNT_COL_NAME       = 'count'
    WORD_TABLE_NAME      = 'word'
    INDEX_NAME           = 'i_word'
    PARAM_TABLE_NAME     = 'param'
    KEY_COL_NAME         = 'name'
    VAL_COL_NAME         = 'value'
    
    def _check_column_count(self, count):
        if count < 2:
            raise ValueError('Invalid column_count value, must be >= 2')
        
    def _make_column_name_list(self, column_count):
        return ', '.join([self.WORD_COL_NAME_PREFIX + str(n) for n in range(1, column_count + 1)])
        
    def _make_column_names_and_placeholders(self, column_count):
        return ' AND '.join(['%s%s=?' % (self.WORD_COL_NAME_PREFIX, n) for n in range(1, column_count + 1)])

    def create_word_table_sql(self, column_count):
        return 'CREATE TABLE IF NOT EXISTS %s (%s, %s)' % (self.WORD_TABLE_NAME, self._make_column_name_list(column_count), self.COUNT_COL_NAME)
    
    def create_param_table_sql(self):
        return 'CREATE TABLE IF NOT EXISTS %s (%s, %s)' % (self.PARAM_TABLE_NAME, self.KEY_COL_NAME, self.VAL_COL_NAME)
    
    def set_param_sql(self):
        return 'INSERT INTO %s (%s, %s) VALUES (?, ?)' % (self.PARAM_TABLE_NAME, self.KEY_COL_NAME, self.VAL_COL_NAME)
    
    def get_param_sql(self):
        return 'SELECT %s FROM %s WHERE %s=?' % (self.VAL_COL_NAME, self.PARAM_TABLE_NAME, self.KEY_COL_NAME)

    def create_index_sql(self, column_count):
        return 'CREATE INDEX IF NOT EXISTS %s ON %s (%s)' % (self.INDEX_NAME, self.WORD_TABLE_NAME, self._make_column_name_list(column_count))
    
    def select_count_for_words_sql(self, column_count):
        return 'SELECT %s FROM %s WHERE %s' % (self.COUNT_COL_NAME, self.WORD_TABLE_NAME, self._make_column_names_and_placeholders(column_count)) 
    
    def update_count_for_words_sql(self, column_count):
        return 'UPDATE %s SET %s=? WHERE %s' % (self.WORD_TABLE_NAME, self.COUNT_COL_NAME, self._make_column_names_and_placeholders(column_count)) 
    
    def insert_row_for_words_sql(self, column_count):
        columns = self._make_column_name_list(column_count) + ', ' + self.COUNT_COL_NAME
        values  = ', '.join(['?'] * (column_count + 1))
        
        return 'INSERT INTO %s (%s) VALUES (%s)' % (self.WORD_TABLE_NAME, columns, values) 
    
    def select_words_and_counts_sql(self, column_count):
        last_word_col_name = self.WORD_COL_NAME_PREFIX + str(column_count)
        
        return 'SELECT %s, %s FROM %s WHERE %s' % (last_word_col_name, self.COUNT_COL_NAME, self.WORD_TABLE_NAME, self._make_column_names_and_placeholders(column_count - 1))
    
    def delete_words_sql(self):
        return 'DELETE FROM ' + self.WORD_TABLE_NAME

#-----db.py-----

class Db:
	DEPTH_PARAM_NAME = 'depth'
	
	def __init__(self, conn, sql):
		self.conn   = conn 
		self.cursor = conn.cursor()
		self.sql    = sql
		self.depth  = None

	def setup(self, depth):
		self.depth = depth
		self.cursor.execute(self.sql.create_word_table_sql(depth))
		self.cursor.execute(self.sql.create_index_sql(depth))
		self.cursor.execute(self.sql.create_param_table_sql())
		self.cursor.execute(self.sql.set_param_sql(), (self.DEPTH_PARAM_NAME, depth))

	def _get_word_list_count(self, word_list):
		if len(word_list) != self.get_depth():
			raise ValueError('Expected %s words in list but found %s' % (self.get_depth(), len(word_list)))

		self.cursor.execute(self.sql.select_count_for_words_sql(self.get_depth()), word_list)
		r = self.cursor.fetchone()
		if r:
			return r[0]
		else:
			return 0

	def get_depth(self):
		if self.depth == None:
			self.cursor.execute(self.sql.get_param_sql(), (self.DEPTH_PARAM_NAME,))
			r = self.cursor.fetchone()
			if r:
				self.depth = int(r[0])
			else:
				raise ValueError('No depth value found in database, db does not seem to have been created by this utility')
			
		return self.depth
		
	def add_word(self, word_list):
		count = self._get_word_list_count(word_list)
		if count:
			self.cursor.execute(self.sql.update_count_for_words_sql(self.get_depth()), [count + 1] + word_list)
		else:
			self.cursor.execute(self.sql.insert_row_for_words_sql(self.get_depth()), word_list + [1])

	def commit(self):
		self.conn.commit()

	def get_word_count(self, word_list):
		counts = {}
		sql = self.sql.select_words_and_counts_sql(self.get_depth())
		for row in self.cursor.execute(sql, word_list):
			counts[row[0]] = row[1]

		return counts
        

#------gen.py-------


class Generator:
	def __init__(self, db):
		self.db   = db



#-----parse.py-----

class Parser:
	SENTENCE_START_SYMBOL = '^'
	SENTENCE_END_SYMBOL = '$'

	def __init__(self, name, db, sentence_split_char = '\n', word_split_char = ''):
		self.name = name
		self.db   = db
		self.sentence_split_char = sentence_split_char
		self.word_split_char = word_split_char
		self.whitespace_regex = re.compile('\s+')

	def parse(self, txt):
		depth = self.db.get_depth()
		sentences = txt.split(self.sentence_split_char)
		i = 0

		for sentence in sentences:
			sentence = self.whitespace_regex.sub(" ", sentence).strip()

			list_of_words = None
			if self.word_split_char:
				list_of_words = sentence.split(self.word_split_char)
			else:
				list_of_words = list(sentence.lower())

			words = [Parser.SENTENCE_START_SYMBOL] * (depth - 1) + list_of_words + [Parser.SENTENCE_END_SYMBOL] * (depth - 1)
			
			for n in range(0, len(words) - depth + 1):
				self.db.add_word(words[n:n+depth])

			self.db.commit()
			i += 1
			if i % 1000 == 0:
				print(i)
				sys.stdout.flush()



#---markov.py---
#
SENTENCE_SEPARATOR = '\n'
WORD_SEPARATOR = ' '
db_mutex = threading.BoundedSemaphore(1)

addwl=['markovchaincactus', 'theothercactus', '#kspofficial'] #whitelisted channels (the ones that lines will be added from)

def setup(bot):
	bot.memory['markov_db'] = bot.config.markov.db #'/home/cactus/.willie/markov4.db'
	bot.memory['markov_randline_probdiv'] = int(bot.config.markov.randl_probdiv) #1800
	bot.memory['markov_randline_lastts'] = {}
	bot.memory['markov_autochans'] = set(bot.config.markov.get_list('autochans'))
	if not bot.memory.setdefault('markov_firstwordcache', {}):
		print('generating first-word cache...')
		print(gen_new_fwcache(bot))

def gen_new_fwcache(bot):#generate a quick-lookup buffer for first words (as it tends to be quite sizeable)
	db = None
	try:
		db_mutex.acquire()
		db = Db(sqlite3.connect(bot.memory['markov_db']), Sql())
		depth = db.get_depth()
		bot.memory['markov_firstwordcache'] = db.get_word_count([Parser.SENTENCE_START_SYMBOL] * (depth - 1)) #get the actual dict
	finally:
		try:
			del db
		finally:
			db_mutex.release()
		return len(bot.memory['markov_firstwordcache'])


def genline(bot, word_separator=' '):
	'''generates a random line.'''
	try:
		db_mutex.acquire()
		db = Db(sqlite3.connect(bot.memory['markov_db']), Sql()) #DB objects are not shareable between threads, so we need to create a new one each time.
		if not bot.memory['markov_firstwordcache']:
			gen_new_fwcache(bot) #generate the cache if we don't have any
		depth = db.get_depth()
		#look the first word up in the cache
		sentence = [Parser.SENTENCE_START_SYMBOL] * (depth - 1) + [select_next_word(bot.memory['markov_firstwordcache'])]
		end_symbol = [Parser.SENTENCE_END_SYMBOL] * (depth - 1)
		while True:
			tail = sentence[(-depth+1):]
			if tail == end_symbol:
				break
			candidate_words = db.get_word_count(tail)
			if len(candidate_words) > 1:
				print(str(len(candidate_words)) + str(tail))
				if len(candidate_words) < 10:
					print(candidate_words)
			word = select_next_word(candidate_words)
			sentence.append(word)
		del db
	finally:
		db_mutex.release()
		print('')
		return word_separator.join(sentence[depth-1:][:1-depth])
	

def select_next_word(candidate_words):
	'''Selects the next word in the chain.'''
	total_next_words = sum(candidate_words.values())
	i = random.randint(1, total_next_words)
	t=0
	for w in candidate_words.keys():
		t += candidate_words[w]
		if (i <= t):
			return w
	assert False


@willie.module.commands('mgen', 'markov', 'spit', 'spew', 'rline',  'mission')
def spitline(bot, trigger):
	'''.mgen, .markov, .spit, .spew, .rline: spits out a random line generated from the channel logs'''
	bot.say(genline(bot))

@willie.module.commands('mrkon')
def chansubscr(bot,trigger):
	'''.mrkon [channel]: Turns on unprompted random lines in a particular channel. This command is only available to the ops of the channel in question and bot admins. If channel argument is not given, subscribes the channel the command is issued in.'''
	chan=trigger.group(2)
	chan=chan.strip() if chan else trigger.sender
	if str(trigger.nick) in bot.ops.get(chan, []) or str(trigger.nick) in bot.config.core.get_list('admins'):
		chan=chan.lower()
		if chan in bot.memory['markov_autochans']:
			bot.say('automarkov is already on here.')
			return
		bot.memory['markov_autochans'].add(chan)
		bot.config.markov.autochans=list(bot.memory['markov_autochans'])
		bot.config.save()
		bot.say('Done.')
	else:
		bot.say('nope')

@willie.module.commands('mrkoff')
def chanunsub(bot,trigger):
	'''.mrkoff [channel]: Turns off unprompted random lines in a particular channel. See .help subschan for details.'''
	chan=trigger.group(2)
	chan=chan.strip() if chan else trigger.sender
	if str(trigger.nick) in bot.ops.get(chan, []) or str(trigger.nick) in bot.config.core.get_list('admins'):
		chan=chan.lower()
		try:
			bot.memory['markov_autochans'].remove(chan)
		except KeyError:
			bot.say('automarkov is already off here.')
			return
		bot.config.markov.autochans=list(bot.memory['markov_autochans'])
		bot.config.save()
		bot.say('Done.')
	else:
		bot.say('nope')

@willie.module.rule('(?i)^$nickname[,:!].*|.*$nickname(?:.{0,5}|.+[?!])$|.*automatic appeals.*')
def asl(bot, trigger):
	if trigger.sender.strip().lower() in bot.memory['markov_autochans']:
		spitline(bot, trigger)


@willie.module.rule('.*')
def upd_rsl_counter(bot, trigger):
	if trigger.sender.strip().lower() not in bot.memory['markov_autochans']:
		return
	np = bot.memory['markov_randline_lastts'].setdefault(trigger.sender,[0,0])
	np[0] += 1 #message counter
	if np[0] > 10:#reset it, we need a short-term assessment
		np = [1, time.time() - (time.time() - np[1]) / np[0]]
	bot.memory['markov_randline_lastts'][trigger.sender] = np

@willie.module.interval(60)
def randspitline(bot):
	probdiv = bot.memory['markov_randline_probdiv']
	for chan in bot.memory['markov_randline_lastts']:
		chlt = bot.memory['markov_randline_lastts'][chan]
		if not chlt[0]:
			continue
		else:
			ntime = (time.time() - chlt[1]) / chlt[0]
			bot.memory['markov_randline_lastts'][chan] = [0, time.time()]
			prob = (ntime / probdiv)**1.3
			if random.random() <= prob:
				print(prob)
				bot.msg(chan, genline(bot))


@willie.module.rule('^[^.].*$')
def addline(bot, trigger):
	'''adds line to markov-chain DB'''
	#sys.stderr.write('{}: {} threads.\n'.format(time.time(), len(threading.enumerate())))
	if trigger.sender.lower() not in addwl:
		return
	sentence=trigger.group(0)
	try:
		db_mutex.acquire()
		with sqlite3.connect(bot.memory['markov_db']) as conn:
			db = Db(sqlite3.connect(bot.memory['markov_db']), Sql())
			Parser('', db, SENTENCE_SEPARATOR, WORD_SEPARATOR).parse(sentence)
			del db
	finally:
		db_mutex.release()
	try:
		firstword = sentence.split()[0]
	except IndexError:
		return
	bot.memory['markov_firstwordcache'][firstword] = bot.memory['markov_firstwordcache'].setdefault(firstword, 0) + 1

