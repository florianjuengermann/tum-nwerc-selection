import telegram as tg
import main
import time, traceback
from ranking import Ranking
from util import Table
import util

#infinity, so no contest reminder is sent during first run of checkUpcomingContest()
lastTimeChecked = 1e15

def handleRanking(chatId, txt):
  table = ranking.getTable()
  n = len(ranking.getContestNames())
  msg = "Current standings after __n={}__ contests:\n".format(n)
  msg_ineligible = ">> Contestants marked with \* are ineligible <<"
  tg.sendMessage(chatId, msg + "```\n" + table.toStr(width=25) + "```\n" + msg_ineligible)

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

def msgAll(text):
  print("send: {}".format(text))
  for chatId in chatIds:
    tg.sendMessage(chatId, text)

def checkAnnouncement():
  global lastTimeChecked
  dates = ranking.getDates()
  curTimeCheck = time.time()
  for d in dates:
    oneDayBef = d["time"] - 60*60*24
    twoHourBef = d["time"] - 60*60*2
    type = d["type"].capitalize()
    if lastTimeChecked < twoHourBef and twoHourBef <= curTimeCheck:
      msgAll("**Reminder:** Rated {} contest starts in 2h.".format(type))
    if lastTimeChecked < oneDayBef and oneDayBef <= curTimeCheck:
      msgAll("**Reminder:** Rated {} contest starts in 24h.".format(type))
  lastTimeChecked = curTimeCheck

def updateUpcomingContest():
  ranking.updateDates()

def mainLoop():
  global config
  global ranking
  global chatIds
  config = util.readConfig()
  ranking = Ranking(config)
  chatIds = util.readChatIds()

  tg.readRequestUrl()
  callbacks = [
  (updateUpcomingContest,3600,0),
  (checkAnnouncement,60,0),
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
