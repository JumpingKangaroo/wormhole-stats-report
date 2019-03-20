import json
import requests

# This script takes in the json filename, and processes it to 
# count kills.

def read_json(corporationID, mailType):
  with open(corporationID + '_' + mailType + ".json") as json_file:
    data = json.load(json_file)
  return data

def calculate_efficiency(zkb_json, ccp_json, corporationID):
    killsSum = 0
    lossesSum = 0
    for kill in zkb_json:
        # check if its a loss, else its a kill
        if ccp_json[kill["killmail_id"]]["victim"]["corporation_id"] == corporationID:
            lossesSum += kill["zkb"]["totalValue"]
        else:
            killsSum += kill["zkb"]["totalValue"]
    efficiency = killsSum / lossesSum
    return efficiency 

# Returns a dict with the 
def process_kills(corporationID):
    zkill_json = read_json(corporationID, "zkill")
    ccp_json = read_json(corporationID, "ccp")
    statsDict = {}
    statsDict["name"] = corporationID
