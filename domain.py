#!/usr/bin/python
# -*- coding:utf8 -*-

import urllib2
import re
import os
import argparse
import signal
import sys
import time

search_api = r"http://pandavip.www.net.cn/check/check_ac1.cgi?domain=%s"
available_mark = u"domain name is available"
too_fast_mark = u"query frequency is too high, please try again later"
exist_mark = u"domain exists"
domain_counter = 0
domain_available_counter = 0
only_one_domain = None
target_domain = u'.com'
save_file = u'com'
fail_file = u'fail'
exist_file = u"exist"
prefix = u''
suffix = u''
max_length = 5
log_exist_domain_name = False
keep_working = True

try_agagin = False
each_time_sleep = 1
time_sleep = 30
time_step = 5

retry_fail = False
retry_file = u'fial'

start_domain = None

alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
	'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
alphabet_str = 'abcdefghijklmnopqrstuvwxyz'
counter_list = []
current_point = 0

header = r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'

def init_args():
	global only_one_domain, target_domain, save_file, prefix, suffix, max_length, log_exist_domain_name, each_time_sleep, time_sleep, time_step, current_point, retry_fail, retry_file, start_domain
	parse = argparse.ArgumentParser()
	parse.add_argument('-n', '--name', dest='name', type=str,
		nargs='?', const=None, default=None,
		help=u"Only search one domain name.")
	parse.add_argument('-d', '--domain', dest='domain', type=str,
		nargs='?', const=u'.com', default=u'.com',
		help=u"The target domain, default is '.com' .")
	parse.add_argument('-f', '--file', dest='savefile', type=str,
		nargs='?', const=None, default=None,
		help=u'The file to save the result.')
	parse.add_argument('-p', '--prefix', dest='prefix', type=str,
		nargs='?', const=u'', default=u'',
		help=u'The prefix string for domain name.')
	parse.add_argument('-s', '--suffix', dest='suffix', type=str,
		nargs='?', const=u'', default=u'',
		help=u"The suffix string for domain name.")
	parse.add_argument('-m', '--max', dest='maxlength', type=int,
		nargs='?', const=5, default=5,
		help=u"The max dynamic length name to search, default is 5.")
	parse.add_argument('-l', '--log', dest='logexist', action='store_true', default=False,
		help=u"Log the existed domain name, default is false.")
	parse.add_argument('-t', '--timesleep', dest='timesleep', type=int,
		nargs='?', const=30, default=30,
		help=u"When checking too fast, the sleep time. Default is 30s.")
	parse.add_argument('--timestep', dest='timestep', type=int,
		nargs='?', const=5, default=5, 
		help=u"The second times checking too fast, sleep time will add time step.Default time step is 5s.")
	parse.add_argument('-e', '--eachsleep', dest='eachsleep', type=int,
		nargs='?', const=1, default=1,
		help=u"Checking every domain name's sleep time.Default is 1s.")
	parse.add_argument('--startpoint', dest='startpoint', type=int,
		nargs='?', const=0, default=0,
		help=u"The start domain name's length.")
	parse.add_argument('--retryfail', dest='retryfail', action='store_true', default=False,
		help=u"Retry the fail domain name of last checking.Default is false")
	parse.add_argument('--retryfile', dest='retryfile', type=str,
		nargs='?', const=u'fail', default=u'fail',
		help=u"Use the retry fail file data.Default is the 'fail'.")
	parse.add_argument('--startdomain', dest='startdomain', type=str,
		nargs='?', const=None, default=None,
		help=u"The start domain format.")
	args = parse.parse_args()
	only_one_domain = args.name
	target_domain = args.domain
	save_file = args.savefile
	prefix = args.prefix
	suffix = args.suffix
	max_length = args.maxlength
	log_exist_domain_name = args.logexist
	each_time_sleep = args.eachsleep
	time_sleep = args.timesleep
	time_step = args.timestep
	current_point = args.startpoint
	retry_fail = args.retryfail
	retry_file = args.retryfile
	start_domain = args.startdomain
	if not target_domain.startswith(u'.'):
		target_domain = u'.' + target_domain
	if save_file is None:
		save_file = target_domain.split(u'.')[-1]
	if (only_one_domain is not None) and (only_one_domain.find(u'.') == -1):
		only_one_domain = only_one_domain + target_domain
	if current_point >= max_length:
		current_point = 0
	print(u"\n======================================================================")
	print(u"Progress Setting:")
	print(u"Target domain is %s" % target_domain)
	print(u"Save file is %s" % save_file)
	print(u"Prefix string is %s" % prefix)
	print(u"Suffix string is %s" % suffix)
	print(u"Max length is %s" % max_length)
	print(u"Current point is %s" % current_point)
	print(u"Log existed domain name? %s" % log_exist_domain_name)
	print(u"Sleep time is %s s" % time_sleep)
	print(u"Sleep time step is %s s" % time_step)
	print(u"Each sleep time is %s s" % each_time_sleep)
	print(u"You can press Ctrl+C to exit progress.")
	print(u"======================================================================\n")

