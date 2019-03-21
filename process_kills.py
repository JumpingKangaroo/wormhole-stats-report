import json
import requests

# This script takes in the json filename, and processes it to 
# count kills.

# Verbose DEBUG output
DEBUG = False

# Read in a given corps json, depending on the type
def read_json(corporationID, mailType):
  with open(str(corporationID) + '_' + mailType + ".json") as json_file:
    data = json.load(json_file)
  return data

# Write out a given json to a _stats.json file
def write_file(corpID, data):
  with open(str(corpID) + "_stats.json", "w") as dataFile:
    dataFile.write(json.dumps(data, indent=2, sort_keys=False))


# Takes in the zkb_json of a corp and returns the sum of kills and losses
def calculate_efficiency(zkb_json):
  killsSum = 0.0
  lossesSum = 0.0
  for kill in zkb_json["kills"]:
    killsSum += kill["zkb"]["totalValue"]
  for loss in zkb_json["losses"]:
    lossesSum += loss["zkb"]["totalValue"]

  # Debug print statements
  if DEBUG: print ("Kill count:", len(zkb_json["kills"]))
  if DEBUG: print ("Loss count:", len(zkb_json["losses"]))
  if DEBUG: print ("zkb count: {:,}".format(len(zkb_json)))
  
  return (killsSum, lossesSum)

# Takes in a list of corporation IDs, and returns a dict of the stats
def process_kills(corporationIDs):
  statsDict = {}
  # For each corp ID given, calculate statistics and add to dict
  for corpID in corporationIDs:
    # Read in the jsons from files 
    zkill_json = read_json(corpID, "zkill")

    # Create a new statsDict entry with the corp ID
    statsDict[corpID] = {}
    statsDict[corpID]["corporationID"] = corpID
    # Now start calculating stats

    # Calculate kills/losses sum and save to dict
    killsSum, lossesSum = calculate_efficiency(zkill_json)
    statsDict[corpID]["killsSum"] = killsSum
    statsDict[corpID]["lossesSum"] = lossesSum

    # TODO calculate the following stats:
    # Wormhole only kills/deaths
    # Ratio of k-space to wh kills
    # Capital kills (seperated by type?)
    # Amount killed in home vs out of home?
    # NPC only losses
    # Dictors (sorted by type)
    

    # Save stats dict to file 
    write_file(corpID, statsDict)

# result = process_kills([98504356]) # mcav
process_kills([98504356]) # mcav
