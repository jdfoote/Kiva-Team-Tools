import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import getKivaData
from google.appengine.ext import db

class TeamStats(db.Model):
    teamID = db.IntegerProperty()
    loans = db.IntegerProperty()
    members = db.IntegerProperty()
    amountLoaned = db.IntegerProperty()
    rank = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        template_values = {'teamID':0, 'teamStats':0}
        self.response.out.write(template.render(path, template_values))

class TeamHandler(webapp.RequestHandler):
    def post(self):
        teamName = self.request.get("teamName")
        teamID = getKivaData.getTeamID(teamName)
        teamStats_query = TeamStats.all().filter('teamID =', teamID)
        teamStatsObject = teamStats_query.fetch(100)
        teamStats=[]
        for statsObject in teamStatsObject:
        	teamStats.append((statsObject.teamID, statsObject.loans, statsObject.date, statsObject.rank))
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        template_values = {'teamID':teamID, 'teamStats':teamStats
                          }
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                 [('/', MainPage),
                                  ('/displayTeamStats', TeamHandler)],
                                 debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
