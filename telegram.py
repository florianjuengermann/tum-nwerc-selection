import json, requests, time, urllib.parse
import sys, traceback, random, hashlib, os
import bot

requestUrl = ''
lastUpdateID = -1

def readRequestUrl():
  global requestUrl
  if os.path.isfile('.telegram_api_url'):
    requestUrl = [line.rstrip('\n') for line in open('.telegram_api_url')][0]

def sendMessage(chatId, text, reply_markup = None):
  if requestUrl == '':
    return
  # dont send msg 100sec after restart
  #if time.time() - RESTART < 100:
  #  return
  params = {
  'parse_mode':'Markdown',
  'chat_id':str(chatId),
  'text':text,
  'reply_markup': reply_markup
  }
  try:
    r = requests.post(requestUrl + 'sendMessage', data=params, timeout=5)
    r = r.json()
    if r['ok']:
      return r['result']['message_id']
    else:
      print('!!!!!Fehler beim senden der Nachricht: ' + r['description']+ " !!!!!")
      return False
  except Exception as e:
    traceback.print_exc()
    print(traceback.format_exc())
    return False


def poll():
  if requestUrl == '':
    return []
  try:
    r = requests.get(requestUrl + 'getUpdates?offset=' + str(lastUpdateID+1), timeout=5)
    r = r.json()
  except Exception as e:
    traceback.print_exc()
    print(traceback.format_exc())
    return []
  if r['ok']:
    return r['result']
  else:
    return []

def startPolling():
  curUpd = poll()
  for u in curUpd:
    handleUpdate(u)

def handleUpdate(update):
  global lastUpdateID
  lastUpdateID = update['update_id']
  if 'message' in update:
    bot.handleMessage(update['message']['chat']['id'], update['message']['text'])
  elif 'edited_message' in update:
    bot.handleMessage(update['edited_message']['chat']['id'], update['edited_message']['text'])
  

