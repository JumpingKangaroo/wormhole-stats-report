import sqlite3, os, json
from sqlite3 import Error 

class mailDB:

  DEBUG = True

  def __init__(self, db_filename, blank=False):
    try: 
      if blank:
        # os.remove(db_filename)
        self.conn = sqlite3.connect(db_filename)
        self.migrate()
      else:
        self.conn = sqlite3.connect(db_filename)        
      self.cursor = self.conn.cursor()
      if self.DEBUG: print(sqlite3.version)
    except Error as e:
      print(e)
      return None

  def __del__(self):
    self.conn.commit()
    self.cursor.close()
    self.conn.close()

  def getCursor(self):
    return self.cursor

  def migrate(self):
    c = self.conn.cursor()

    c.execute(''' CREATE TABLE killmails (
      id integer, hash text, locationID integer, fittedValue real, 
      npc integer, awox integer, attackers text, victimShipType integer,
      victimDamage integer, victimCorp integer, victimAlliance integer,
      corpID integer
    ) ''')

    c.execute(''' CREATE TABLE lossmails (
      id integer, hash text, locationID integer, fittedValue real, 
      npc integer, awox integer, attackers text, victimShipType integer,
      victimDamage integer, victimCorp integer, victimAlliance integer, 
      corpID integer
    ) ''')

  def addKillmail(self, zkbKill, ccpKill, mailType, corpID):
    print("Adding killmail")
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

    # Cast corpID in case I'm bad
    corpID = int(corpID)

    # Assemble tuple
    data = (killID, killHash, locationID, fittedValue, npc, awox, attackers, 
            victimShipType, victimDamage, victimCorp, victimAlliance, corpID)
    if mailType == "kill":
      # Add to killmails table
      print("adding to kills table")
      self.cursor.execute('''INSERT INTO killmails 
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', data)
    elif mailType == "loss":
      # Add to losses table
      print("adding to losses table")
      self.cursor.execute('''INSERT INTO lossmails 
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', data)
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

