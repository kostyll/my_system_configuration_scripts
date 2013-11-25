#!/usr/bin/python

from __future__ import unicode_literals

from md5 import md5
import re
from collections import namedtuple
from datetime import datetime
SwitchRec = namedtuple('SwitchRec',"date time action title")

data_file = "/home/andrew/.qtile_history"
search_template = re.compile('\[(\d\d\d\d-\d\d-\d\d)\]\[(\d\d:\d\d:\d\d)\]\[\{(.*)\}(.*)\]')

raw_data = open(data_file,'rt').readlines()
data = []

for line in raw_data:
	line = line.decode('utf-8')
	# print (line)
	scan_result = search_template.search(line)
	rec = None
	if scan_result is not None:
		rec = SwitchRec(
			date = scan_result.groups()[0],
			time = scan_result.groups()[1],
			action = scan_result.groups()[2],
			title = scan_result.groups()[3]
		)
		# print (rec)
		if rec is not None:
			record = SwitchRec(
					date = datetime.strptime(rec.date,"%Y-%m-%d"),
					time = datetime.strptime(
							rec.date+"*"+rec.time,
							"%Y-%m-%d*%H:%M:%S"
						),
					action = rec.action,
					title = rec.title
				)
			#print record
			data.append(record)
		else:
			print "rec is none"
	else:
		pass
# print data

def get_title(item):
	return (
		item.title.replace(
					"'",
					''
				)
			)

def get_hash(item):
	return str(md5(get_title(item).encode('utf-8')).hexdigest())


def check_item (item):
	if len(item.title) != 0:
		if item.title is not None or item.title != '':
			return True
	return False

Item = namedtuple('Item',"title seconds")
items = {}

for item in data:
	if check_item(item):
		if not items.has_key(get_hash(item)):		
			item_key = get_hash(item)
			items.update(
				eval(
						"{'%s':Item(title='%s', seconds=0)}"% (
							item_key,
							get_title(
									item
								)
							)
					)
				)

seconds_sum = 0

def print_items_time():
	global seconds_sum
	seconds_sum = 0
	for key in items.keys():
		if isinstance(items[key],Item):
			seconds_sum += int(items[key].seconds)
			print (
					"Item [%s](%s): %s seconds" % (key,items[key].title,items[key].seconds)
				)
		else :
			print (
				"item [%s] = %s" % (
						key, 
						items[key]
					)
				)

def summarize_time():
	seconds_sum = 0
	for key in items.keys():
		if isinstance(items[key],Item):
			seconds_sum += int(items[key].seconds)
	return seconds_sum

def print_items_time_inpercent():
	global seconds_sum
	if seconds_sum == 0:
		seconds_sum = summarize_time()
		for key in items.keys():
			if isinstance(items[key],Item):
				print (
						"(%s): {%0.1f}%% in seconds %d | in minutes %d|in hours - %0.1f |[%s]" % (
								items[key].title,
								(items[key].seconds/float(seconds_sum)*100),
								items[key].seconds,
								items[key].seconds/60,
								items[key].seconds/3600.0,
								key,								
							)
					)
	else:
		print "U have to sumarize time before..."

			
# print_items_time()

for index, item in enumerate(data):
	if check_item(item):
		item_key = get_hash(data[index])
		try:
			delta = (data[index+1].time-data[index].time).seconds
		except:
			delta = 0
		if isinstance(items[item_key],Item):
			seconds = items[item_key].seconds
			title = items.get(item_key).title
			if seconds is not None:
				seconds += int(delta)
				items.update(
					eval(
							# "{'%s':%s}" % (get_hash(item),seconds)
							"{'%s':Item(title='%s', seconds=%s)}"% (
							get_hash(item),
							get_title(
									item
								),
							seconds
							)
						)
					)

# print_items_time()		
print_items_time_inpercent()