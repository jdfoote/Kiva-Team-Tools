import getKivaData
import kivarecruit_main

# Get all of the teams
allTeams = getKivaData.getTeams(50)
# Just get the stuff we want
teamData = getKivaData.getTeamStats(allTeams)
# Put the team data into the DB.

teamInsert = kivarecruit_main.TeamStats()
i = 1
for team in teamData:
	teamInsert.teamID = team['teamID']
	teamInsert.members = team['members']
	teamInsert.rank = i
	teamInsert.amountLoaned = team['loanAmount']
	teamInsert.loans = team['loans']
	userPrefs.put()
