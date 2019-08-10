from ranking import Ranking
import util
from util import Table, readConfig

if __name__ == '__main__':
	config = readConfig()
	ranking = Ranking(config)
	table = ranking.getTable()
	print("\nSTANDINGS:\n ")
	print(table.toStr(width=80))
