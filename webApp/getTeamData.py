import getKivaData
import kivarecruit_main
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class cronGetTeams(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Loading teams into the DB')
        teamsDone = getTeamData(50)
        self.response.out.write(str(teamsDone) + ' teams loaded')

def getTeamData(teamCount):
	# Get all of the teams
	allTeams = getKivaData.getTeams(teamCount)
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
	return i

application = webapp.WSGIApplication(
                                     [('/tasks/teamData', cronGetTeams)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
