from save_kills_to_db import json_to_database
from fetch_jsons import fetch_corp_info
from db_controller import mailDB
import json

def read_json(filename):
  with open(filename) as json_file:
    data = json.load(json_file)
  return data

# Configuration of script
month = 3

# Read in corp IDs from names.json
json_names = read_json("names.json")
corpIDs = []
for key in json_names:
  corpIDs.append(int(key))
print("IDs:", corpIDs)

# Setup database
killmails_db = mailDB("killmails.db", blank=True)

for corpID in corpIDs:
  fetch_corp_info(corpID, month)
  json_to_database(corpID, killmails_db)