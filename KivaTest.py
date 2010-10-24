import urllib
import simplejson
data = urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read()
testdata = simplejson.loads(data)
l = testdata['lenders']
for i in range(len(l)):
	f = l[i]
	w = i['whereabouts']
	print 'Location' w
