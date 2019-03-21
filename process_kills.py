import json
import requests

# This script takes in the json filename, and processes it to 
# count kills.

DEBUG = True

def read_json(corporationID, mailType):
  with open(str(corporationID) + '_' + mailType + ".json") as json_file:
    data = json.load(json_file)
  return data

def calculate_efficiency(zkb_json, ccp_json, corporationID):
    killsSum = 0.0
    killCount = 0
    lossesSum = 0.0
    lossesCount = 0
    for kill in zkb_json:
        # If its an NPC kill, skip
        # if kill["zkb"]["npc"] or kill["zkb"]["awox"]:
        #   continue
        # check if its a loss, else its a kill
        if str(ccp_json[str(kill["killmail_id"])]["victim"]["corporation_id"]) == str(corporationID):
            # if DEBUG: print (kill["killmail_id"], "\tis a loss worth \t{:,}".format(kill["zkb"]["totalValue"]), "\tKill url:", "https://zkillboard.com/kill/" + str(kill["killmail_id"]) + "/")
            lossesSum += kill["zkb"]["totalValue"]
            lossesCount += 1
        else:
            if DEBUG: print (kill["killmail_id"], "\tis a kill worth \t{:,}".format(kill["zkb"]["totalValue"]), "\tKill url:", "https://zkillboard.com/kill/" + str(kill["killmail_id"]) + "/")
            killsSum += kill["zkb"]["totalValue"]
            killCount += 1
    if DEBUG: print ("Kill count:", killCount)
    if DEBUG: print ("Loss count:", lossesCount)
    if DEBUG: print ("zkb count: {:,} ccp count: {:,}".format(len(zkb_json), len(ccp_json)))
    print("Kills sum: {:,}".format(killsSum))
    print("Losses sum: {:,}".format(lossesSum))
    return (killsSum, lossesSum)

# Takes in a list of corporation IDs, and returns a dict of the stats
def process_kills(corporationIDs):
    statsDict = {}
    for corpID in corporationIDs:
      zkill_json = read_json(corpID, "zkill")
      ccp_json = read_json(corpID, "ccp")
      statsDict[corpID] = {}
      statsDict[corpID]["corporationID"] = corpID
      killsSum, lossesSum = calculate_efficiency(zkill_json, ccp_json, corpID)
      statsDict[corpID]["killsSum"] = killsSum
      statsDict[corpID]["lossesSum"] = lossesSum
    return statsDict

# result = process_kills([98504356]) # mcav
result = process_kills([1705300610]) # mcav
# print("Kills sum: {:,}".format(result[98504356]["killsSum"]))
# print("Losses sum: {:,}".format(result[98504356]["lossesSum"]))
