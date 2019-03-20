import json

def read_corp_json(corpname):
  with open(corpname + ".json") as json_file:
    data = json.load(json_file)
  return data

json_read = read_corp_json("mcav")
print(json.dumps(json_read, indent=2, sort_keys=False))