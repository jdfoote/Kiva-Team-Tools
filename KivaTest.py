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
    f = open('last5Lenders.txt','r') # Opens the text file
    lastFiveLenders = eval(f.read()) # Converts the string to a list
    print lastFiveLenders
    f.close() # Closes the file
except IOError:
    lastFiveLenders = ''
    print "File doesn't exist"

try:
    f = open('last5Mormons.txt','r')
    lastFiveMormons = eval(f.read())
    print lastFiveMormons
    f.close()
except IOError:
    lastFiveMormons = ''
    print "File doesn't exist"
    
try:
    f = open('invitesSentList.txt','r')
    inviteSent = eval(f.read())
    f.close()
    print inviteSent
except IOError:
    inviteSent = ''
    print "File doesn't exist"


# Get all of the recent lenders
newLendersRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest').read())['paging']['pages']
lenders = []
i = 1
while i <= newLendersRange:
    urlStr = 'http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest&page=' + str(i) # Load each of the pages
    newLenders = simplejson.loads(urllib.urlopen(urlStr).read())['lenders']
    i = i+1
    for j in newLenders:
        lenderID = j['uid']
	if lenderID not in lastFiveLenders:
		lenders.append(lenderID)

	else:
		i = newLendersRange + 1 # This is a hack to end the while loop. I don't know how to end it correctly.
		break

# Get all of the recent Mormons
mormonsRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read())['paging']['pages']
mormons = []
i = 1
while i <= mormonsRange:
    newMormons = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?sort_by=newest&page=' + str(i)).read())['lenders']
    i=i+1
    for j in newMormons:
		mormonID = j['uid']        
		if mormonID not in lastFiveMormons:
			mormons.append(mormonID)
		else:
			i = mormonsRange + 1
			break

#Compare the recent lenders and the recent Mormons
k = 0
for i in lenders:
		if i not in mormons:
			if i not in inviteSent:
				print 'Potential Recruit: ' + i
				k = k+1
				if k <= 25:
					webbrowser.open("http://www.kiva.org/lender/" + i) # This opens a browser window for each lender's page, so that a message can be sent. We can activate this when we are sure everything is working correctly.
					inviteSent.append(i)
					
## NEXT LENDER: matthew3477					

# Write the 5 most recent UIDs to the docs
s = str(lenders[:5])
f = open('last5Lenders.txt', 'w')
f.write(s)
f.close()

s = str(mormons[:5])
f = open('last5Mormons.txt', 'w')
f.write(s)
f.close()

s = str(inviteSent)
f = open('invitesSentList.txt', 'w')
f.write(s)
f.close()
