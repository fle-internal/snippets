""" KEVIN NGO 
	FLE INTERNSHIP CHALLENGE! """

import random
import sys
### Function to print the members in alphabetical order ###
def printMembers(fleTeam):
	fleTeam = [x.upper() for x in fleTeam]
	fleTeam.sort()
	for member in fleTeam:
		print member
	print ""

### Function to update the team for groupings, by adding or removing ###
def updateList(update):
	update2 = update
	## ADDING ###
	while update:
		person = raw_input("Enter the name of a new FLE contributor: ")
		person = person.upper()
		fleTeam.append(person)
		printMembers(fleTeam)
		addCheck = raw_input("From this new list, do you still want to add (yes or no)? ")
		addCheck = addCheck.upper()
		while True:
			if addCheck == "NO":
				return
			elif addCheck == "YES":
				break
			else:
				addCheck = raw_input("Wrong command! Do you still want to add to the list?! (yes or no exactly) ")
				addCheck = addCheck.upper()	
	## DELETING ###
	while not update2:
		person = raw_input("Enter the name of an absent FLE contributor: ")
		person = person.upper()
		try:
			fleTeam.remove(person)
		except ValueError:
			print "Who is that?! " + person+" is not in the list!! Know your team man!"
			continue
		printMembers(fleTeam)
		removeCheck = raw_input("From this new list, do you still want to remove (yes or no)? ")
		removeCheck = removeCheck.upper()
		while True:
			if removeCheck == "NO":
				return
			elif removeCheck == "YES":
				break
			else:
				removeCheck = raw_input("Wrong command! Do you still want to remove to the list?! (yes or no exactly) ")
				removeCheck = removeCheck.upper()

### Function to distribute the last group amongst others if there is a heavy inbalance ###
def distributeLastGroup(groupNumber, numberOfPeople, leftOver):
	offset = 0
	print "---------------------------------------------------------------------------------------------" 	
	for i in range(groupNumber):
		print ""
		print "GROUP " + str(i+1) + ":" 
		for j in range(numberOfPeople):
			print fleTeam[offset]
			offset = offset + 1
		if leftOver > 0 and groupNumber != 1:
			print fleTeam[offset]
			offset = offset +1
			leftOver = leftOver -1
	#print the rest if there are some left
	for k in range(leftOver):
		print fleTeam[offset]
		offset = offset + 1
	#print fleTeam[offset]
	print "---------------------------------------------------------------------------------------------" 	

     
########################################## MAIN STARTS HERE #################################################################
print ""
print "Welcome to the FLE Pair/Group Generator! The current AWESOME team is: "
print " "
fleTeam = ["BEN", "DYLAN", "ELIZABETH", "GUAN", "JAMIE", "RICHARD", "RUI", "ARON", "KEVIN", "ANGELIQUE", "ANDRES"]
printMembers(fleTeam)
check = raw_input("In this list of " + str(len(fleTeam)) + " AWESOME people, is the list correct to generate groups (yes or no)? ")
check = check.upper()

while True:
		if check == "YES":
			break;

		elif check == "NO":
			check2 = raw_input("Do you want to remove or add from this AWESOME list? (add or remove) ")
			check2 = check2.upper()
			if check2 == "ADD":
				update = True
				updateList(update)
			elif check2 == "REMOVE":
				update = False
				updateList(update)
			else:
				print "You did not input a valid answer  ): (add or remove exactly)" 
				continue
			printMembers(fleTeam)
			check = raw_input("Is this FINAL AWESOME list correct to generate the groups (yes or no) ? ")
			check = check.upper()
			continue

		else:
			print "You did not input a valid answer! ): (yes or no exactly) "
			printMembers(fleTeam)
			check = raw_input("In this AWESOME list of " + str(len(fleTeam)) + " is it correct (yes or no)? ")
			check = check.upper()
			continue


### Beginning to distribute groups ###
while True:
	try:
		numberOfPeople = raw_input("How many people are in a group? (This must be less than " + str(len(fleTeam)) + "): ")
		numberOfPeople = int(numberOfPeople)
		break
	except ValueError:
		print "Enter a Number!! Stop being careless!"

leftOver = len(fleTeam)%numberOfPeople
groupNumber = len(fleTeam)/numberOfPeople
random.shuffle(fleTeam)
print " "
if leftOver == 0: 	
	print str(groupNumber) + " AWESOME groups were generated with " + str(numberOfPeople) + " AWESOME people (give or take " + str(leftOver) + " people)" 
else:
	print str(groupNumber +1 ) + " AWESOME groups were generated with " + str(numberOfPeople) + " AWESOME people (give or take " + str(leftOver) + " people)" 
print "---------------------------------------------------------------------------------------------" 	

### Printing out the Groups ###
offset = 0
offset2 = 0
for i in range(groupNumber):
	print "GROUP " + str(i+1) + ":" 
	for j in range(numberOfPeople):
		print fleTeam[offset]
		offset = offset + 1
	print " "
	offfset2 = offset
if leftOver != 0:
	print "GROUP " + str(groupNumber+1) + " is the remaining people:"
	for k in range(leftOver):
		print fleTeam[offset]
		offset = offset + 1
print "---------------------------------------------------------------------------------------------" 	

if leftOver == 0:
	print "YAY! You're done with the group generator! FLE RULES!"
	sys.exit()
## Final Steps to see if the groups are okay ###
distribute = raw_input("Do you want to distribute the last group between the other groups?? ")
distribute = distribute.upper()
while True:
	if distribute == "NO":
		print "YAY! You're done with the group generator! FLE RULES!"
		sys.exit()
	elif distribute == "YES":
		distributeLastGroup(groupNumber, numberOfPeople, leftOver)
		print "YAY! You're done with the group generator! FLE RULES!"
		sys.exit()
	else:
		distribute = raw_input("Wrong command! Do you want to distribute the remaining people to even out the groups?! (yes or no exactly) ")
		distribute = distribute.upper()













