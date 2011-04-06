#!/usr/bin/python
import getKivaData
import kivarecruit_main
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class cronGetTeams(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'html'
		self.response.out.write('<html><body>Loading teams into the DB')
		teamsDone = getTeamNames(2000)
		if teamsDone:
			self.response.out.write('<br/>' + str(teamsDone) + ' teams loaded')
		else:
			self.response.out.write('<br/> Something went wrong.')

def getTeamNames(numberOfTeams):
	teamData = getKivaData.getRankedTeams(numberOfTeams)
	newData = []
	i = 0
	for team in teamData:
		teamInsert = kivarecruit_main.TeamNames(key_name = str(team['id']),
												teamID = team['id'],
												name = team['name'])
		newData.append(teamInsert)
		i += 1
	kivarecruit_main.db.put(newData)
	return i

application = webapp.WSGIApplication(
									 [('/tasks/teamNames', cronGetTeams)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
