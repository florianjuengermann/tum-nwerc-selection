from contest import Contest
import codeforcesApi as cfApi
import re

class CodeforcesContest(Contest):

	def __init__(self, id, handleMap):
		self.handleString = "codeforces-handle"
		super().__init__(id, handleMap)

	def updateScores(self):
		print("fetching scores for CF contest ", self.id)
		cfStandings = cfApi.request("contest.standings", {"contestId": self.id})
		if cfStandings is False:
			return
		roundNr = re.search("[0-9][0-9]", cfStandings["contest"]["name"]).group()
		self.name = "CF-" + str(roundNr)

		# reset everything
		self.handlesSolved = {}
		self.numberSolved = {}
		for i in range(len(cfStandings["problems"])):
			self.numberSolved[i] = 0

		rows = cfStandings["rows"]
		for r in rows:
			handle = r["party"]["members"][0]["handle"]
			for i in range(len(r["problemResults"])):
				solved =  r["problemResults"][i]["points"] > 0
				if not handle in self.handlesSolved:
					self.handlesSolved[handle] = []
				if solved:
					self.handlesSolved[handle].append(i)
					self.numberSolved[i] += 1
