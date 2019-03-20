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
  headers = { "Accept": "application/json" }
  i = 0
  size = len(zkb_json)
  for kill in zkb_json:
    baseUrl = "https://esi.evetech.net/dev/killmails/"
    url = baseUrl + str(kill["killmail_id"]) + "/" + kill["zkb"]["hash"] + "/"
    if DEBUG: print("Printing:", i, "of", size, "\tccp url:", url)
    r = requests.get(url, timeout=1, headers=headers)
    ccp_json[kill["killmail_id"]] = r.json()
  return ccp_json

def fetch_corporation_kills_zkill(corpID, month):
  pageNumber = 1
  headers = { 'user-agent': 'Maintainer: Arya Elf-Bron', 'Accept-Encoding': 'gzip'}
  urlParams = [ 'corporationID', str(corpID), 'month', month, 'page' ]
  if DEBUG: print("requesting page:", pageNumber) 
  url = get_url(urlParams, pageNumber)
  r = requests.get(url, headers=headers, timeout=1)
  r = r.json()
  json_zkill = r
  if DEBUG: print("length of r:", len(r)) 
  while len(r) == 200:
    pageNumber += 1
    time.sleep(1)
    if DEBUG: print("requesting page:", pageNumber)
    url = get_url(urlParams, pageNumber) 
    r = requests.get(url, headers=headers)
    r = r.json()
    json_zkill = json_zkill + r
    if DEBUG: print("length of r:", len(r)) 
  if DEBUG: print("Final length", len(json_zkill))
  if DEBUG: print("Now fetching from CCP servers")
  json_ccp = fetch_ccp_kill_info(json_zkill)
  if DEBUG: print('Now saving to file')
  write_file(corpID, json_ccp, "ccp")
  write_file(corpID, json_zkill, "zkill")



fetch_corporation_kills_zkill(98504356, 2)

