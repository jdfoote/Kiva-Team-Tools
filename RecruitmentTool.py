#!/usr/bin/python
import urllib
import simplejson
import webbrowser

#Get the recent lenders and sent invites list
try:
    f = open('lendersList.txt','r') # Opens the text file
    lenders = eval(f.read()) # Converts the string to a list
    f.close() # Closes the file
except IOError:
    lenders = []
    print "File doesn't exist"

try:
    f = open('teamList.txt','r')
    team = eval(f.read())
    f.close()
except IOError:
    team = []
    print "File doesn't exist"
    
try:
    f = open('invitesSentList.txt','r')
    inviteSent = eval(f.read())
    f.close()
except IOError:
    inviteSent = []
    print "File doesn't exist"

def getLenders(query,recruitsNeeded):
	print 'Starting query ' + query
	totalPages = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/lenders/search.json?country_code=US&q=' + query + '&sort_by=newest').read())['paging']['pages']
	print 'Total Pages: ' + totalPages
	i = 1
	while i <= totalPages and recruitsNeeded > 0:
		urlStr = 'http://api.kivaws.org/v1/lenders/search.json?country_code=US&q=' + query + '&sort_by=newest&page=' + str(i)
		# Get the lenders on this page
		newLenders = simplejson.loads(urllib.urlopen(urlStr).read())['lenders']
		print 'Page: ' + str(i)
		i = i+1
		for j in newLenders:
# Get the uid for the lender
		    lenderID = j['uid']
		    # Make sure they aren't already on the list
   		    if lenderID not in lenders:
				lenders.append(lenderID)
 	       	    if lenderID not in team: # Make sure the new lender isn't on the team
				if lenderID not in inviteSent and recruitsNeeded > 0: # Make sure the new lender hasn't already been invited, and that we still need recruits
					print 'Potential Recruit: ' + lenderID
					webbrowser.open("http://www.kiva.org/lender/" + lenderID) # This opens a browser window for each lender's page, so that a message can be sent.
					inviteSent.append(lenderID)
					recruitsNeeded -= 1
					print 'Recruits Left: ' + str(recruitsNeeded)
	# Returns how many people are still needed
	return recruitsNeeded 


# Get all of the recent team members
def getNewTeamMembers(teamID, stillNeeded):
	inTeamCount = 0
	membersAdded = 0
	teamRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/' + str(teamID) + '/lenders.json').read())['paging']['pages']
	i = teamRange
	# The API sorts by newest (broken right now, so I'm reversing it), so we should always be able to stop when we hit someone that we've seen before, but just in case they leave the team and then come back, we wait until we've seen 5 of them on one page.
	while i >= 1 and inTeamCount < 5:
		newTeamMembers = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/' + str(teamID) + '/lenders.json?sort_by=oldest&page=' + str(i)).read())['lenders']
		i -= 1
		inTeamCount = 0
		for j in newTeamMembers:
			memberID = j['uid']
			if memberID not in team:
				team.append(memberID)
				webbrowser.open("http://www.kiva.org/lender/" + memberID) # This opens a browser window for each lender's page, so that a message can be sent.
				print 'New Team Member: ' + memberID
				membersAdded += 1
				stillNeeded -= 1
			else:
				inTeamCount += 1
	# Returns the number of people added, and how many emails are left
	memberResults = {'newMembers': membersAdded, 'emailsLeft': stillNeeded}
	return memberResults
				
emailsAllowed = 25
teamID = 96
memberResults = getNewTeamMembers(teamID, emailsAllowed)
print 'New Team Members: ' + str(memberResults['newMembers'])
stillNeeded = getLenders('Utah',memberResults['emailsLeft'])
getLenders('UT',stillNeeded)

# Write the new UIDs to the docs
s = str(lenders)
f = open('lendersList.txt', 'w')
f.write(s)
f.close()

s = str(team)
f = open('teamList.txt', 'w')
f.write(s)
f.close()

s = str(inviteSent)
f = open('invitesSentList.txt', 'w')
f.write(s)
f.close()
