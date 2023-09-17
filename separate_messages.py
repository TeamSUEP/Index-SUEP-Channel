import datetime
import json

with open("dist/messages.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

messages.sort(key=lambda m: m["ctime"], reverse=True)

messages_by_year = {}
for m in messages:
    year = datetime.datetime.fromtimestamp(m["ctime"]).strftime("%Y")
    if year not in messages_by_year:
        messages_by_year[year] = []
    messages_by_year[year].append(m)

for year in messages_by_year:
    with open(f"{year}.json", "w", encoding="utf-8") as f:
        json.dump(messages_by_year[year], f, indent=4, ensure_ascii=False)
