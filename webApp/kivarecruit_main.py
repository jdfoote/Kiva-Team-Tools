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

class TeamNames(db.Model):
	teamID = db.IntegerProperty()
	teamName = db.StringProperty()

class MainPage(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		template_values = {}
		self.response.out.write(template.render(path, template_values))

class TeamHandler(webapp.RequestHandler):
	def post(self):
		teamNameInput = self.request.get("teamName")
		if is_number(teamNameInput):
			teamID = int(teamNameInput)
		else:
			teamID = getKivaData.getTeamID(teamNameInput)
		teamName = getKivaData.getTeamName(teamID)
		teamNames_query = TeamNames.all().filter('teamID =',teamID)
		teamNames = teamNames_query.get()
		if teamNames is None:
			teamNameInsert = TeamNames()
			teamNameInsert.teamID = teamID
			teamNameInsert.teamName = teamName
			teamNameInsert.put()
		teamStats_query = TeamStats.all().filter('teamID =', teamID)
		teamStatsObject = teamStats_query.fetch(1000)
		teamStats=[]
		membersList = []
		amountLoanedList = []
		rankList = []
		loansList = []
		for statsObject in teamStatsObject:
			membersList.append(statsObject.members)
			amountLoanedList.append(statsObject.amountLoaned)
			rankList.append(statsObject.rank)
			loansList.append(statsObject.loans)
			teamStats.append((statsObject.teamID, statsObject.amountLoaned, statsObject.date, statsObject.rank))
		amountLoanedURL = createGraph(teamName, 'Amount Loaned', amountLoanedList)
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		template_values = {'teamID':teamID, 'amountLoanedURL':amountLoanedURL
				}
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
								 [('/', MainPage),
								  ('/displayTeamStats', TeamHandler)],
								 debug=True)

def main():
	run_wsgi_app(application)
	
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def createGraph(teamName, dataType, dataList):
	title = teamName + ' ' + dataType
	stringList = [str(i) for i in dataList]
	data = ','.join(stringList)
	dataMax = max(dataList)
	dataMin = min(dataList)
	URL = 'http://chart.apis.google.com/chart?chxl=0:|Date1|Date2|Date3&chxt=x,y&chs=440x220&cht=lc&chco=3072F3,FF0000&chd=t:' + data +'&chds=' + str(max(0,dataMin-1000)) + ',' + str(dataMax+1000) + '&chxr=1,' + str(max(0,dataMin-1000)) + ',' + str(dataMax+1000) + '&chdl=' + dataType.replace(' ', '+') + '&chdlp=b&chls=2&chma=5,5,5,25&chtt=' + teamName.replace(' ', '+')
	return URL

if __name__ == "__main__":
	main()
