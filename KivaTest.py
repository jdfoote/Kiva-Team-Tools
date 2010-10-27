# So far, this just grabs the first page of data from each of the searches that we want. The next step is to append the next pages to the list.

import urllib
import simplejson
try:
        f = open('last5lenders.txt')
        topFiveUsers = f.read()
        print topFiveUsers
        f.close()
except IOError:
        topFiveUsers = ''
        print "File doesn't exist"
queryString = 'Utah'
newLenderSearch = 'http://api.kivaws.org/v1/lenders/search.json?q=' + queryString
print newLenderSearch
newLendersRange = simplejson.loads(urllib.urlopen(newLenderSearch))['paging']['pages'] 
print newLenderRange
mormonsRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read())['paging']['pages']
potentialMembers = []
for i in range(newLendersRange):
	newPotentialMembers = simplejson.loads(urllib.urlopen(newLenderSearch + '&page=' + str(i+1)).read())['lenders']
	for j in newPotentialMembers:
		lenderID = j['uid']
		potentialMembers.append(lenderID)
print potentialMembers
mormons = []
for i in range(mormonsRange):
	newMormons = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?page=' + str(i+1)).read())['lenders']
	for j in newMormons:
		newLenderID = j['uid']
		mormons.append(newLenderID)
