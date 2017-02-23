#!/usr/bin/env python

import operator
import datetime
import diversity
from random import randint
import sys

# parameters
input_g = 0
investigation_mode = "explore" 		# can be "explore" or "exploit"
time_limit = 200 					# in miliseconds
k = 5								# number of returned records
input_file = "groups.dat"			# user group file
lowest_acceptable_similarity = 0.2
stop_visiting_once = False			# should the algorithm stop if it reaches the end of the index (i.e., scanning all records once)
buffer_activated = False			# should the algorithm prevent showing previsouly seen groups

# capture command-line parameters	
if sys.argv[1] == "buffer-reset":
	frest = open("buffer.dat","w")
	frest.close()
	print "- buffer is now empty!"
	exit()
try:
	input_g = int(sys.argv[1])
except:
	print "ERROR: group ID should be a number! \""+sys.argv[1]+"\" is given."
	exit()

# Note that in case of user group analysis, each group is a record. In case of spatiotemporal data, each geo point is a record.

# begin - list functions
def intersect(a, b):
    return list(set(a) & set(b))

def union(a, b):
    return list(set(a) | set(b))

def add_to_list(a, b):
	return list(a + b)
# end - list functions

# begin - retrieval functions
def get_distances_of(elements):
	# this function uses the glabal variables "k" and "distance_by_id[]"
	my_distances = []
	for i in range(0,k):
		my_distances.append(distance_by_id[elements[i]])
	return my_distances

def make_new_records(elements,new_element):
	# it updates the list of k elements with new_element. the position of the new element will be randomly chosen.
	# this functions uses the global variables "k" and "records[]"
	output= {}
	for i in range(0,k):
		output[i] = elements[i]
	replacement = randint(0,k-1)
	output[replacement] = records[new_element]
	return output

def is_inside(bigger_set, smaller_set):
	# it verifies the subset relationship between two groups.
	# if smaller_set is a subset of bigger_set, it returns True, otherwise False.
	for user in smaller_set:
		if user not in bigger_set:
			return False
	return True
# end - retrieval functions

# begin - variables
current_records = {}		# the ID of current k records will be recorded in this object.
new_records = {}			# ths ID of next potential k records will be recorded in this object.
total_time = 0.0			# total execution time
# end - variables

# begin - read buffer contents
my_buffer = []
if buffer_activated == True:
	buffer_file_read = open("buffer.dat")
	for group in buffer_file_read:
		group = group.strip()
		my_buffer.append(int(group))
# end - read buffer contents

# IUGA dimensions
# these two dictionaries will contain values of similarity and distance for each group.
# the key of these dictionaries is group_id
similarities = {}
distances = {}

# begin recording preprocessing time
# just for illustration purposes
preprocessing_begin_time = datetime.datetime.now()

# begin - read groups

# group file is given as "input_file". The structure of this file is enforced by LCM [Uno et al.].
# an autoincrement ID will be given to groups. The first group will be identified with "0".

# following dictionaries keep users, items and supports of groups.
# the key for dictionaries if group_id.
users_list = {}	# each element is itself a list of users.
items_list = {}	# each element is a string of items.
supports = {}	# each element is a number.

group_cnt = 0	# autoincrement counter for group_id
f = open(input_file)
for line in f:
	line = line.strip()
	open_par = 0
	close_par = 0
	for i in range(0,len(line)):
		if line[i] == "(" and str.isdigit(line[i+1]) == True:
			open_par = i
		if line[i] == ")" and str.isdigit(line[i-1]) == True:
			close_par = i
	items = line[0:open_par]
	users = line[close_par+1:].split(",")
	try:
		my_support = int(line[open_par+1:close_par])
	except:
		my_support = 0
	for i in range(0,len(users)):
		users[i] = users[i].strip()
	users_list[group_cnt] = users
	items_list[group_cnt] = items
	supports[group_cnt] = my_support
	group_cnt += 1
# end - read group

