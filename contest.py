from abc import ABC

class Contest(ABC):
	"""abstract contest"""
	id = "" 						# contest ID
	name = ""
	allStandings = None # [{"handle":…,"solved": <bool> }]
	handleString = "" 	# ∈ {"codefores-handle", "atcoder-handle"}
	handleMap = None 		# [{"clear-name":…, "codforces-handle": …, "atc.h":…}]
	def __init__(self, id, handleMap):
		self.handleMap
		self.id = id

	# clear name of user (not handle) -> score in this contest
	def getScore(name: str) -> float:
		if allStandings is None:
			self.updateScores()
		return 1.0

		
	# re-fetches all scores (may take a while)
	# sets allStandings
	@abstractmethod
	def updateScores():
		pass
