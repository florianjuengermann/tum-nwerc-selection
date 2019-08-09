from contest import Contest
import contestDates as dates
from codeforcesContest import CodeforcesContest

class Ranking:
  def __init__(self, handles):
    self.contestList = []
    self.handleMap = handles
    self.updateRanking()

  def getRanking(self):
    return self.ranking

  def updateRanking():
    fetchContests()
    calcStandings()

  def fetchContests():
    newContestDates = dates.getDates()
    if newContestDates != self.contestDates:
      self.contestDates = newContestDates
      contestList = []
      for date in self.contestDates:
        if date['type'] == 'atcoder':
          contestList.append(AtcoderContest(date['id']), self.handleMap)
        else:
          contestList.append(CodeforcesContest(date['id']), self.handleMap)

  def calcStandings():
    self.names = handleMap.keys()
    standings = []
    for name in self.names:
      currentNameScores = []
      for c in contestList:
        currentNameScores.append(c.getScore(name))
      standings.append(currentNameScores)

