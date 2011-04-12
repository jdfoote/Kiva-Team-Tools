#!/usr/bin/python
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import getKivaData
from google.appengine.ext import db
import simplejson

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

# This DB just stores the current team table
class TeamTableData(db.Model):
	teamTable = db.TextProperty()


class MainPage(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		# Get the table data from the DB
		teamTable_query = TeamTableData.all()
		teamTableQueryData = teamTable_query.get()
		if teamTableQueryData:
			teamTableData = eval(teamTableQueryData.teamTable)
		else:
			teamTableData = []
		template_values = {'teamTableData': teamTableData}
		charts = []
		self.response.out.write(template.render(path, template_values))

class TeamHandler(webapp.RequestHandler):
	def post(self):
		# Get the input from the web form
		teamNameInput = self.request.get("teamName")
		teamID, teamName = getNameAndID(teamNameInput)

		# Figure out if the team is in the TeamNames DB. If it isn't, then add it.
		# Eventually, we can choose to get data from teams in this DB, that aren't in the top 2000 teams.
		teamNames_query = TeamNames.all().filter('teamID =',teamID)
		teamNames = teamNames_query.get()
		if teamNames is None:
			teamNameInsert = TeamNames()
			teamNameInsert.key_name = str(teamID)
			teamNameInsert.teamID = teamID
			teamNameInsert.teamName = teamName
			teamNameInsert.put()

		# If there is an actual Kiva Team, then get stats for the team
		if teamName is not None:
			teamStatsObject = queryTeamStats(teamID, 1000)
		else:
			teamStatsObject = None
			

		# If we don't have stats, then let the user know that.
		if teamStatsObject is None or len(teamStatsObject)<1:
			errorMessage = 'No team found. We currently only track data for the top 1500 teams.'
			template_values = {'errorMessage':errorMessage}
		else:		
			# Get stats for the team before and after the top team
			currRank = teamStatsObject[-1].rank
			teamStatsObjectList = [teamStatsObject]
			teamNamesList = [teamName]
			# If they are the first place team, then only get the team after them.
			if currRank > 1:
				i = currRank - 1
			else:
				i = currRank + 1
			while i <= currRank + 1:
				# Get the team ID of the team with the given rank.
				otherTeamID_query = TeamStats.all().filter('rank =', i).order("-date")
				otherTeamID_Object = otherTeamID_query.get()
				otherTeamID = otherTeamID_Object.teamID
				# Get the team name, for labelling the chart
				otherTeamName = queryTeamName(otherTeamID)
				teamNamesList.append(smart_truncate(otherTeamName,25))
				# Get the data for this team
				otherTeamStatsObject = queryTeamStats(otherTeamID, 1000)
				# Add the data to the list
				teamStatsObjectList.append(otherTeamStatsObject)
				i += 2
			# Prepare the lists of column names
			amountLoanedColumns = []
			membersColumns = []
			loansColumns = []

			for i in teamNamesList:
				amountLoanedColumns.append(i + ' Amount')
				membersColumns.append(i + ' Members')
				loansColumns.append(i + ' Loans')

			# Prepare the data
			membersData = []
			amountLoanedData = []
			loansData = []
			charts = []
			for i, teamStatsObject in enumerate(teamStatsObjectList):
			# Create lists for each of the stats
				for statsObject in teamStatsObject:
					if len(membersData) < 1:
						membersData.append({'date': statsObject.date, membersColumns[i]: statsObject.members})
					else:
						for j in membersData:
							if statsObject.date == j['date']:
								j[membersColumns[i]] = (statsObject.members)
							else:
								membersData.append({'date': statsObject.date, membersColumns[i]: statsObject.members}) 
					if len(amountLoanedData) < 1:
						amountLoanedData.append({'date': statsObject.date, amountLoanedColumns[i]: statsObject.amountLoaned}) 
					else:
						for j in amountLoanedData:
							if statsObject.date == j['date']:
								j[amountLoanedColumns[i]] = (statsObject.amountLoaned)
							else:
								amountLoanedData.append({'date': statsObject.date, amountLoanedColumns[i]: statsObject.amountLoaned}) 
					if len(loansData) < 1:
						loansData.append({'date': statsObject.date, loansColumns[i]: statsObject.loans})
					else:
						for j in loansData:
							if statsObject.date == j['date']:
								j[loansColumns[i]] = (statsObject.loans)
							else:
								loansData.append({'date': statsObject.date, loansColumns[i]: statsObject.loans})

			# Create graphs for each stat
			charts.append(createTimeline(teamName + ' Amount Loaned', 'amountLoaned', amountLoanedColumns, amountLoanedData))
			charts.append(createTimeline(teamName + ' Members', 'members', membersColumns, membersData))
			charts.append(createTimeline(teamName + ' Total Loans', 'loans', loansColumns, loansData))
			
			# Get the table data from the DB
			teamTable_query = TeamTableData.all()
			teamTableQueryData = teamTable_query.get()
			if teamTableQueryData:
				teamTableData = eval(teamTableQueryData.teamTable)
			else:
				teamTableData = []
			
			template_values = {'rank':currRank, 'charts': charts, 'teamTableData': teamTableData, 'teamName': teamName
					}
		# Write to index.html
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
								 [('/', MainPage),
								  ('/displayTeamStats', TeamHandler)],
								 debug=True)

	
# Check if a string is a number
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

# Create the data needed for a Google Timeline chart
def createTimeline(chartName, chartType, columnNames, chartData):
	'''Create a for Google Visualization Timeline, given a chart name, chart Type, a list of names for the non-date columns, and data in the format [{'date': date0, 'columnName0': data0, 'columnName1': data1}]'''
	chart = {'chartName': chartName, 'chartType': chartType, 'columns': columnNames}
	data = []
	i = 0
	# Go through each of the items in the dataList, and put them in the format required by the Visualization API
	while i <len(chartData):
		for dataItem in chartData:
			dateItem = str(dataItem['date'].year) + ',' + str(dataItem['date'].month - 1) + ',' + str(dataItem['date'].day)
			dataPoints = []
			for j in columnNames:
				if j in dataItem:
					dataPoints.append(str(dataItem[j]))
				else:
					dataPoints.append('undefined')
			dataPointsString = ','.join(dataPoints)
			data.append('(' + dateItem + '),' + dataPointsString)
		i += 1
	chart['columns'] = columnNames
	chart['data'] = data
	return chart
	
def queryTeamStats(teamID, results):
	teamStats_query = TeamStats.all().filter('teamID =', teamID).order("date")
	teamStatsObject = teamStats_query.fetch(1000)
	return teamStatsObject

def queryTeamName(teamID):
	teamNameQuery = TeamNames.get_by_key_name(str(teamID))
	teamName = teamNameQuery.teamName
	return teamName
	
def getNameAndID(teamNameInput):
	# If it's a number, assume that it's the Team ID
	if is_number(teamNameInput):
		teamID = int(teamNameInput)
		teamName = queryTeamName(teamID)
	# If it's a string, then get the team ID and name of the first match
	else:
		teamID, teamName = getKivaData.getTeamID(teamNameInput)
	return teamID, teamName

def smart_truncate(content, length=100, suffix='...'):
	if len(content) <= length:
		return content
	else:
		return content[:length].rsplit(' ', 1)[0]+suffix

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
