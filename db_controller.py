import sqlite3, os
from sqlite3 import Error 

DEBUG = False

def create_connection(db_file):
  try: 
    conn = sqlite3.connect(db_file)
    if DEBUG: print(sqlite3.version)
    return conn
  except Error as e:
    print(e)
    return None

def migrate_db():
  killmails_db = create_connection("killmails.db")
  c = killmails_db.cursor()

  c.execute(''' CREATE TABLE killmails (
    id integer, hash text, locationID integer, fittedValue real, 
    npc integer, awox integer, attackers text, victimShipType int,
    victimDamage int, victimCorp int, victimAlliance int
  ) ''')

  killmails_db.close()

if __name__ == '__main__':
  os.remove("killmails.db")
  migrate_db()
  db = create_connection("killmails.db")
  c = db.cursor()
  c.execute("SELECT * FROM killmails")
  for row in c:
    print(row)

  db.close()
