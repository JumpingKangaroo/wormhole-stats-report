from db_controller import mailDB
import json

def write_file(data, filename):
  with open(filename, "w") as dataFile:
    dataFile.write(json.dumps(data, indent=4, sort_keys=False))

def calculateStats(database):
  finalSums = {}
  c = database.getCursor()
  # Get list of all distinct corpIDs
  c.execute(''' SELECT DISTINCT corpID
    FROM killmails
    ''')
  corpIDs = []
  for corpID in c:
    corpIDs.append(corpID[0])

  # Calculate stats for every corp
  for corpID in corpIDs:
    # Set up data tuple for sql, and setup dict to store results
    data = (corpID,)
    finalSums[corpID] = {}
    # Find sum of value of total kills
    c.execute(''' SELECT SUM(totalValue)
      FROM killmails 
      WHERE corpID IS ?
    ''', data)
    finalSums[corpID]["totalKillsValue"] = round(c.fetchone()[0], 1)
    # Find sum of value of total losses
    c.execute(''' SELECT SUM(totalValue)
      FROM lossmails 
      WHERE corpID IS ?
    ''', data)
    finalSums[corpID]["totalLossesValue"] = round(c.fetchone()[0], 1)
    # Calculate efficiency
    finalSums[corpID]["efficiency"] = round(finalSums[corpID]["totalKillsValue"] / (finalSums[corpID]["totalKillsValue"] + finalSums[corpID]["totalLossesValue"]) * 100, 1)


  # Save data to json file
  write_file(finalSums, "stats.json")

if __name__ == "__main__":
  killmails_db = mailDB("killmails.db")
  calculateStats(killmails_db)
  