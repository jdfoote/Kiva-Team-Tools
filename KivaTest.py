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
	newJSON = urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?page=' + str(i+1)).read()
	new = simplejson.loads(newJSON)['lenders']
	mormons.extend(new)
print mormons
