import codeforcesApi as cfapi
from datetime import datetime

def getCFContests(start, end):
	contests = cfapi.request('contest.list', {'gym':'false'})
	contests = [c for c in contests if c.get('startTimeSeconds', -1) >= start]
	contests = [c for c in contests if c.get('startTimeSeconds', -1) <= end]
	contests = [c for c in contests if "Educational" in c['name']]

	return [{		"time": c['startTimeSeconds'],
							"type": "codeforces",
							"id": 	c["id"]} for c in contests]

def getACContests(start, end):
	return [] # TODO

def getTimestamp(dateString) -> float:
 return datetime.timestamp(datetime.strptime(dateString, "%d.%m.%Y"))

def getDates(config):
	start = getTimestamp(config["startDate"])
	end = getTimestamp(config["endDate"])
	contests = getCFContests(start, end) + getACContests(start, end)
	#contests = [{'type':'codeforces', 'id':'1202'}]
	return sorted(contests)

