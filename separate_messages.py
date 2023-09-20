import datetime
import json
import os


def split_year(source_file, dest_folder, year):
    with open(source_file, "r", encoding="utf-8") as f:
        messages = json.load(f)

    messages.sort(key=lambda m: m["ctime"], reverse=True)

    messages = [
        m
        for m in messages
        if datetime.datetime.fromtimestamp(m["ctime"]).strftime("%Y") == year
    ]

    messages_by_month = {}
    for m in messages:
        month = datetime.datetime.fromtimestamp(m["ctime"]).strftime("%m")
        if month not in messages_by_month:
            messages_by_month[month] = []
        messages_by_month[month].append(m)

    for month, messages in messages_by_month.items():
        month_file = os.path.join(dest_folder, f"{year}/{month}.json")
        os.makedirs(os.path.dirname(month_file), exist_ok=True)
        with open(month_file, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    year_files = {}
    for root, dirs, files in os.walk("dist/data/years"):
        for file in files:
            if file.endswith(".json"):
                year = file[:4]
                year_files[year] = os.path.join(root, file)

    for year, file in year_files.items():
        split_year(file, "dist/data/months", year)
