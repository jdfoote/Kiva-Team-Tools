import string
import urllib2
import simplejson

# This may be used in the future, to get a specific list of teams. The downside is that this wouldn't give us ranking info.
def getTeams(listOfTeams):
	'''Given a list of team IDs, returns a list of dictionaries with team information'''
	stringList = [str(i) for i in listOfTeams]
	teamInfo = []
	start = 0 # First team to get
	end = 20 # Last team to get in first run of the API
	while start < len(listOfTeams):
		teamList = ','.join(stringList[start:end])
		urlStr = 'http://api.kivaws.org/v1/teams/' + teamList + '.json'
		content = simplejson.loads(urllib2.urlopen(urlStr).read())
		newTeams = content['teams']
		start += 20 # Add 20 to the parameters, and get the next set of teams.
		end += 20
		for team in newTeams:
			teamInfo.append(team)
	return teamInfo

def getRankedTeams(numberOfTeams):
	'''Returns a list of dictionaries with team information for the top n teams'''
	keepGoing = 'true'
	rankedTeams = [] # Will store the info for all of the teams
	i = 1
	while keepGoing == 'true':
			urlStr = 'http://api.kivaws.org/v1/teams/search.json&sort_by=loaned_amount&page=' + str(i)
			try:
				response = urllib2.urlopen(urlStr)
				content = simplejson.loads(response.read())
				newTeams = content['teams']
				i += 1
				for team in newTeams:
					# Stop when we hit the number of teams requested
					if len(rankedTeams) < numberOfTeams:
						rankedTeams.append(team)
					else:
						keepGoing = 'false'
						break
			except URLError, e:
				if hasattr(e, 'reason'):
					return 'We failed to reach a server.'
					print 'Reason: ', e.reason
				elif hasattr(e, 'code'):
					return 'The server couldn\'t fulfill the request.'
					print 'Error code: ', e.code
	return rankedTeams

# This is pretty unnecessary, but I use it anyway.
def getTeamStats(teamInfo):
	'''Grabs only the desired statistics for the given team, and puts them into a dictionary'''
	teamStats = {'teamID': teamInfo['id'], 'members': teamInfo['member_count'], 'loans': teamInfo['loan_count'], 'loanAmount': teamInfo['loaned_amount']}
	return teamStats

# We don't use this yet, so I'm not positive how well it works, but it may be useful later.
def getAllTeamMembers(teamID):
	'''Returns a list of dictionaries for each member of a team'''
	i = 1
	url = 'http://api.kivaws.org/v1/teams/' + str(teamID) + '/lenders.json'
	content = simplejson.loads(urllib2.urlopen(url).read())
	pages = content['paging']['pages']
	teamMembers = []
	print pages
	while i <= pages:
		print i
		urlStr = url + '&page=' + str(i)
		content = simplejson.loads(urllib2.urlopen(urlStr).read())
		lenders = content['lenders']
		for lender in lenders:
			teamMembers.append(lender)
		i += 1
	return teamMembers

# Probably should get rid of this - it's the same as getTeams, but only for 1 team
def getTeamInfo(teamID):
	'''Returns the info for a team, given the team ID.'''
	url = 'http://api.kivaws.org/v1/teams/' + str(teamID) + '.json'
	content = simplejson.loads(urllib2.urlopen(url).read())
	teamInfoList = content['teams']
	if teamInfoList:
		teamInfo = teamInfoList[0]
		return teamInfo
	else:
		return None
	
	
def getTeamID(query):
	'''Searches for a team ID, given a string, and returns the first result'''
	url = 'http://api.kivaws.org/v1/teams/search.json?q=' + APIEncode(query) + '&sort_by=query_relevance'
	content = simplejson.loads(urllib2.urlopen(url).read())
	teamInfoList = content['teams']
	if teamInfoList:
		teamID = teamInfoList[0]['id'] # There may be multiple results here, but we only return the first
		return int(teamID)
	else:
		return None
		
def getTeamName(teamID):
	'''Returns a team name, given an ID'''
	url = 'http://api.kivaws.org/v1/teams/' + str(teamID) + '.json'
	try:
		teamInfoList = simplejson.loads(urllib2.urlopen(url).read())
		try:
			teamName = teamInfoList['teams'][0]['name'] # This is the official team name, and shouldn't be confused with the search query.
			return teamName
		except KeyError:
			return None
	except ValueError:
		return None

def APIEncode(queryString):
	'''Takes a string and changes spaces to '+'. Will either make more complex in the future, or find a library that does it'''
	output = queryString.replace(' ','+')
	return output
