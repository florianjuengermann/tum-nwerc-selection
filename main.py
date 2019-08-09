import json
from ranking import Ranking

def readConfig():
  global config
  with open('config.json') as f:
    config = json.load(f)
    print(config)

readConfig()
ranking = Ranking(config)
names = ranking.getNames()
standings = ranking.getStandings()
for name, scores in zip(names, stadings):
  rowStr = name + ":"
  for score in scores:
    rowStr.append(" " + str(score))
  print(rowStr)
