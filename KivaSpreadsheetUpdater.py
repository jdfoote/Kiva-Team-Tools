#!/usr/bin/python

try: 
  from xml.etree import ElementTree
except ImportError:  
  from elementtree import ElementTree
import gdata.spreadsheet.service
import gdata.service
import atom.service
import gdata.spreadsheet
import atom
import string
import urllib
import simplejson
import datetime

# Get information about the 3 Kiva teams we are comparing, and store it in 3 dictionaries
teams = simplejson.loads(urllib.urlopen('http://api.kivaws.org/v1/teams/96,257,191.json').read())['teams']
members = {}
loans = {}
loanAmount = {}
for team in teams:
	members[team['id']] = str(team['member_count'])
	loans[team['id']] = str(team['loan_count'])
	loanAmount[team['id']] = str(team['loaned_amount'])

# Find the Kiva Mormons current rank, who is ahead of us, and how far ahead	
i = 1
foundMormons = 'false'
keepGoing = 'true'
rankedTeams = []
while keepGoing == 'true':
		urlStr = 'http://api.kivaws.org/v1/teams/search.json&sort_by=loaned_amount&page=' + str(i)
		newTeams = simplejson.loads(urllib.urlopen(urlStr).read())['teams']
		i += 1
		if foundMormons == 'true':
			keepGoing = 'false'
		for team in newTeams:
			rankedTeams.append(team)
			if team['id'] == 96:
				foundMormons = 'true'
for index, team in enumerate(rankedTeams):
	if team['id'] == 96:
		mormonRank = index

teamAhead = rankedTeams[mormonRank - 1]['name']
amountAhead = rankedTeams[mormonRank - 1]['loaned_amount'] - rankedTeams[mormonRank]['loaned_amount']
teamBehind = rankedTeams[mormonRank + 1]['name']
amountBehind = rankedTeams[mormonRank]['loaned_amount'] - rankedTeams[mormonRank + 1]['loaned_amount']
print rankedTeams

gd_client = gdata.spreadsheet.service.SpreadsheetsService()
gd_client.email = 'jdfoote1@gmail.com'
gd_client.password = 'crfhy4f7qtaxacla'
gd_client.source = 'KivaSpreadsheetUpdater'
gd_client.ProgrammaticLogin()

# Inserts data into a spreadsheet
def ListInsertAction(gd_client, key, wksht_id, row_data):
  entry = gd_client.InsertRow(row_data, key, wksht_id)
  if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
    print 'Inserted!'

# Spreadsheet key and worksheet key
key = '0ApcJLrkFKwXdcGdFZE1CWGRuUlA0aHVWVTN1aWRBY2c'
wksht_id = 'od6'

#Get today's date
now = datetime.datetime.now()
date = str(now.strftime("%m/%d/%Y"))

# Create dictionary to insert and insert the data rows
row_data = {'date1': date, 'k.mormonsmembers': members[96], 's.monstermembers': members[191], 'catholicmembers': members[257], 'k.mormonsloans': loans[96], 's.monsterloans': loans[191], 'catholicloans': loans[257], 'kmamount': loanAmount[96], 'smamount': loanAmount[191], 'catholicamount': loanAmount[257], 'smloans-kmloans': '=R[0]C[-19]-R[0]C[-20]', 'smamount-kmamount': '=R[0]C[-16]-R[0]C[-17]', 'kivamormonsrank': str(mormonRank + 1), 'teamaheadofus': teamAhead, 'amountaheadofus': str(amountAhead), 'teambehindus': teamBehind, 'amountbehindus': str(amountBehind)}
# Copy date to all date columns
i = 2
while i <=7:
	row_data['date' + str(i)] = '=R[0]C' + '[-' + str((i-1)*4) + ']'
	i = i+1
# Add the data manipulation rows (e.g., 'amount per loan')
list = ['kivamormonsamtperloan','fsmamtperloan','catholicsamtperloan']
for item in list:
	row_data[item] = '=R[0]C[-4]/R[0]C[-8]'
list = ['kivamormonsamtpercapita','fsmamtpercapita','catholicsamtpercapita']
for item in list:
	row_data[item] = '=R[0]C[-8]/R[0]C[-16]'
list = ['kivamormonsloanspercapita','fsmloanspercapita','catholicsloanspercapita']
for item in list:
	row_data[item] = '=R[0]C[-16]/R[0]C[-20]'
# Actually do the insert into the spreadsheet
ListInsertAction(gd_client, key, wksht_id, row_data)
