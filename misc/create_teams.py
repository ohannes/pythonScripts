# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.environ["ohannes"])
from ohannes import *
from random import randint

comment = "#"
dummy_member = " "
number_of_dummy_members = 0
default_member_per_team  = 6
default_output_file_name = "created_teams"
output_file_name_recursive = 1

input_file_name = getStrArg(1, 1)

if len(sys.argv) > 2:
	member_per_team = getIntArg(2, 2)
else:
	member_per_team = default_member_per_team
	print "Empty argument for member per team: default value", member_per_team, "will be used"

if len(sys.argv) > 3:
	output_file_name_recursive = getIntArg(3, 3)

team_names = 	[
					"Dulkadiroğulları",
					"Germiyanoğulları",
					"Karesioğulları",
					"Karamanoğulları",
					"Saruhanoğulları",
					"Candaroğulları"
				]

def getRandomIndex(max_length, used_indexes):
	random_number = randint(0, max_length)
	while random_number in used_indexes:
		random_number = randint(0, max_length)
	return random_number
	
def getOutputFileName():
	global default_output_file_name
	file_name = default_output_file_name
	index = 0
	while os.path.exists(file_name):
		file_name = default_output_file_name + str(index)
		index += 1
	return file_name

used_indexes = []
members = []
teams = []

lines = getFileLines(input_file_name)

for line in lines:
	if line[0] != comment:
		members.append(line[:-1])

while len(members) % member_per_team:
	print "number of members is being regulated by number of member per team"
	members.append(dummy_member)
	number_of_dummy_members += 1
	
number_of_members = len(members)
number_of_teams = len(members) / member_per_team

#while number_of_dummy_members > number_of_teams:
#	print "member per team is being regulated by number of dummy members"
#	member_per_team -= 1
#	number_of_teams = len(members) / member_per_team

#print "number of members:", number_of_members
#print "number of teams:", number_of_teams

for i in range(number_of_teams):
	empty_array = []
	teams.append(empty_array)

for i in range(member_per_team):
	for j in range(number_of_teams):
		random_index = getRandomIndex(number_of_members-1, used_indexes)
		random_member = members[random_index]
		while random_member == dummy_member and dummy_member in teams[j]:
			random_index = getRandomIndex(number_of_members-1, used_indexes)
			random_member = members[random_index]
		#print "random index:", random_index
		#print "random member:", random_member
		used_indexes.append(random_index)
		teams[j].append(random_member)

#if len(team_names) < number_of_teams:
#	sys.exit("ERROR: not enough team names " + str(len(team_names)) + "/" + str(number_of_teams))

if output_file_name_recursive > 0:
	output_file_name = getOutputFileName()
else:
	output_file_name = default_output_file_name
ftw = open(output_file_name, "w")
for i in range(number_of_teams):
	if i > len(team_names) - 1:
		ftw.write("Team " + str(i) + "\n")
	else:
		ftw.write(team_names[i] + "\n")
	for member in teams[i]:
		ftw.write("\t" + member + "\n")
	ftw.write("\n")
ftw.close()

print "number of members:", number_of_members - number_of_dummy_members
print "member per team:", member_per_team
print "number of teams:", number_of_teams

print "output file:", output_file_name
