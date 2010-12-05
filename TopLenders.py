## Top lenders for a team, by number of loans
import urllib
import simplejson
import operator

# Get all of the recent team members
teamRange = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json').read())['paging']['pages']
i = 1
teamLoans = []
while i <= teamRange:
	newTeamMembers = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96/lenders.json?sort_by=newest&page=' + str(i)).read())['lenders']
	team = []
	for j in newTeamMembers:
		memberID = j['uid']
		team.append(memberID)
	s = ','.join(team)

	lenderLoanList = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/lenders/' + str(s) + '.json').read())['lenders']
	for k in lenderLoanList:
		lenderID = k['lender_id']
		name = k['name']
		if 'loan_count' in k:
			loanCount = k['loan_count']
		else:
			loanCount = 0
		t = lenderID, name, loanCount
		teamLoans.append(t)
	i=i+1


sorted_teamLoans = sorted(teamLoans, key=operator.itemgetter(2), reverse=True)
print sorted_teamLoans



