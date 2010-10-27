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
newLenderSearch = 'http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest'
newLendersRange = simplejson(urllib.urlopen(newLenderSearch).read())['paging']['pages']
potentialMembers = []
for i in range(10):
    #newPotentialMembers = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/lenders/search.json?q=' + queryString + '&sort_by=newest&page=' + str(i+1)).read()['lenders']
    pass
    for j in newPotentialMembers:
        lenderID = j['uid']
        potentialMembers.append(lenderID)
print potentialMembers
mormonsRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read())['paging']['pages']
mormons = []
for i in range(mormonsRange):
    newMormons = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?page=' + str(i+1)).read())['lenders']
    for j in newMormons:
        newLenderID = j['uid']
        mormons.append(newLenderID)
#print mormons 