def init_env():
	global save_file, fail_file, max_length, current_point, counter_list, retry_file, exist_file, start_domain, alphabet_str
	reload(sys)
	sys.setdefaultencoding('utf-8')
	current_path = os.getcwd()
	data_path = os.path.join(current_path, u"result")
	if not os.path.isdir(data_path):
		os.mkdir(data_path)
	save_file = os.path.join(data_path, save_file)
	fail_file = os.path.join(data_path, fail_file)
	retry_file = os.path.join(data_path, retry_file)
	exist_file = os.path.join(data_path, exist_file)
	counter_list = []
	for i in range(max_length):
		if i == 0:
			counter_list.append(-1)
		else:
			counter_list.append(0)
	if (start_domain is not None) and (len(start_domain) <= max_length):
		for index in range(len(start_domain)):
			counter_list[index] = alphabet_str.find(start_domain[index])
			if counter_list[index] == -1:
				counter_list[index] = 0
		current_point = len(start_domain) - 1
		if current_point < 0:
			current_point = 0
	elif current_point > 0:
		counter_list[0] = 0
#	print(u"counter_list is %s" % counter_list) 

def signal_handler(signum, frame):
	global keep_working
	keep_working = False
	print(u"\nStart finish the last progress and will auto exit...\n")

def get_current_time_string():
	return time.strftime(u"[%Y-%m-%d %H:%M:%S]", time.localtime())

def get_domain_log(domain_name, msg):
	return time.strftime(u"[%Y-%m-%d %H:%M:%S]", time.localtime()) + domain_name + u' - ' + msg

def get_domain_from_log(msg):
	return msg.split(']')[1].split(' - ')[0]

def append_line_to_file(filename, data):
	try:
		with open(filename, 'a') as append_file:
			append_file.write(data + u'\n')
	except:
		print(get_current_time_string() + u"Sorry!Save %s to %s fail." % (data, filename))

def next_domain_name():
	global max_length, current_point, counter_list, alphabet, prefix, suffix, target_domain
	target_point = current_point
	target_name = u''
	while target_point >= 0:
		if counter_list[target_point] < 25:
			break
		target_point = target_point - 1
	if target_point == -1:
		current_point = current_point + 1
		if current_point >= max_length:
			return None
		else:
			for index in range(current_point):
				counter_list[index] = 0
	else:
		counter_list[target_point] = counter_list[target_point] + 1
		if target_point < current_point:
			for index in range(target_point + 1, current_point + 1):
				counter_list[index] = 0		
	for index in range(current_point + 1):
		target_name = target_name + alphabet[counter_list[index]]
	return prefix + target_name + suffix + target_domain

def check_domain_name(domain_name):
	global keep_working, search_api, available_mark, too_fast_mark, exist_mark, try_again, time_sleep, time_step, domain_counter, domain_available_counter, log_exist_domain_name, exist_file, save_file, fail_file
	url = search_api % domain_name
	domain_counter = domain_counter + 1
	need_try_again = True
	try:
		while keep_working and need_try_again:
			result = urllib2.urlopen(url, timeout=30).read().lower()
			if result.find(exist_mark) >= 0:
				if log_exist_domain_name:
					print(get_domain_log(domain_name, u"existed"))
				append_line_to_file(exist_file, get_domain_log(domain_name, u"existed"))
				need_try_again = False
				try_again = False
				return False
			elif result.find(available_mark) >= 0:
				domain_available_counter = domain_available_counter + 1
				print(get_domain_log(domain_name, u"available"))
				append_line_to_file(save_file, get_domain_log(domain_name, u"available")) 
				need_try_again = False
				try_again = False
				return True
			elif result.find(too_fast_mark) >= 0:
				if try_again:
					time_sleep = time_sleep + time_step
				print(get_currrent_time_string() + u"checking to fast, sleep %s s" % time_sleep)
				time.sleep(time_sleep)
				need_try_again = True
				try_again = True
			else:
				print(get_current_time_string() + u"check %s happen unknow problem:" % domain_name)
				print(result)
				append_line_to_line(fail_file, get_domain_log(domain_name, result))
				need_try_again = False
				try_again = False
				return False 
	except:
		print(get_current_time_string() + u"Sorry, check %s fail." % domain_name)
		append_line_to_file(fail_file, get_domain_log(domain_name, u"other error."))
		return False

def start_progress():
	global keep_working, domain_counter, domain_available_counter, each_time_sleep
	keep_working = True
	while keep_working:
		check_name = next_domain_name()
		if check_name is None:
			keep_working = False
		else:
			check_domain_name(check_name)
			time.sleep(each_time_sleep)
	else:
		print(u"======================================")
		print(u"Checking progress finished.")
		print(u"All checing %s domain name." % domain_counter)
		print(u"Get %s available domain name." % domain_available_counter)
		print(u"======================================")


init_args()
init_env()
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)
#signal.signal(signal.SIGKILL, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
if only_one_domain is not None:
	log_exist_domain_name = True
	check_domain_name(only_one_domain)
elif retry_fail:
	try:
		log_exist_domain_name = True
		retry_list = []
		with open(retry_file, 'r') as data:
			for line in data:
				retry_list.append(line)
		for item in retry_list: 
			if keep_working:
				check_domain_name(get_domain_from_log(item))
				time.sleep(each_time_sleep)
			else:
				break
		print(u"========================================")
		print(u"Retry fail domain name done.")
		print(u"All checing %s domain name." % domain_counter)
		print(u"Get %s available domain name." % domain_available_counter)
		print(u"========================================")
	except KeyboardInterrupt:
		print(u"Unnatural exit.")
	except:
		print(u"Sorry!Retry fail.")
	else:
		print(u"GoodBye!")
else:
	try:
		start_progress()
	except KeyboardInterrupt:
		print(u"Unnatural exit.")
	except:
		print(u"Unkown exception.")
	else:
		print(u"Goodbye.")

