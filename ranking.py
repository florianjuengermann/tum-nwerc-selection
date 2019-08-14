from contest import Contest
import contestDates as dates
from codeforcesContest import CodeforcesContest
from atcoderContest import AtcoderContest
from contestDates import ContestDates
from util import Table
import time

class Ranking:
  def __init__(self, config):
    self.contestObjList = [] #contains only past or started contest objects
    self.contestDateList = [] #contains past and future contest dates
    self.handleMap = config['users']
    self.startDate = config['startDate']
    self.endDate = config['endDate']
    self.contestDates = ContestDates(config)
    self.updateRanking()

  def getRanking(self):
    return self.ranking

  def getNames(self):
    return self.names

  def getDates(self):
    return self.contestDateList

  def getContestNames(self):
    return [c.name for c in self.contestObjList]

  def updateRanking(self):
    self.contestDateList = []
    self.fetchContests()
    self.calcStandings()

  def fetchContests(self):
    newContestDates = self.contestDates.getDates()
    if newContestDates != self.contestDates:
      self.contestDateList = newContestDates
      self.contestObjList = []
      for date in self.contestDateList:
        if date['time'] > time.time():
          continue
        if date['type'] == 'atcoder':
          self.contestObjList.append(AtcoderContest(date['id'], self.handleMap))
        else:
          self.contestObjList.append(CodeforcesContest(date['id'], self.handleMap))

  def calcStandings(self):
    self.names = self.handleMap.keys()
    self.ranking = []
    '''
    # TEST
    cache = [[3.664998986028648], [3.664998986028648], [1.3171947472706973], [5.651676218323456], [0.0]]
    cache = [x*15 for x in cache]
    self.ranking = cache
    return
'''
    for name in self.names:
      currentNameScores = []
      for c in self.contestObjList:
        currentNameScores.append(c.getScore(name))
      self.ranking.append(currentNameScores)

  def sortingKey(self, pair):
    name, scores = pair
    # sort descending
    scoresCopy = scores.copy()
    scoresCopy.sort()
    scoresCopy.reverse()
    n = len(scoresCopy)
    scoreSum = 0
    # take ceil(n/2) scores
    for i in range((n+1)//2):
      scoreSum += scoresCopy[i]
    return scoreSum

  def getTable(self) -> Table:
    table = Table()
    table.setHead("", self.getContestNames())
    lst = zip(self.names, self.ranking)
    for name, scores in reversed(sorted(lst, key=self.sortingKey)):
      scoreStrings = ["{:04.2f}".format(s) for s in scores]
      table.addRow("{:.15}".format(name), scoreStrings)
    return table
