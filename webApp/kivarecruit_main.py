import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import getKivaData
from google.appengine.ext import db

# Database classes
# This class stores daily stats for a team
class TeamStats(db.Model):
	teamID = db.IntegerProperty()
	loans = db.IntegerProperty()
	members = db.IntegerProperty()
	amountLoaned = db.IntegerProperty()
	rank = db.IntegerProperty()
	date = db.DateProperty(auto_now_add=True)

# This class maps teamIDs to team names
class TeamNames(db.Model):
	teamID = db.IntegerProperty()
	teamName = db.StringProperty()


class MainPage(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		template_values = {}
		charts = []
		self.response.out.write(template.render(path, template_values))

class TeamHandler(webapp.RequestHandler):
	def post(self):
		# Get the input from the web form
		teamNameInput = self.request.get("teamName")
		# If it's a number, assume that it's the Team ID
		if is_number(teamNameInput):
			teamID = int(teamNameInput)
		# If it's a string, then get the team ID of the first match
		else:
			teamID = getKivaData.getTeamID(teamNameInput)
		# Get the official name of the team
		teamName = getKivaData.getTeamName(teamID)
		# Figure out if the team is in the TeamNames DB. If it isn't, then add it.
		# Eventually, we can choose to get data from teams in this DB, that aren't in the top 2000 teams.
		teamNames_query = TeamNames.all().filter('teamID =',teamID)
		teamNames = teamNames_query.get()
		if teamNames is None:
			teamNameInsert = TeamNames()
			teamNameInsert.teamID = teamID
			teamNameInsert.teamName = teamName
			teamNameInsert.put()
		# If there is an actual Kiva Team, then get stats for the team
		if teamName is not None:
			teamStats_query = TeamStats.all().filter('teamID =', teamID).order("date")
			teamStatsObject = teamStats_query.fetch(1000)
		else:
			teamStatsObject = None
		# If we don't have stats, then let the user know that.
		if teamStatsObject is None or len(teamStatsObject)<1:
			errorMessage = 'No team found. We currently only track data for the top 2000 teams.'
			template_values = {'errorMessage':errorMessage}
		else:
			membersList = [{'dataType': 'Members'}]
			amountLoanedList = [{'dataType': 'Amount Loaned'}]
			rankList = []
			loansList = [{'dataType': 'Loans'}]
			membersDataList = []
			amountLoanedDataList = []
			loansDataList = []
			charts = []
			# Create lists for each of the stats
			for statsObject in teamStatsObject:
				membersDataList.append((statsObject.date,statsObject.members))
				amountLoanedDataList.append((statsObject.date,statsObject.amountLoaned))
				rankList.append((statsObject.date,statsObject.rank))
				loansDataList.append((statsObject.date,statsObject.loans))
			amountLoanedList[0]['data'] = amountLoanedDataList
			membersList[0]['data'] = membersDataList
			loansList[0]['data'] = loansDataList
			# Create graphs for each stat
			charts.append(createTimeline(teamName + ' Amount Loaned', 'amountLoaned', amountLoanedList))
			charts.append(createTimeline(teamName + ' Members', 'members', membersList))
			charts.append(createTimeline(teamName + ' Total Loans', 'loans', loansList))
			# Get latest rank
			currRank = rankList[-1][1]
			template_values = {'rank':currRank, 'charts': charts
					}
		# Write to index.html
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
								 [('/', MainPage),
								  ('/displayTeamStats', TeamHandler)],
								 debug=True)

def main():
	run_wsgi_app(application)
	
# Check if a string is a number
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

# Create the data needed for a Google Timeline chart
def createTimeline(chartName, chartType, dataList):
	'''Create a for Google Visualization Timeline, given a team name, graph name, and a data list in the format [{'dataType': 'Type of Data', 'data': [(date,dataPoint),(date1,dataPoint1)}]'''
	chart = {'chartName': chartName, 'chartType':chartType}
	columns = []
	data = []
	i = 0
	# Go through each of the items in the dataList
	while i <len(dataList):
		# Get the data types, and put them into 'columns'
		columns.append(dataList[i]['dataType'])
		# Go through every data item, put them in the format required by the Visualization API
		for dataItem in dataList[i]['data']:
			dateItem = str(dataItem[0].year) + ',' + str(dataItem[0].month - 1) + ',' + str(dataItem[0].day)
			data.append('(' + dateItem + '),' + 'undefined,'*i + str(dataItem[1]) + ',undefined'*(len(dataList)-i-1))
		i += 1
	chart['columns'] = columns
	chart['data'] = data
	return chart

if __name__ == "__main__":
	main()
