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
standings = ranking.getRanking()
for name, scores in zip(names, standings):
  rowStr = name + ":"
  for score in scores:
    rowStr.append(" " + str(score))
  print(rowStr)
