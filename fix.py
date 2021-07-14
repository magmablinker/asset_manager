import glob
import json
from datetime import datetime
from pprint import pprint

oldFormat = "%d-%m-%Y %H:%M:%S"
newFormat = "%Y-%m-%dT%H:%M:%S"

#files = glob.glob("data/assets/*.json")
files = []
files.append("data/total_balance.json")

for file in files:
    with open(file, "r") as f:
        data = json.load(f)

    for entry in data["data"]:
        entry["timestamp"] = datetime.strptime(entry["timestamp"], oldFormat).strftime(newFormat)

    with open(file, "w") as f:
        json.dump(data, f, indent=4)