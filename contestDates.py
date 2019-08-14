from bs4 import BeautifulSoup
import codeforcesApi as cfapi
import time, requests
import util
import re
from datetime import datetime
from pytz import timezone

def getTimestamp(dateString) -> float:
	return datetime.timestamp(datetime.strptime(dateString, "%d.%m.%Y"))

class ContestDates:
	def __init__(self, config):
		self.config = config
		self.contests = []
		self.update()

	def getCFContests(self, start, end):
		contests = cfapi.request('contest.list', {'gym':'false'})
		if contests is False:
			return []
		contests = [c for c in contests if c.get('startTimeSeconds', -1) >= start]
		contests = [c for c in contests if c.get('startTimeSeconds', -1) <= end]
		contests = [c for c in contests if "Educational" in c['name']]

		return [{		"time": c['startTimeSeconds'],
								"type": "codeforces",
								"id": 	c["id"]} for c in contests]

	def getACContests(self, start, end):
		request = requests.get("https://atcoder.jp/contests/archive?category=1")
		html = request.text
		parsed = BeautifulSoup(html, "lxml")
		contests = self.parseACTable(parsed.find('table'), start, end)

		request = requests.get("https://atcoder.jp/contests/")
		html = request.text
		parsed = BeautifulSoup(html, "lxml")
		upcomingTable = parsed.find(id='contest-table-upcoming').find('table')
		contests += self.parseACTable(upcomingTable, start, end)
		return contests
	
	def parseACTable(self, table, start, end):
		rows = table.find('tbody').find_all('tr')
		contests = []
		for row in rows:
			values = row.find_all('td')
			timeUrl = values[0].find('a').get('href')
			timestr = re.search('[0-9]+T[0-9]*', timeUrl).group()
			japanTime = datetime.strptime(timestr, "%Y%m%dT%H%M")
			utcTime = util.convertTimeZone(japanTime, "Asia/Tokyo", "Europe/Berlin")
			timeStmp = datetime.timestamp(utcTime)
			contestUrl = values[1].find('a').get('href')
			contestRegex = re.search('agc[0-9]*', contestUrl)
#			if contestRegex is not None and timeStmp >= start-50*24*60*60 and timeStmp <= end:
			if contestRegex is not None and timeStmp >= start and timeStmp <= end:
				contestId = contestRegex.group()
				contests.append({
						'time':timeStmp,
						'type':'atcoder',
						'id':contestId
						})
		return contests

	def getDates(self):
		return self.contests;
		
	def update(self):
		start = getTimestamp(self.config["startDate"])
		end = getTimestamp(self.config["endDate"])
		contests = self.getCFContests(start, end) + self.getACContests(start, end)
		#contests = [{'time': time.time() - 60*60*24*5, 'type':'codeforces', 'id':'1202'}]
		self.contests = sorted(contests, key=lambda k:k['time'])

