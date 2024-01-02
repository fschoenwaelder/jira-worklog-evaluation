import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import csv

load_dotenv()

filename = os.getenv("JIRA_OUT_FILENAME")

with open(f'{filename}.json', 'r', encoding="utf-8") as openfile:
    # Reading from json file
    json_data = json.load(openfile)

# Sorting json entries by started date
json_data = sorted(json_data, key=lambda k: k['started'])

# Resetting the data and weekly sum
weekly_sum = 0
processed_entries = []

# Determine the start and end dates from the data
start_date = min(datetime.strptime(entry["started"], "%Y-%m-%d %H:%M:%S").date() for entry in json_data)
end_date = max(datetime.strptime(entry["started"], "%Y-%m-%d %H:%M:%S").date() for entry in json_data)

# Create empty json entry 
empty_entry = dict.fromkeys([*json_data[0].keys(), "soll", "ist", "compare"])

# Initialize weekly sums and the list for the updated data
weekly_sums = {}
updated_data = []

current_date = start_date
while current_date <= end_date:
    # Reset weekly sums on Mondays
    if current_date.weekday() == 0:
        weekly_sums = {}

    is_date_in_json = False

    # Add the current date's data to the updated data list and update weekly sums
    for entry in json_data:
        entry_date = datetime.strptime(entry["started"], "%Y-%m-%d %H:%M:%S").date()
        if entry_date == current_date:
            new_entry = entry.copy()
            new_entry["soll"] = None
            new_entry["ist"] = None
            new_entry["compare"] = None
            updated_data.append(new_entry)
            author = entry["author"]
            weekly_sums.setdefault(author, 0)
            weekly_sums[author] += entry["workedMinutes"]
            is_date_in_json = True

    # Add empty dates to summary too 
    if(not(is_date_in_json)):
        new_entry = empty_entry.copy()
        new_entry["compare"] = None
        new_entry["weekday"] = current_date.strftime("%A")
        new_entry["started"] = current_date.strftime("%Y-%m-%d")
        updated_data.append(new_entry)

    # Add a weekly summary entry for each author on Sundays
    if current_date.weekday() == 6 or current_date == end_date:
        for author, sum_minutes in weekly_sums.items():
            new_entry = empty_entry.copy()
            new_entry["name"] = f"Weekly Summary for {author}"
            new_entry["started"] = current_date.strftime("%Y-%m-%d")   
            new_entry["soll"] = str(20)
            new_entry["ist"] = str(round(sum_minutes/60,2))
            new_entry["compare"] = '>=' if int(new_entry["soll"])*60 <= int(sum_minutes) else "<"
            updated_data.append(new_entry)

    # Move to the next day
    current_date += timedelta(days=1)

# # Export as JSON
# with open('jira_worklog_output_adv.json', 'w') as openfile:
#     # Convert to JSON
#     json_output = json.dumps(updated_data, indent=4)

#     # Reading from json file
#     openfile.write(json_output)

# Export as CSV
# with open(f"{filename}_adv.csv", "w", encoding="utf-8") as file:
#     csv_file = csv.writer(file)
    
#     # Write header
#     csv_file.writerow(updated_data[0].keys())
    
#     # Write entries
#     for item in updated_data:
#         fields = list(item.values())
#         csv_file.writerow(fields)

from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('table.html', data=updated_data)

if __name__ == '__main__':
    app.run(debug=True)
