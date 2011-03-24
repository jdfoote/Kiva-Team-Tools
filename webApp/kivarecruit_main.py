import cgi
import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class TeamStats(db.Model):
    teamID = db.IntegerProperty()
    loans = db.IntegerProperty()
    members = db.IntegerProperty()
    amountLoaned = db.IntegerProperty()
    rank = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class TeamNames(db.Model):
	teamID = db.IntegerProperty()
	teamName = db.StringProperty()
	
class UserPrefs(db.Model):
	userID = db.StringProperty()
	userTeam = db.StringProperty()

class MainPage(webapp.RequestHandler):
    def get(self):
    	user = users.get_current_user()
    	imgurl = 'http://chart.apis.google.com/chart?chs=440x220&cht=lxy&chco=3072F3,FF0000&chd=t:10,20,40,80,90,95,99|20,30,40,50,60,70,80|-1|5,10,22,35,85&chdl=Ponies|Unicorns&chdlp=b&chls=2,4,1|1&chma=5,5,5,25&chtt=Team+Data" width="440" height="220" alt="Team Data'
        if user:
			userTeams = []
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			userPrefs_query = UserPrefs.all().filter('userID =', user.user_id())
			userPrefs = userPrefs_query.fetch(15)
			for u in userPrefs:
				userTeams.append(u.userTeam)
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login to save your teams'
            userPrefs = []
            userID = 'None'

        template_values = {
            'userPrefs': userTeams,
            'url': url,
            'url_linktext': url_linktext,
            'imgurl': imgurl,
            #'user': userID,
        }
	path = os.path.join(os.path.dirname(__file__), 'index.html')
	self.response.out.write(template.render(path, template_values))
        
class DisplayTeamStats(webapp.RequestHandler):
    def post(self):
        userPrefs = UserPrefs()

        if users.get_current_user():
            userPrefs.userID = users.get_current_user().user_id()

        userPrefs.userTeam = self.request.get('content')
        userPrefs.put()
        self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/displayTeamStats', DisplayTeamStats)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
