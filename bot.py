import telegram as tg
import main
import time, traceback

def handleRanking(chatId, txt):
  table = main.getRankingTable()
  tg.sendMessage(chatId, "```\n" + table.toStr(width=32) + "```")

def invalidCommand(cid, msg):
  tg.sendMessage(cid, "Invalid command!")

def handleMessage(chatId, text):
  print("-> " + text + " <-")
  text = text.replace("@tum_nwerc_selection_bot", "")
  msgSwitch = {
    "/ranking": handleRanking
  }
  func = msgSwitch.get(text.lower().strip(), invalidCommand)
  func(str(chatId), text)


def mainLoop():
  tg.readRequestUrl()
  callbacks = [
  #(cf.loadCurrentContests, 3600, time.time()),
  #(checkUpcomingContest,50,0)
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
