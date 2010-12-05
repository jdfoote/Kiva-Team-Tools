# I think that this is pretty close to being done.
# To Do:
# If possible, I would like to look into sending the messages through Python, or at least filling in the message field on the web page, but other than that, we're there. 
# Need to do some error checking, still. Maybe write some unit tests, but that might be overkill.
# Should also write out the UIDs that have been messaged, along with a timestamp?

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


# Get all of the recent lenders
newLendersRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest').read())['paging']['pages']
i = 1
while i <= newLendersRange:
    urlStr = 'http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest&page=' + str(i) # Load each of the pages
    newLenders = simplejson.loads(urllib.urlopen(urlStr).read())['lenders']
    i = i+1
    for j in newLenders:
        lenderID = j['uid']
	if lenderID not in lenders:
		lenders.append(lenderID)

	else:
		i = newLendersRange + 1 # This is a hack to end the while loop. I don't know how to end it correctly.
		break

# Get all of the recent team members
teamRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read())['paging']['pages']
i = 1
while i <= teamRange:
    newTeamMembers = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?sort_by=newest&page=' + str(i)).read())['lenders']
    i=i+1
    for j in newTeamMembers:
		memberID = j['uid']        
		if memberID not in team:
			team.append(memberID)
		else:
			i = teamRange + 1
			break

#Compare the recent new Kiva lenders with the team list and the inviteSent list
k = 0
for i in lenders:
		if i not in team:
			if i not in inviteSent:
				print 'Potential Recruit: ' + i
				k = k+1
				if k <= 25:
					webbrowser.open("http://www.kiva.org/lender/" + i) # This opens a browser window for each lender's page, so that a message can be sent.
					inviteSent.append(i)
								

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
