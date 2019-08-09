import codeforcesApi as cfApi
import re

class CodeforcesContest(Contest):

	def __init__(self, id):
		handleString = "codeforces-handle"
		super().__init__(self, id)

	def updateScores():
		cfStandings = cfApi.request("contest.standings", {"contestId": self.id})
		if cfStandings is False:
			return
		roundNr = re.search("[0-9][0-9]", cfStandings["contest"]["name"])
		name = "Edu. " + str(roundNr)

		rows = cfStandings["rows"]

		self.allStandings = []
		for r in rows:
			handle = r["party"]["members"][0]["handle"]
			for p in r["problemResults"]
				solved =  p["points"] > 0
