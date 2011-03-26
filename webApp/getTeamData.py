import getKivaData
import kivarecruit_main
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class cronGetTeams(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'html'
        self.response.out.write('<html><body>Loading teams into the DB')
        teamsDone = getTeamData()
        self.response.out.write('<br/>' + str(teamsDone) + ' teams loaded')

def getTeamData():
	# Get all of the teams
#	teamNames_query = kivarecruit_main.TeamStats.all()
#	teamNamesObject = teamNames_query.fetch(1000)
	teamIDList = []
#	for p in teamNamesObject:
#		teamIDList.append(p.teamID)
	# Get the info
	allTeams = getKivaData.getRankedTeams(2000)
	# Just get the stuff we want
	teamData=[]
	for team in allTeams:
		teamData.append(getKivaData.getTeamStats(team))

	# Put the team data into the DB.

	i = 1
	for team in teamData:
		teamInsert = kivarecruit_main.TeamStats()
		teamInsert.teamID = team['teamID']
		teamInsert.members = team['members']
		teamInsert.rank = i
		teamInsert.amountLoaned = team['loanAmount']
		teamInsert.loans = team['loans']
		teamInsert.put()
		i += 1
	return i - 1

application = webapp.WSGIApplication(
                                     [('/tasks/teamData', cronGetTeams)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
