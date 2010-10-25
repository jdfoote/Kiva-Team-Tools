# So far, this just grabs the first page of data from each of the searches that we want. The next step is to append the next pages to the list.

import urllib
import simplejson
mormonsJSON = urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read() # Get the names of the Kiva Mormons members.
newLenderSearch = 'http://api.kivaws.org/v1/lenders/search.json?q=Utah'
newLendersJSON = urllib.urlopen(newLenderSearch).read()
mormons = simplejson.loads(mormonsJSON)['lenders'] # Gets list of lenders from Kiva Mormons team. 
newLenders = simplejson.loads(newLendersJSON)['lenders'] # Gets list of new lenders
for s in newLenders:
	print s
