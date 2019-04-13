from save_kills_to_db import json_to_database
from fetch_jsons import fetch_corp_info
from db_controller import mailDB

# Configuration of script
corpIDs = [98504356, 98293472]
month = 3

# Setup database
killmails_db = mailDB("killmails.db", blank=True)

for corpID in corpIDs:
  # fetch_corp_info(corpID, month)
  json_to_database(corpID, killmails_db)