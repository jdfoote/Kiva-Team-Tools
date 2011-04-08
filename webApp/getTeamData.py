#!/usr/bin/python
import getKivaData
import kivarecruit_main
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class cronGetTeams(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'html'
		self.response.out.write('<html><body>Loading teams into the DB')
		teamsDone = getTeamData()
		if teamsDone:
			self.response.out.write('<br/>' + str(teamsDone) + ' teams loaded')
		else:
			self.response.out.write('<br/> Something went wrong.')

def getTeamData():
	# Get the info for all of the teams
	allTeams = getKivaData.getRankedTeams(2000)
	# Just get the stuff we want
	if allTeams:
		# Info for the team stats stored in the DB
		teamData=[]
		for team in allTeams:
			teamData.append(getKivaData.getTeamStats(team))
		# Info for the current table of all teams
		teamTableData = getKivaData.prepTeamTableStats(allTeams)
		# Put the team data into the DB.
		teamTableInsert = kivarecruit_main.TeamTableData(key_name = 'currentData',
														teamTable = str(teamTableData))
		teamTableInsert.put()
		i = 1
		newData = []
		for team in teamData:
			teamInsert = kivarecruit_main.TeamStats(teamID = team['teamID'],
													members = team['members'],
													rank = i,
													amountLoaned = team['loanAmount'],
													loans = team['loans'])
			newData.append(teamInsert)
			i += 1
		kivarecruit_main.db.put(newData)
		return i-1
	else:
		return None

application = webapp.WSGIApplication(
									 [('/tasks/teamData', cronGetTeams)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
