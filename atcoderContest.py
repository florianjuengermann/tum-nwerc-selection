import json, requests
from bs4 import BeautifulSoup
from contest import Contest

class AtcoderContest(Contest):
	def __init__(self, id, handleMap):
		self.handleString = "atcoder-handle"
		super().__init__(id, handleMap)

	def initSession():
		[username, password] = [line.rstrip('\n') for line in open('.atcoder_config.txt')]
		AtcoderContest.session = requests.Session()
		loginUrl = "https://atcoder.jp/login"
		request = AtcoderContest.session.get(loginUrl)
		parsed = BeautifulSoup(request.text)
		csrf_token = [element['value'] for element in parsed.find_all('input') if element['name'] == "csrf_token"][0]
		loginData = {'username': username,
								 'password': password,
								 'csrf_token': csrf_token}
		res = AtcoderContest.session.post(loginUrl, data=loginData)

	def endSession():
		AtcoderContest.session.close()

	def updateScores(self):
		print("fetching scores for Atcoder contest ", self.id)
		self.handlesSolved = {}
		self.numberSolved = {}
		self.name = self.id[:3] + self.id[4:] # leave out '0' -> 5 chars only
		try:
			url = "https://atcoder.jp/contests/" + self.id + "/standings/json"
			r = self.session.get(url, timeout=15)
			r = r.json()

			scoresForTask = {} # taskname -> {score -> index in numberSolved/handlesSolved}
			for task in r['TaskInfo']:
				scoresForTask[task['TaskScreenName']] = {}

			taskIndex = 0
			# Initialize scores for task for handling subtasks
			for row in r['StandingsData']:
				for taskName, result in row['TaskResults'].items():
					if result['Score'] > 0 and result['Score'] not in scoresForTask[taskName]:
						scoresForTask[taskName][result['Score']] = taskIndex
						self.numberSolved[taskIndex] = 0
						taskIndex += 1

			for row in r['StandingsData']:
				# only people with at least one submission are counted
				if row['TotalResult']['Count'] == 0:
					continue 
				handle = row['UserScreenName']
				self.handlesSolved[handle] = []
				for taskName, result in row['TaskResults'].items():
					if result['Score'] > 0:
						for score, index in scoresForTask[taskName].items():
							# User solved all subtasks with score <= their score
							if score <= result['Score']:
								self.handlesSolved[handle].append(index)
								self.numberSolved[index] += 1
		except requests.exceptions.Timeout as e:
			print("Fetching Atcoder results failed")
			return False
