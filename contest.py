from abc import ABC, abstractmethod
import math

class Contest(ABC):
	"""abstract contest"""
	id = "" 						# contest ID
	name = ""
	handlesSolved = None # {"handle": [<int>] } handle -> list of solved tasks
	numberSolved = None	# {<int>: <int>} taskId -> number of people who solved it
	handleString = "" 	# ∈ {"codefores-handle", "atcoder-handle"}
	handleMap = None 		# {"clear-name": {"codforces-handle": …, "atc.h":…} }
	def __init__(self, id, handleMap):
		self.handleMap = handleMap
		self.id = id

	# clear name of user (not handle) -> score in this contest
	def getScore(self, name: str) -> float:
		if self.handlesSolved is None:
			self.updateScores()
		#print(self.numberSolved)
		handle = self.handleMap[name][self.handleString]
		return self.calcHandleScore(handle)

	def calcHandleScore(self, handle:str) -> float:
		avgScore = self.getAvgScore()
		score = self.getRawScore(handle)
		scaledScore = score / avgScore
		#print("avgScore: {:04.2f}, score for {}: {:04.2f}".format(avgScore, handle, score))
		return scaledScore
	
	# the unscaled score for a handle
	def getRawScore(self, handle:str) -> float:
		# number of total participants
		participants = len(self.handlesSolved)
		score = 0
		for taskI in self.handlesSolved.get(handle, []):
			solvedFraction = self.numberSolved[taskI]/participants
			score += (1 - math.log(solvedFraction))
		return score

	def getAvgScore(self) -> float:
		# number of total participants
		participants = len(self.handlesSolved)
		avgScore = 0
		for taskI in self.numberSolved:
			solvedFraction = self.numberSolved[taskI]/participants
			if solvedFraction > 0:
				avgScore += solvedFraction * (1 - math.log(solvedFraction))

		return avgScore

	# re-fetches all scores (may take a while)
	# sets allStandings
	@abstractmethod
	def updateScores(self):
		pass