# begin - compute similarities
input_users = users_list[input_g]
for i in range(0,group_cnt):
	if i == input_g:
		continue
	users1 = users_list[i]
	if investigation_mode == "exploit" and is_inside(input_users, users1) == False:
		continue
	if i in my_buffer:
		continue
	my_intersect = intersect(users1,input_users)
	my_union = union(users1,input_users)
	sim = round(float(len(my_intersect)) / float(len(my_union)),2)
	similarities[i] = sim
# end - compute similarities

# sorting similarities in descending order
similarities_sorted = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)

# begin - prepare lists for easy retrieval
# the dictionary "records" contains group_id in descending order of their similarity. Key is autoincrement.
# the dictionary "similarity_by_id" contains similarity value. Key is group_id.
records = {}
similarity_by_id = {}
distance_by_id = {}

cnt = 0
for value in similarities_sorted:
	records[cnt] = value[0]
	similarity_by_id[value[0]] = value[1]
	cnt += 1
# end - prepare lists for easy retrieval

preprocessing_end_time = datetime.datetime.now()
preprocessing_duration = (preprocessing_end_time - preprocessing_begin_time).microseconds / 1000.0

print "- input group: " + items_list[input_g] + "("+str(supports[input_g])+" members)"
print "- " + str(len(records))+" records retrieved and indexed. (in "+str(preprocessing_duration)+ " ms)"
if len(records) <= max(k,10):
	print "ERROR: not enough groups found! Try another group or change the investigation mode."
	exit()
print "- mode set to "+ investigation_mode+"."
if buffer_activated == True:
	print "- buffer is activated. Previsouly seen groups won't be shown again."
print

	
# initialization by k most similar records
for i in range(0,k):
	current_records[i]=records[i]

# greedy algorithm
pointer = k-1
nb_iterations = 1
nb_lookups = 0
while total_time < time_limit and pointer < len(records):
	nb_lookups += 1
	# if pointer == len(records)-1:
		# pointer = 0
		# continue
	pointer += 1
	redundancy_flag = False
	for i in range(0,k):
		if current_records[i] == records[pointer]:
			redundancy_flag = True
			break
	if redundancy_flag == True:
		continue
	begin_time = datetime.datetime.now()
	all_users1 = []
	for i in range(0,k):
		all_users1 +=  users_list[current_records[i]]
	current_diversity = diversity.diversity(all_users1)
	new_records = make_new_records(current_records, pointer)
	all_users2 = []
	for i in range(0,k):
		all_users2 +=  users_list[new_records[i]]
	new_diversity = diversity.diversity(all_users2)
	if new_diversity > current_diversity:
		current_records = new_records
	end_time = datetime.datetime.now()
	duration = (end_time - begin_time).microseconds / 1000.0
	total_time += duration
	if similarity_by_id[records[pointer]] < lowest_acceptable_similarity:
		if stop_visiting_once == False:
			pointer = k
			nb_iterations += 1
		else:
			break

# begin - output result to stdout
buffer_file_append = open("buffer.dat","a")
for i in range(0,k):
	print str(i+1)+". G"+str(current_records[i])+": "+items_list[current_records[i]]+"("+str(supports[current_records[i]])+" members)"
	if buffer_activated == True:
		buffer_file_append.write(str(current_records[i])+"\n")

# compute diversity of the final result
all_users = []
for i in range(0,k):
	all_users +=  users_list[current_records[i]]
current_diversity = diversity.diversity(all_users)
print "- diversity: " + str(round(current_diversity,2)) + " (1.0 being the most diverse)"

# compute average similarity of the final result
max_sims = 0
for i in range(0,k):
	if similarity_by_id[current_records[i]] > max_sims:
		max_sims = similarity_by_id[current_records[i]]
print "- similarity stopped at " + str(round(max_sims,2))+" (limit bound: "+str(lowest_acceptable_similarity)+")"

print
print "- execution time (ms)", total_time
print "- nb. lookups", nb_lookups
print "- nb. iterations", nb_iterations
# end - output result to stdout