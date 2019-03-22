import sqlite3, os, json
from sqlite3 import Error 

class mailDB:

  DEBUG = True

  def __init__(self, db_file):
    try: 
      self.conn = sqlite3.connect(db_file)
      self.cursor = self.conn.cursor()
      if self.DEBUG: print(sqlite3.version)
    except Error as e:
      print(e)
      return None

  def __del__(self):
    self.cursor.close()
    self.conn.close()

  def getCursor(self):
    return self.cursor

  def migrate(self):
    c = self.conn.cursor()

    c.execute(''' CREATE TABLE killmails (
      id integer, hash text, locationID integer, fittedValue real, 
      npc integer, awox integer, attackers text, victimShipType int,
      victimDamage int, victimCorp int, victimAlliance int
    ) ''')

    c.execute(''' CREATE TABLE lossmails (
      id integer, hash text, locationID integer, fittedValue real, 
      npc integer, awox integer, attackers text, victimShipType int,
      victimDamage int, victimCorp int, victimAlliance int
    ) ''')

  def addKillmail(self, zkbKill, ccpKill, mailType):
    # Load info from zkill dict
    killID = int(zkbKill["killmail_id"])
    killHash = str(zkbKill["zkb"]["hash"])
    locationID = int(zkbKill["zkb"]["locationID"])
    fittedValue = float(zkbKill["zkb"]["fittedValue"])
    npc = int(zkbKill["zkb"]["npc"])
    awox = int(zkbKill["zkb"]["awox"])
    
    # Load info from CCP dict (serializing lists)
    attackers = str(json.dumps(ccpKill["attackers"]))
    victimShipType = int(ccpKill["victim"]["ship_type_id"])
    victimDamage = int(ccpKill["victim"]["damage_taken"])
    victimCorp = int(ccpKill["victim"]["corporation_id"])
    victimAlliance = int(ccpKill["victim"]["corporation_id"])
    # Assemble tuple
    data = (killID, killHash, locationID, fittedValue, npc, awox, attackers, 
            victimShipType, victimDamage, victimCorp, victimAlliance)
    if mailType == "kill":
      # Add to killmails table
      self.cursor.execute('''INSERT INTO killmails 
          VALUES (?,?,?,?,?,?,?,?,?,?,?)''', data)
    elif mailType == "loss":
      # Add to losses table
      self.cursor.execute('''INSERT INTO lossmails 
          VALUES (?,?,?,?,?,?,?,?,?,?,?)''', data)
    else:
      # Invalid kill type
      print ("Error, unexpected kill type") 



if __name__ == '__main__':
  os.remove("killmails.db")
  db = mailDB("killmails.db")
  c = db.getCursor()
  db.migrate()
  c.execute("SELECT * FROM killmails")
  for row in c:
    print(row)

