import sqlite3 
from sqlite3 import Error 
from db_controller import mailDB
from fetch_jsons import read_json

def json_to_database(corporationID, mails_db):
  zkb_json = read_json(corporationID, "zkill")
  ccp_json = read_json(corporationID, "ccp")
  for kill in zkb_json["kills"]:
    mails_db.addKillmail(kill, ccp_json["kills"][str(kill["killmail_id"])], "kill", corporationID)
  for loss in zkb_json["losses"]:
    mails_db.addKillmail(loss, ccp_json["losses"][str(loss["killmail_id"])], "loss", corporationID)
  

if __name__ == '__main__':
  killmails_db = mailDB("killmails.db", blank=True)
  json_to_database(98504356, killmails_db)
