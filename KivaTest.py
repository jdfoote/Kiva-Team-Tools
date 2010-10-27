# So far, this just grabs the first page of data from each of the searches that we want. The next step is to append the next pages to the list.

import urllib
import simplejson
# queryString = 'Utah'
# newLenderSearch = 'http://api.kivaws.org/v1/lenders/search.json?q=' + queryString
# newLendersJSON = urllib.urlopen(newLenderSearch).read()
# newLenders = simplejson.loads(newLendersJSON)['lenders'] # Gets list of new lenders
mormonsRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read())['paging']['pages']
mormons = []
for i in range(mormonsRange):
<<<<<<< HEAD
	newMormons = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?page=' + str(i+1)).read())['lenders']
	for j in newMormons:
		new = j['uid']
		mormons.extend(new)
=======
	newJSON = urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?page=' + str(i+1)).read()
	new = simplejson.loads(newJSON)['lenders']
	mormons.extend(new)
>>>>>>> 1fc01c0c7e6fff05b1efb501a9f1738a7e60845b
print mormons
