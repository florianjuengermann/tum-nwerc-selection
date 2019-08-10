import codeforcesApi as cfapi
import time
from datetime import datetime

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
		return [] # TODO

	def getDates(self):
		return self.contests;
		
	def update(self):
		start = getTimestamp(self.config["startDate"])
		end = getTimestamp(self.config["endDate"])
		contests = self.getCFContests(start, end) + self.getACContests(start, end)
		#contests = [{'time': time.time() - 60*60*24*5, 'type':'codeforces', 'id':'1202'}]
		self.contests = sorted(contests)

