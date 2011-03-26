import string
import urllib
import simplejson

def getTeams(listOfTeams):
	'''Given a list of team IDs, returns a list of dictionaries with team information'''
	stringList = [str(i) for i in listOfTeams]
	teamInfo = []
	start = 0
	end = 20
	while start < len(listOfTeams):
		teamList = ','.join(stringList[start:end])
		urlStr = 'http://api.kivaws.org/v1/teams/' + teamList + '.json'
		newTeams = simplejson.loads(urllib.urlopen(urlStr).read())['teams']
		start += 20
		end += 20
		for team in newTeams:
			teamInfo.append(team)
	return teamInfo

def getRankedTeams(numberOfTeams):
	'''Returns a list of dictionaries with team information for the top n teams'''
	keepGoing = 'true'
	rankedTeams = []
	i = 1
	while keepGoing == 'true':
			urlStr = 'http://api.kivaws.org/v1/teams/search.json&sort_by=loaned_amount&page=' + str(i)
			newTeams = simplejson.loads(urllib.urlopen(urlStr).read())['teams']
			i += 1
			for team in newTeams:
				if len(rankedTeams) < numberOfTeams:
					rankedTeams.append(team)
				else:
					keepGoing = 'false'
					break
	return rankedTeams


def getTeamStats(teamInfo):
	'''Grabs only the desired statistics for the given team, and puts them into a dictionary'''
	teamStats = {'teamID': teamInfo['id'], 'members': teamInfo['member_count'], 'loans': teamInfo['loan_count'], 'loanAmount': teamInfo['loaned_amount']}
	return teamStats

def getAllTeamMembers(teamID):
	'''Returns a list of dictionaries for each member of a team'''
	i = 1
	url = 'http://api.kivaws.org/v1/teams/' + str(teamID) + '/lenders.json'
	pages = simplejson.loads(urllib.urlopen(url).read())['paging']['pages']
	teamMembers = []
	print pages
	while i <= pages:
		print i
		urlStr = url + '&page=' + str(i)
		lenders = simplejson.loads(urllib.urlopen(urlStr).read())['lenders']
		for lender in lenders:
			teamMembers.append(lender)
		i += 1
	return teamMembers

def getTeamInfo(teamID):
	'''Returns the info for a team, given the team ID.'''
	url = 'http://api.kivaws.org/v1/teams/' + str(teamID) + '.json'
	teamInfoList = simplejson.loads(urllib.urlopen(url).read())['teams']
	if teamInfoList:
		teamInfo = teamInfoList[0]
		return teamInfo
	else:
		return None
	
def getTeamID(query):
	'''Searches for a team ID, given a string'''
	url = 'http://api.kivaws.org/v1/teams/search.json?q=' + str(query) + '&sort_by=query_relevance'
	teamInfoList = simplejson.loads(urllib.urlopen(url).read())['teams']
	if teamInfoList:
		teamID = teamInfoList[0]['id']
		return int(teamID)
	else:
		return None
		
def getTeamName(teamID):
	'''Returns a team name, given an ID'''
	url = 'http://api.kivaws.org/v1/teams/' + str(teamID) + '.json'
	teamInfoList = simplejson.loads(urllib.urlopen(url).read())['teams']
	if teamInfoList:
		teamName = teamInfoList[0]['name']
		return teamName
	else:
		return None
