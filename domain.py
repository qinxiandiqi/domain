#!/usr/bin/python
# -*- coding:utf8 -*-

import urllib2
import re
import os
import argparse
import signal
import sys

search_api = r"http://pandavip.www.net.cn/check/check_ac1.cgi?domain=%s"
available_mark = u"domain name is available"
domain_counter = 0
domain_available_counter = 0
only_one_domain = None
target_domain = u'.com'
save_file = u'com'
prefix = u''
suffix = u''
max_length = 5
log_exist_domain_name = False
keep_working = True

alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
	'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
available_domain_name_list = []
counter_list = []
current_point = 0

header = r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'

def init_args():
	global only_one_domain, target_domain, save_file, prefix, suffix, max_length, log_exist_domain_name 
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
	args = parse.parse_args()
	only_one_domain = args.name
	target_domain = args.domain
	save_file = args.savefile
	prefix = args.prefix
	suffix = args.suffix
	max_length = args.maxlength
	log_exist_domain_name = args.logexist
	if not target_domain.startswith(u'.'):
		target_domain = u'.' + target_domain
	if save_file is None:
		save_file = target_domain.split(u'.')[-1]
	if (only_one_domain is not None) and (only_one_domain.find(u'.') == -1):
		only_one_domain = only_one_domain + target_domain
	print(u"\n======================================================================")
	print(u"Progress Setting:")
	print(u"Target domain is %s" % target_domain)
	print(u"Save file is %s" % save_file)
	print(u"Prefix string is %s" % prefix)
	print(u"Suffix string is %s" % suffix)
	print(u"Max length is %s" % max_length)
	print(u"Log existed domain name? %s" % log_exist_domain_name)
	print(u"You can press Ctrl+Z to exit progress.")
	print(u"======================================================================\n")

def init_env():
	global save_file, max_length, current_point, counter_list 
	reload(sys)
	sys.setdefaultencoding('utf-8')
	current_path = os.getcwd()
	data_path = os.path.join(current_path, u"result")
	if not os.path.isdir(data_path):
		os.mkdir(data_path)
	save_file = os.path.join(data_path, save_file)
	current_point = 0
	counter_list = []
	for i in range(max_length):
		if i == 0:
			counter_list.append(-1)
		else:
			counter_list.append(0)
	print(u"counter_list is %s" % counter_list) 

def signal_handler(signum, frame):
	global keep_working
	keep_working = False
	print(u"\nStart finish the last progress and will auto exit...\n")

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
	global search_api, available_mark, domain_counter, domain_available_counter, log_exist_domain_name
	url = search_api % domain_name
	domain_counter = domain_counter + 1
	try:
		result = urllib2.urlopen(url, timeout=30).read()
		if result.lower().find(available_mark) == -1:
			if log_exist_domain_name:
				print(u"%s is existed" % domain_name)
			return False
		else:
			domain_available_counter = domain_available_counter + 1
			print(u"%s is avaiable." % domain_name)
			return True
	except:
		print(u"Sorry, check %s fail." % domain_name)
		return False

def start_progress():
	global keep_working, available_domain_name_list, domain_counter, domain_available_counter
	keep_working = True
	while keep_working:
		check_name = next_domain_name()
		if check_name is None:
			keep_working = False
		else:
			if check_domain_name(check_name):
				available_domain_name_list.append(check_name)
	else:
		print(u"======================================")
		print(u"Checking progress finished.")
		print(u"All checing %s domain name." % domain_counter)
		print(u"Get %s available domain name." % domain_available_counter)
		print(u"======================================")

def save_domain_file():
	global save_file, available_domain_name_list
	try:
		with open(save_file, 'w') as domain_file:
			for name in available_domain_name_list:
				domain_file.write(name + '\n')
	except:
		print(u"Sorry! Save domain name file fail.")
	else:
		print(u"Save domain name file success.")

init_args()
init_env()
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)
if only_one_domain is None:
	try:
		start_progress()
	except KeyboardInterrupt:
		save_domain_file()
		print(u"Unnatural exit.")
	except:
		save_domain_file()
		print(u"Unkown exception.")
	else:
		save_domain_file()
		print(u"Goodbye.")
else:
	log_exist_domain_name = True
	check_domain_name(only_one_domain)

