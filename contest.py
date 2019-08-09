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
		self.handleMap
		self.id = id

	# clear name of user (not handle) -> score in this contest
	def getScore(self, name: str) -> float:
		if self.handlesSolved is None:
			self.updateScores()
		#print(self.numberSolved)
		handle = self.handleMap[name][handleString]
		return self.calcHandleScore(handle)

	def calcHandleScore(self, handle:str) -> float:
		# number of total participants
		participants = len(self.handlesSolved)
		avgScore = 0

		for nbSolved in numberSolved:
			solvedFraction = nbSolved/participants
			avgScore += solvedFraction * (1 - math.log(solvedFraction))
		
		# the unadjusted score for handle
		score = 0
		for taskI in handlesSolved[handle]:
			solvedFraction = numberSolved[taskI]/participants
			score += (1 - math.log(solvedFraction))

		scaledScore = score / avgScore
		return scaledScore
		
	# re-fetches all scores (may take a while)
	# sets allStandings
	@abstractmethod
	def updateScores(self):
		pass
