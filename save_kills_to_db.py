import sqlite3 
from sqlite3 import Error 
from db_controller import mailDB
from fetch_jsons import read_json

def json_to_database(corporationID):
  zkb_json = read_json(corporationID, "zkill")
  ccp_json = read_json(corporationID, "ccp")

if __name__ == '__main__':
  killmails_db = mailDB("killmails.db")
