import os
import math
import json
from jira import JIRA
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def format_time(time_str, format = "%Y-%m-%d %H:%M:%S"):
    """Converts time string to a more readable format."""
    time_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    return datetime.strptime(time_str, time_format).strftime(format)

def get_jira_worklog():
    """Fetches and processes worklog data from JIRA."""
    try:
        jira_host = os.getenv('JIRA_HOST')
        auth_token = os.getenv('AUTH_TOKEN')
        project_name = os.getenv("JIRA_PROJECT")
        base_filename = os.getenv("JIRA_OUT_FILENAME")

        if not all([jira_host, auth_token, project_name, base_filename]):
            print("Missing required environment variables.")
            return

        print(f"Connecting to JIRA host: {jira_host}...")
        auth_jira = JIRA(server=jira_host, token_auth=auth_token)

        print(f"Fetching issues for project: {project_name}...")
        issues = auth_jira.search_issues(f"project={project_name}", maxResults=False)  # Get all issues

        output = []
        for issue in issues:
            worklogs = auth_jira.worklogs(issue.id)

            output.extend([{
                "id": issue.key,
                "name": issue.fields.summary,
                "author": worklog.author.displayName,
                "weekday": format_time(worklog.started, "%A"),
                "started": format_time(worklog.started),
                "workedMinutes": int(math.floor(worklog.timeSpentSeconds / 60)),
            } for worklog in worklogs])

        # Sort output by started date asc
        output = sorted(output, key=lambda k: k['started'])

        with open(f"{base_filename}.json", "w", encoding="utf-8") as outfile:
            json.dump(output, outfile, indent=4, ensure_ascii=False)
        print("Data exported to JSON file successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    get_jira_worklog()
