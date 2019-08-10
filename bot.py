import telegram as tg
import main
import time, traceback
from ranking import Ranking
from util import Table
import util

def handleRanking(chatId, txt):
  table = ranking.getTable()
  tg.sendMessage(chatId, "```\n" + table.toStr(width=32) + "```")

def invalidCommand(cid, msg):
  tg.sendMessage(cid, "Invalid command!")

def handleMessage(chatId, text):
  if not chatId in chatIds:
    chatIds.append(chatId)
    util.saveChatIds(chatIds)
  print("-> " + text + " <-")
  text = text.replace("@tum_nwerc_selection_bot", "")
  msgSwitch = {
    "/ranking": handleRanking
  }
  func = msgSwitch.get(text.lower().strip(), invalidCommand)
  func(str(chatId), text)

def update():
  #global ranking
  print("updating ranking object")
  ranking.update()

def checkUpcomingContest():
  dates = ranking.getDates()
  for d in dates:
    curT = time.time()
    oneDayBef = d["time"] - 60*60*24
    twoHourBef = d["time"] - 60*60*2
    if curT > oneDayBef and curT < oneDayBef + 60:
      pass
    if curT > oneDayBef and curT < oneDayBef + 60:
      pass



def mainLoop():
  global config
  global ranking
  global chatIds
  config = util.readConfig()
  ranking = Ranking(config)
  chatIds = util.readChatIds()

  tg.readRequestUrl()
  callbacks = [
  (update, 3600, time.time()),
  (checkUpcomingContest,60,0),
  (tg.startPolling,1,0)
  ]
  while True:
    for i in range(len(callbacks)):
      (fun, timeIt, lastTimeStamp) = callbacks[i]
      if time.time() - lastTimeStamp >= timeIt:
        callbacks[i] = (fun, timeIt, time.time())
        try:
          fun()
        except Exception as e:
          traceback.print_exc()
          print(traceback.format_exc())
    time.sleep(0.01)
