import json, requests, time
import sys, traceback, random
codeforcesUrl = 'https://codeforces.com/api/'

def request(method, params):
  rnd = random.randint(0, 100000)
  rnd = str(rnd).zfill(6)
  tailPart = method + '?'

  for key in sorted(params):
    tailPart += key + '=' + str(params[key]) + '&'
  request = codeforcesUrl

  request += tailPart
  try:
    r = requests.get(request, timeout=15)
  except requests.exceptions.Timeout as errt:
    print("Timeout on Codeforces.", errt)
    return False
  r = r.json()
  if r['status'] == 'OK':
    return r['result']
  else:
    return False
