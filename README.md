# Jira Worklog Data Exporter and Evaluation

These python scripts are a tool for fetching and processing worklog data from Jira, evaluating it, and displaying the results in a web-based table using Flask. It uses the Jira API, along with the `dotenv`, `json`, `csv`, and `flask` libraries.

## Prerequisites

Before using this script, make sure you have the following:

- Run the `install.sh` script
> `sudo bash install.sh`

Make sure: 
- Python 3 installed on your system.
- Required Python packages are installed (`dotenv`, `json`, `csv`, `flask`).
- You have access to a Jira instance.
- Jira API token and host URL are valid.
- Environment variables set for Jira host, API token, project name, and output filename (as specified in the `.env` file).

## Setup

1. Clone this repository to your local machine.

2. Update the `.env` file in the project directory and replace the placeholder with your specific values:
> `JIRA_HOST="<URL>"`<br>
> `JIRA_PROJECT="<PROJECT_NAME>"`<br>
> `JIRA_OUT_FILENAME="jira_worklog"`<br><br>
> `AUTH_TOKEN="<PAT_TOKEN>"`

## Usage

### Download the worklog data
1. Run the script using the following command:
> `python3 main.py`

2. The script will connect to your Jira instance, fetch all issues for the specified project, retrieve worklog data for each issue.

### Evaluate the worklog data (needs worklog data)
1. Run the script using the following command:
> `python3 evaluation.py`

2. The script will read the previous saved worklog data and perform data evaluation

3. The processed data will be displayed in a web-based table at `http://localhost:5000/`.

## Script Details

- The evaluation script reads worklog data from a JSON file, sorts it by the "started" date, and calculates weekly summaries for each author.

- It uses Flask to create a simple web application that displays the processed data in an HTML table.

- You can customize the HTML template for displaying the data as needed (e.g., create a `table.html` file in your project directory).

## Notes

- This script is a basic example and may require additional customization based on your specific evaluation criteria and HTML template requirements.

- Ensure that your Jira API token and environment variables are kept secure.

- Refer to the [Jira API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/) for more information on available API endpoints and authentication.

- For any issues or questions, feel free to reach out to the script's author.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
