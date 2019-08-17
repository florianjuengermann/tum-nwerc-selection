import json, requests
from contest import Contest

class AtcoderContest(Contest):
	def __init__(self, id, handleMap):
		self.handleString = "atcoder-handle"
		super().__init__(id, handleMap)

	def updateScores(self):
		print("fetching scores for Atcoder contest ", self.id)
		self.handlesSolved = {}
		self.numberSolved = {}
		self.name = self.id
		try:
			url = "https://atcoder.jp/contests/" + self.id + "/standings/json"
			r = requests.get(url, timeout=15)
			r = r.json()
			mapToNum = {}
			i = 0
			for task in r['TaskInfo']:
				mapToNum[task['TaskScreenName']] = i
				self.numberSolved[i] = 0
				i += 1
			for row in r['StandingsData']:
				# only people with at least one submission are counted
				if row['TotalResult']['Count'] == 0:
					continue 
				handle = row['UserScreenName']
				self.handlesSolved[handle] = []
				for taskName, result in row['TaskResults'].items():
					if result['Score'] > 0:
						self.handlesSolved[handle].append(mapToNum[taskName])
						self.numberSolved[mapToNum[taskName]] += 1
		except requests.exceptions.Timeout as e:
			print("Fetching Atcoder results failed")
			return False
