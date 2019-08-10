import json
from ranking import Ranking
from util import Table

def readConfig():
  global config
  with open('config.json') as f:
    config = json.load(f)
    #print(config)

def sortingKey(pair):
	name, scores = pair
	# sort descending
	scores.sort()
	scores.reverse()
	n = len(scores)
	scoreSum = 0
	# take ceil(n/2) scores
	for i in range((n+1)//2):
		scoreSum += scores[i]
	return scoreSum

#table = Table()


#exit()

readConfig()
ranking = Ranking(config)
names = ranking.getNames()
standings = ranking.getRanking()
table = Table()
table.setHead("Names", ranking.getContestNames())
print("\nSTANDINGS:\n ")
for name, scores in reversed(sorted(zip(names, standings), key=sortingKey)):
	scoreStrings = ["{:04.2f}".format(s) for s in scores]
	table.addRow("{:.15}".format(name), scoreStrings)

print(table.toStr(width=60))
