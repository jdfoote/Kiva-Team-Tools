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
newLenderSearch = 'http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest'
newLendersRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest').read())['paging']['pages']
potentialMembers = []
for i in range(newLendersRange):
    urlStr = 'http://api.kivaws.org/v1/lenders/search.json?q=Utah&sort_by=newest&page=' + str(i+1)
    newPotentialMembers = simplejson.loads(urllib.urlopen(urlStr).read())['lenders']
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
