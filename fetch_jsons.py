import requests 
import time
import json

DEBUG = True

def write_file(corpID, data, mailType):
  with open(str(corpID) + "_" + mailType + ".json", "w") as dataFile:
    dataFile.write(json.dumps(data, indent=2, sort_keys=False))

def read_zkb_json(corpID):
  with open(corpID + "_zkill.json") as json_file:
    data = json.load(json_file)
  return data

def read_json(corporationID, mailType):
  with open(str(corporationID) + '_' + mailType + ".json") as json_file:
    data = json.load(json_file)
  return data


def get_url(params, pageNumber):
  url = 'https://zkillboard.com/api/'
  for param in params:
    if param == "page":
      if pageNumber > 1:
        url += str(param) + '/' + str(pageNumber) + "/" 
    else:
      url += str(param) + "/"
  if DEBUG: print("url:", url) 
  return url

def fetch_ccp_kill_info(zkb_json):
  ccp_json = {}
  ccp_json["kills"] = {}
  ccp_json["losses"] = {}
  headers = { "Accept": "application/json" }
  i = 0
  size = len(zkb_json["kills"])
  for kill in zkb_json["kills"]:
    baseUrl = "https://esi.evetech.net/dev/killmails/"
    url = baseUrl + str(kill["killmail_id"]) + "/" + kill["zkb"]["hash"] + "/"
    if DEBUG: print("Getting:", i, "of", size, "\tccp url:", url)
    success = False 
    while not success:
      try:
        r = requests.get(url, headers=headers)
        ccp_json["kills"][int(kill["killmail_id"])] = r.json()
        success = True 
      except:
        print ("Failed, retrying")
        pass
    i += 1
    time.sleep(0.3)

  i = 0
  size = len(zkb_json["losses"])
  for loss in zkb_json["losses"]:
    baseUrl = "https://esi.evetech.net/dev/killmails/"
    url = baseUrl + str(loss["killmail_id"]) + "/" + loss["zkb"]["hash"] + "/"
    if DEBUG: print("Getting:", i, "of", size, "\tccp url:", url)
    success = False 
    while not success:
      try:
        r = requests.get(url, headers=headers)
        ccp_json["losses"][int(loss["killmail_id"])] = r.json()
        success = True 
      except:
        print ("Failed, retrying")
        pass
    i += 1
    time.sleep(0.3)

  return ccp_json

def fetch_corporation_kills_zkill(corpID, month):
  pageNumber = 1
  json_zkill = {}
  headers = { 'user-agent': 'Maintainer: Arya Elf-Bron', 'Accept-Encoding': 'gzip'}
  urlParams = [ 'corporationID', str(corpID), 'npc', 0, 'kills', 'month', month, 'page' ]

  if DEBUG: print("requesting kills page:", pageNumber) 
  url = get_url(urlParams, pageNumber)
  r = requests.get(url, headers=headers)
  r = r.json()
  json_zkill["kills"] = r
  if DEBUG: print("length of r:", len(r)) 
  while len(r) == 200:
    pageNumber += 1
    time.sleep(1)
    if DEBUG: print("requesting kills page:", pageNumber)
    url = get_url(urlParams, pageNumber) 
    r = requests.get(url, headers=headers)
    r = r.json()
    json_zkill["kills"] += r
    if DEBUG: print("length of r:", len(r)) 
  if DEBUG: print("Final length", len(json_zkill))
  
  urlParams = [ 'corporationID', str(corpID), 'losses', 'npc', 0, 'month', month, 'page' ]

  pageNumber = 1
  if DEBUG: print("requesting losses page:", pageNumber) 
  url = get_url(urlParams, pageNumber)
  r = requests.get(url, headers=headers)
  r = r.json()
  json_zkill["losses"] = r
  if DEBUG: print("length of r:", len(r)) 
  while len(r) == 200:
    pageNumber += 1
    time.sleep(1)
    if DEBUG: print("requesting losses page:", pageNumber)
    url = get_url(urlParams, pageNumber) 
    r = requests.get(url, headers=headers)
    r = r.json()
    json_zkill["losses"] += r
    if DEBUG: print("length of r:", len(r)) 
  if DEBUG: print("Final num of kills", len(json_zkill["kills"]))
  if DEBUG: print("Final num of losses", len(json_zkill["losses"]))

  if DEBUG: print("Now fetching from CCP servers")
  write_file(corpID, json_zkill, "zkill")
  if DEBUG: print('Now saving to file')
  return json_zkill



json_zkill = fetch_corporation_kills_zkill(98504356, 2) 
json_ccp = fetch_ccp_kill_info(json_zkill)
write_file(98504356, json_ccp, "ccp")

