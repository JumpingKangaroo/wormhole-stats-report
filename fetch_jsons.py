import requests 
import time
import json

DEBUG = True

def write_file(filename, data):
  dataFile = open(filename + ".json", "w")   
  # parsedJson = json.loads(data)
  dataFile.write(json.dumps(data, indent=2, sort_keys=False))

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

def fetch_corporation_kills(corporationName, corporationId, month):
  pageNumber = 1
  headers = { 'user-agent': 'Maintainer: Arya Elf-Bron', 'Accept-Encoding': 'gzip'}
  urlParams = [ 'corporationID', str(corporationId), 'month', month, 'page' ]
  if DEBUG: print("requesting page:", pageNumber) 
  url = get_url(urlParams, pageNumber)
  r = requests.get(url, headers=headers)
  r = r.json()
  finalJson = r
  if DEBUG: print("length of r:", len(r)) 
  while len(r) == 200:
    pageNumber += 1
    time.sleep(3)
    if DEBUG: print("requesting page:", pageNumber)
    url = get_url(urlParams, pageNumber) 
    r = requests.get(url, headers=headers)
    r = r.json()
    finalJson = finalJson + r
    if DEBUG: print("length of r:", len(r)) 
  if DEBUG: print("Final length", len(finalJson))
  if DEBUG: print('Now saving to file')
  write_file(corporationName, finalJson)

      
  
fetch_corporation_kills("mcav", 98504356, 2)

