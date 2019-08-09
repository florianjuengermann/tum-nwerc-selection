from contest import Contest
import contestDates as dates
from codeforcesContest import CodeforcesContest

class Ranking:
  def __init__(self, config):
    self.contestList = []
    self.handleMap = config['users']
    self.startDate = config['startDate']
    self.endDate = config['endDate']
    self.updateRanking()

  def getRanking(self):
    return self.ranking

  def getNames(self):
    return self.names

  def updateRanking(self):
    self.contestDates = []
    self.fetchContests()
    self.calcStandings()

  def fetchContests(self):
    newContestDates = dates.getDates()
    if newContestDates != self.contestDates:
      self.contestDates = newContestDates
      self.contestList = []
      for date in self.contestDates:
        if date['type'] == 'atcoder':
          self.contestList.append(AtcoderContest(date['id'], self.handleMap))
        else:
          self.contestList.append(CodeforcesContest(date['id'], self.handleMap))

  def calcStandings(self):
    self.names = self.handleMap.keys()
    self.ranking = []
    for name in self.names:
      currentNameScores = []
      for c in self.contestList:
        currentNameScores.append(c.getScore(name))
      self.ranking.append(currentNameScores)

