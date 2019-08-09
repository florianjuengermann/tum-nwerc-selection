import json
from ranking import Ranking

def readConfig():
  global config
  with open('config.json') as f:
    config = json.load(f)
    #print(config)

readConfig()
ranking = Ranking(config)
names = ranking.getNames()
standings = ranking.getRanking()
print("\n------------- STANDINGS -----------------")
for name, scores in zip(names, standings):
  rowStr = "{:20}: ".format(name)
  for score in scores:
    rowStr += " {:04.2f}".format(score)
  print(rowStr)
print("-----------------------------------------\n")
