from ranking import Ranking
import util
from util import Table, readConfig
from contestDates import ContestDates

if __name__ == '__main__':
	config = readConfig()

	contestDates = ContestDates(config)
	newContestDates = contestDates.getDates()
	print(newContestDates)

	ranking = Ranking(config)
	table = ranking.getTable()
	print("\nSTANDINGS:\n ")
	print(table.toStr(width=80))
	print(">> Contestants marked with * are ineligible <<")
